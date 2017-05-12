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

from webservice.websocket.web_socket_connections import WebSocketConnections

from tornado import websocket


class WebSocketConnectionHandler(websocket.WebSocketHandler):

    def initialize(self, app):
        pass

    def check_origin(self, origin):
        #return bool(re.match(r'^.*?\.mydomain\.com', origin))
        return True

    def open(self):
        print("WebSocket opened")
        token = str(uuid.uuid4())
        WebSocketConnections.register(token, self)
        self.write_message(json.dumps({'type': 'TOKEN', 'value': token}))

    def on_message(self, message):
        self.write_message(json.dumps({'error': 'Use REST api for send data'}))

    def on_close(self):
        WebSocketConnections.unregister(self)
        print("WebSocket closed")
