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

from application.controller.device_controller import DeviceController
from pluginsmanager.util.persistence_decoder import PersistenceDecoder
from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.auth import RequiresAuthMixing
from webservice.util.handler_utils import integer, exception


class BankHandler(RequiresAuthMixing, AbstractRequestHandler):
    decoder = None
    manager = None

    def initialize(self, app, webservice):
        super(BankHandler, self).initialize(app, webservice)

        self.manager = self.app.manager
        sys_effect = self.app.controller(DeviceController).sys_effect
        self.decoder = PersistenceDecoder(sys_effect)

    def prepare(self):
        self.auth()

    @exception(Exception, 500)
    @exception(KeyError, 400, message="Missing parameter {}")
    @exception(IndexError, 400)
    @integer('bank_index')
    def get(self, bank_index):
        bank = self.manager.banks[bank_index]

        self.write(bank.json)

    @exception(Exception, 500)
    def post(self):
        json = self.request_data
        bank = self.decoder.read(json)

        with self.observer:
            self.manager.append(bank)

        self.created({"index": bank.index})

    @exception(Exception, 500)
    @exception(KeyError, 400, message="Missing parameter {}")
    @exception(IndexError, 400)
    @integer('bank_index')
    def put(self, bank_index):
        json = self.request_data

        bank = self.decoder.read(json)
        with self.observer:
            self.manager.banks[bank_index] = bank

        self.success()

    @exception(Exception, 500)
    @exception(KeyError, 400, message="Missing parameter {}")
    @exception(IndexError, 400)
    @integer('bank_index')
    def delete(self, bank_index):
        bank_index = int(bank_index)

        with self.observer:
            del self.manager.banks[bank_index]

        self.success()
