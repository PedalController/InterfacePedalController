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

from application.controller.pedalboard_controller import PedalboardController
from application.controller.banks_controller import BanksController


class MovePedalboardHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.app = app

        self.banks = self.app.controller(BanksController)
        self.controller = self.app.controller(PedalboardController)

    @integer('bank_index', 'from_index', 'to_index')
    def put(self, bank_index, from_index, to_index):
        try:
            pedalboards = self.banks.banks[bank_index].pedalboards
            pedalboard = pedalboards[from_index]

            self.controller.move(pedalboard, to_index, self.token)

            return self.success()

        except Exception:
            self.print_error()
            return self.send(500)
