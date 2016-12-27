from websocket.web_socket_connections import WebSocketConnections
from tornado import websocket
import json
import uuid


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
