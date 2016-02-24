from architecture.privatemethod import privatemethod

from controller.BanksController import BanksController
from controller.PluginsController import PluginsController

from dao.CurrentDao import CurrentDao

class CurrentController:
    def __init__(self, app):
        self.app = app
        
        data = app.dao(CurrentDao).load()
        self.bank = data["bank"]
        self.patch = data["patch"]

    def setPatch(self, patch):
        if self.patch == patch:
            return
        
        self.patch = patch
        self.loadDevicePatch(self.bank, self.patch)
        self.saveCurrent(self.bank, self.patch)

    def setBank(self, bank):
        if self.bank == bank:
            return

        self.bank = bank
        self.loadDevicePatch(self.bank, self.patch)
        self.saveCurrent(self.bank, self.patch)
        
    @privatemethod
    def saveCurrent(self, bank, patch):
        print("saving:", bank, patch)

    @privatemethod
    def loadDevicePatch(self, bank, patch):
        deviceController = self.app.controller(DeviceController)
        banksController = self.app.controller(BanksController)
        
        bank = banksController.banks[self.bank]
        patch = self.bank.getPatch(self.patch)
        
        deviceController.setPatch(patch)