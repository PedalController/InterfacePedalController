import tornado.web

from application.controller.BanksController import BanksController

class BanksHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
    def get(self):
        controller = self.app.controller(BanksController)
        
        self.write({"banks": controller.banks.json})