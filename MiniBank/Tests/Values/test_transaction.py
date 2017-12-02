import unittest
from MiniBank.Domains.Values.Transaction import *

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.deposit = Transaction("deposit", 5.5)
        self.withdraw = Transaction("withdraw", 5.5)

    def test_eq(self):
        self.assertTrue(self.deposit == Transaction("deposit", 5.5))

    def test_float(self):
        self.assertEqual(float(self.deposit),5.5)

    def test_str(self):
        self.assertEqual(str(self.deposit), "+5.50")
        self.assertEqual(str(self.withdraw), "-5.50")

    def test_dict(self):
        tdict = {'kind': "deposit", 'amount':5.5}
        cast = dict(self.deposit)
        for key in cast:
            self.assertEqual(tdict[key], cast[key])
    def test_from_dict(self):
        tdict = {'kind': "deposit", 'amount':5.5}
        self.assertEqual(self.deposit,Transaction(tdict))

if __name__ == "__main__":
    unittest.main()
