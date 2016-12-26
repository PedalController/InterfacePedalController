from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.current_controller import CurrentController
from application.controller.banks_controller import BanksController

from util.RestOverloading import register, verb


class HandlerUtils(object):
    @staticmethod
    def toInt(*params):
        data = []
        for element in params:
            value = int(element) if element is not None else None
            data.append(value)

        return data


class SetStatusHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app
        self.controller = app.controller(CurrentController)
        self.banks = app.controller(BanksController)

    @register('SetStatusHandler')
    def put(self, function, *args, **kwargs):
        try:
            function(self, *args, **kwargs)
            self.success()

        except IndexError as error:
            return self.error(str(error))
        except Exception as error:
            self.print_error()
            return self.send(500)

    @verb('put', 'SetStatusHandler')
    def put_current_pedalboard(self, bank_index, pedalboard_index):
        bank_index, pedalboard_index = HandlerUtils.toInt(bank_index, pedalboard_index)

        bank_changed_and_pedalboard_not_changed = self.controller.bank_number != bank_index \
                                              and self.controller.pedalboard_number == pedalboard_index

        bank = self.banks.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        self.controller.set_bank(bank, notify=bank_changed_and_pedalboard_not_changed, token=self.token)
        self.controller.set_pedalboard(pedalboard, token=self.token)

    @verb('put', 'SetStatusHandler')
    def putStatusEffect(self, effectIndex):
        effectIndex = int(effectIndex)
        self.controller.toggleStatusEffect(effectIndex, self.token)

    @verb('put', 'SetStatusHandler')
    def putParam(self, effectIndex, paramIndex):
        effectIndex, paramIndex = HandlerUtils.toInt(effectIndex, paramIndex)
        self.controller.setEffectParam(effectIndex, paramIndex)
