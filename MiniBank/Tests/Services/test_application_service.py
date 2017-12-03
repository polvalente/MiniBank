from MiniBank.Domains.Services.ApplicationService import *
from MiniBank.Domains.Database.EventRepository import *
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Values.Event import *
from MiniBank.Domains.Values.Transaction import *

import unittest, json
from copy import deepcopy as dcopy

class test_ApplicationService(unittest.TestCase):
    def setUp(self):
        self.event_repo = InMemoryEventRepository()
        #user
        new_user = User(1,"Paulo",True)
        self.new_user = new_user
        event_user_dict = {'user':dict(new_user)}

        #account
        new_account = Account(1, 1, 0)
        self.new_account = new_account
        event_account_dict = {'account':dict(new_account), 'owner':dict(new_user)} 
        
        #transactions
        event_deposit1_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 10))}
        event_deposit2_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 200))}
        event_withdraw1_dict = {'account': dict(new_account),'transaction': dict(Transaction("withdraw",110))}

        self.events = [
                Event("Create User",event_user_dict,1),
                Event("Create Account", event_account_dict,2),
                Event("Deposit",event_deposit1_dict,3),
                Event("Deposit",event_deposit2_dict,4),
                Event("Withdraw",event_withdraw1_dict,5)
                ]
        #for event in self.events:
        #    self.event_repo.persist_event(event)
        
        self.post_user = dcopy(new_user)
        self.post_account = dcopy(new_account)
        self.post_user.add_account(self.post_account)
        self.post_account.deposit(10)
        self.post_account.deposit(200)
        self.post_account.withdraw(110)

        self.app_service = ApplicationService(self.event_repo)

    def test_create_user(self):
        result = self.app_service.create_user(self.new_user)
        self.assertEqual(self.events[0], result)

    def test_create_account(self):
        result = self.app_service.create_user(self.new_user)
        result = self.app_service.create_account(self.new_user.uid, self.new_account)
        self.assertEqual(self.events[1], result, msg="\ns:"+json.dumps(dict(self.events[1]))+'\nr:'+json.dumps(dict(result)))

    def test_apply_transaction(self):
        for event in self.events:
            self.event_repo.persist_event(event)
        self.app_service.build_application_state(3)
        result = self.app_service.apply_transaction(self.new_account, Transaction("deposit",200))
        self.assertEqual(result, self.events[3])
        result = self.app_service.apply_transaction(self.new_account, Transaction("withdraw", 110))
        self.assertEqual(result, self.events[4])

    def test_search_user_by_uid(self):
        for event in self.events:
            self.event_repo.persist_event(event)
        self.app_service = ApplicationService(self.event_repo)
        result = self.app_service.search_user_by_uid(1)
        

        self.assertEqual(result, self.post_user, '\nres:'+json.dumps(dict(result))+'\nmy:'+json.dumps(dict(self.new_user)))

    def test_get_new_user_id(self):
        result = self.app_service.get_new_user_id()
        self.assertEqual(result, 1)

    #def test_add_account(self):
    #    for event in self.events:
    #        self.event_repo.persist_event(event)
    #    self.app_service = ApplicationService(self.event_repo)

    #    account = Account(2,1,0)
    #    user = self.app_service.search_user_by_uid(1)
    #    result = self.app_service.add_account(user, account)
    #    self.assertEqual(result, account) 

    def test_get_account_by_id(self):
        for event in self.events:
            self.event_repo.persist_event(event)
        self.app_service = ApplicationService(self.event_repo)
        result = self.app_service.get_account_by_id(1)
        self.assertEqual(result, self.post_account, json.dumps(dict(result))+"||"+json.dumps(dict(self.post_account)))

    def test_get_accounts_by_owner_id(self):
        for event in self.events:
            self.event_repo.persist_event(event)
        self.app_service = ApplicationService(self.event_repo)

        account = Account(2,1,0)
        user = self.app_service.search_user_by_uid(1)
        result = self.app_service.create_account(user.uid, account)
        result = self.app_service.get_accounts_by_owner_id(1)
        acc_list = [self.post_account, account]
        self.assertEqual(result, acc_list, "\n\n\n>>"+json.dumps(map(dict,result))+"\n\n\n>>"+json.dumps(map(dict,acc_list)))
