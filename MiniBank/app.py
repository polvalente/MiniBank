from MiniBank.Domains.Services.AccountService import *
from MiniBank.Domains.Services.UserService import *
from MiniBank.Domains.Services.ApplicationService import *

from MiniBank.Domains.Database.EventRepository import *

def run(db_data):
    if db_data['type'] == 'in memory':
        event_repository = InMemoryEventRepository(db_data)
    else:
        event_repository = PersistentEventRepository(db_data)

    application_service = EventHandler(event_repository)
    account_service = AccountService(event_handler)
    user_service = UserService(application_service, account_service)
