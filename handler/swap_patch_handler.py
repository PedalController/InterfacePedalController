from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.banks_controller import BanksController, BankError

from util.HandlerUtils import HandlerUtils


class SwapPatchHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    def put(self, bankIndex, patchAIndex, patchBIndex):
        try:
            bankIndex, patchAIndex, patchBIndex = HandlerUtils.toInt(
                bankIndex, patchAIndex, patchBIndex
            )

            patches = self.controller.banks[bankIndex].patches
            patchA = patches[patchAIndex]
            patchB = patches[patchBIndex]

            self.controller.swapPatches(patchA, patchB)

            return self.success()

        except BankError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
