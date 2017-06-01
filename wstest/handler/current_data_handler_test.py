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

from wstest.handler.handler_test import Test, BankMock


class CurrentDataHandlerTest(Test):

    def test_get(self):
        current_index = self.rest.get_current_index().json()
        bank = BankMock('mock CurrentDataHandlerTest test_get')
        bank.index = current_index['bank']

        current_bank = self.rest.get_bank(bank).json()
        current_pedalboard_index = current_index['pedalboard']

        response = self.rest.get_current_data()
        self.assertEqual(Test.SUCCESS, response.status_code)

        expected = {
            'bank': current_bank,
            'pedalboard': current_pedalboard_index
        }
        self.assertEqual(expected, response.json())
