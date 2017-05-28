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

from .handler_test import Test
from pluginsmanager.model.pedalboard import Pedalboard


class MovePedalboardHandlerTest(Test):

    def test_get(self):
        bank = self.default_bank_mock
        bank.append(Pedalboard('Pedalboard 2'))
        bank.append(Pedalboard('Pedalboard 3'))

        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]
        index = 2

        r = self.rest.move_pedalboard(pedalboard, index)
        self.assertEqual(Test.SUCCESS, r.status_code)

        persisted = self.rest.get_bank(bank).json()
        bank.pedalboards.move(pedalboard, index)
        self.assertEqual(bank.json, persisted)

        self.rest.delete_bank(bank)
