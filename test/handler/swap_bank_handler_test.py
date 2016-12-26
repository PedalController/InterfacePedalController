from .handler_test import Test

from pluginsmanager.model.pedalboard import Pedalboard


class SwapBankHandlerTest(Test):

    def test_swap(self):
        bank = self.default_bank
        bank2 = self.default_bank

        bank.index = self.rest.create_bank(bank).json()['index']
        bank2.index = self.rest.create_bank(bank2).json()['index']

        response = self.rest.swap_banks(bank, bank2)
        self.assertEqual(Test.SUCCESS, response.status_code)

        bank.index, bank2.index = bank2.index, bank.index

        response = self.rest.get_bank(bank)
        response2 = self.rest.get_bank(bank2)

        self.assertEqual(Test.SUCCESS, response.status_code)

        self.assertEqual(bank.json, response.json())
        self.assertEqual(bank2.json, response2.json())

        self.rest.delete_bank(bank)
        self.rest.delete_bank(bank2)
