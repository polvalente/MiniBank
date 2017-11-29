from MiniBank.Domains.Values.Transaction import *
class Account():
    def __init__(self, acc_id,  owner, balance=0):
    # create an account
        self.acc_id = acc_id
        self.owner = owner
        self.balance = balance
        self.history = [Transaction("deposit", balance)]

    def __iter__(self):
        yield 'account_id', self.acc_id
        yield 'owner', self.owner
        yield 'balance', self.balance
        yield 'history', self.history

    def deposit(self, amount):
        #check if amount is valid
        if(not (amount >= 0)):
           return None

        #amount is valid, add amount to account balance
        self.balance += amount

        #Add transaction to account history
        t = Transaction("deposit", amount)
        self.history.append(t)

        #Return the transaction
        return t

    def withdraw(self, amount):
        #check if amount is valid and if there is enough balance
        if(not(amount >= 0) or (not (self.balance >= amount))):
            return None

        #everything is ok, subtract amount from account balance
        self.balance -= amount

        #Add transaction to account history
        t = Transaction("withdraw", amount)
        self.history.append(t)
        #Return the transaction
        return t

    def summary(self):
        s =  "--- Account %d summary: ---\n" % self.acc_id
        s += '\n'.join(map(lambda x: '> '+str(x), self.history))  
        s += '\nBalance: %.2f' % (sum(map(float, self.history)))
        return s
