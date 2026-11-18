#!/usr/bin/env python3
"""Exercise HTTP UI and API against an identified local demonstration service."""
import argparse,datetime,http.cookiejar,json,re,urllib.error,urllib.parse,urllib.request,uuid

def run(base):
    if urllib.parse.urlsplit(base).hostname not in ['127.0.0.1','localhost','app']:
        raise SystemExit('Cible refusée : utiliser uniquement le laboratoire local nommé.')
    opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    checks=[]
    def request(path,method='GET',payload=None,form=False,expected=200):
        body=None;headers={}
        if payload is not None:
            body=(urllib.parse.urlencode(payload) if form else json.dumps(payload)).encode()
            headers['Content-Type']='application/x-www-form-urlencoded' if form else 'application/json'
        try:response=opener.open(urllib.request.Request(base+path,data=body,method=method,headers=headers),timeout=10)
        except urllib.error.HTTPError as error:response=error
        content=response.read().decode();assert response.status==expected,(path,response.status,expected,content[:180])
        checks.append({'method':method,'path':path,'status':response.status})
        return content
    version=json.loads(request('/version'));assert version['application']=='OpsDesk'
    request('/health/live');request('/health/ready')
    html=request('/tickets');assert '<form' in html and 'Créer le ticket' in html
    token=re.search(r'name="csrf" value="([a-f0-9]+)"',html).group(1)
    marker='Ticket de preuve '+uuid.uuid4().hex[:12]
    created=json.loads(request('/api/tickets','POST',{'title':marker,'description':'Données fictives — test SQL et accents.','priority':'normal'},expected=201))
    ticket_id=created['id'];assert created['status']=='open'
    assert json.loads(request(f'/api/tickets/{ticket_id}'))['title']==marker
    assert any(row['id']==ticket_id for row in json.loads(request('/api/tickets')))
    assert json.loads(request(f'/api/tickets/{ticket_id}','PATCH',{'status':'in_progress'}))['status']=='in_progress'
    assert json.loads(request(f'/api/tickets/{ticket_id}','PATCH',{'status':'closed'}))['status']=='closed'
    request(f'/api/tickets/{ticket_id}','PATCH',{'status':'open'},expected=409)
    request('/api/tickets','POST',{'title':'a'},expected=400)
    request('/api/tickets/9223372036854775806',expected=404)
    page=request('/tickets','POST',{'csrf':token,'title':'UI '+marker,'description':'<script>alert(1)</script>','priority':'low'},form=True)
    assert 'UI '+marker in page and '&lt;script&gt;' in page and '<script>alert(1)</script>' not in page
    request('/tickets','POST',{'title':'Refus CSRF'},form=True,expected=400)
    assert 'opsdesk_database_up 1' in request('/metrics')
    result={'checked_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'application':version,'base_url':base,'status':'PASS','persisted_ticket_id':ticket_id,'checks':checks,'limits':['Local synthetic data only; no authentication or Internet exposure','No CI, K3s, cloud or restore qualification implied']}
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base-url',default='http://127.0.0.1:18081');args=parser.parse_args();run(args.base_url.rstrip('/'))
