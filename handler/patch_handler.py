from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController
from application.controller.patch_controller import PatchController

from util.HandlerUtils import HandlerUtils


class PatchHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PatchController)
        self.banksController = self.app.controller(BanksController)

    def get(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            bank = self.banksController.banks[bankIndex]
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
            body = self.getRequestData()

            bank = self.banksController.banks.banks[bankIndex]
            index = self.controller.createPatch(bank, body, self.token)

            return self.created({"index": index})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def put(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            patch = self.banksController.banks[bankIndex].patches[patchIndex]
            data = self.getRequestData()

            self.controller.updatePatch(patch, data, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def delete(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            patch = self.banksController.banks[bankIndex].patches[patchIndex]
            self.controller.deletePatch(patch, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
