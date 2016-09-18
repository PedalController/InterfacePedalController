from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController
from application.controller.ParamController import ParamController

from util.HandlerUtils import HandlerUtils


class ParamHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(ParamController)
        self.banksController = self.app.controller(BanksController)

    def get(self, bankIndex, patchIndex, effectIndex, paramIndex):
        try:
            bankIndex, patchIndex, effectIndex, paramIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex, paramIndex
            )
            bank = self.banksController.banks[bankIndex]

            param = bank.patches[patchIndex].effects[effectIndex].params[paramIndex]
            return self.write(param.json)

        except IndexError as error:
            return self.error(str(error))
        except Exception as error:
            self.printError()
            return self.send(500)

    def put(self, bankIndex, patchIndex, effectIndex, paramIndex):
        try:
            bankIndex, patchIndex, effectIndex, paramIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex, paramIndex
            )

            bank = self.banksController.banks[bankIndex]
            param = bank.patches[patchIndex].effects[effectIndex].params[paramIndex]
            value = self.getRequestData()

            self.controller.updateValue(param, value, self.token)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
