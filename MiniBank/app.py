from MiniBank.Domains.Services.AccountService import *
from MiniBank.Domains.Services.UserService import *
from MiniBank.Domains.Services.EventHandler import *

from MiniBank.Domains.Database.AccountRepository import *
from MiniBank.Domains.Database.UserRepository import *
from MiniBank.Domains.Database.EventRepository import *

def run(db_in_memory=True):
    if db_in_memory:
        event_repository = in_memory_EventRepository()
        user_repository = in_memory_UserRepository()
        account_repository = in_memory_AccountRepository
    else:
        event_repository = EventRepository()
        user_repository =UserRepository()
        account_repository = AccountRepository

    event_handler = EventHandler(event_repository)
    account_service = AccountService(account_repository, event_handler)
    user_service = UserService(user_repository, event_handler, account_service)
