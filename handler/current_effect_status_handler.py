from handler.abstract_request_handler import AbstractRequestHandler

from application.controller.effect_controller import EffectController
from application.controller.current_controller import CurrentController

from util.handler_utils import integer


class CurrentEffectStatusHandler(AbstractRequestHandler):
    app = None
    current = None
    controller = None

    def initialize(self, app):
        self.app = app
        self.controller = app.controller(EffectController)
        self.current = app.controller(CurrentController)

    @integer('effect_index')
    def put(self, effect_index):
        effect = self.current.current_pedalboard.effects[effect_index]
        self.controller.toggle_status(effect, token=self.token)
