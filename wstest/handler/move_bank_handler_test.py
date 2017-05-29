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


class MoveBankHandlerTest(Test):

    def test_swap(self):
        bank = self.default_bank_mock
        bank2 = self.default_bank_mock
        bank3 = self.default_bank_mock

        bank.index = self.rest.create_bank(bank).json()['index']
        bank2.index = self.rest.create_bank(bank2).json()['index']
        bank3.index = self.rest.create_bank(bank3).json()['index']

        response = self.rest.move_bank(bank, bank3.index)
        self.assertEqual(Test.SUCCESS, response.status_code)

        bank.index, bank2.index, bank3.index = bank3.index, bank.index, bank2.index

        self.maxDiff = None
        self.assertDictEqual(bank.json, self.rest.get_bank(bank).json())
        self.assertDictEqual(bank2.json, self.rest.get_bank(bank2).json())
        self.assertDictEqual(bank3.json, self.rest.get_bank(bank3).json())

        self.rest.delete_bank(bank)
        self.rest.delete_bank(bank2)
        self.rest.delete_bank(bank3)
