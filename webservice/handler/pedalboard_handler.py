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
from webservice.util.handler_utils import integer, exception

from application.controller.device_controller import DeviceController

from pluginsmanager.util.persistence_decoder import PedalboardReader


class PedalboardHandler(AbstractRequestHandler):
    _manager = None
    _decode = None

    def initialize(self, app, webservice):
        super(PedalboardHandler, self).initialize(app, webservice)

        self._manager = self.app.manager

        self._decode = PedalboardReader(self.app.controller(DeviceController).sys_effect)

    @exception(Exception, 500)
    @exception(IndexError, 400, message='Invalid index')
    @integer('bank_index', 'pedalboard_index')
    def get(self, bank_index, pedalboard_index):
        bank = self._manager.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        return self.write(pedalboard.json)

    @exception(Exception, 500)
    @exception(IndexError, 400, message='Invalid index')
    @integer('bank_index')
    def post(self, bank_index):
        pedalboard = self._decode.read(self.request_data)

        bank = self._manager.banks[bank_index]
        with self.observer:
            bank.append(pedalboard)

        return self.created({"index": len(bank.pedalboards) - 1})

    @exception(Exception, 500)
    @exception(IndexError, 400, message='Invalid index')
    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        bank = self._manager.banks[bank_index]
        pedalboard = self._decode.read(self.request_data)

        with self.observer:
            bank.pedalboards[pedalboard_index] = pedalboard

        return self.success()

    @exception(Exception, 500)
    @exception(IndexError, 400, message='Invalid index')
    @integer('bank_index', 'pedalboard_index')
    def delete(self, bank_index, pedalboard_index):
        bank = self._manager.banks[bank_index]

        with self.observer:
            del bank.pedalboards[pedalboard_index]

        return self.success()
