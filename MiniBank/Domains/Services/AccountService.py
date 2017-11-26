from copy import deepcopy as dcopy
from MiniBank.Domains.Entities.Account import * 

class AccountService():
    def __init__(self, account_repository):
        self.account_repository = account_repository

    def create_account(self, owner, initial_balance=0):
        account_id = account_repository.get_new_account_id()
        new_account = Account(account_id, owner, initial_balance)
        return self.account_repository.persist_account(new_account)

    def search_account_by_id(self, account_id):
        return self.account_repository.search_account_by_id(account_id)

    def search_accounts_by_owner(self, owner): 
        return self.account_repository.search_accounts_by_owner(owner)

    def deposit_to_account(self, account_id, amount):
        account = self.search_account_by_id(account_id)
        if account is None:
            return None
        account.deposit(amount)
        transaction = self.account_repository.persist_account(account)
        return dcopy(transaction)
        
    def withdraw_from_account(self, owner, account_id, amount):
        account = self.search_account_by_id(account_id)

        if account is None or account.owner != owner:
            return None

        transaction = account.withdraw(amount)
        self.account_repository.persist_account(account)

        return dcopy(transaction)
