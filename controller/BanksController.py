from dao.BankDao import BankDao
from architecture.privatemethod import privatemethod

from model.Bank import Bank

class BanksController:
    banks = []
    
    def __init__(self, app):
        self.app = app
        self.load()

    @privatemethod
    def load(self):
        self.banks = self.app.dao(BankDao).all

    '''
    ***********************************
    Data CRUD
    ***********************************
    '''
    def createBank(self, banks, bank):
        bank = Bank(bank)
        banks.append(bank)
        return len(banks) - 1
    
    def createPatch(self, bank, patch):
        bank.addPatch(patch)
        return len(bank.patches) - 1
    
    def addEffect(self, bank, indexPatch, effect):
        bank.addEffect(indexPatch, effect)
        return len(bank.getEffects(indexPatch)) - 1
    
    def update(self, data, value):
        data.clear()
        data.update(value)