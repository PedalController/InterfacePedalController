# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from webservice.handler.abstract_request_handler import AbstractRequestHandler

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
