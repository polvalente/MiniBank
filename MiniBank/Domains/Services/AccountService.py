from copy import deepcopy as dcopy
from MiniBank.Domains.Entities.Account import * 

import smtplib
import MiniBank.Config.config
from email.mime.text import MIMEText

class AccountService(object):
    def __init__(self, account_repository, event_handler):
        self.account_repository = account_repository
        self.event_handler = event_handler

    def create_account(self, owner, initial_balance=0):
        #Getting new account's id from repo
        account_id = account_repository.get_new_account_id()
        #creating new account
        new_account = Account(account_id, owner, initial_balance)
        #adding event to event stack
        self.event_handler.create_account(new_account)

        self.send_mail_to_cfo(self, new_account)

        return self.account_repository.persist_account(new_account) # returns maybe account
 
    def search_account_by_id(self, account_id):
        return self.account_repository.search_account_by_id(account_id)

    def search_accounts_by_owner(self, owner): 
        return self.account_repository.search_accounts_by_owner(owner)

    def deposit_to_account(self, account_id, amount):
        account = self.search_account_by_id(account_id)
        if account is None:
            return None
        #apply transaction to account 
        transaction = account.deposit(amount)

        #persist modified account to repo
        self.account_repository.persist_account(account)

        #add transaction to event stack
        self.event_handler.apply_transaction(transaction)

        return dcopy(transaction)
        
    def withdraw_from_account(self, owner, account_id, amount):
        account = self.search_account_by_id(account_id)

        if account is None or account.owner != owner:
            return None

        #withdraw amount
        transaction = account.withdraw(amount)

        #persist modified account
        self.account_repository.persist_account(account)

        #add transaction to event stack
        self.event_handler.apply_transaction(transaction)

        return dcopy(transaction)

    def send_mail_to_cfo(self, account):
        server = smtplib.SMTP(config.smtp_server_url, config.smtp_server_port)

        dacc = dict(account)
        dacc['owner'] = dacc['owner'].name

        subject = "[Account Creation Notification Service]"

        msg  = "Account Created\n"
        msg += "--- Account Data: ---\n"
        msg += json.dumps(dacc,sort_keys=True,indent=4,separators=(',',':'))

        mail = """From: [SERVER] <%s>
        To: CFO <%s>
        Subject: %s

        %s""" % (config.mail_server, config.cfo_email, subject, msg)

        server.sendmail(config.mail_server, [config.cfo_email], mail) 
