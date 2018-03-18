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


class AuthHandlerTest(Test):

    def test_post_correct_username(self):
        response = self.rest.auth()

        self.assertEqual(Test.SUCCESS, response.status_code)

    @unittest.skipIf('Pycharm' in os.environ['PWD'], 'Ignore if the test are running in Pycharm')
    def test_post_component_username(self):
        response = self.rest.auth(WSProperties.COMPONENT_USERNAME, WSProperties.COMPONENT_PASSWORD)

        self.assertEqual(Test.SUCCESS, response.status_code)

    def test_post_wrong_username(self):
        response = self.rest.auth(username="wrong username")

        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_post_invalid_data(self):
        response = self.rest.post('auth', {})

        self.assertEqual(Test.SERVER_ERROR, response.status_code)

    def test_post_wrong_password(self):
        response = self.rest.auth(password="wrong password")

        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_auth_missing_authorization(self):
        response = self.custom_get('banks', authorization=None)
        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_auth_invalid_token(self):
        response = self.custom_get('banks', 'bearer invalid-token')
        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_auth_missing_token(self):
        response = self.custom_get('banks', 'bearer')
        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_auth_invalid_header_authorization(self):
        response = self.custom_get('banks', 'bearer-wrong {}'.format(self.rest.token))
        self.assertEqual(Test.AUTH_ERROR, response.status_code)

    def test_ignore_method(self):
        response = self.rest.options('banks')
        self.assertEqual(204, response.status_code)

    def custom_get(self, url, authorization=None):
        headers = {'content-type': 'application/json'}

        if authorization:
            headers['Authorization'] = authorization

        print('[GET]', self.rest.address + url)
        return requests.get(
            self.rest.address + url,
            headers=headers
        )