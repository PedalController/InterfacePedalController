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
    def getBank(self, index):
        return self.get('bank/{0}'.format(index))

    def createBank(self, data):
        return self.post('bank', data)

    def updateBank(self, index, data):
        return self.put('bank/{0}'.format(index), data)

    def deleteBank(self, index):
        return self.delete('bank/{0}'.format(index))
    
    # **********************
    # Patch
    # **********************
    def getPatch(self, bankIndex, patchIndex):
        return self.get('bank/{0}/patch/{1}'.format(bankIndex, patchIndex))

    def createPatch(self, bankIndex, data):
        return self.post('bank/{0}/patch'.format(bankIndex), data)

    def updatePatch(self, bankIndex, patchIndex, data):
        return self.put('bank/{0}/patch/{1}'.format(bankIndex, patchIndex), data)

    def deletePatch(self, bankIndex, patchIndex):
        return self.delete('bank/{0}/patch/{1}'.format(bankIndex, patchIndex))