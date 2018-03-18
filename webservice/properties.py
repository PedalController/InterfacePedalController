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

from webservice.util.auth import generate_random_string


class WSProperties(object):
    DATA_KEY = 'WebService'

    DEVICE_NAME = 'device_name'
    USER = 'user'

    """ Default username for component clients"""
    COMPONENT_USERNAME = generate_random_string(16)
    """ Default password for component clients"""
    COMPONENT_PASSWORD = generate_random_string(16)

    @staticmethod
    def auth_client_component(username, password):
        """
        :param string username:
        :param string password:
        :return:
        """
        return username == WSProperties.COMPONENT_USERNAME \
           and password == WSProperties.COMPONENT_PASSWORD
