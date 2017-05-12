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


class WebSocketConnections(object):
    connections = dict()

    @staticmethod
    def register(token, connection):
        WebSocketConnections.connections[connection] = token

    @staticmethod
    def unregister(connection):
        del WebSocketConnections.connections[connection]

    @staticmethod
    def send_broadcast(data, token=None):
        for connection in WebSocketConnections.connections:
            connection_token = WebSocketConnections.connections[connection]

            if token is None or token != connection_token:
                connection.write_message(data)
