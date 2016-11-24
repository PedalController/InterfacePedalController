import requests

from .handler_test import Test


class ComponentDataHandlerTest(Test):
    address = 'http://localhost:3000/'
    defaultBank = {
        "name": "REST - Default Bank",
        "patches": [{
            "name": "Example patch",
            "effects": [],
            "connections": []
        }]
    }

    def setUp(self):
        self.key = 'ComponentDataHandlerTest'
        try:
            self.rest.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    ########################
    # Tests
    ########################
    def test_empty_get(self):
        r = self.rest.getComponentData(self.key)
        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(r.json(), {})

    def test_content_get(self):
        data = {'test': 'test_content_get'}

        r = self.rest.postComponentData(self.key, data)
        self.assertEqual(Test.SUCCESS, r.status_code)

        r = self.rest.getComponentData(self.key)
        self.assertEqual(Test.SUCCESS, r.status_code)
        self.assertEqual(r.json(), data)

        self.rest.deleteComponentData(self.key)

    def test_override_content(self):
        data = {'test': 'test_override_content'}
        data2 = {'test': 'test_override_content', 'fu': 'bá'}

        r = self.rest.postComponentData(self.key, data)
        self.assertEqual(Test.SUCCESS, r.status_code)

        r = self.rest.getComponentData(self.key)
        self.assertEqual(r.json(), data)

        r = self.rest.postComponentData(self.key, data2)
        self.assertEqual(Test.SUCCESS, r.status_code)

        r = self.rest.getComponentData(self.key)
        self.assertEqual(r.json(), data2)

        self.rest.deleteComponentData(self.key)

    def test_directly_changes_not_works(self):
        r = self.rest.postComponentData(self.key, {'test': 'test_directly_changes_not_works'})
        self.assertEqual(Test.SUCCESS, r.status_code)

        data = self.rest.getComponentData(self.key).json()
        data['new-key'] = 'new value'

        self.assertNotEqual(self.rest.getComponentData(self.key).json(), data)

        self.rest.deleteComponentData(self.key)

    def test_delete_content(self):
        data = {'test': 'test_delete_content'}

        r = self.rest.postComponentData(self.key, data)
        self.assertEqual(Test.SUCCESS, r.status_code)

        r = self.rest.getComponentData(self.key)
        self.assertNotEqual(r.json(), {})

        r = self.rest.deleteComponentData(self.key)
        self.assertEqual(Test.DELETED, r.status_code)

        r = self.rest.getComponentData(self.key)
        self.assertEqual(r.json(), {})
