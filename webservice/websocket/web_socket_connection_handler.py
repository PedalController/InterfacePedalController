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

import json
import uuid
import logging

from webservice.websocket.web_socket_connections import WebSocketConnections
from webservice.websocket.websocket_connection_observer import WebSocketConnectionObserver

from tornado import websocket


class WebSocketConnectionHandler(websocket.WebSocketHandler):
    webservice = None

    def initialize(self, app, webservice):
        self.webservice = webservice
        pass

    def check_origin(self, origin):
        #return bool(re.match(r'^.*?\.mydomain\.com', origin))
        return True

    def open(self):
        token = str(uuid.uuid4())
        logging.info('WebSocket opened - Token {}'.format(token))

        observer = WebSocketConnectionObserver(self)

        self.webservice.register_observer(observer)
        WebSocketConnections.register(token, self, observer)

        self.write_message(json.dumps({'type': 'TOKEN', 'value': token}))

    def on_message(self, message):
        self.write_message(json.dumps({'error': 'Use REST api for send data'}))

    def on_close(self):
        token, observer = WebSocketConnections.unregister(self)
        self.webservice.unregister_observer(observer)

        logging.info('WebSocket closed - Token {}'.format(token))
