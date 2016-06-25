from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController
from application.controller.EffectController import EffectController

from util.HandlerUtils import HandlerUtils


class EffectHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(EffectController)
        self.banksController = self.app.controller(BanksController)

    def get(self, bankIndex, patchIndex, effectIndex):
        try:
            bankIndex, patchIndex, effectIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex
            )
            bank = self.banksController.banks[bankIndex]

            return self.write(bank.getEffect(patchIndex, effectIndex))

        except IndexError as error:
            return self.error(str(error))

        except Exception as error:
            self.printError()
            return self.send(500)

    def post(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)
            body = self.getRequestData()

            bank = self.banksController.banks[bankIndex]
            patch = bank.patches[patchIndex]
            index = self.controller.createEffect(bank, patch, body)

            return self.created({"index": index})

        except IndexError as error:
            return self.error(str(error))

        except Exception as error:
            self.printError()
            return self.send(500)

    def delete(self, bankIndex, patchIndex, effectIndex):
        try:
            bankIndex, patchIndex, effectIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex
            )

            bank = self.banksController.banks[bankIndex]
            patch = bank.patches[patchIndex]

            self.controller.deleteEffect(bank, patch, effectIndex)
            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
