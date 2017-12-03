from MiniBank.Domains.Entities.Account import *

class User():
    def __init__(self, dict_or_uid, name=None, is_person=None):
        if(isinstance(dict_or_uid, dict)):
            self.uid = dict_or_uid['uid']
            self.name = dict_or_uid['name']
            self.is_person = dict_or_uid['is_person']
            #converting accounts from dict to 
            self.accounts = map(lambda a: Account(a), dict_or_uid['accounts'])
        else:
            self.uid = dict_or_uid
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
        yield 'accounts', map(dict, self.accounts)

    def __eq__(self, other):
        return self.uid == other.uid and\
                self.name == other.name and\
                self.is_person == other.is_person and\
                self.accounts == other.accounts
