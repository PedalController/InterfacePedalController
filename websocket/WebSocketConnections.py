# -*- coding: utf-8 -*-


class WebSocketConnections(object):
    connections = []

    @staticmethod
    def register(connection):
        WebSocketConnections.connections.append(connection)

    @staticmethod
    def unregister(connection):
        WebSocketConnections.connections.remove(connection)

    @staticmethod
    def sendBroadcast(data):
        for connection in WebSocketConnections.connections:
            connection.write_message(data)
