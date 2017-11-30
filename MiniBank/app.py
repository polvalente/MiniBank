from MiniBank.Domains.Services.AccountService import *
from MiniBank.Domains.Services.UserService import *
from MiniBank.Domains.Services.EventHandler import *

from MiniBank.Domains.Database.AccountRepository import *
from MiniBank.Domains.Database.UserRepository import *
from MiniBank.Domains.Database.EventRepository import *

def run(db_in_memory=True):
    if db_in_memory:
        event_repository = in_memory_EventRepository()
    else:
        event_repository = EventRepository()

    event_handler = EventHandler(event_repository)
    account_service = AccountService(event_handler)
    user_service = UserService(event_handler, account_service)
