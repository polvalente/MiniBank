class EventHandler(object):
    def __init__(self, event_repository, app_state='last'):
        self.event_repository = event_repository
        self.application_state = {'users':[], 'accounts':[], 'next_uid':0, 'next_account_id':0}
        self.build_application_state(app_state)

    def build_application_state(self, app_state):
        raise NotImplementedError

    def create_account(self, owner, new_account):
        event = Event("Create Account", {'account': dict(new_account), 'owner': owner})
        self.application_state['next_account_id'] += 1
        return self.event_repository.persist_event(event)

    def apply_transaction(self, account, transaction):
        if transaction.kind == "deposit":
            event = Event("Deposit", {'account':dict(account), 'transaction':dict(transaction)})
        elif transaction.kind == "withdraw":
            event = Event("Withdraw", {'account':dict(account), 'transaction'   :dict(transaction)})

        return self.event_repository.persist_event(event)    

    def create_user(self, new_user):
        event = Event("Create User", dict(new_user))
        self.application_state['next_user_id'] += 1

        return self.event_repository.persist_event(event)

    def search_user_by_username(self, username):
        return filter(lambda u: u.name == username, self.application_state['users'])

    def get_new_user_id(self):
        return self.application_state['next_uid']

    def add_account(self, user, account):
        self.application_state['accounts'].append(account)
        return self.event_repository.persist_event(event)

    def get_new_account_id(self):
        return self.application_state['next_account_id']

    def get_account_by_id(self, account_id):
        return self.application_state['accounts'][account_id]

    def get_accounts_by_owner(self, owner):
        if type(owner) == type(''):
            owner = filter(lambda u: u.name == owner, self.application_state['users'])
        else:
            owner = filter(lambda u: u.name == owner.name, self.application_state['users'])
        return owner.accounts

