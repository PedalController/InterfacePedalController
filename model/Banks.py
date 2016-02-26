class Banks:
    banks = []
    
    '''
    @param banksList = List[Bank]
    '''
    def __init__(self, banksList):
        self.banks = banksList
    
    def __len__(self):
        return len(self.banks)
    
    def __getitem__(self, index):
        return self.get(index)

    def get(self, index):
        hasBank = len(self.banks) >= index+1
        try:
            return self.banks[index]
        except IndexError:
            raise IndexError("Element not found")
    
    def append(self, bank):
        self.banks.append(bank)
        
    @property
    def json(self):
        banks = []
        for bank in self.banks:
            banks.append(bank.data)

        return banks