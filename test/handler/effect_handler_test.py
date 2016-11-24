from .handler_test import Test


class EffectHandlerTest(Test):
    def test_get(self):
        bank = self.default_bank
        bank.index = self.rest.create_bank(bank).json()['index']

        effect = bank.patches[0].effects[0]
        response = self.rest.get_effect(effect)

        self.assertEqual(Test.SUCCESS, response.status_code)
        self.assertEqual(effect.json, response.json())

        self.rest.delete_bank(bank)

    def test_post(self):
        bank = self.default_bank
        pedalboard = bank.patches[0]

        bank.index = self.rest.create_bank(bank).json()['index']

        uri = 'http://guitarix.sourceforge.net/plugins/gxtubedelay#tubedelay'
        effect = self.plugins_builder.build(uri)

        response = self.rest.post_effect(pedalboard, uri)
        self.assertEqual(Test.CREATED, response.status_code)

        pedalboard.append(effect)

        get_effect = self.rest.get_effect(effect)
        self.assertEqual(effect.json, get_effect.json())

        self.rest.delete_bank(bank)

    def test_delete(self):
        bank = self.default_bank
        pedalboard = bank.patches[0]

        bank.index = self.rest.create_bank(bank).json()['index']

        uri = 'http://guitarix.sourceforge.net/plugins/gxtubedelay#tubedelay'
        effect = self.plugins_builder.build(uri)

        self.rest.post_effect(pedalboard, uri)

        pedalboard.append(effect)

        r = self.rest.delete_effect(effect)
        self.assertEqual(Test.DELETED, r.status_code)

        pedalboard.effects.remove(effect)

        get_bank = self.rest.get_bank(bank)
        self.assertEqual(bank.json, get_bank.json())

        self.rest.delete_bank(bank)
