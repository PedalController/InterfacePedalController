from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController
from application.controller.patch_controller import PatchController

from util.HandlerUtils import HandlerUtils

from pluginsmanager.util.persistence import PatchReader


class PatchHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PatchController)
        self.banks = self.app.controller(BanksController)

        self.decode = PatchReader(self.app.controller(DeviceController).sys_effect)

    def get(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            bank = self.banks.banks[bankIndex]
            patch = bank.patches[patchIndex]

            return self.write(patch.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def post(self, bankIndex):
        try:
            bankIndex = int(bankIndex)
            patch = self.decode.read(self.getRequestData())

            bank = self.banks.banks[bankIndex]
            bank.append(patch)
            self.controller.created(patch, self.token)

            return self.created({"index": len(bank.patches) - 1})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def put(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            old_patch = self.banks.banks[bankIndex].patches[patchIndex]
            new_patch = self.decode.read(self.getRequestData())

            self.controller.replace(old_patch, new_patch, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def delete(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            patch = self.banks.banks[bankIndex].patches[patchIndex]
            self.controller.delete(patch, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
