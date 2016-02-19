class Banks:
    banks = []
    
    def __init__(self, banksList):
        self.banks = banksList
    
    def get(self, index):
        hasBank = len(self.banks) >= index+1
        return self.banks[index] if hasBank else None
    
    @property
    def json(self):
        banks = []
        for bank in self.banks:
            banks.append(bank.data)

        return banks