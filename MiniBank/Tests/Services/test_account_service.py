import unittest, json
from copy import deepcopy as dcopy
from MiniBank.Domains.Services.AccountService import *
from MiniBank.Domains.Services.ApplicationService import *
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Values.Event import *
from MiniBank.Domains.Database.EventRepository import *

class test_AccountService(unittest.TestCase):
    def setUp(self):
        self.event_repo = InMemoryEventRepository()
        #user
        new_user = User(1,"Paulo",True)
        self.new_user = new_user
        event_user_dict = {'user':dict(new_user)}

        #account
        new_account = Account(1, 1, 0, 1)
        self.new_account = new_account
        event_account_dict = {'account':dict(new_account), 'owner':dict(new_user)} 
        
        #transactions
        event_deposit1_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 10, 2))}
        event_deposit2_dict  = {'account': dict(new_account), 'transaction': dict(Transaction("deposit", 200, 3))}
        event_withdraw1_dict = {'account': dict(new_account),'transaction': dict(Transaction("withdraw",110, 4))}

        self.events = [
                Event("Create User",event_user_dict,1),
                Event("Create Account", event_account_dict,2),
                Event("Deposit",event_deposit1_dict,3),
                Event("Deposit",event_deposit2_dict,4),
                Event("Withdraw",event_withdraw1_dict,5)
                ]
        self.post_user = dcopy(new_user)
        self.post_account = dcopy(new_account)
        self.post_user.add_account(self.post_account)
        self.post_account.deposit(10, 2)
        self.post_account.deposit(200, 3)
        self.post_account.withdraw(110, 4)

        self.event_repo.persist_event(self.events[0])
        self.app_service = ApplicationService(self.event_repo)
        self.account_service = AccountService(self.app_service)

    def test_create_account(self):
        result = self.account_service.create_account(self.new_user.uid)
        self.assertEqual(self.new_account, result)

    def test_search_account_by_id(self):
        self.event_repo = InMemoryEventRepository()
        for event in self.events:
            self.event_repo.persist_event(event)
        app_service = ApplicationService(self.event_repo)
        account_service = AccountService(app_service)
        
        result = account_service.search_account_by_id(1)
        self.assertEqual(result, self.post_account)

    def test_search_accounts_by_owner_id(self):
        event_repo = InMemoryEventRepository()
        for event in self.events:
            event_repo.persist_event(event)
        app_service = ApplicationService(event_repo)
        account_service = AccountService(app_service)

        account = account_service.create_account(1)
        result = account_service.search_accounts_by_owner_id(1)
        acc_list = [self.post_account, account]
        msg = "\n\nres:"+json.dumps(map(dict, result),indent=4)
        msg += "\n\nacc:"+json.dumps(map(dict, acc_list), indent=4)
        self.assertEqual(result, acc_list, msg)

    def test_deposit_to_account(self):
        event_repo = InMemoryEventRepository()
        for event in self.events:
            event_repo.persist_event(event)
        app_service = ApplicationService(event_repo)
        account_service = AccountService(app_service)

        result = account_service.deposit_to_account(1,-10)
        self.assertEqual(result, None)
        result = account_service.deposit_to_account(1,100)

        account = dcopy(self.post_account)

        event = Event("Deposit", {'account':dict(account), 'transaction':dict(Transaction("deposit",100,5))}, 6)
        
        msg = "\n\nres:"+json.dumps(dict(result),indent=4)
        msg += "\n\nevt:"+json.dumps(dict(event), indent=4)
        
        self.assertEqual(result, event,msg)
        

    def test_withdraw_from_account(self):
        event_repo = InMemoryEventRepository()
        for event in self.events:
            event_repo.persist_event(event)
        app_service = ApplicationService(event_repo)
        account_service = AccountService(app_service)

        #withdraw negative value
        result = account_service.withdraw_from_account(1,1,-10)
        self.assertEqual(result, None)
        
        #withdraw from wrong uid
        result = account_service.withdraw_from_account(1,2,-10)
        self.assertEqual(result, None)
        
        result = account_service.withdraw_from_account(1,1,100)

        account = dcopy(self.post_account)

        event = Event("Withdraw", {'account':dict(account), 'transaction':dict(Transaction("withdraw",100,5))}, 6)
        
        msg = "\n\nres:"+json.dumps(dict(result),indent=4)
        msg += "\n\nevt:"+json.dumps(dict(event), indent=4)
        
        self.assertEqual(result, event,msg)
