from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.pedalboard_controller import PedalboardController
from application.controller.banks_controller import BanksController

from util.handler_utils import integer


class SwapPedalboardHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app

        self.banks = self.app.controller(BanksController)
        self.controller = self.app.controller(PedalboardController)

    @integer('bank_index', 'pedalboard_a_index', 'pedalboard_b_index')
    def put(self, bank_index, pedalboard_a_index, pedalboard_b_index):
        try:
            pedalboards = self.banks.banks[bank_index].pedalboards
            pedalboard_a = pedalboards[pedalboard_a_index]
            pedalboard_b = pedalboards[pedalboard_b_index]

            self.controller.swap(pedalboard_a, pedalboard_b, self.token)

            return self.success()

        except Exception:
            self.print_error()
            return self.send(500)
