from handler.AbstractRequestHandler import AbstractRequestHandler

from controller.CurrentController import CurrentController
from controller.BanksController import BanksController



class CurrentDataHandler(AbstractRequestHandler):
    app = None
    controller = None
    banksController = None

    def initialize(self, app):
        self.controller = app.controller(CurrentController)
        self.banksController = app.controller(BanksController)

    def get(self):
        json = {
            'bank': self.banksController.banks[self.controller.bankNumber].json,
            'patch': self.controller.patchNumber
        }

        self.send(200, json)
