import unittest
from MiniBank.Domains.Values.ApplicationState import *
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Values.Transaction import *
from MiniBank.Domains.Values.Event import *
import json


class TestApplicationState(unittest.TestCase):
    def setUp(self):
        #user
        new_user = User(1,"Paulo",True)
        event_user_dict = {'user':dict(new_user)}

        #account
        new_account = Account(1, 1, 0,1)
        event_account_dict = {'account':dict(new_account), 'owner':dict(new_user)} 
        
        #transactions
        event_deposit1_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 10, 1))}
        event_deposit2_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 200, 2))}
        event_withdraw1_dict = {'account': dict(new_account),'transaction': dict(Transaction("withdraw",110, 3))}
        self.events = [
                Event("Create User",event_user_dict,1),
                Event("Create Account", event_account_dict,2),
                Event("Deposit",event_deposit1_dict,3),
                Event("Deposit",event_deposit2_dict,4),
                Event("Withdraw",event_withdraw1_dict,5)
                ]
        #create list of events
        self.app_state = ApplicationState()

    def test_get_next_account_id(self):
        self.assertEqual(self.app_state.get_next_account_id(), 1)
    
    def test_get_next_uid(self):
        self.assertEqual(self.app_state.get_next_uid(), 1)

    def test_add_and_eq(self):
        new_state = dcopy(self.app_state)
        #apply user creation manually
        new_state.users[self.events[0].value['user']['uid']] = User(self.events[0].value['user'])
        new_state.next_uid += 1
        new_state.events.append(self.events[0])
        
        result = self.app_state + self.events[0]

        #msg = "r.events:"+str(result.next_uid) + "\nn.events:"+str(new_state.next_uid)
        #msg += '=='+str(result.next_uid == new_state.next_uid)

        #test if addition works
        #self.assertEqual(self.app_state + self.events[0], new_state, msg)
        self.assertEqual(self.app_state + self.events[0], new_state)

    def test_add_user(self):
        #'test_add_and_eq' already takes care of this
        pass

    def test_add_account(self): 
        new_state = dcopy(self.app_state)
        #apply user creation manually
        account = Account(self.events[1].value['account'])
        new_state.accounts[self.events[1].value['account']['account_id']] = account
        new_state.next_account_id += 1
        new_state.events.append(self.events[1])
        new_state.users[self.events[1].value['owner']['uid']] = User(self.events[1].value['owner'])
        new_state.users[self.events[1].value['owner']['uid']].accounts.append(account)
        new_state.next_transaction_id = 1
        
        result = self.app_state + self.events[1]

        #msg = "r.events:"+str(result.next_uid) + "\nn.events:"+str(new_state.next_uid)
        #msg += '=='+str(result.next_uid == new_state.next_uid)
        self.assertEqual(result, new_state)


    def test_add_deposit(self):
        new_state = dcopy(self.app_state)
        new_state += self.events[1]
    
    def test_add_withdraw(self):
        pass

    def test_build_from(self):
        new_state = dcopy(self.app_state)
        new_state += self.events[0]
        new_state += self.events[1]
        new_state += self.events[2]
        new_state += self.events[3]
        new_state += self.events[4]
        
        
        result = self.app_state.build_from(self.events)
        #msg  = "\nres:"+str(map(lambda e: e.etype, result.events)) 
        #msg += "\nnew:"+str(map(lambda e: e.etype, new_state.events))
        #msg += '\nres==new:'+str(result.events == new_state.events)
        msg = ''
        self.assertEqual(result, new_state, msg)

if __name__ == '__main__':
    unittest.main()
