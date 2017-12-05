import unittest
from copy import deepcopy
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Values.Transaction import *

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(-1, 1, 100,1) 

    def test_create_account(self):
        '''Created account should have the variables stored accordingly'''
        account = self.account
        self.assertEqual(account.acc_id,-1)
        self.assertEqual(account.owner_id, 1)
        self.assertEqual(account.balance, 100)
        self.assertEqual(account.history, [Transaction("deposit", 100, 1)])

    def test_deposit(self):
        account = self.account
        self.assertEqual(account.deposit(20, 2), Transaction("deposit", 20, 2))
        self.assertEqual(account.balance, 120)
        self.assertEqual(account.history, [Transaction("deposit", 100, 1), Transaction("deposit", 20, 2)])
        self.assertEqual(account.deposit(-1, 3), None)

    def test_withdraw(self):
        account = self.account
        self.assertEqual(account.withdraw(20, 2), Transaction("withdraw", 20, 2))
        self.assertEqual(account.history, [Transaction("deposit",100, 1), Transaction("withdraw", 20, 2)])
        self.assertEqual(account.withdraw(-1, 3), None)
        self.assertEqual(account.withdraw(81, 3), None)
        self.assertEqual(account.balance, 80)

    def test_summary(self):
        account = self.account
        account.deposit(10, 2)
        account.withdraw(10, 3)
        account.withdraw(20, 4)
        expected_summary = "--- Account -1 summary: ---\n"
        expected_summary+= "> +100.00\n"
        expected_summary+= "> +10.00\n"
        expected_summary+= "> -10.00\n"
        expected_summary+= "> -20.00\n"
        expected_summary+= "Balance: 80.00"
        self.assertEqual(account.summary(),expected_summary)

    def test_dict(self):
        account = self.account
        adict = {'account_id': -1, 'owner_id': 1, 'balance': 100, 'history': [dict(Transaction("deposit", 100, 1))]}
        cast = dict(account)
        for key in adict:
            self.assertEqual(adict[key],cast[key])

    def test_from_dict(self):
        account = self.account
        adict = {'account_id': -1, 'owner_id': 1, 'balance': 100, 'history': [dict(Transaction("deposit", 100, 1))]}
        new_account = Account(adict)
        self.assertEqual(account.acc_id,new_account.acc_id)
        self.assertEqual(account.owner_id, new_account.owner_id)
        self.assertEqual(account.balance, new_account.balance)
        self.assertEqual(account.history, new_account.history)






if __name__ == "__main__":
    unittest.main()
