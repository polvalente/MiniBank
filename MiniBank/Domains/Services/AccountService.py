from copy import deepcopy as dcopy
from MiniBank.Domains.Entities.Account import * 

import smtplib
import MiniBank.Config.config
from email.mime.text import MIMEText

class AccountService(object):
    def __init__(self, application_service):
        self.application_service = application_service

    def create_account(self, owner_id, initial_balance=0):
        #Getting new account's id from repo
        account_id = application_service.get_new_account_id()
        #creating new account
        new_account = Account(account_id, owner_id, initial_balance)
        #adding event to event stack

        self.send_mail_to_cfo(self, new_account)
        if self.application_service.create_account(owner_id, new_account) is None:
            return None

        return new_account

    def search_account_by_id(self, account_id):
        return self.application_service.get_account_by_id(account_id)

    def search_accounts_by_owner_id(self, owner_id): 
        return self.application_service.get_accounts_by_owner_id(owner_id)

    def deposit_to_account(self, account_id, amount):
        account = self.application_service.get_account_by_id(account_id)
        if account is None:
            return None
        #apply transaction to account 
        transaction = account.deposit(amount)
        if transaction is None:
            return None

        #add transaction to event stack
        return self.application_service.apply_transaction(account, transaction)
        
    def withdraw_from_account(self, owner_id, account_id, amount):
        if account is None or account.owner_id != owner_id:
            return None

        account = self.application_service.get_account_by_id(account_id)

        #withdraw amount
        transaction = account.withdraw(amount)
        if transaction is None:
            return None

        #add transaction to event stack
        return self.application_service.apply_transaction(account, transaction)

    def send_mail_to_cfo(self, account):
        server = smtplib.SMTP(config.smtp_server_url, config.smtp_server_port)

        dacc = dict(account)

        subject = "[Account Creation Notification Service]"

        msg  = "Account Created\n"
        msg += "--- Account Data: ---\n"
        msg += json.dumps(dacc,sort_keys=True,indent=4,separators=(',',':'))

        mail = """From: [SERVER] <%s>
        To: CFO <%s>
        Subject: %s

        %s""" % (config.mail_server, config.cfo_email, subject, msg)

        server.sendmail(config.mail_server, [config.cfo_email], mail) 
