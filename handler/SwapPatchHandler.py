from architecture.EffectException import EffectException
from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController
from application.controller.PatchController import PatchController

from util.HandlerUtils import HandlerUtils


class SwapPatchHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PatchController)
        self.banksController = self.app.controller(BanksController)

    def put(self, bankIndex, patchIndex, effectAIndex, effectBIndex):
        try:
            bankIndex, patchIndex, effectAIndex, effectBIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectAIndex, effectBIndex
            )

            patch = self.banksController.banks[bankIndex].patches[patchIndex]
            effects = patch.effects
            effectA = effects[effectAIndex]
            effectB = effects[effectBIndex]

            self.controller.swapEffects(effectA, effectB)

            return self.success()

        except EffectException as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
