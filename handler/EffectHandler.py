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

            effect = self.banksController.banks[bankIndex].patches[patchIndex].effects[effectIndex]

            return self.write(effect.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def post(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            patch = self.banksController.banks[bankIndex].patches[patchIndex]
            uri = self.getRequestData()

            index = self.controller.createEffect(patch, uri)

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

            effect = self.banksController.banks[bankIndex].patches[patchIndex].effects[effectIndex]

            self.controller.deleteEffect(effect)
            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
