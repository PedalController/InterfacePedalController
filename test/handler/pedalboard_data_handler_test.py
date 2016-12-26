from .handler_test import Test

from pluginsmanager.model.pedalboard import Pedalboard


class PedalboardDataHandlerTest(Test):

    @property
    def default_pedalboard(self):
        return Pedalboard('New default pedalboard')

    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        key = 'test_get'

        pedalboard = bank.pedalboards[0]
        self.assert_data_equal(pedalboard, key)

        pedalboard.data[key] = {'name': 'value1'}
        self.update_data(pedalboard, key)

        self.assert_data_equal(pedalboard, key)

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        key1 = 'key1'
        key2 = 'key2'

        pedalboard = bank.pedalboards[0]

        self.assert_data_equal(pedalboard, key1)

        pedalboard.data[key1] = {'name': 'value1'}
        self.update_data(pedalboard, key1)
        self.assert_data_equal(pedalboard, key1)

        pedalboard.data[key2] = {'name': 'value2'}
        self.update_data(pedalboard, key2)

        self.assert_data_equal(pedalboard, key1)
        self.assert_data_equal(pedalboard, key2)

        self.rest.delete_bank(bank)

    def assert_data_equal(self, pedalboard, key):
        response = self.rest.get_pedalboard_data(pedalboard, key)
        self.assertEqual(Test.SUCCESS, response.status_code)
        if key in pedalboard.data:
            self.assertEqual(pedalboard.data[key], response.json())
        else:
            self.assertEqual({}, response.json())

    def update_data(self, pedalboard, key):
        response = self.rest.update_pedalboard_data(pedalboard, key)
        self.assertEqual(Test.SUCCESS, response.status_code)
