from MiniBank.Domains.Services.UserService import *
import unittest, json
from copy import deepcopy as dcopy

from MiniBank.Domains.Services.ApplicationService import *
from MiniBank.Domains.Services.AccountService import *

from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Entities.User import *

from MiniBank.Domains.Values.Event import *

from MiniBank.Domains.Database.EventRepository import *


class test_UserService(unittest.TestCase):
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
        self.post_user = dcopy(new_user)
        self.post_account = dcopy(new_account)
        self.post_user.add_account(self.post_account)
        self.post_account.deposit(10)
        self.post_account.deposit(200)
        self.post_account.withdraw(110)

        self.app_service = ApplicationService(self.event_repo)
        self.account_service = AccountService(self.app_service)
        self.user_service = UserService(self.app_service, self.account_service)

        self.post_event_repo = InMemoryEventRepository()
        map(self.post_event_repo.persist_event, self.events)
        self.post_app_service = ApplicationService(self.post_event_repo)
        self.post_account_service = AccountService(self.post_app_service)
        self.post_user_service = UserService(self.post_app_service, self.post_account_service)

    def test_create_user(self):
        result = self.user_service.create_user("Paulo", True)
        event = self.events[0]
        self.assertEqual(result, event)

    def test_create_account(self):
        result = self.user_service.create_user("Paulo", True)

        #test wrong uid
        result = self.user_service.create_account(0) 
        self.assertEqual(result, None)

        #test ok
        account = self.new_account
        result = self.user_service.create_account(1)
        msg = "\n\ne:"+json.dumps(dict(account),indent=2)
        msg+= "\n\nr:"+json.dumps(dict(result),indent=2)
        self.assertEqual(result, account, msg)

    def test_get_account_summary(self):
        #test wrong uid
        self.assertEqual(self.post_user_service.get_account_summary(10),None)

        #test ok
        result =  self.post_user_service.get_account_summary(1)
        expected = "--- Account Summaries: ---\n"
        expected+= self.post_account.summary()
        self.assertEqual(result, expected)
    
    def test_search_user_by_uid(self):
        #test wrong uid
        self.assertEqual(self.post_user_service.search_user_by_uid(10), None)
        #test ok
        self.assertEqual(self.post_user_service.search_user_by_uid(1), self.post_user)
