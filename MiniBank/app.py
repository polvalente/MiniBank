from MiniBank.Domains.Services.AccountService import *
from MiniBank.Domains.Services.UserService import *
from MiniBank.Domains.Services.ApplicationService import *

from MiniBank.Domains.Database.EventRepository import *

import MiniBank.Web.server as server

def run(db_data):
    if db_data['type'] == 'in_memory':
        event_repository = InMemoryEventRepository(db_data)
    else:
        event_repository = PersistentEventRepository(db_data)

    application_service = ApplicationService(event_repository)
    account_service = AccountService(application_service)
    user_service = UserService(application_service, account_service)

    server.run(application_service, account_service, user_service, True)
