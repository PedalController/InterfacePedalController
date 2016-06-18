__author__ = 'SrMouraSilva'

import tornado.web
import json


class AbstractRequestHandler(tornado.web.RequestHandler):

    def getRequestData(self):
        return json.loads(self.request.body.decode('utf-8'))

    def success(self):
        self.send(204)

    def created(self, message):
        self.send(201, message)

    def error(self, message):
        self.send(400, {"error": message})

    def send(self, status, message=None):
        self.clear()
        self.set_status(status)
        self.finish(message)