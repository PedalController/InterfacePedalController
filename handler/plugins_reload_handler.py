from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.plugins_controller import PluginsController, PluginTechnology


class PluginsReloadHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def put(self):
        controller = self.app.controller(PluginsController)

        try:
            controller.reload_lv2_plugins_data()
            self.write({'status': 'ok'})
        except ImportError:
            self.error('"lilv" not configured')
