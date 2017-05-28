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


class SwapBankHandlerTest(Test):

    def test_swap(self):
        bank = self.default_bank_mock
        bank2 = self.default_bank_mock

        bank.index = self.rest.create_bank(bank).json()['index']
        bank2.index = self.rest.create_bank(bank2).json()['index']

        response = self.rest.swap_banks(bank, bank2)
        self.assertEqual(Test.SUCCESS, response.status_code)

        bank.index, bank2.index = bank2.index, bank.index

        response = self.rest.get_bank(bank)
        response2 = self.rest.get_bank(bank2)

        self.assertEqual(Test.SUCCESS, response.status_code)

        self.assertEqual(bank.json, response.json())
        self.assertEqual(bank2.json, response2.json())

        self.rest.delete_bank(bank)
        self.rest.delete_bank(bank2)
