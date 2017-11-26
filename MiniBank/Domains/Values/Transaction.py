class Transaction():
    def __init__(self, kind, value):
        self.kind = kind
        self.amount = value

    def __eq__(self, other):
        return (self.kind == other.kind) and (self.amount == other.amount)

    def __float__(self):
        multiplier = 1
        if self.kind == "deposit":
            multiplier = 1
        elif self.kind == "withdraw":
            multiplier = -1

        return  multiplier*self.value
    
    def __str__(self):
        s = ""
        if self.kind == "deposit":
            s = "+"
        elif self.kind == "withdraw":
            s = "-"
        
        s += "%.02f" % self.amount
        return s

    def __dict__(self):
        return {
                'kind': self.kind,
                'amount': self.amount
                }

