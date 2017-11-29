from MiniBank.Domains.Entities.Account import *

class User():
    def __init__(self, uid, name, is_person):
        self.uid = uid
        self.name = name
        self.is_person = is_person
        self.accounts = []

    def add_account(self, newAccount):
        self.accounts.append(newAccount)
        return newAccount

    def get_account_summary(self):
        s = "--- Account Summaries: ---\n"
        s+= '\n'.join(map(lambda x: x.summary(), self.accounts))
        return s

    def __iter__(self):
        yield 'uid', self.uid
        yield 'name', self.name
        yield 'is_person', self.is_person
        yield 'accounts', self.accounts
