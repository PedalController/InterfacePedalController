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
from application.controller.pedalboard_controller import PedalboardController

from pluginsmanager.util.persistence_decoder import PedalboardReader


class PedalboardHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None
    decode = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PedalboardController)
        self.banks = self.app.controller(BanksController)

        self.decode = PedalboardReader(self.app.controller(DeviceController).sys_effect)

    @integer('bank_index', 'pedalboard_index')
    def get(self, bank_index, pedalboard_index):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]

            return self.write(pedalboard.json)

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index')
    def post(self, bank_index):
        try:
            pedalboard = self.decode.read(self.request_data)

            bank = self.banks.banks[bank_index]
            bank.append(pedalboard)
            self.controller.created(pedalboard, self.token)

            return self.created({"index": len(bank.pedalboards) - 1})

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        try:
            old_pedalboard = self.banks.banks[bank_index].pedalboards[pedalboard_index]
            new_pedalboard = self.decode.read(self.request_data)

            self.controller.replace(old_pedalboard, new_pedalboard, self.token)

            return self.success()

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def delete(self, bank_index, pedalboard_index):
        try:
            pedalboard = self.banks.banks[bank_index].pedalboards[pedalboard_index]
            self.controller.delete(pedalboard, self.token)

            return self.success()

        except IndexError as error:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)
