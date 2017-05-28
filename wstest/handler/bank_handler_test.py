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


class BankHandlerTest(Test):

    def test_get(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        response = self.rest.get_bank(bank)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(bank.json, response.json())

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank_mock

        response = self.rest.create_bank(bank)
        self.assertEqual(Test.CREATED, response.status_code)

        bank.index = response.json()['index']

        persisted = self.rest.get_bank(bank).json()
        self.assertEqual(bank.json, persisted)

        self.rest.delete_bank(bank)

    def test_put(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        bank.name = 'REST - Default Bank - New name'

        response = self.rest.update_bank(bank)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_bank = self.rest.get_bank(bank)

        self.assertEqual(bank.json, get_bank.json())

        self.rest.delete_bank(bank)

    def test_delete(self):
        bank = self.default_bank_mock
        data = self.rest.create_bank(bank).json()
        bank.index = data['index']
        print('My bank', bank.index, data)
        print('banks', len(self.rest.get_banks().json()['banks'] ))


        r = self.rest.delete_bank(bank)
        self.assertEqual(Test.DELETED, r.status_code)
