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

from wstest.handler.handler_test import Test


class CurrentPedalboardHandlerTest(Test):

    def test_put(self):
        original_current_index = self.rest.get_current_index().json()

        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]

        response = self.rest.set_current_pedalboard(pedalboard)
        self.assertEqual(Test.SUCCESS, response.status_code)

        new_current_index = self.rest.get_current_index().json()

        self.assertNotEqual(original_current_index, new_current_index)
        self.assertEqual({'bank': bank.index, 'pedalboard': pedalboard.index}, new_current_index)

        self.assertEqual(pedalboard.json, self.rest.get_current_pedalboard().json())

        self.rest.set_current_pedalboard_by_index(original_current_index['bank'], original_current_index['pedalboard'])
        self.rest.delete_bank(bank)
