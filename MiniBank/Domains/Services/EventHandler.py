class EventHandler(object):
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def create_account(self, owner, new_account):
        event = Event("Create Account", {'account': dict(new_account), 'owner': owner})
        return self.event_repository.persist_event(event)

    def apply_transaction(self, account, transaction):
        if transaction.kind == "deposit":
            event = Event("Deposit", {'account':dict(account), 'transaction':dict(transaction)})
        elif transaction.kind == "withdraw":
            event = Event("Withdraw", {'account':dict(account), 'transaction':dict(transaction)})
        return self.event_repository.persist_event(event)    

    def create_user(self, new_user):
        event = Event("Create User", dict(new_user))
        return self.event_repository.persist_event(event)

    def search_user_by_username(self, username):
        raise NotImplementedError

    def get_new_user_id(self):
        raise NotImplementedError

    def add_account(self, user, account):
        raise NotImplementedError

    def get_new_account_id(self):
        raise NotImplementedError

    def get_account_by_id(self, account_id):
        raise NotImplementedError

    def get_accounts_by_owner(self, owner):
        raise NotImplementedError

