from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController, BankError

from util.handler_utils import integer


class SwapPedalboardHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    @integer('bank_index', 'pedalboard_a_index', 'pedalboard_b_index')
    def put(self, bank_index, pedalboard_a_index, pedalboard_b_index):
        try:
            pedalboards = self.controller.banks[bank_index].patches
            pedalboard_a = pedalboards[pedalboard_a_index]
            pedalboard_b = pedalboards[pedalboard_b_index]

            self.controller.swapPatches(pedalboard_a, pedalboard_b)

            return self.success()

        except BankError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
