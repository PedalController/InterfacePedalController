import unittest
import requests

from .test import Test


class BanksControllerTest(Test):
    address = 'http://localhost:3000/'
    defaultBank = {
        "name": "REST - Default Bank",
        "patches": [{
            "name": "Example patch",
            "effects": [],
            "connections": []
        }]
    }

    
    def setUp(self):
        try:
            self.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    ########################
    # CRUD
    ########################
    def getBank(self, index):
        return self.get('bank/{0}'.format(index))

    def createBank(self, data):
        return self.post('bank', data)

    def updateBank(self, index, data):
        return self.put('bank/{0}'.format(index), data)

    def deleteBank(self, index):
        return self.delete('bank/{0}'.format(index))


    ########################
    # Tests
    ########################
    def test_get(self):
        index = self.createBank(self.defaultBank).json()['index']
        r = self.getBank(index)

        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(index, r.json()['index'])

        self.deleteBank(index)

    def test_post(self):
        r = self.createBank(self.defaultBank)
        self.assertEqual(Test.CREATED, r.status_code)

        index = r.json()['index']
        bankPersisted = self.getBank(index).json()
        self.assertEqual(index, bankPersisted['index'])

        self.deleteBank(index)

    def test_put(self):
        index = self.createBank(self.defaultBank).json()['index']
        newName = 'REST - Default Bank - New name'

        bankCopy = dict(self.defaultBank)
        bankCopy['name'] = newName
        bankCopy['index'] = index

        r = self.updateBank(index, bankCopy)
        self.assertEqual(Test.UPDATED, r.status_code)
        
        self.deleteBank(index)

    def test_delete(self):
        index = self.createBank(self.defaultBank).json()['index']

        r = self.delete('bank/{0}'.format(index))
        self.assertEqual(Test.DELETED, r.status_code)
