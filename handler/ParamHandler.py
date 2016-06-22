from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController

from util.HandlerUtils import HandlerUtils


class PatchHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    def get(self, bankIndex, patchIndex, effectIndex, paramIndex):
        try:
            bankIndex, patchIndex, effectIndex, paramIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex, paramIndex
            )
            bank = self.controller.banks.getById(bankIndex)

            param = bank.getParam(patchIndex, effectIndex, paramIndex)
            return self.write(param)

        except IndexError as error:
            return self.error(str(error))
        except Exception as error:
            return self.send(404)

    def put(self, bankIndex, patchIndex, effectIndex, paramIndex):
        try:
            bankIndex, patchIndex, effectIndex, paramIndex = HandlerUtils.toInt(
                bankIndex, patchIndex, effectIndex, paramIndex
            )

            body = self.getRequestData()
            bank = self.controller.banks.getById(bank)

            # Pensar em mudar isso aqui para mudar diretamente
            # no banco e através de um observer, detectar a mudança
            # e aplicar (persistir e chamar deviceController)
            #self.controller.updateParam(
            #    bank, patchNumber, effectNumber, paramNumber, body
            #)

        except IndexError as error:
            return self.error(str(error))
        except KeyError as error:
            return self.send(404)
        except Exception as error:
            return self.send(500)

        self.success()
