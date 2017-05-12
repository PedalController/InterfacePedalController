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

from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController

from pluginsmanager.util.persistence_decoder import PersistenceDecoder


class BankHandler(AbstractRequestHandler):
    app = None
    controller = None
    decoder = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(BanksController)
        sys_effect = self.app.controller(DeviceController).sys_effect
        self.decoder = PersistenceDecoder(sys_effect)

    @integer('bank_index')
    def get(self, bank_index):
        try:
            bank = self.controller.banks[bank_index]

            self.write(bank.json)

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    def post(self):
        try:
            json = self.request_data
            bank = self.decoder.read(json)

            index = self.controller.create(bank, self.token)

            self.created({"index": index})

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index')
    def put(self, bank_index):
        try:
            json = self.request_data

            new_bank = self.decoder.read(json)
            old_bank = self.controller.banks[bank_index]

            self.controller.replace(old_bank, new_bank, self.token)

            self.success()

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index')
    def delete(self, bank_index):
        bank_index = int(bank_index)

        try:
            self.controller.delete(self.controller.banks[bank_index], self.token)
            self.success()
        except IndexError as error:
            return self.error("Invalid index")
