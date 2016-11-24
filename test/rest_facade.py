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

    def put(self, url, data):
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
    # Patch
    # **********************
    def get_patch(self, bank, patch_index):
        return self.get('bank/{0}/patch/{1}'.format(bank.index, patch_index))

    def create_patch(self, patch):
        bank_index = patch.bank.index
        return self.post('bank/{0}/patch'.format(bank_index), patch.json)

    def update_patch(self, patch):
        bank_index = patch.bank.index
        patch_index = patch.bank.patches.index(patch)
        return self.put('bank/{0}/patch/{1}'.format(bank_index, patch_index), patch.json)

    def delete_patch(self, patch):
        bank_index = patch.bank.index
        patch_index = patch.bank.patches.index(patch)
        return self.delete('bank/{0}/patch/{1}'.format(bank_index, patch_index))

    # **********************
    # Effect
    # **********************
    def get_effect(self, patch, effect_index):
        bank_index = patch.bank.index
        patch_index = patch.bank.patches.index(patch)
        return self.get(self._url_effect(bank_index, patch_index, effect_index))

    def post_effect(self, patch, effect):
        patch_index = patch.bank.patches.index(patch)
        bank_index = patch.bank.patches.index(patch)

        url = 'bank/{0}/patch/{1}/effect'.format(bank_index, patch_index)
        return self.post(url, effect.json)

    def delete_effect(self, effect):
        patch = effect.patch

        effect_index = patch.effects.index(effect)
        patch_index = patch.bank.patches.index(patch)
        bank_index = patch.bank.index

        return self.delete(self._url_effect(bank_index, patch_index, effect_index))
    
    def _url_effect(self, bank_index, patch_index, effect_index):
        return 'bank/{0}/patch/{1}/effect/{2}'.format(
            bank_index,
            patch_index,
            effect_index
        )

    # **********************
    # Param
    # **********************
    def getParam(self, bankIndex, patchIndex, effectIndex, paramIndex):
        return self.get(self.urlParam(bankIndex, patchIndex, effectIndex, paramIndex))

    def putParam(self, bankIndex, patchIndex, effectIndex, paramIndex, value):
        url = self.urlParam(bankIndex, patchIndex, effectIndex, paramIndex)
        return self.put(url, value)

    def urlParam(self, bankIndex, patchIndex, effectIndex, paramIndex):
        return 'bank/{0}/patch/{1}/effect/{2}/param/{3}'.format(
            bankIndex,
            patchIndex,
            effectIndex,
            paramIndex
        )

    # **********************
    # ComponentData
    # **********************
    def getComponentData(self, key):
        return self.get(self.urlComponentData(key))

    def postComponentData(self, key, data):
        return self.post(self.urlComponentData(key), data)

    def deleteComponentData(self, key):
        return self.delete(self.urlComponentData(key))

    def urlComponentData(self, key):
        return 'data/{0}'.format(key)
