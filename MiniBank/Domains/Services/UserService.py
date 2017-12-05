from MiniBank.Domains.Entities.User import *

class UserService(object):
    def __init__(self, application_service, account_service):
        self.application_service = application_service
        self.account_service = account_service

    def create_user(self, username, is_person):
        uid = self.application_service.get_new_user_id()
        user = User(uid, username, is_person)
        return self.application_service.create_user(user) # returns maybe user
    
    def create_account(self, uid, balance = 0):
        account = self.account_service.create_account(uid, balance)
        if account is None:
            #self.application_service.application_state.next_account_id -= 1
            return None
        return account

    def get_account_summary(self, uid):
        user = self.search_user_by_uid(uid)
        if user is None: 
            return None

        return user.get_account_summary()

    def search_user_by_uid(self, uid):
        return self.application_service.search_user_by_uid(uid)
