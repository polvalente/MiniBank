from MiniBank.Domains.Values.Transaction import *

class Account():
    def __init__(self, dict_or_acc_id,  owner_id=None, balance=0):
    # create an account
        if(isinstance(dict_or_acc_id, dict)):
            self.acc_id = dict_or_acc_id['account_id']
            self.owner_id = dict_or_acc_id['owner_id'] 
            self.balance = dict_or_acc_id['balance']
            self.history = map(lambda t: Transaction(t), dict_or_acc_id['history'])
        else:
            self.acc_id = dict_or_acc_id
            self.owner_id = owner_id
            self.balance = balance
            self.history = [Transaction("deposit", balance)]

    def __eq__(self, other):
        return self.acc_id == other.acc_id and\
                self.owner_id == other.owner_id and\
                self.balance == other.balance and\
                self.history == other.history

    def __iter__(self):
        yield 'account_id', self.acc_id
        yield 'owner_id', self.owner_id
        yield 'balance', self.balance
        yield 'history', map(dict,self.history)

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
