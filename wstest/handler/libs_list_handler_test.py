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

import os
import unittest

import requests
from webservice.properties import WSProperties
from wstest.handler.handler_test import Test


class LibsListHandlerTest(Test):

    def test_get_libs(self):
        response = self.rest.configurations_list_libs()

        self.assertEqual(Test.SUCCESS, response.status_code)
