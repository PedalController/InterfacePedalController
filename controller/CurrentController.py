from architecture.privatemethod import privatemethod

from controller.BanksController import BanksController
from controller.PluginsController import PluginsController
from controller.DeviceController import DeviceController

from dao.CurrentDao import CurrentDao

class CurrentController:
    bank = 0
    patch = 0
    def __init__(self, app):
        self.app = app
        
        data = app.dao(CurrentDao).load()
        self.bank = data["bank"]
        self.patch = data["patch"]
    
    def toggleStatusEffect(self, effectNumber):
        patch = self.getCurrentPatch()

        try:
            effect = patch["effects"][effectNumber]
        except IndexError:
            raise IndexError("Element not found")
            
        effect["active"] = not effect["active"]

        deviceController = self.app.controller(DeviceController)
        deviceController.toggleStatusEffect(effectNumber)
        self.saveCurrent()
        
    def setPatch(self, patch):
        if self.patch == patch:
            return
        
        self.patch = patch
        self.loadDevicePatch(self.bank, self.patch)
        self.saveCurrent()

    def setBank(self, bank):
        if self.bank == bank:
            return

        self.bank = bank
        self.patch = 0
        self.loadDevicePatch(self.bank, self.patch)
        self.saveCurrent()
    
    @privatemethod
    def saveCurrent(self):
        
        print("saving:", self.bank)

    @privatemethod
    def save(self, bank):
        print("saving:", bank)

    @privatemethod
    def loadDevicePatch(self, bank, patch):
        deviceController = self.app.controller(DeviceController)
        patch = self.getPatch(bank, patch)
        
        deviceController.setPatch(patch)
    
    @privatemethod
    def getCurrentPatch(self):
        return self.getPatch(self.bank, self.patch)
    
    @privatemethod
    def getPatch(self, bank, patch):
        banksController = self.app.controller(BanksController)
        
        bank = banksController.banks[bank]
        return bank.getPatch(patch)