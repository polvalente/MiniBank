import unittest
from copy import deepcopy
from MiniBank.Domains.Entities.Account import *
from MiniBank.Domains.Values.Transaction import *

class TestAccount(unittest.TestCase):

    def setUp(self):
        self.account = Account(-1, "Paulo", 100) 

    def test_create_account(self):
        '''Created account should have the variables stored accordingly'''
        account = self.account
        self.assertEqual(account.acc_id,-1)
        self.assertEqual(account.owner, "Paulo")
        self.assertEqual(account.balance, 100)
        self.assertEqual(account.history, [])

    def test_deposit(self):
        account = self.account
        self.assertEqual(account.deposit(20), Transaction("deposit", 20))
        self.assertEqual(account.balance, 120)
        self.assertEqual(account.history, [Transaction("deposit", 20)])
        self.assertEqual(account.deposit(-1), None)

    def test_withdraw(self):
        account = self.account
        self.assertEqual(account.withdraw(20), Transaction("withdraw", 20))
        self.assertEqual(account.history, [Transaction("withdraw", 20)])
        self.assertEqual(account.withdraw(-1), None)
        self.assertEqual(account.withdraw(81), None)
        self.assertEqual(account.balance, 80)

if __name__ == "__main__":
    unittest.main()
