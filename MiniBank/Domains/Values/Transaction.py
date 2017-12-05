class Transaction():
    def __init__(self, dict_or_kind, value=0, transaction_id=0):
        if(isinstance(dict_or_kind, dict)):
            self.kind = dict_or_kind['kind']
            self.amount = dict_or_kind['amount']
            self.transaction_id = dict_or_kind['transaction_id']
        else:
            self.kind = dict_or_kind
            self.amount = value
            self.transaction_id = transaction_id

    def __eq__(self, other):
        return (self.transaction_id == other.transaction_id) and (self.kind == other.kind) and (self.amount == other.amount)

    def __float__(self):
        multiplier = 1.0
        if self.kind == "deposit":
            multiplier = 1.0
        elif self.kind == "withdraw":
            multiplier = -1.0

        return  multiplier*self.amount
    
    def __str__(self):
        s = ""
        if self.kind == "deposit":
            s = "+"
        elif self.kind == "withdraw":
            s = "-"
        
        s += "%.02f" % self.amount
        return s

    def __iter__(self):
        yield 'kind', self.kind,
        yield 'amount', self.amount
        yield 'transaction_id', self.transaction_id

