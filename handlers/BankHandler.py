import tornado.web
import json

from application.architecture.privatemethod import privatemethod

from application.controller.BanksController import BanksController

from application.util.HandlerUtils import HandlerUtils
from application.util.RestOverloading import register, verb

class BankHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)
        self.banks = self.controller.banks

    @register('BankHandler')
    def get(self, function, *args, **kwargs):
        try:
            data = function(self, *args, **kwargs)
            self.write(data)

        except IndexError as error:
            self.error(str(error))
        except Exception as error:
            return self.send(404)
    
    @verb('get', 'BankHandler')
    def getBank(self, bank):
        bank = int(bank)
        bank = self.banks.get(bank)
        return bank.json

    @verb('get', 'BankHandler')
    def getPatch(self, bank, patch):
        bank, patch = HandlerUtils.toInt(bank, patch)
        bank = self.banks.get(bank)
        return bank.getPatch(patch)

    @verb('get', 'BankHandler')
    def getEffect(self, bank, patch, effect):
        bank, patch, effect = HandlerUtils.toInt(bank, patch, effect)
        bank = self.banks.get(bank)
        return bank.getEffect(patch, effect)
        
    @verb('get', 'BankHandler')
    def getParam(self, bank, patch, effect, param):
        bank, patch, effect, param = HandlerUtils.toInt(bank, patch, effect, param)
        bank = self.banks.get(bank)
        return bank.getParam(patch, effect, param)

    @register('BankHandler')
    def post(self, function, *args, **kwargs):
        try:
            index = function(self, *args, **kwargs)
            self.created({"index":index})

        except IndexError as error:
            self.error(str(error))
        except KeyError as error:
            print(error)
            return self.send(404)
        except Exception as error:
            print(error)
            return self.send(500)

    @verb("post", 'BankHandler')
    def postBank(self):
        body = json.loads(self.request.body.decode('utf-8'))
        return self.controller.createBank(self.banks, body)

    @verb("post", 'BankHandler')
    def postPatch(self, bank):
        bank = int(bank)
        body = json.loads(self.request.body.decode('utf-8'))
        bank = self.banks.get(bank)
        return self.controller.createPatch(bank, body)

    @verb("post", 'BankHandler')
    def postEffect(self, bank, patch):
        bank, patch = HandlerUtils.toInt(bank, patch)
        body = json.loads(self.request.body.decode('utf-8'))
        bank = self.banks.get(bank)
        return self.controller.addEffect(bank, patch, body)
    
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

        self.success()
    
    
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
    
    ''''''
    @privatemethod
    def getData(self, bank, patch, effect, param):
        if patch is None:
            return bank.json
        elif effect is None:
            return bank.getPatch(patch)
        elif param is None:
            return bank.getEffect(patch, effect)
        else:
            return bank.getParam(patch, effect, param)
    ''''''