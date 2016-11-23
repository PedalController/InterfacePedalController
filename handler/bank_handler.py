from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController

from pluginsmanager.util.persistence import Persistence


class BankHandler(AbstractRequestHandler):
    app = None
    controller = None
    decoder = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)
        sys_effect = self.app.controller(DeviceController).sys_effect
        self.decoder = Persistence(sys_effect)

    def get(self, bankIndex):
        try:
            bankIndex = int(bankIndex)
            bank = self.controller.banks[bankIndex]

            self.write(bank.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def post(self):
        try:
            json = self.getRequestData()
            bank = self.decoder.read(json)

            index = self.controller.create(bank, self.token)

            self.created({"index": index})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def put(self, bankIndex):
        try:
            json = self.getRequestData()
            bankIndex = int(bankIndex)

            new_bank = self.decoder.read(json)
            old_bank = self.controller.banks[bankIndex]

            self.controller.replace(old_bank, new_bank, self.token)

            self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def delete(self, bankIndex):
        bankIndex = int(bankIndex)

        try:
            self.controller.delete(self.controller.banks[bankIndex], self.token)
            self.success()
        except IndexError as error:
            return self.error(str(error))
