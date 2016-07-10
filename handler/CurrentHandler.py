from handler.AbstractRequestHandler import AbstractRequestHandler

from controller.CurrentController import CurrentController


class CurrentHandler(AbstractRequestHandler):
    app = None

    controller = None

    def initialize(self, app):
        self.controller = app.controller(CurrentController)

    def get(self):
        json = {
            'bank': self.controller.bankNumber,
            'patch': self.controller.patchNumber
        }

        self.send(200, json)
