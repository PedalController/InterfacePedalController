import requests

from .test import Test

'''
class EffectHanddlerTest(Test):
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
        bankIndex, patchIndex, effectIndex = 0, 0, 0
        r = self.rest.getEffect(bankIndex, patchIndex, effectIndex)

        self.assertEqual(Test.SUCCESS, r.status_code)

    def test_post(self):
        bankIndex, patchIndex = 0, 0
        uri = 'http://guitarix.sourceforge.net/plugins/gxtubedelay#tubedelay'

        r = self.rest.postEffect(bankIndex, patchIndex, uri)
        self.assertEqual(Test.CREATED, r.status_code)

        effectIndex = r.json()['index']
        effectPersisted = self.rest.getEffect(bankIndex, patchIndex, effectIndex).json()
        self.assertEqual(uri, effectPersisted['uri'])

        self.rest.deleteEffect(bankIndex, patchIndex, effectIndex)

    def test_delete(self):
        bankIndex, patchIndex = 0, 0
        uri = 'http://guitarix.sourceforge.net/plugins/gxtubedelay#tubedelay'

        effectIndex = self.rest.postEffect(bankIndex, patchIndex, uri).json()['index']

        r = self.rest.deleteEffect(bankIndex, patchIndex, effectIndex)
        self.assertEqual(Test.DELETED, r.status_code)
'''
