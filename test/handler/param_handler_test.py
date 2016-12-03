import requests

from .handler_test import Test


class ParamHandlerTest(Test):
    address = 'http://localhost:3000/'
    
    def setUp(self):
        try:
            self.rest.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    ########################
    # Tests
    ########################
    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        param = bank.pedalboards[0].effects[0].params[0]
        response = self.rest.get_param(param)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(param.json, response.json())

        self.rest.delete_bank(bank)

    def test_put(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        param = bank.pedalboards[0].effects[0].params[0]
        param.value += 1

        response = self.rest.put_param(param)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_value = self.rest.get_param(param)
        self.assertEqual(param.json, get_value.json())

        self.rest.delete_bank(bank)
