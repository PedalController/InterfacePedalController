import tornado.web


class PluginHandler(tornado.web.RequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self, uri):
        plugins = self.app.controllers["plugins"]

        data = plugins.all[uri] if uri in plugins.all else {}
        self.write(data)
