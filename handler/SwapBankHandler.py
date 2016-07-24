from architecture.BankError import BankError
from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController

from util.HandlerUtils import HandlerUtils


class SwapBankHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app
        self.controller = self.app.controller(BanksController)

    def put(self, bankAIndex, bankBIndex):
        try:
            bankAIndex, bankBIndex = HandlerUtils.toInt(bankAIndex, bankBIndex)

            banks = self.controller.banks
            bankA = banks[bankAIndex]
            bankB = banks[bankBIndex]

            self.controller.swapBanks(bankA, bankB)

            return self.success()

        except BankError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
