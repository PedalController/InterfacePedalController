from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.component_data_controller import ComponentDataController


class ComponentDataHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.controller = app.controller(ComponentDataController)

    def get(self, key):
        self.send(200, self.controller[key])

    def post(self, key):
        self.controller[key] = self.request_data

        self.success()

    def delete(self, key):
        del self.controller[key]

        self.success()
