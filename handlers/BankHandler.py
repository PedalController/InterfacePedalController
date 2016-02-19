import tornado.web

from architecture.privatemethod import privatemethod

from controller.BanksController import BanksController

class BankHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
    def get(self, bank, patch=None, effect=None, param=None):
        banks = self.app.controller(BanksController).banks

        bank = banks.get(int(bank))
        patch  = int(patch)  if patch  is not None else None
        effect = int(effect) if effect is not None else None
        param  = int(param)  if param  is not None else None
        
        if bank is None:
            self.write({})
            return
        
        if patch is None:
            data = bank.json
        elif effect is None:
            data = bank.getPatch(patch)
        elif param is None:
            data = bank.getEffect(patch, effect)
        else:
            data = bank.getParam(patch, effect, param)
        
        if data is None:
            data = {}
        
        self.write(data)
