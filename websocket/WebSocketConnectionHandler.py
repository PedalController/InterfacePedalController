# -*- coding: utf-8 -*-
from websocket.WebSocketConnections import WebSocketConnections
from tornado import websocket
import json


class WebSocketConnectionHandler(websocket.WebSocketHandler):
  
    def check_origin(self, origin):
        #return bool(re.match(r'^.*?\.mydomain\.com', origin))
        return True

    def open(self):
        WebSocketConnections.register(self)
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(json.dumps({'error': 'Use REST api for send data'}))

    def on_close(self):
        WebSocketConnections.unregister(self)
        print("WebSocket closed")
