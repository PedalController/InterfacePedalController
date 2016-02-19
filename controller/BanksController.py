from dao.BankDao import BankDao
from architecture.privatemethod import privatemethod

class BanksController:
    banks = []
    
    def __init__(self, app):
        self.app = app
        self.load()

    @privatemethod
    def load(self):
        self.banks = self.app.dao(BankDao).all
