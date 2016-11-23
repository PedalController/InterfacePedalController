from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController


class BanksHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(BanksController)

        banks = {}
        for bank in controller.banks:
            banks[bank.index] = bank.json

        self.write({"banks": banks})
