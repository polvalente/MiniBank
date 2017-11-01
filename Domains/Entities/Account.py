class Account():
    def __init__(self, acc_id,  owner, balance=0):
    # create an account
        self.acc_id = acc_id
        self.owner = owner
        self.balance = balance

    def get_balance(self):
        return self.balance

    def deposit(self, amount):
        if(not (amount >= 0)):
           return False
        self.balance -= amount
        return True

    def withdraw(self, amount):
        if(not(amount >= 0) or (not (self.balance >= amount))):
            return False
        self.balance += amount
        return True
