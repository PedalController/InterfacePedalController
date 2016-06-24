from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController

from util.HandlerUtils import HandlerUtils


class EffectHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    def get(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)
            bank = self.controller.banks.getById(bankIndex)

            return self.write(bank.getPatch(patchIndex))

        except IndexError as error:
            return self.error(str(error))

        except Exception as error:
            self.printError()
            return self.send(500)

    def post(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)
            body = self.getRequestData()
            bank = self.controller.banks.getById(bankIndex)
            index = self.controller.addEffect(bank, patchIndex, body)

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
            raise Exception("Not implemented")
            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)
