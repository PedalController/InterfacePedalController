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


class PedalboardDataHandlerTest(Test):

    @property
    def default_pedalboard(self):
        return Pedalboard('New default pedalboard')

    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        key = 'test_get'

        pedalboard = bank.pedalboards[0]
        self.assert_data_equal(pedalboard, key)

        pedalboard.data[key] = {'name': 'value1'}
        self.update_data(pedalboard, key)

        self.assert_data_equal(pedalboard, key)

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        key1 = 'key1'
        key2 = 'key2'

        pedalboard = bank.pedalboards[0]

        self.assert_data_equal(pedalboard, key1)

        pedalboard.data[key1] = {'name': 'value1'}
        self.update_data(pedalboard, key1)
        self.assert_data_equal(pedalboard, key1)

        pedalboard.data[key2] = {'name': 'value2'}
        self.update_data(pedalboard, key2)

        self.assert_data_equal(pedalboard, key1)
        self.assert_data_equal(pedalboard, key2)

        self.rest.delete_bank(bank)

    def assert_data_equal(self, pedalboard, key):
        response = self.rest.get_pedalboard_data(pedalboard, key)
        self.assertEqual(Test.SUCCESS, response.status_code)
        if key in pedalboard.data:
            self.assertEqual(pedalboard.data[key], response.json())
        else:
            self.assertEqual({}, response.json())

    def update_data(self, pedalboard, key):
        response = self.rest.update_pedalboard_data(pedalboard, key)
        self.assertEqual(Test.SUCCESS, response.status_code)
