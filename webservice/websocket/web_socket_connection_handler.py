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

from tornado import websocket
from webservice.util.auth import JWTAuth, UnauthorizedError
from webservice.websocket.web_socket_connections import WebSocketConnections
from webservice.websocket.websocket_connection_observer import WebSocketConnectionObserver


class WebSocketConnectionHandler(websocket.WebSocketHandler):
    webservice = None
    app = None

    def initialize(self, app, webservice):
        super(WebSocketConnectionHandler, self).initialize()
        self.app = app
        self.webservice = webservice

    def check_origin(self, origin):
        #return bool(re.match(r'^.*?\.mydomain\.com', origin))
        return True

    def open(self):
        self.app.log('WebSocket opened - Waiting data connection')

    def on_message(self, message):
        message = json.loads(message)
        if 'register' not in message:
            self.write_message(json.dumps({'error': 'Use REST api for send data'}))
            return

        token = message['register']
        try:
            JWTAuth.auth_token(token)
        except UnauthorizedError:
            self.app.log('WebSocket not registered - Wrong token {}'.format(token))
            self.close()
            return

        if not WebSocketConnections.has_registered(self):
            self.app.log('WebSocket registered - Token {}'.format(token))
            self._register_observer(token)

        else:
            self.app.log('WebSocket token updated - Token {}'.format(token))
            self._update_token_observer(token)

    def _register_observer(self, token):
        observer = WebSocketConnectionObserver(self, token)

        self.webservice.register_observer(observer)
        WebSocketConnections.register(token, self, observer)

    def _update_token_observer(self, token):
        observer = WebSocketConnections.get_observer(self)
        observer.token = token

    def on_close(self):
        if WebSocketConnections.has_registered(self):
            token, observer = WebSocketConnections.unregister(self)
            self.webservice.unregister_observer(observer)

            self.app.log('WebSocket closed - Token {}'.format(token))
