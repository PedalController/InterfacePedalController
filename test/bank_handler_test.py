import requests

from .test import Test


class BankHanddlerTest(Test):
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
            self.rest.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    ########################
    # Tests
    ########################
    def test_get(self):
        index = self.rest.createBank(self.defaultBank).json()['index']
        r = self.rest.getBank(index)

        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(index, r.json()['index'])

        self.rest.deleteBank(index)

    def test_post(self):
        r = self.rest.createBank(self.defaultBank)
        self.assertEqual(Test.CREATED, r.status_code)

        index = r.json()['index']
        bankPersisted = self.rest.getBank(index).json()
        self.assertEqual(index, bankPersisted['index'])

        self.rest.deleteBank(index)

    def test_put(self):
        index = self.rest.createBank(self.defaultBank).json()['index']
        newName = 'REST - Default Bank - New name'

        bankCopy = self.rest.getBank(index).json()
        bankCopy['name'] = newName

        r = self.rest.updateBank(index, bankCopy)
        self.assertEqual(Test.UPDATED, r.status_code)

        self.rest.deleteBank(index)

    def test_delete(self):
        index = self.rest.createBank(self.defaultBank).json()['index']

        r = self.rest.deleteBank(index)
        self.assertEqual(Test.DELETED, r.status_code)
