from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController


class BankHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    def get(self, bankIndex):
        try:
            bankIndex = int(bankIndex)
            bank = self.controller.banks[bankIndex]

            self.write(bank.json)

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def post(self):
        try:
            body = self.getRequestData()
            index = self.controller.createBank(body, self.token)
            self.created({"index": index})

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def put(self, bankIndex):
        try:
            body = self.getRequestData()
            bankIndex = int(bankIndex)
            bank = self.controller.banks[bankIndex]

            self.controller.updateBank(bank, body, self.token)

            self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.printError()
            return self.send(500)

    def delete(self, bankIndex):
        bankIndex = int(bankIndex)

        try:
            self.controller.deleteBank(self.controller.banks[bankIndex], self.token)
            self.success()
        except IndexError as error:
            return self.error(str(error))
