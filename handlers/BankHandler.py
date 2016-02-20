import tornado.web
import json

from architecture.privatemethod import privatemethod

from controller.BanksController import BanksController

from util.HandlerUtils import HandlerUtils

class BankHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
        #prepare
        self.controller = self.app.controller(BanksController)
        self.banks = self.controller.banks
    
    def prepare(self):
        pass

    def get(self, bank, patch=None, effect=None, param=None):
        bank, patch, effect, param = HandlerUtils.toInt(bank, patch, effect, param)

        try:
            bank = self.banks.get(bank)
            data = self.getData(bank, patch, effect, param)
        except IndexError as error:
            self.error(str(error))
            return
        
        self.write(data)

    def post(self, bank=None, patch=None, effect=None):
        bank, patch, effect = HandlerUtils.toInt(bank, patch, effect)
        
        body = json.loads(self.request.body.decode('utf-8'))
        
        index = -1
        try:            
            if bank is None:
                index = self.controller.createBank(self.banks, body)
            elif patch is None:
                bank = self.banks.get(bank)
                index = self.controller.createPatch(bank, body)
            elif effect is None:
                bank = self.banks.get(bank)
                index = self.controller.addEffect(bank, patch, body)
            
        except IndexError as error:
            self.error(str(error))
            return
        
        self.clear()
        self.set_status(201)
        self.finish({"index":index})

    def put(self, bank, patch=None, effect=None, param=None):
        bank, patch, effect = HandlerUtils.toInt(bank, patch, effect)
        
        body = json.loads(self.request.body.decode('utf-8'))
        
        try:
            bank = self.banks.get(bank)
            data = self.getData(bank, patch, effect, param)
            
            self.controller.update(data, body)

        except IndexError as error:
            self.error(str(error))
            return

        self.clear()
        self.set_status(204)
        self.finish()
    
    @privatemethod
    def error(self, message):
        self.clear()
        self.set_status(400)
        self.finish({"error": message})
    
    #@privatemethod
    def getData(self, bank, patch, effect, param):
        if patch is None:
            return bank.json
        elif effect is None:
            return bank.getPatch(patch)
        elif param is None:
            return bank.getEffect(patch, effect)
        else:
            return bank.getParam(patch, effect, param)