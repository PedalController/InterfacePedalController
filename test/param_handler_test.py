import unittest
import requests

from .test import Test


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
        bankIndex, patchIndex, effectIndex, paramIndex = 0, 0, 0, 0
        r = self.rest.getParam(bankIndex, patchIndex, effectIndex, paramIndex)

        self.assertEqual(Test.SUCCESS, r.status_code)

    def test_put(self):
        bankIndex, patchIndex, effectIndex, paramIndex = 0, 0, 0, 0

        param = self.rest.getParam(bankIndex, patchIndex, effectIndex, paramIndex).json()
        originalValue = param['value']
        newValue = originalValue+1

        r = self.rest.putParam(bankIndex, patchIndex, effectIndex, paramIndex, newValue)
        self.assertEqual(Test.UPDATED, r.status_code)
        self.assertEqual(
            newValue,
            self.rest.getParam(bankIndex, patchIndex, effectIndex, paramIndex).json()['value']
        )

        # Restoring
        r = self.rest.putParam(bankIndex, patchIndex, effectIndex, paramIndex, originalValue)
