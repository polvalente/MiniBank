from MiniBank.Domains.Entities.Account import *

class User():
    def __init__(self, uid, name, is_person):
        self.uid = uid
        self.name = name
        self.is_person = is_person
        self.accounts = []

    def create_account(self, acc_id, balance=0):
        newAccount = Account(acc_id, self, balance)
        self.accounts.append(newAccount)
        return newAccount

    def get_account_summary(self):
        s = "--- Account Summaries: ---\n"
        s+= '\n'.join(map(lambda x: x.summary(), self.accounts))
        return s
