from handler.AbstractRequestHandler import AbstractRequestHandler

from application.controller.BanksController import BanksController


class BankHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)

    def get(self, bankIndex):
        try:
            bankIndex = int(bankIndex)
            bank = self.controller.banks.getById(bankIndex)

            self.write(bank.json)

        except IndexError as error:
            self.error(str(error))
        except Exception as error:
            return self.send(404)

    def post(self):
        try:
            body = self.getRequestData()
            index = self.controller.createBank(body)
            self.created({"index": index})

        except IndexError as error:
            self.error(str(error))
        except KeyError as error:
            return self.send(404)
        except Exception as error:
            print(error)
            return self.send(500)

    def put(self, bankIndex):
        try:
            body = self.getRequestData()
            bankIndex = int(bankIndex)
            bank = self.controller.banks.getById(bankIndex)

            self.controller.updateBank(bank, body)

            self.success()

        except IndexError as error:
            self.error(str(error))
        except KeyError as error:
            return self.send(404)
        except Exception as error:
            return self.send(500)

    def delete(self, bank):
        bank = int(bank)

        try:
            self.controller.deleteBank(self.controller.banks.getById(bank))
            self.success()
        except IndexError as error:
            self.error(str(error))
            return
