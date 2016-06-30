# -*- coding: utf-8 -*-
from socket.WebSocketConnections import WebSocketConnections


class AbstractSocketHandler(object):

    def send(self, data):
        WebSocketConnections.sendBroadcast(data)
