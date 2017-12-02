class Transaction():
    def __init__(self, dict_or_kind, value=None):
        if(isinstance(dict_or_kind, dict)):
            self.kind = dict_or_kind['kind']
            self.amount = dict_or_kind['amount']
        else:
            self.kind = dict_or_kind
            self.amount = value

    def __eq__(self, other):
        return (self.kind == other.kind) and (self.amount == other.amount)

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

