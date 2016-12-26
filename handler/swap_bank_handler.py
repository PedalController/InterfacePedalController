from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController, BankError

from util.handler_utils import integer


class SwapBankHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app
        self.controller = self.app.controller(BanksController)

    @integer('bank_a_index', 'bank_b_index')
    def put(self, bank_a_index, bank_b_index):
        try:
            banks = self.controller.banks
            bank_a = banks[bank_a_index]
            bank_b = banks[bank_b_index]

            self.controller.swap(bank_a, bank_b, self.token)

            return self.success()

        except BankError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
