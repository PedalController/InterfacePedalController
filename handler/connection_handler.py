from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.effect_controller import EffectController
from application.controller.banks_controller import BanksController
from application.controller.device_controller import DeviceController

from util.handler_utils import integer

from pluginsmanager.util.persistence_decoder import ConnectionReader


class ConnectionHandler(AbstractRequestHandler):
    app = None
    controller = None
    banks = None

    def initialize(self, app):
        self.controller = app.controller(EffectController)
        self.banks = app.controller(BanksController)

    @integer('bank_index', 'pedalboard_index')
    def put(self, bank_index, pedalboard_index):
        bank = self.banks.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        connection = ConnectionReader(pedalboard, DeviceController.sys_effect).read(self.request_data)
        pedalboard.connections.append(connection)

        self.controller.connected(pedalboard, connection, token=self.token)

        self.send(200)

    @integer('bank_index', 'pedalboard_index')
    def post(self, bank_index, pedalboard_index):
        bank = self.banks.banks[bank_index]
        pedalboard = bank.pedalboards[pedalboard_index]

        connection = ConnectionReader(pedalboard, DeviceController.sys_effect).read(self.request_data)
        pedalboard.connections.remove(connection)

        self.controller.disconnected(pedalboard, connection, token=self.token)

        self.send(200)
