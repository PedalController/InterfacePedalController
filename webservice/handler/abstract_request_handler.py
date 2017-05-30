# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tornado.web
import json
from tornado_cors import CorsMixin

from unittest.mock import MagicMock
from webservice.websocket.web_socket_connections import WebSocketConnections


class AbstractRequestHandler(CorsMixin, tornado.web.RequestHandler):
    CORS_ORIGIN = '*'
    CORS_CREDENTIALS = True
    CORS_MAX_AGE = 21600
    CORS_HEADERS = 'Content-Type, x-xsrf-token'

    app = None
    ws = None

    def initialize(self, app, webservice):
        """
        :param Application app:
        :param WebService webservice:
        """
        self.app = app
        self.ws = webservice

    @property
    def request_data(self):
        return json.loads(self.request.body.decode('utf-8'))

    def success(self):
        self.send(200)

    def created(self, message):
        self.send(201, message)

    def error(self, message):
        self.send(400, {"error": message})

    def send(self, status, message=None):
        self.clear()
        self.set_status(status)
        self.finish(message)

    @property
    def token(self):
        return self.request.headers.get('x-xsrf-token')

    @property
    def observer(self):
        token = self.token
        if token is None:
            return MagicMock()
        else:
            return WebSocketConnections.observers[token]
