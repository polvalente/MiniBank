from MiniBank.Domains.Values.Event import *

class ApplicationService(object):
    def __init__(self, event_repository, app_state='last'):
        self.event_repository = event_repository

        self.application_state = ApplicationState()

        self.build_application_state(app_state)

    def build_application_state(self, app_state):
        events = self.event_repository.get_all_events(app_state)
        application_state.build_from(events)

    def create_account(self, owner, new_account):
        event_id = self.event_repository.get_next_id()
        event = Event("Create Account", {'account': dict(new_account), 'owner': dict(owner)}, event_id)
        return self.event_repository.persist_event(event)

    def apply_transaction(self, account, transaction):
        #no need to change application state here because we already do it in account_service
        event_id = self.event_repository.get_next_id()
        if transaction.kind == "deposit":
            event = Event("Deposit", {'account':dict(account), 'transaction':dict(transaction)}, event_id)
        elif transaction.kind == "withdraw":
            event = Event("Withdraw", {'account':dict(account), 'transaction'   :dict(transaction)}, event_id)

        return self.event_repository.persist_event(event)    

    def create_user(self, new_user):
        event_id = self.event_repository.get_next_id()
        event = Event("Create User", {'user':dict(new_user)}, event_id)
        #need to change internal value for user_id

        return self.event_repository.persist_event(event)

    def search_user_by_username(self, username):
        #search done on in_memory application_state
        return filter(lambda u: u.name == username, self.application_state.users.values())

    def get_new_user_id(self):
        #get from internal value
        return self.application_state.get_next_uid()

    def add_account(self, user, account):
        #add account to app_state
        self.application_state.accounts[account.acc_id] = account
        #no need to add event to repo, because every account has its user and account is added to user on user_service.create_account()
        return True

    def get_new_account_id(self):
        #get next account id from app_state
        return self.application_state.get_next_account_id()

    def get_account_by_id(self, account_id):
        #find account by id; app_state['accounts'] is alway ordered by account_id
        return self.application_state.accounts[account_id]

    def get_accounts_by_owner_id(self, owner_id):
        return self.application_state[owner_id].accounts

