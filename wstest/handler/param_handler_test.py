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


class ParamHandlerTest(Test):

    def test_get(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        param = bank.pedalboards[0].effects[0].params[0]
        response = self.rest.get_param(param)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(param.json, response.json())

        self.rest.delete_bank(bank)

    def test_put(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        param = bank.pedalboards[0].effects[0].params[0]
        param.value += 1

        response = self.rest.put_param(param)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_value = self.rest.get_param(param)
        self.assertEqual(param.json, get_value.json())

        self.rest.delete_bank(bank)
