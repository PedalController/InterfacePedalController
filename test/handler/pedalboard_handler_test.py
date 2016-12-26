from .handler_test import Test

from pluginsmanager.model.pedalboard import Pedalboard


class PedalboardHandlerTest(Test):

    @property
    def default_pedalboard(self):
        return Pedalboard('New default pedalboard')

    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        response = self.rest.get_pedalboard(bank.pedalboards[0])

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(bank.pedalboards[0].json, response.json())

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = self.default_pedalboard
        bank.append(pedalboard)
        response = self.rest.create_pedalboard(pedalboard)

        self.assertEqual(Test.CREATED, response.status_code)
        get_pedalboard = self.rest.get_pedalboard(pedalboard)

        self.assertEqual(pedalboard.json, get_pedalboard.json())

        self.rest.delete_bank(bank)

    def test_put(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]

        new_name = 'REST - Default pedalboard - New name'
        pedalboard.name = new_name

        response = self.rest.update_pedalboard(pedalboard)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_pedalboard = self.rest.get_pedalboard(pedalboard)
        self.assertEqual(pedalboard.json, get_pedalboard.json())

        self.rest.delete_bank(bank)

    def test_delete(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.pedalboards[0]
        r = self.rest.delete_pedalboard(pedalboard)
        bank.pedalboards.remove(pedalboard)

        self.assertEqual(Test.DELETED, r.status_code)

        response = self.rest.get_bank(bank)
        self.assertEqual(bank.json, response.json())

        self.rest.delete_bank(bank)
