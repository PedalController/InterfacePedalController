from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.plugins_controller import PluginsController


class PluginsHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(PluginsController)

        self.write({'plugins': list(controller.plugins.values())})
