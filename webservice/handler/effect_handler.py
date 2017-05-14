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
from webservice.util.handler_utils import integer

from application.controller.banks_controller import BanksController
from application.controller.effect_controller import EffectController
from application.controller.plugins_controller import PluginsController


class EffectHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None
    plugins = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(EffectController)
        self.banks = self.app.controller(BanksController)
        self.plugins = self.app.controller(PluginsController)

    @integer('bank_index', 'pedalboard_index', 'effect_index')
    def get(self, bank_index, pedalboard_index, effect_index):
        try:
            effect = self.banks.banks[bank_index].pedalboards[pedalboard_index].effects[effect_index]

            return self.write(effect.json)

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def post(self, bank_index, pedalboard_index):
        try:
            pedalboard = self.banks.banks[bank_index].pedalboards[pedalboard_index]
            uri = self.request_data

            effect = self.plugins.lv2_effect(uri)
            pedalboard.append(effect)
            self.controller.created(effect, self.token)
            effect_index = len(pedalboard.effects) - 1

            return self.created({"index": effect_index, "effect": effect.json})

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index', 'effect_index')
    def delete(self, bank_index, pedalboard_index, effect_index):
        try:
            effect = self.banks.banks[bank_index].pedalboards[pedalboard_index].effects[effect_index]

            self.controller.delete(effect, self.token)
            return self.success()

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)
