import json
import glob

from dao.DataBank import DataBank
from architecture.privatemethod import privatemethod

from model.Bank import Bank
from model.Banks import Banks

class BankDao:
    dataPath = ""
    
    def __init__(self, dataPath):
        self.dataPath = dataPath + 'banks/'
    
    @property
    def all(self):
        return self.readBanks(self.dataPath)
        
    #@privatemethod
    def readBanks(self, dataPath):
        banks = Banks([])
        
        for file in glob.glob(dataPath + "*.json"):
            bank = Bank(DataBank.read(file))
            banks.append(bank)
        
        return banks

    '''
    def saveBank(self, bank):
        url = self.dataPath + "/" + bank.name + ".json"
        DataBank.save(url, bank)
    '''

    '''
    @my_attribute.setter
    def my_attribute(self, value):
        # Do something if you want
        self._my_attribute = value
    '''

