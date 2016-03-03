import tornado.web

from architecture.privatemethod import privatemethod

from controller.CurrentController import CurrentController

from util.RestOverloading import register, verb


class SetStatusHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        self.controller = app.controller(CurrentController)
        
    @register
    def get(self, *args, **kwargs):
        pass
    
    '''
    def put(self, *args, **kwargs):
        method = register.method(*args, **kwargs)
        args = HandleUtils(*args)

        try:
            method(args)
        except IndexError as error:
            self.error(str(error))
            return
        
        self.success()
    '''
        
    @verb("get")
    def putBank(self, bank):
        bank = int(bank)
        
        try:
            self.controller.setBank(bank)
        except IndexError as error:
            self.error(str(error))
            return
        
        self.success()

    @verb("get")
    def putPatch(self, patch):
        patch = int(patch)
        
        try:
            self.controller.setPatch(patch)
        except IndexError as error:
            self.error(str(error))
            return
        
        self.success()
    
    @verb("get")
    def putEffect(self, effect):
        effect = int(effect)
        
        try:
            self.controller.toggleStatusEffect(effect)
        except IndexError as error:
            self.error(str(error))
            return
        
        self.success()

    @privatemethod
    def success(self):
        self.clear()
        self.set_status(204)
        self.finish()

    @privatemethod
    def error(self, message):
        self.clear()
        self.set_status(400)
        self.finish({"error": message})