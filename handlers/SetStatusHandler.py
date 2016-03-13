import tornado.web

from architecture.privatemethod import privatemethod

from controller.CurrentController import CurrentController

from util.HandlerUtils import HandlerUtils
from util.RestOverloading import register, verb


class SetStatusHandler(tornado.web.RequestHandler):
    app = None
    
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
            print(error)
            return self.send(404)
        
    @verb('put', 'SetStatusHandler')
    def putBank(self, bank):
        bank = int(bank)
        self.controller.setBank(bank)

    @verb('put', 'SetStatusHandler')
    def putPatch(self, patch):
        patch = int(patch)
        self.controller.setPatch(patch)
    
    @verb('put', 'SetStatusHandler')
    def putStatusEffect(self, effect):
        effect = int(effect)
        self.controller.toggleStatusEffect(effect)

    @verb('put', 'SetStatusHandler')
    def putParam(self, effect, param):
        effect, param = HandlerUtils.toInt(effect, param)
        self.controller.setEffectParam(effect, param)

    @privatemethod
    def success(self):
        self.send(204)
    
    @privatemethod
    def created(self, message):
        self.send(201, message)

    @privatemethod
    def error(self, message):
        self.send(400, {"error": message})
        
    @privatemethod
    def send(self, status, message=None):
        self.clear()
        self.set_status(status)
        self.finish(message)