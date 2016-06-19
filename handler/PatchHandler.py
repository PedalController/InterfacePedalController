from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController

from util.HandlerUtils import HandlerUtils


class BankHandler(AbstractRequestHandler):
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
            return self.send(404)

    def post(self, bankIndex):
        try:
            bankIndex = int(bankIndex)
            body = self.getRequestData()
            bank = self.controller.banks.getById(bankIndex)
            index = self.controller.createPatch(bank, body)

            return self.created({"index": index})

        except IndexError as error:
            return self.error(str(error))
        except KeyError as error:
            return self.send(404)
        except Exception as error:
            print(error)
            return self.send(500)

    def put(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

            body = self.getRequestData()
            bank = self.controller.banks.getById(bankIndex)

            self.controller.updatePatch(bank, patchIndex, body)

        except IndexError as error:
            return self.error(str(error))
        except KeyError as error:
            return self.send(404)
        except Exception as error:
            return self.send(500)

        self.success()

    def delete(self, bankIndex, patchIndex):
        try:
            bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)
            raise Exception("Not implemented")
            self.success()
        except IndexError as error:
            self.error(str(error))
