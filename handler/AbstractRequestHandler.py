import tornado.web
import json
from tornado_cors import CorsMixin


class AbstractRequestHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600

    def getRequestData(self):
        return json.loads(self.request.body.decode('utf-8'))

    def success(self):
        self.send(200)

    def created(self, message):
        self.send(201, message)

    def error(self, message):
        self.send(400, {"error": message})

    def printError(self):
        import traceback
        import sys
        print(traceback.format_exc(), file=sys.stderr, flush=True)

    def send(self, status, message=None):
        self.clear()
        self.set_status(status)
        self.finish(message)
