from .handler_test import Test

from pluginsmanager.model.patch import Patch


class PatchHandlerTest(Test):

    @property
    def default_patch(self):
        return Patch('New default patch')

    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        response = self.rest.get_patch(bank, 0)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(bank.patches[0].json, response.json())

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        patch = self.default_patch
        bank.append(patch)
        response = self.rest.create_patch(patch)

        self.assertEqual(Test.CREATED, response.status_code)
        get_patch = self.rest.get_patch(bank, bank.patches.index(patch))

        self.assertEqual(patch.json, get_patch.json())

        self.rest.delete_bank(bank)

    def test_put(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        patch = bank.patches[0]

        new_name = 'REST - Default patch - New name'
        patch.name = new_name

        response = self.rest.update_patch(patch)
        self.assertEqual(Test.UPDATED, response.status_code)

        get_patch = self.rest.get_patch(bank, bank.patches.index(patch))
        self.assertEqual(patch.json, get_patch.json())

        self.rest.delete_bank(bank)

    def test_delete(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        patch = bank.patches[0]
        r = self.rest.delete_patch(patch)
        bank.patches.remove(patch)

        self.assertEqual(Test.DELETED, r.status_code)

        response = self.rest.get_bank(bank)
        self.assertEqual(bank.json, response.json())

        self.rest.delete_bank(bank)
