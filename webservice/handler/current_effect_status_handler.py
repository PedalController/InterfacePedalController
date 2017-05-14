# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.handler_utils import integer

from application.controller.effect_controller import EffectController
from application.controller.current_controller import CurrentController


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
