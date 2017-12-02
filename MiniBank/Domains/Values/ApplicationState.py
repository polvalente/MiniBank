from copy import deepcopy as dcopy

class ApplicationState():
    def __init__(self, events=[], users=[], accounts=[], next_uid=0, next_account_id=0):
        self.events = events
        self.users = users
        self.accounts = accounts
        self.next_uid = next_uid
        self.next_account_id = next_account_id

    def get_next_account_id(self):
        self.next_account_id += 1
        return self.next_account_id

    def get_next_uid(self)
        self.next_uid += 1
        return self.next_uid

    def build_from(self, events):
        '''Evaluate events to build application state'''
        self.events = events
        self = reduce(lambda state, event: state + event, events, self)

    def __add__(self, event):
        '''Define how to add: application state + event = new application state'''
        new_state = dcopy(self)
        if not isinstance(event,Event):
            raise NotImplementedError

        #User events
        if event.etype == "Create User":
            new_state.next_uid += 1
            user = User(event.value['user'])
            new_state.users[user.uid] = user
        #Account events
        elif event.etype == "Create Account":
            new_state.next_account_id += 1

            account = Account(event.value['account'])
            owner = User(event.value['owner'])
            new_state.users[owner.uid] = owner
            new_state.accounts[account.acc_id] = account

        elif event.etype == "Deposit":
            account = Account(event.value['account'])
            transaction = Transaction(event.value['transaction'])
            new_state.accounts[account.acc_id].deposit(transaction.value)

        elif event.etype == "Withdraw":
            account = Account(event.value['account'])
            transaction = Transaction(event.value['transaction'])
            new_state.accounts[account.acc_id].deposit(transaction.value)
        return new_state
