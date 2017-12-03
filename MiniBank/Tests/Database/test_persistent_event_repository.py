import unittest, json

from MiniBank.Domains.Database.EventRepository import *
from MiniBank.Domains.Values.Event import *
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Entities.Account import *
import MiniBank.Config.config as config

class test_PersistentEventRepository(unittest.TestCase):
    def setUp(self):
        repo_data = {
            'dbname':config.db_name,
            'address':config.db_address,
            'port':config.db_port,
            'user':config.db_user,
            'pass':config.db_pass
            }
        self.db = PersistentEventRepository(repo_data)
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
        self.db.persist_event(self.events[0])
        ev = self.db.get_all_events()

        self.assertEqual(ev[0],self.events[0])
        self.db.persist_event(self.events[1])
        ev = self.db.get_all_events()
        self.assertEqual(ev[1],self.events[1])

    def test_get_all_events(self):
        for e in self.events:
            self.db.persist_event(e)
        self.assertEqual(self.db.get_all_events(),self.events)
