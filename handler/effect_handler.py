from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.effect_controller import EffectController
from application.controller.plugins_controller import PluginsController

from util.handler_utils import integer


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
            effect = self.banks.banks[bank_index].patches[pedalboard_index].effects[effect_index]

            return self.write(effect.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def post(self, bank_index, pedalboard_index):
        try:
            pedalboard = self.banks.banks[bank_index].patches[pedalboard_index]
            uri = self.request_data

            effect = self.plugins.lv2_effect(uri)
            pedalboard.append(effect)
            self.controller.created(effect, self.token)
            effect_index = len(pedalboard.effects) - 1

            return self.created({"index": effect_index, "effect": effect.json})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index', 'effect_index')
    def delete(self, bank_index, pedalboard_index, effect_index):
        try:
            effect = self.banks.banks[bank_index].patches[pedalboard_index].effects[effect_index]

            self.controller.delete(effect, self.token)
            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
