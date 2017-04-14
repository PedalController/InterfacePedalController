from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.param_controller import ParamController

from util.handler_utils import integer


class ParamHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(ParamController)
        self.banks = self.app.controller(BanksController)

    @integer('bank_index', 'pedalboard_index', 'effect_index', 'param_index')
    def get(self, bank_index, pedalboard_index, effect_index, param_index):
        try:
            bank = self.banks.banks[bank_index]

            param = bank.pedalboards[pedalboard_index].effects[effect_index].params[param_index]
            return self.write(param.json)

        except IndexError as error:
            return self.error("Invalid index")
        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index', 'effect_index', 'param_index')
    def put(self, bank_index, pedalboard_index, effect_index, param_index):
        try:
            bank = self.banks.banks[bank_index]
            param = bank.pedalboards[pedalboard_index].effects[effect_index].params[param_index]
            value = self.request_data

            param.value = value
            self.controller.updated(param, self.token)

            return self.success()

        except IndexError as error:
            return self.error("Invalid index")
        except Exception:
            self.print_error()
            return self.send(500)
