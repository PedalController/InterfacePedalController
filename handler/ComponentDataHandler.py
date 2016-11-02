from handler.AbstractRequestHandler import AbstractRequestHandler

from controller.ComponentDataController import ComponentDataController


class ComponentDataHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.controller = app.controller(ComponentDataController)

    def get(self, key):
        self.send(200, self.controller[key])

    def post(self, key):
        self.controller[key] = self.getRequestData()

        self.success()

    def delete(self, key):
        del self.controller[key]

        self.success()
