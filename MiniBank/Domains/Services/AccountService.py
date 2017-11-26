from copy import deepcopy as dcopy
from MiniBank.Domains.Entities.Account import * 

class AccountService():
    def __init__(self, account_repository, event_handler):
        self.account_repository = account_repository
        self.event_handler = event_handler

    def create_account(self, owner, initial_balance=0):
        #Getting new account's id from repo
        account_id = account_repository.get_new_account_id()
        #creating new account
        new_account = Account(account_id, owner, initial_balance)
        #adding event to event stack
        self.event_handler.create_account(new_account)

        return self.account_repository.persist_account(new_account)

    def search_account_by_id(self, account_id):
        return self.account_repository.search_account_by_id(account_id)

    def search_accounts_by_owner(self, owner): 
        return self.account_repository.search_accounts_by_owner(owner)

    def deposit_to_account(self, account_id, amount):
        account = self.search_account_by_id(account_id)
        if account is None:
            return None
        #apply transaction to account 
        transaction = account.deposit(amount)

        #persist modified account to repo
        self.account_repository.persist_account(account)

        #add transaction to event stack
        self.event_handler.apply_transaction(transaction)

        return dcopy(transaction)
        
    def withdraw_from_account(self, owner, account_id, amount):
        account = self.search_account_by_id(account_id)

        if account is None or account.owner != owner:
            return None

        #withdraw amount
        transaction = account.withdraw(amount)

        #persist modified account
        self.account_repository.persist_account(account)

        #add transaction to event stack
        self.event_handler.apply_transaction(transaction)

        return dcopy(transaction)
