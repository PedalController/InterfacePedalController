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

import socket

from wstest.handler.handler_test import Test


class DeviceNameHandlerTest(Test):

    def name_json(self, name):
        return {'name': name}

    def test_get(self):
        name = socket.gethostname().split('.')[0]

        response = self.rest.configurations_get_name()

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(self.name_json(name), response.json())

    def test_put(self):
        original_name = socket.gethostname().split('.')[0]
        new_name = 'My awesome Pedal Pi'

        response = self.rest.configurations_put_name(new_name)
        self.assertEqual(Test.SUCCESS, response.status_code)

        response = self.rest.configurations_get_name()
        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(self.name_json(new_name), response.json())

        import time
        time.sleep(10)

        response = self.rest.configurations_put_name(original_name)
        self.assertEqual(Test.SUCCESS, response.status_code)

        response = self.rest.configurations_get_name()
        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(self.name_json(original_name), response.json())
