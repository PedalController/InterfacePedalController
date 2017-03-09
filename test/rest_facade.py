import requests
import json


class RestFacade(object):
    address = 'http://localhost:3000/'
    
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
    def getBanks(self):
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
    # Swap
    # **********************
    def swap_banks(self, bank_a, bank_b):
        url = 'swap/bank-a/{0}/bank-b/{1}'.format(
            bank_a.index,
            bank_b.index
        )

        return self.put(url)

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
