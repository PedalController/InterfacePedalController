import json
import glob

from architecture.privatemethod import privatemethod

from model.Bank import Bank

class DataController:
    dataPath = ""
    _banks = []
    
    def __init__(self, dataPath):
        self.dataPath = dataPath
        self.readBank(dataPath)
        
    @privatemethod
    def readBank(self, dataPath):
        for file in glob.glob(dataPath + "*.json"):
            bank = Bank(DataBank.read(file))
            self._banks.append(bank)

    def saveBank(self, bank):
        url = self.dataPath + "/" + bank.name + ".json"
        DataBank.save(url, bank)

    @property
    def banks(self):
        return self._banks

    '''
    @my_attribute.setter
    def my_attribute(self, value):
        # Do something if you want
        self._my_attribute = value
    '''

class DataBank:

    @staticmethod
    def read(url):
        with open(url) as data_file:    
            return json.load(data_file)

    def save(url, data):
        jsonFile = open(url, "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()
