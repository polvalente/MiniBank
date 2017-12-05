from copy import deepcopy as dcopy
from MiniBank.Domains.Entities.Account import * 

import smtplib, json
from MiniBank.Config import config
from email.mime.text import MIMEText

class AccountService(object):
    def __init__(self, application_service):
        self.application_service = application_service
        self.accounts_to_send = []

    def create_account(self, owner_id, initial_balance=0):
        #Getting new account's id from repo
        account_id = self.application_service.get_new_account_id()
        transaction_id = self.application_service.get_new_transaction_id()
        #creating new account
        if initial_balance < 0:
            return None
        new_account = Account(account_id, owner_id, initial_balance, transaction_id)
        #adding event to event stack

        self.send_mail_to_cfo(new_account)
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
        if not account.can_deposit(amount):
            return None
        
        transaction_id = self.application_service.get_new_transaction_id()
        transaction = Transaction("deposit", amount, transaction_id)

        #add transaction to event stack
        return self.application_service.apply_transaction(account, transaction)
        
    def withdraw_from_account(self, owner_id, account_id, amount):
        account = self.application_service.get_account_by_id(account_id)
        if account is None or account.owner_id != owner_id:
            return None

        #withdraw amount
        if not account.can_withdraw(amount):
            return None

        transaction_id = self.application_service.get_new_transaction_id()
        transaction = Transaction("withdraw", amount, transaction_id)

        #add transaction to event stack
        return self.application_service.apply_transaction(account, transaction)

    def send_mail_to_cfo(self, account):
        self.accounts_to_send.append(account)
        try:
            server = smtplib.SMTP(config.smtp_server_url, config.smtp_server_port)
        except:
            return None

        self.accounts_to_send.append(account)
        for account in self.accounts_to_send:
            dacc = dict(account)

            subject = "[Account Creation Notification Service]"

            msg  = "Account Created\n"
            msg += "--- Account Data: ---\n"
            msg += json.dumps(dacc,sort_keys=True,indent=4,separators=(',',':'))

            mail = """From: [SERVER] <%s>
            To: CFO <%s>
            Subject: %s

            %s""" % (config.mail_server, config.cfo_email, subject, msg)

            try:
                server.sendmail(config.mail_server, [config.cfo_email], mail) 
            except:
                return
        self.accounts_to_send = []

