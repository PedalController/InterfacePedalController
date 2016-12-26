from handler.abstract_request_handler import AbstractRequestHandler


class PluginHandler(AbstractRequestHandler):
    app = None

    def initialize(self, app):
        self.app = app

    def get(self, uri):
        plugins = self.app.controllers["plugins"]

        data = plugins.all[uri] if uri in plugins.all else {}
        self.write(data)
