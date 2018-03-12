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

import requests
import json


class RestFacade(object):
    address = 'http://localhost:3000/v1/'
    
    # **********************
    # CRUD
    # **********************
    def get(self, url):
        print('[GET]', self.address + url)
        return requests.get(self.address + url)

    def post(self, url, data):
        print('[POST]', self.address + url)
        return requests.post(
            self.address + url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

    def put(self, url, data=''):
        print('[PUT]', self.address + url)
        return requests.put(
            self.address + url,
            data=json.dumps(data),
            headers={'content-type': 'application/json'}
        )

    def delete(self, url):
        print('[DELETE]', self.address + url)
        return requests.delete(self.address + url)

    # **********************
    # Banks
    # **********************
    def get_banks(self):
        return self.get('banks')

    # **********************
    # Bank
    # **********************
    def get_bank(self, bank):
        return self.get('bank/{0}'.format(bank.index))

    def create_bank(self, bank):
        return self.post('bank', bank.json)

    def update_bank(self, bank):
        return self.put('bank/{0}'.format(bank.index), bank.json)

    def delete_bank(self, bank):
        return self.delete('bank/{0}'.format(bank.index))

    def move_bank(self, bank, new_index):
        url = 'move/bank/{0}/to/{1}'.format(
            bank.index,
            new_index
        )

        return self.put(url)

    # **********************
    # Pedalboard
    # **********************
    def get_pedalboard(self, pedalboard):
        bank_index = pedalboard.bank.index
        return self.get('bank/{0}/pedalboard/{1}'.format(bank_index, pedalboard.index))

    def create_pedalboard(self, pedalboard):
        bank_index = pedalboard.bank.index
        return self.post('bank/{0}/pedalboard'.format(bank_index), pedalboard.json)

    def update_pedalboard(self, pedalboard):
        bank_index = pedalboard.bank.index
        return self.put('bank/{0}/pedalboard/{1}'.format(bank_index, pedalboard.index), pedalboard.json)

    def delete_pedalboard(self, pedalboard):
        bank_index = pedalboard.bank.index
        return self.delete('bank/{0}/pedalboard/{1}'.format(bank_index, pedalboard.index))

    def get_pedalboard_data(self, pedalboard, key):
        bank_index = pedalboard.bank.index
        return self.get('bank/{0}/pedalboard/{1}/data/{2}'.format(bank_index, pedalboard.index, key))

    def update_pedalboard_data(self, pedalboard, key):
        bank_index = pedalboard.bank.index
        content = pedalboard.data[key]
        return self.put('bank/{0}/pedalboard/{1}/data/{2}'.format(bank_index, pedalboard.index, key), content)

    def move_pedalboard(self, pedalboard, new_index):
        bank_index = pedalboard.bank.index
        return self.put("move/bank/{}/pedalboard/{}/to/{}".format(bank_index, pedalboard.index, new_index))

    # **********************
    # Effect
    # **********************
    def get_effect(self, effect):
        return self.get(self._url_effect(effect))

    def post_effect(self, pedalboard, uri):
        bank_index = pedalboard.bank.index

        url = 'bank/{0}/pedalboard/{1}/effect'.format(bank_index, pedalboard.index)
        return self.post(url, uri)

    def delete_effect(self, effect):
        return self.delete(self._url_effect(effect))
    
    def _url_effect(self, effect):
        pedalboard = effect.pedalboard

        return 'bank/{0}/pedalboard/{1}/effect/{2}'.format(
            pedalboard.bank.index,
            pedalboard.index,
            effect.index
        )

    # **********************
    # Param
    # **********************
    def get_param(self, param):
        return self.get(self._url_param(param))

    def put_param(self, param):
        url = self._url_param(param)
        return self.put(url, param.value)

    def put_param_value_wrong_value(self, param, param_value):
        url = self._url_param(param)
        return self.put(url, param_value)

    def _url_param(self, param):
        effect = param.effect
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        return 'bank/{0}/pedalboard/{1}/effect/{2}/param/{3}'.format(
            bank.index,
            pedalboard.index,
            effect.index,
            param.index
        )

    # **********************
    # Connection
    # **********************
    def create_connection(self, connection):
        return self.put(self._url_connection(connection), connection.json)

    def create_connection_without_type(self, connection):
        data = connection.json
        del data['type']
        return self.put(self._url_connection(connection), data)

    def delete_connection(self, connection):
        return self.post(self._url_connection(connection), connection.json)

    def _url_connection(self, connection):
        effect = connection.output.effect
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        return 'bank/{0}/pedalboard/{1}/connect'.format(
            bank.index,
            pedalboard.index
        )

    # **********************
    # ComponentData
    # **********************
    def get_component_data(self, key):
        return self.get(self._url_component_data(key))

    def post_component_data(self, key, data):
        return self.post(self._url_component_data(key), data)

    def delete_component_data(self, key):
        return self.delete(self._url_component_data(key))

    def _url_component_data(self, key):
        return 'data/{0}'.format(key)

    # **********************
    # Configurations
    # **********************
    def configurations_get_name(self):
        return self.get('configurations/device_name')

    def configurations_put_name(self, new_name):
        return self.put('configurations/device_name/{}'.format(new_name))

    # **********************
    # Current
    # **********************
    def get_current_pedalboard(self):
        data = self.get_current_index().json()
        return self.get('bank/{0}/pedalboard/{1}'.format(data['bank'], data['pedalboard']))

    def set_current_pedalboard(self, pedalboard):
        bank = pedalboard.bank

        return self.set_current_pedalboard_by_index(bank.index, pedalboard.index)

    def set_current_pedalboard_by_index(self, bank_index, pedalboard_index):
        return self.put('current/bank/{}/pedalboard/{}'.format(bank_index, pedalboard_index))

    def get_current_index(self):
        return self.get('current')

    def get_current_data(self):
        return self.get('current/data')

    def toggle_effect_current_pedalboard(self, effect):
        return self.put('current/effect/{}'.format(effect.index))

    # **********************
    # Plugin
    # **********************
    def get_plugins(self):
        return self.get('plugins')

    def get_plugin(self, uri):
        return self.get('plugin/{}'.format(uri))

    def reload_plugin(self):
        return self.put('plugins/reload')
