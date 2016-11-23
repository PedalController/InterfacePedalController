import requests

from .test import Test
from pluginsmanager.model.bank import Bank


class BankHandlerTest(Test):
    address = 'http://localhost:3000/'

    def setUp(self):
        try:
            self.rest.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    @property
    def default_bank(self):
        return Bank('REST - Default Bank')

    ########################
    # Tests
    ########################
    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        response = self.rest.get_bank(bank.index)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(bank.json, response.json())

        self.rest.delete_bank(bank.index)

    def test_post(self):
        bank = self.default_bank

        response = self.rest.create_bank(bank)
        self.assertEqual(Test.CREATED, response.status_code)

        bank.index = response.json()['index']

        persisted = self.rest.get_bank(bank.index).json()
        self.assertEqual(bank.json, persisted)

        self.rest.delete_bank(bank.index)

    def test_put(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        bank.name = 'REST - Default Bank - New name'

        response = self.rest.update_bank(bank)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_bank = self.rest.get_bank(bank.index)

        self.assertEqual(bank.json, get_bank.json())

        self.rest.delete_bank(bank.index)

    def test_delete(self):
        index = self.rest.create_bank(self.default_bank).json()['index']

        r = self.rest.delete_bank(index)
        self.assertEqual(Test.DELETED, r.status_code)
