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

from .handler_test import Test


class PluginHandlerTest(Test):

    def test_get(self):
        r = self.rest.get_plugin('http://calf.sourceforge.net/plugins/MultiChorus')
        self.assertEqual(Test.SUCCESS, r.status_code)

    @unittest.skipIf('TRAVIS' in os.environ, 'Travis not contains audio interface')
    def test_get_custom_uri(self):
        uri = 'http://guitarix.sourceforge.net/plugins/gx_scream_#_scream_'.replace('#', '%23')
        r = self.rest.get_plugin(uri)
        self.assertEqual(Test.SUCCESS, r.status_code)

    def test_get_invalid(self):
        r = self.rest.get_plugin('http://calf.sourceforge.net/plugins/MultiChorus1234567890')
        self.assertEqual(Test.ERROR, r.status_code)
