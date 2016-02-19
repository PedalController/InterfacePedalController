import tornado.web

class EffectsHandler(tornado.web.RequestHandler):
    app = None
    
    def initialize(self, app):
        self.app = app
        
    def get(self):
        plugins = self.app.controllers["plugins"]
        
        self.write(plugins.all)