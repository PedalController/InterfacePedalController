from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.current_controller import CurrentController

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

    def initialize(self, app):
        self.app = app
        self.controller = app.controller(CurrentController)

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
    def putCurrentPatch(self, bankIndex, patchIndex):
        bankIndex, patchIndex = HandlerUtils.toInt(bankIndex, patchIndex)

        bankChangedAndPatchNotChanged = self.controller.bankNumber != bankIndex \
                                    and self.controller.patchNumber == patchIndex

        self.controller.setBank(bankIndex, notify=bankChangedAndPatchNotChanged, token=self.token)
        self.controller.setPatch(patchIndex, token=self.token)

    @verb('put', 'SetStatusHandler')
    def putStatusEffect(self, effectIndex):
        effectIndex = int(effectIndex)
        self.controller.toggleStatusEffect(effectIndex, self.token)

    @verb('put', 'SetStatusHandler')
    def putParam(self, effectIndex, paramIndex):
        effectIndex, paramIndex = HandlerUtils.toInt(effectIndex, paramIndex)
        self.controller.setEffectParam(effectIndex, paramIndex)
