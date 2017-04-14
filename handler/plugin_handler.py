from handler.abstract_request_handler import AbstractRequestHandler
from application.controller.plugins_controller import PluginsController, PluginTechnology


class PluginHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self, uri):
        controller = self.app.controller(PluginsController)
        plugins = controller.by(PluginTechnology.LV2)

        if uri in plugins:
            self.write(plugins[uri].json)
        else:
            self.error('Plugin "{}" not installed'.format(uri))
