from controller.BanksController import BanksController
import tornado.web

class BanksHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
    def get(self):
        controller = self.app.controller(BanksController)
        
        self.write({"banks": controller.banks.json})