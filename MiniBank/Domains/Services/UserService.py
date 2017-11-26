class UserService(object):
    def __init__(self, user_repository, event_handler, account_service):
        self.user_repository = user_repository
        self.event_handler = event_handler
        self.account_service = account_service

    def create_user(self, username, is_person):
        uid = self.user_repository.get_new_user_id()
        user = User(uid, username, is_person)
        return self.user_repository.persist_user(user) # returns maybe user
    
    def create_account(self, username, balance = 0):
        user = self.search_user_by_username(username) 
        if user is None:
            return None
        
        new_account = self.account_service.create_account(user, balance)
        if new_account is None:
            return None

        return user.add_account(account)

    def get_account_summary(self, username):
        user = self.search_user_by_username(username)
        if user in None: return None

        return user.get_account_summary()

    def search_user_by_username(self, username):
        return self.user_repository.search_user_by_username(username)
