import unittest
import requests

from .test import Test


class BanksControllerTest(Test):
    address = 'http://localhost:3000/'
    defaultBank = {}

    ########################
    # CRUD
    ########################
    def getBank(self, index):
        return self.get('bank/{0}'.format(index))

    def createBank(self, data):
        return self.post('bank/', data)

    def updateBank(self, index, data):
        return self.put('bank/{0}'.format(index), params=data)

    def deleteBank(self, index):
        return self.delete('bank/{0}'.format(index))

    def setUp(self):
        try:
            self.get(self.address)
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    ########################
    # Tests
    ########################
    def test_get(self):
        index = self.createBank(self.defaultBank).json()['index']
        r = self.getBank(index)

        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(self.defaultBank, r.json())

        self.deleteBank(index)

    def test_post(self):
        index = self.createBank(self.defaultBank).json()['index']
        self.assertEqual(Test.CREATED, r.status_code)

        bankPersisted = self.getBank(index).json()
        self.assertEqual(self.defaultBank, r.json())

        self.deleteBank(index)

    def test_put(self):
        self.fail(self.createBank(self.defaultBank).text)
        index = self.createBank(self.defaultBank).json()['index']
        newName = 'New name'

        bankCopy = dict()
        bankCopy.update(self.defaultBank)
        bankCopy['name'] = newName

        r = self.updateBank(index, bankCopy)
        self.assertEqual(Test.UPDATED, r.status_code)
        
        self.deleteBank(index)

    def test_delete(self):
        index = self.createBank(self.defaultBank).json()['index']

        r = self.delete('bank/{0}'.format(index))
        self.assertEqual(Test.DELETED, r.status_code)

        self.deleteBank(index)
