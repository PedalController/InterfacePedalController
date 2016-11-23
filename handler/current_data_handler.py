from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController


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
