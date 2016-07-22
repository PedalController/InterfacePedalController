from controller.PluginsController import PluginsController
from handler.AbstractRequestHandler import AbstractRequestHandler


class PluginsHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(PluginsController)

        self.write({'plugins': list(controller.plugins.values())})
