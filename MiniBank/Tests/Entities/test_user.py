import unittest
from MiniBank.Domains.Entities.User import *
from MiniBank.Domains.Entities.Account import *

class TestUser(unittest.TestCase):
    def setUp(self):
        self.user = User(-1, "Paulo", True)

    def test_add_account(self):
        user = self.user
        account1 = Account(0, user.uid)
        user.add_account(account1)
        self.assertEqual(user.accounts[-1].acc_id, account1.acc_id)

    def test_get_account_summary(self):
        user = self.user
        account0 = Account(0, user.uid)
        account1 = Account(1, user.uid)
        account2 = Account(2, user.uid)
        user.add_account(account0)
        user.add_account(account1)
        user.add_account(account2)
        expected_summary = "--- Account Summaries: ---\n"
        expected_summary+= account0.summary()+"\n"
        expected_summary+= account1.summary()+"\n"
        expected_summary+= account2.summary()
        self.assertEqual(user.get_account_summary(),expected_summary)

    def test_dict(self):
        user = self.user
        account0 = Account(0, user.uid)
        user.add_account(account0)

        udict = {'uid': -1, 'name': "Paulo", 'is_person':True, 'accounts':[dict(account0)]}
        cast = dict(user)
        for key in udict:
            self.assertEqual(udict[key],cast[key])

    def test_from_dict(self):
        user = self.user
        new_user = User(dict(user))
        self.assertEqual(user.uid, new_user.uid)
        self.assertEqual(user.name, new_user.name)
        self.assertEqual(user.is_person, new_user.is_person)
        self.assertEqual(user.accounts, new_user.accounts)

if __name__ == "__main__":
    unittest.main()
