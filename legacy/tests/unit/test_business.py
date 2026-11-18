import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'app'))
from opsdesk.business import InvalidTicket,next_status,ticket_input

class BusinessRules(unittest.TestCase):
    def test_normalizes_only_ticket_text(self):
        self.assertEqual(ticket_input({'title':'  Réseau laboratoire  ','description':' Test ','priority':'high'}),{'title':'Réseau laboratoire','description':'Test','priority':'high'})
    def test_defaults_are_explicit(self):
        self.assertEqual(ticket_input({'title':'Ticket fictif'})['priority'],'normal')
    def test_invalid_input_is_not_coerced(self):
        for value in [[],None,{'title':[]},{'title':'ab'},{'title':'x'*121},{'title':'valide','description':3},{'title':'valide','priority':'urgent'},{'title':'abc\x00'},{'title':'abc\ud800'},{'title':'valide','description':'nul\x00'}]:
            with self.subTest(value=value),self.assertRaises(InvalidTicket):ticket_input(value)
    def test_limits_allow_maximum_text(self):
        self.assertEqual(len(ticket_input({'title':'x'*120,'description':'y'*2000})['description']),2000)
    def test_valid_status_flow(self):
        self.assertEqual(next_status('open','in_progress'),'in_progress')
        self.assertEqual(next_status('in_progress','closed'),'closed')
    def test_retry_of_same_status_is_idempotent(self):
        for status in ['open','in_progress','closed']:self.assertEqual(next_status(status,status),status)
    def test_cannot_skip_or_reopen(self):
        for current,target in [('open','closed'),('closed','open'),('open','unknown'),('open',[])]:
            with self.subTest(current=current,target=target),self.assertRaises(InvalidTicket):next_status(current,target)

if __name__=='__main__':unittest.main()
