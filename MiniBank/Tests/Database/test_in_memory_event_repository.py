import unittest

from MiniBank.Domains.Database.EventRepository import *
from MiniBank.Domains.Values.Event import *
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Entities.Account import *

class test_InMemoryEventRepository(unittest.TestCase):
    def setUp(self):
        self.db = InMemoryEventRepository()
        #user
        new_user = User(1,"Paulo",True)
        event_user_dict = {'user':dict(new_user)}

        #account
        new_account = Account(1, 1, 0)
        event_account_dict = {'account':dict(new_account), 'owner':dict(new_user)} 
        
        self.events = [
                Event("Create User",event_user_dict,1),
                Event("Create Account", event_account_dict,2),
                ]
    
    def test_persist_event(self):
        result = self.db.persist_event(self.events[0])
        self.assertEqual(result,self.events[0])
        result = self.db.persist_event(self.events[1])
        self.assertEqual(result,self.events[1])

    def test_get_all_events(self):
        for e in self.events:
            self.db.persist_event(e)
        self.assertEqual(self.db.get_all_events(),self.events)
