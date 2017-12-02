import unittest
from MiniBank.Domains.Values.ApplicationState import *

class TestApplicationState():
    def setUp(self):
        return
        self.events = [
                Event("Create User",{},1),
                Event("Create Account", {},2),
                Event("Deposit",{},3),
                Event("Deposit",{},4),
                Event("Withdraw",{},5)
                ]
        #create list of events
        self.app_state = ApplicationState()

    def test_get_next_account_id(self):
        self.assertEqual(self.app_state.get_next_account_id(), 1)
        self.assertEqual(self.app_state.get_next_account_id(), 2)
    
    def test_get_next_uid(self):
        self.assertEqual(self.app_state.get_next_uid(), 1)
        self.assertEqual(self.app_state.get_next_uid(), 2)

    def test_add(self):
        new_state = dcopy(self.app_state)
        #apply user creation manually
        new_state.users.append(User(self.events[0].value['user']))
        self.assertEqual(self.app_state + self.events[0], new_state)

    def test_build_from(self):
        new_state = dcopy(self.app_state)
        new_state += self.events[0]
        new_state += self.events[1]
        new_state += self.events[2]
        new_state += self.events[3]
        new_state += self.events[4]
        self.assertEqual(self.app_state.build_from(self.events), new_state)
