class UserService(object):
    def __init__(self, event_handler):
        self.event_handler = event_handler

    def create_user(self, username, is_person):
        uid = self.event_handler.get_new_user_id()
        user = User(uid, username, is_person)
        return self.event_handler.create_user(user) # returns maybe user
    
    def create_account(self, username, balance = 0):
        user = self.search_user_by_username(username) 
        if user is None:
            return None
        
        new_account = self.account_service.create_account(user, balance)
        if new_account is None:
            return None

        return self.event_handler.add_account(user, account)

    def get_account_summary(self, username):
        user = self.search_user_by_username(username)
        if user in None: 
            return None

        return user.get_account_summary()

    def search_user_by_username(self, username):
        return self.event_handler.search_user_by_username(username)
