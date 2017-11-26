class EventHandler(object):
    def __init__(self, event_repository):
        self.event_repository = event_repository

    def create_account(self, new_account):
        event = Event("Create Account", dict(new_account))
        return self.event_repository.persist_event(event)

    def apply_transaction(transaction):
        if transaction.kind == "deposit":
            event = Event("Deposit", dict(transaction))
        elif transaction.kind == "withdraw":
            event = Event("Withdraw", dict(transaction))
        return self.event_repository.persist_event(event)    

    def create_user(self, new_user):
        event = Event("Create User", dict(new_user))
        return self.event_repository.persist_event(event)
