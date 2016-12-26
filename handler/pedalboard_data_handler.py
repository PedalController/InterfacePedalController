from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.pedalboard_controller import PedalboardController

from util.handler_utils import integer

from pluginsmanager.util.persistence_decoder import PedalboardReader


class PedalboardDataHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PedalboardController)
        self.banks = self.app.controller(BanksController)

    @integer('bank_index', 'pedalboard_index')
    def get(self, bank_index, pedalboard_index, key):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]

            if key not in pedalboard.data:
                return self.write({})

            return self.write(pedalboard.data[key])

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index, key):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]
            pedalboard.data[key] = self.request_data

            self.controller.update(pedalboard, self.token, reload=False)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
