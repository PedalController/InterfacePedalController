from controller.PluginsController import PluginsController
import tornado.web


class PluginsHandler(tornado.web.RequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(PluginsController)

        self.write({'plugins': list(controller.plugins.values())})