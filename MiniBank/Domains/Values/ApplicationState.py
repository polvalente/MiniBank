from copy import deepcopy as dcopy

from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Values.Transaction import *
from MiniBank.Domains.Values.Event import *

class ApplicationState():
    def __init__(self, events=[], users={}, accounts={}, next_uid=0, next_account_id=0, next_transaction_id=0):
        self.events = events
        self.users = users
        self.accounts = accounts
        self.next_uid = next_uid
        self.next_account_id = next_account_id
        self.next_transaction_id = next_transaction_id

    def get_next_account_id(self):
        #self.next_account_id += 1
        return self.next_account_id + 1

    def get_next_uid(self):
        #self.next_uid += 1
        return self.next_uid + 1

    def get_next_transaction_id(self):
        return self.next_transaction_id + 1

    def build_from(self, events):
        '''Evaluate events to build application state'''
        self = reduce(lambda state, event: state + event, events, self)
        return self

    def __add__(self, event):
        '''Define how to add: application state + event = new application state'''
        new_state = dcopy(self)
        if not isinstance(event,Event):
            raise NotImplementedError

        #User events
        if event.etype == "Create User":
            #new_state.next_uid += 1
            user = User(event.value['user'])
            
            new_state.next_uid = max([new_state.next_uid + 1, user.uid])
            
            new_state.users[user.uid] = user
        #Account events
        elif event.etype == "Create Account":

            account = Account(event.value['account'])
            
            new_state.next_account_id = max([new_state.next_account_id + 1, account.acc_id])

            transaction = account.get_last_transaction()
            new_state.next_transaction_id = max([new_state.next_transaction_id + 1, transaction.transaction_id])
            
            owner = User(event.value['owner'])
            new_state.users[owner.uid] = owner
            new_state.users[owner.uid].accounts.append(account)
            new_state.accounts[account.acc_id] = account

        elif event.etype == "Deposit":
            account = Account(event.value['account'])
            transaction = Transaction(event.value['transaction'])
            new_state.next_transaction_id = max([new_state.next_transaction_id + 1, transaction.transaction_id])
            for a in new_state.accounts.values():
                if a.acc_id == account.acc_id and a.get_last_transaction() != transaction:
                    a.deposit(transaction.amount, transaction.transaction_id)
            for a in new_state.users[account.owner_id].accounts:
                if a.acc_id == account.acc_id and a.get_last_transaction() != transaction:
                    a.deposit(transaction.amount, transaction.transaction_id)



        elif event.etype == "Withdraw":
            account = Account(event.value['account'])
            transaction = Transaction(event.value['transaction'])
            new_state.next_transaction_id = max([new_state.next_transaction_id + 1, transaction.transaction_id])
            for a in new_state.accounts.values():
                if a.acc_id == account.acc_id and a.get_last_transaction() != transaction:
                    a.withdraw(transaction.amount, transaction.transaction_id)
            for a in new_state.users[account.owner_id].accounts:
                if a.acc_id == account.acc_id and a.get_last_transaction() != transaction:
                    a.withdraw(transaction.amount, transaction.transaction_id)
        else:
            NotImplementedError

        new_state.events.append(event)
        return new_state

    def __eq__(self, other):
        return (self.events == other.events) and \
               (self.users.values() == other.users.values()) and \
               (self.accounts.values() == other.accounts.values()) and \
               (self.next_uid == other.next_uid) and \
               (self.next_account_id == other.next_account_id) and\
               (self.next_transaction_id == other.next_transaction_id)
