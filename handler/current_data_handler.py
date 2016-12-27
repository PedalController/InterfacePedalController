from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.current_controller import CurrentController


class CurrentDataHandler(AbstractRequestHandler):
    app = None
    controller = None
    banksController = None

    def initialize(self, app):
        self.controller = app.controller(CurrentController)

    def get(self):
        json = {
            'bank': self.controller.current_bank.json,
            'pedalboard': self.controller.pedalboard_number
        }

        self.send(200, json)
