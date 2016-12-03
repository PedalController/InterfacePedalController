from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.pedalboard_controller import PedalboardController

from util.handler_utils import integer

from pluginsmanager.util.persistence_decoder import PedalboardReader


class PedalboardHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None
    decode = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PedalboardController)
        self.banks = self.app.controller(BanksController)

        self.decode = PedalboardReader(self.app.controller(DeviceController).sys_effect)

    @integer('bank_index', 'pedalboard_index')
    def get(self, bank_index, pedalboard_index):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]

            return self.write(pedalboard.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index')
    def post(self, bank_index):
        try:
            pedalboard = self.decode.read(self.request_data)

            bank = self.banks.banks[bank_index]
            bank.append(pedalboard)
            self.controller.created(pedalboard, self.token)

            return self.created({"index": len(bank.pedalboards) - 1})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        try:
            old_pedalboard = self.banks.banks[bank_index].pedalboards[pedalboard_index]
            new_pedalboard = self.decode.read(self.request_data)

            self.controller.replace(old_pedalboard, new_pedalboard, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def delete(self, bank_index, pedalboard_index):
        try:
            pedalboard = self.banks.banks[bank_index].pedalboards[pedalboard_index]
            self.controller.delete(pedalboard, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
