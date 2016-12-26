from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.plugins_controller import PluginsController, PluginTechnology


class PluginsHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self):
        controller = self.app.controller(PluginsController)

        plugins = []
        for plugin in controller.by(PluginTechnology.LV2).values():
            plugins.append(plugin.json)

        self.write({'plugins': plugins})
