from .handler_test import Test

from pluginsmanager.model.patch import Patch


class PedalboardHandlerTest(Test):

    @property
    def default_pedalboard(self):
        return Patch('New default patch')

    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        response = self.rest.get_pedalboard(bank.patches[0])

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(bank.patches[0].json, response.json())

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

        pedalboard = bank.patches[0]

        new_name = 'REST - Default patch - New name'
        pedalboard.name = new_name

        response = self.rest.update_pedalboard(pedalboard)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_pedalboard = self.rest.get_pedalboard(pedalboard)
        self.assertEqual(pedalboard.json, get_pedalboard.json())

        self.rest.delete_bank(bank)

    def test_delete(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        pedalboard = bank.patches[0]
        r = self.rest.delete_pedalboard(pedalboard)
        bank.patches.remove(pedalboard)

        self.assertEqual(Test.DELETED, r.status_code)

        response = self.rest.get_bank(bank)
        self.assertEqual(bank.json, response.json())

        self.rest.delete_bank(bank)
