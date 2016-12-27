from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController

from util.handler_utils import integer


class CurrentPedalboardHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app
        self.controller = app.controller(CurrentController)
        self.banks = app.controller(BanksController)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        bank_changed_and_pedalboard_not_changed = self.controller.bank_number != bank_index \
                                              and self.controller.pedalboard_number == pedalboard_index

        bank = self.banks.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        self.controller.set_bank(bank, notify=bank_changed_and_pedalboard_not_changed, token=self.token)
        self.controller.set_pedalboard(pedalboard, token=self.token)
