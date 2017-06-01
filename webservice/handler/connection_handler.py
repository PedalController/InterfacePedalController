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

from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.handler_utils import integer

from application.controller.device_controller import DeviceController

from pluginsmanager.util.persistence_decoder import ConnectionReader


class ConnectionHandler(AbstractRequestHandler):
    _manager = None

    def initialize(self, app, webservice):
        super(ConnectionHandler, self).initialize(app, webservice)

        self._manager = app.manager

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        bank = self._manager.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        connection = ConnectionReader(pedalboard, DeviceController.sys_effect).read(self.request_data)
        with self.observer:
            pedalboard.connections.append(connection)

        self.send(200)

    @integer('bank_index', 'pedalboard_index')
    def post(self, bank_index, pedalboard_index):
        """
        **Removes** a connection
        """
        bank = self._manager.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        connection = ConnectionReader(pedalboard, DeviceController.sys_effect).read(self.request_data)
        with self.observer:
            pedalboard.connections.remove(connection)

        self.send(200)
