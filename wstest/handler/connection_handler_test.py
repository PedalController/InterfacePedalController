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
from pluginsmanager.model.connection import Connection


class ConnectionHandlerTest(Test):

    def test_put(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects
        connection = Connection(reverb2.outputs[0], reverb.inputs[0])
        pedalboard.connections.append(connection)

        response = self.rest.create_connection(connection)

        self.assertEqual(Test.SUCCESS, response.status_code)

        response = self.rest.get_pedalboard(pedalboard)
        self.assertEqual(pedalboard.json, response.json())

        self.rest.delete_bank(bank)

    def test_put_connection_without_type(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]
        reverb, reverb2 = pedalboard.effects
        connection = Connection(reverb2.outputs[0], reverb.inputs[0])
        pedalboard.connections.append(connection)

        response = self.rest.create_connection_without_type(connection)
        self.assertEqual(Test.ERROR, response.status_code)

        self.rest.delete_bank(bank)

    def test_post_is_delete(self):
        bank = self.default_bank_mock
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]
        connection = pedalboard.connections[0]

        response = self.rest.delete_connection(connection)
        self.assertEqual(Test.DELETED, response.status_code)

        response = self.rest.get_pedalboard(pedalboard)

        pedalboard.connections.remove(connection)
        self.assertEqual(pedalboard.json, response.json())

        self.rest.delete_bank(bank)
