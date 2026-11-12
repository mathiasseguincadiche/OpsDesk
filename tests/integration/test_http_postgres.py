"""Test current source against real PostgreSQL, isolating most data in a TEMP table.

One explicitly named fictional ticket is retained in the development database to
verify read-after-commit through distinct connections. No source data is deleted.
"""
import os,re,sys,unittest,uuid
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'app'))
import psycopg
from opsdesk import web


class ExistingSession:
    def __init__(self,connection):self.connection=connection
    def __enter__(self):return self.connection
    def __exit__(self,kind,value,trace):
        self.connection.rollback() if kind else self.connection.commit()


class HTTPPostgreSQLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection=web.connect()
        cls.connection.execute('CREATE TEMP TABLE tickets (LIKE public.tickets INCLUDING ALL)')
        cls.connection.commit()
    @classmethod
    def tearDownClass(cls):cls.connection.close()
    def setUp(self):
        self.connection.execute('TRUNCATE pg_temp.tickets RESTART IDENTITY')
        self.connection.commit()
        self.connection_patch=patch.object(web,'connect',side_effect=lambda:ExistingSession(self.connection))
        self.connection_patch.start();self.addCleanup(self.connection_patch.stop)
        self.app=web.create_app();self.app.config['TESTING']=True;self.client=self.app.test_client()
    def create(self,**values):
        return self.client.post('/api/tickets',json={'title':'Ticket strictement fictif','description':'Recette applicative TEMP',**values})
    def test_ticket_round_trip_and_state_flow(self):
        response=self.create();self.assertEqual(response.status_code,201);item=response.get_json()
        self.assertEqual(item['status'],'open');self.assertTrue(response.headers['Location'].endswith(str(item['id'])))
        url=response.headers['Location']
        self.assertEqual(self.client.get(url).get_json()['title'],item['title'])
        for state in ['in_progress','closed']:
            response=self.client.patch(url,json={'status':state});self.assertEqual(response.status_code,200);self.assertEqual(response.get_json()['status'],state)
        self.assertEqual(self.client.patch(url,json={'status':'open'}).status_code,409)
    def test_same_state_does_not_change_business_status(self):
        item=self.create().get_json();url=f"/api/tickets/{item['id']}"
        response=self.client.patch(url,json={'status':'open'})
        self.assertEqual(response.status_code,200);self.assertEqual(response.get_json()['status'],'open')
    def test_invalid_create_is_rejected_before_sql(self):
        for value in [None,[],{}, {'title':'a'},{'title':'x'*121},{'title':'Correct','priority':[]},{'title':'Correct','description':7},{'title':'abc\x00'},{'title':'abc\ud800'},{'title':'Correct','description':'nul\x00'}]:
            with self.subTest(value=value):
                response=self.client.post('/api/tickets',json=value) if value is not None else self.client.post('/api/tickets',data='null',content_type='application/json')
                self.assertEqual(response.status_code,400)
        self.assertEqual(self.connection.execute('SELECT count(*) AS n FROM pg_temp.tickets').fetchone()['n'],0)
    def test_patch_requires_only_status(self):
        item=self.create().get_json()
        for payload in [{},{'status':'closed','title':'Cannot alter'},[],{'status':None}]:
            with self.subTest(payload=payload):self.assertIn(self.client.patch(f"/api/tickets/{item['id']}",json=payload).status_code,[400,409])
    def test_missing_ticket_is_json_404(self):
        response=self.client.get('/api/tickets/9999999');self.assertEqual(response.status_code,404);self.assertIn('error',response.get_json())
    def test_mutating_api_requires_json(self):
        self.assertEqual(self.client.post('/api/tickets',data='title=test').status_code,415)
    def test_malformed_json_is_json_400(self):
        response=self.client.post('/api/tickets',data='{',content_type='application/json')
        self.assertEqual(response.status_code,400);self.assertIn('error',response.get_json())
    def test_payload_limit_is_enforced(self):
        self.assertEqual(self.create(description='x'*17000).status_code,413)
    def test_sql_text_is_data_and_not_a_command(self):
        title="Ticket '); DROP TABLE tickets; --"
        item=self.create(title=title).get_json()
        self.assertEqual(self.client.get(f"/api/tickets/{item['id']}").get_json()['title'],title)
        self.assertEqual(self.connection.execute('SELECT count(*) AS n FROM pg_temp.tickets').fetchone()['n'],1)
    def test_html_is_escaped_and_security_headers_present(self):
        item=self.create(title='<script>fictif()</script>').get_json()
        response=self.client.get(f"/tickets/{item['id']}")
        self.assertIn(b'&lt;script&gt;',response.data);self.assertNotIn(b'<script>fictif()</script>',response.data)
        self.assertEqual(response.headers['X-Frame-Options'],'DENY');self.assertIn("frame-ancestors 'none'",response.headers['Content-Security-Policy'])
    def test_html_form_requires_valid_session_csrf(self):
        self.assertEqual(self.client.post('/tickets',data={'title':'Fictif'}).status_code,400)
        page=self.client.get('/tickets');token=re.search(rb'name="csrf" value="([a-f0-9]+)"',page.data).group(1).decode()
        self.assertEqual(self.client.post('/tickets',data={'csrf':'é','title':'Fictif'}).status_code,400)
        response=self.client.post('/tickets',data={'csrf':token,'title':'Fictif avec session'})
        self.assertEqual(response.status_code,303);self.assertEqual(self.client.get(response.headers['Location']).status_code,200)
        self.assertEqual(self.client.post(response.headers['Location']+'/status',data={'csrf':token,'status':'in_progress'}).status_code,303)
        other=self.app.test_client();self.assertEqual(other.post('/tickets',data={'csrf':token,'title':'Mauvaise session'}).status_code,400)
    def test_health_version_and_metrics(self):
        for path in ['/health/live','/health/ready','/version']:
            response=self.client.get(path);self.assertEqual(response.status_code,200);self.assertEqual(response.get_json()['application'],'OpsDesk')
        self.assertIn(b'opsdesk_database_up 1',self.client.get('/metrics').data)
    def test_dependency_failure_distinguishes_live_and_ready(self):
        with patch.object(web,'connect',side_effect=psycopg.OperationalError('Synthetic application test')):
            self.assertEqual(self.client.get('/health/live').status_code,200)
            self.assertEqual(self.client.get('/health/ready').status_code,503)
            response=self.client.get('/api/tickets');self.assertEqual(response.status_code,503);self.assertNotIn('Synthetic',response.get_data(as_text=True))
            self.assertIn(b'opsdesk_database_up 0',self.client.get('/metrics').data)
    def test_untrusted_host_is_rejected(self):
        self.assertEqual(self.client.get('/version',headers={'Host':'untrusted.example.invalid'}).status_code,400)
    def test_loopback_hosts_are_accepted(self):
        for host in ['localhost','127.0.0.1:18081']:
            with self.subTest(host=host):self.assertEqual(self.client.get('/version',headers={'Host':host}).status_code,200)
    def test_no_authentication_is_claimed_by_local_api(self):
        # This deliberately documents a local-demo boundary, not an authorization feature.
        self.assertEqual(self.create().status_code,201)
    def test_list_is_limited_to_latest_hundred(self):
        self.connection.cursor().executemany('INSERT INTO pg_temp.tickets (title,priority) VALUES (%s,%s)',[(f'Ticket fictif {i}','normal') for i in range(105)])
        self.connection.commit();items=self.client.get('/api/tickets').get_json()
        self.assertEqual(len(items),100);self.assertGreater(items[0]['id'],items[-1]['id'])
    def test_postgresql_business_constraints_are_real(self):
        with self.assertRaises(psycopg.errors.CheckViolation):
            self.connection.execute("INSERT INTO pg_temp.tickets (title,priority) VALUES ('ab','normal')")
        self.connection.rollback()


class CommittedDevelopmentReadback(unittest.TestCase):
    def test_current_source_commits_and_reads_through_distinct_connections(self):
        app=web.create_app();client=app.test_client();title='FICTIF-'+uuid.uuid4().hex[:12]
        created=client.post('/api/tickets',json={'title':title,'description':'Recette : témoin conservé, aucune donnée supprimée.'})
        self.assertEqual(created.status_code,201);item=created.get_json();url=f"/api/tickets/{item['id']}"
        next_client=web.create_app().test_client();self.assertEqual(next_client.get(url).get_json()['title'],title)
        with web.connect() as connection:
            row=connection.execute('SELECT title,status FROM public.tickets WHERE id=%s',(item['id'],)).fetchone()
        self.assertEqual(row['title'],title);self.assertEqual(row['status'],'open')
        print(f'PERSISTED_FICTIONAL_TICKET_ID={item["id"]}')
if __name__=='__main__':unittest.main()
