from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.plugins_controller import PluginsController


class BanksHandler(AbstractRequestHandler):
    app = None
    controller = None
    plugins = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)
        self.plugins = self.app.controller(PluginsController)

    def get(self):
        banks = {}

        for bank in self.controller.banks:
            json = bank.json
            banks[bank.index] = json
            for pedalboard in json['pedalboards']:
                for effect in pedalboard['effects']:
                    technology = effect['technology']
                    uri = effect['plugin']

                    effect['pluginData'] = self.plugins.by(technology.upper())[uri].json

        self.write({"banks": banks})
