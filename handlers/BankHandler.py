import tornado.web
from architecture.privatemethod import privatemethod

class BankHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        self.banks = self.app.controllers["data"].banks
        
    def get(self, bank, patch=None, effect=None, param=None):
        banks = self.app.controllers["data"].banks

        bank = int(bank)
        patch  = int(patch)  if patch  is not None else None
        effect = int(effect) if effect is not None else None
        param  = int(param)  if param  is not None else None
        
        if not self.hasBank(bank):
            self.write({})
            return
        
        bank = self.getBank(bank)
        if patch is None:
            data = bank.data
        elif effect is None:
            data = bank.getPatch(patch)
        elif param is None:
            data = bank.getEffect(patch, effect)
        else:
            data = bank.getParam(patch, effect, param)
        
        if data is None:
            data = {}
        
        self.write(data)
    
    #@privatemethod
    def hasBank(self, bank):
        return len(self.banks) >= bank+1
    
    #@privatemethod
    def getBank(self, bank):
        return self.banks[bank]