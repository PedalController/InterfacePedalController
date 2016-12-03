import uuid
import unittest
import requests

from test.rest_facade import RestFacade

from pluginsmanager.model.bank import Bank
from pluginsmanager.model.pedalboard import Pedalboard

from pluginsmanager.model.lv2.lv2_effect_builder import Lv2EffectBuilder


class Test(unittest.TestCase):
    address = 'http://localhost:3000/'

    SUCCESS = 200
    CREATED = 201
    UPDATED = 200
    DELETED = 200

    ERROR = 400
    rest = RestFacade()

    plugins_builder = Lv2EffectBuilder()

    def setUp(self):
        try:
            self.rest.get('')
        except requests.exceptions.ConnectionError:
            self.fail("Server is down")

    @property
    def default_bank(self):
        bank = Bank('REST - Default Bank' + str(uuid.uuid4()))
        pedalboard = Pedalboard('REST - Default Pedalboard')

        reverb = self.plugins_builder.build('http://calf.sourceforge.net/plugins/Reverb')
        reverb2 = self.plugins_builder.build('http://calf.sourceforge.net/plugins/Reverb')

        bank.append(pedalboard)

        pedalboard.append(reverb)
        pedalboard.append(reverb2)

        reverb.outputs[0].connect(reverb2.inputs[0])

        return bank
