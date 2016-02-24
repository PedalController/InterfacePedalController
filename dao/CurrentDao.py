from dao.DataBank import DataBank
from architecture.privatemethod import privatemethod

class CurrentDao:
    dataPath = ""
    
    def __init__(self, dataPath):
        self.dataPath = dataPath + 'current/'
    
    def load(self):
        return self.readFile()
        
    @privatemethod
    def readFile(self):
        return DataBank.read(self.dataPath + "current.json")

