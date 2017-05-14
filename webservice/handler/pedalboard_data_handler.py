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
from application.controller.pedalboard_controller import PedalboardController


class PedalboardDataHandler(AbstractRequestHandler):
    app = None
    controller = None

    def initialize(self, app):
        self.app = app

        self.controller = self.app.controller(PedalboardController)
        self.banks = self.app.controller(BanksController)

    @integer('bank_index', 'pedalboard_index')
    def get(self, bank_index, pedalboard_index, key):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]

            if key not in pedalboard.data:
                return self.write({})

            return self.write(pedalboard.data[key])

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index, key):
        try:
            bank = self.banks.banks[bank_index]
            pedalboard = bank.pedalboards[pedalboard_index]
            pedalboard.data[key] = self.request_data

            self.controller.update(pedalboard, self.token, reload=False)

            return self.success()

        except IndexError as error:
            return self.error(str(error))

        except Exception:
            self.print_error()
            return self.send(500)
