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


class SwapBankHandler(AbstractRequestHandler):
    _manager = None

    def initialize(self, app, webservice):
        super(SwapBankHandler, self).initialize(app, webservice)

        self._manager = app.manager

    @integer('bank_a_index', 'bank_b_index')
    def put(self, bank_a_index, bank_b_index):
        try:
            banks = self._manager.banks
            banks[bank_a_index], banks[bank_b_index] = banks[bank_b_index], banks[bank_a_index]

            return self.success()

        except IndexError:
            return self.error("Invalid index")

        except Exception:
            self.print_error()
            return self.send(500)
