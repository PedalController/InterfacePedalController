import tornado.web

class BanksHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
    def get(self):
        data = {"banks": self.app.controllers["data"].banks}
        
        self.write(data)