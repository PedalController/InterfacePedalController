from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController


class BanksHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(BanksController)

        self.write({"banks": controller.banks.json})
