import requests

from .test import Test

'''
class PatchHanddlerTest(Test):
    address = 'http://localhost:3000/'
    defaultBank = {
        "name": "REST - Default Bank",
        "patches": [{
            "name": "Example patch",
            "effects": [],
            "connections": []
        }]
    }
    defaultPatch = {
        'name': 'REST - Patch name'
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
        bankIndex = self.rest.create_bank(self.defaultBank).json()['index']
        patchIndex = self.rest.createPatch(bankIndex, self.defaultPatch).json()['index']
        r = self.rest.getPatch(bankIndex, patchIndex)

        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(self.defaultPatch['name'], r.json()['name'])

        self.rest.delete_bank(bankIndex)

    def test_post(self):
        bankIndex = self.rest.create_bank(self.defaultBank).json()['index']
        r = self.rest.createPatch(bankIndex, self.defaultPatch)

        self.assertEqual(Test.CREATED, r.status_code)

        patchIndex = r.json()['index']
        patchPersisted = self.rest.getPatch(bankIndex, patchIndex).json()
        self.assertEqual(self.defaultPatch['name'], patchPersisted['name'])

        self.rest.delete_bank(bankIndex)

    def test_put(self):
        bankIndex = self.rest.create_bank(self.defaultBank).json()['index']
        patchIndex = self.rest.createPatch(bankIndex, self.defaultPatch).json()['index']
        newName = 'REST - Default patch - New name'

        patchCopy = self.rest.getPatch(bankIndex, patchIndex).json()
        patchCopy['name'] = newName

        r = self.rest.updatePatch(bankIndex, patchIndex, patchCopy)
        self.assertEqual(Test.UPDATED, r.status_code)

        self.rest.delete_bank(bankIndex)

    def test_delete(self):
        bankIndex = self.rest.create_bank(self.defaultBank).json()['index']
        patchIndex = self.rest.createPatch(bankIndex, self.defaultPatch).json()['index']

        r = self.rest.deletePatch(bankIndex, patchIndex)
        self.assertEqual(Test.DELETED, r.status_code)

        self.rest.delete_bank(bankIndex)
'''