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

from application.component.application_observer import ApplicationObserver

from webservice.websocket.web_socket_connections import WebSocketConnections


class UpdatesObserverSocket(ApplicationObserver):

    @property
    def token(self):
        return None

    def send(self, json_data, token=None):
        WebSocketConnections.send_broadcast(json_data, token)

    def on_current_pedalboard_changed(self, pedalboard, token=None):
        bank = pedalboard.bank

        self.send({
            'type': 'CURRENT',
            'bank': bank.index,
            'pedalboard': bank.pedalboards.index(pedalboard),
            'value': pedalboard.json
        }, token)

    def on_bank_updated(self, bank, update_type, index, origin, token=None, **kwargs):
        self.send({
            'type': 'BANK',
            'updateType': update_type.name,
            'bank': bank.index,
            'value': bank.json
        }, token)

    def on_pedalboard_updated(self, pedalboard, update_type, index, origin, token=None, **kwargs):
        bank = origin
        pedalboard_index = index

        self.send({
            'type': 'PEDALBOARD',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'value': pedalboard.json
        }, token)

    def on_effect_updated(self, effect, update_type, index, origin, token=None, **kwargs):
        pedalboard = origin
        bank = pedalboard.bank
        effect_index = index

        self.send({
            'type': 'EFFECT',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard.index,
            'effect': effect_index,
            'value': effect.json
        }, token)

    def on_effect_status_toggled(self, effect, token=None, **kwargs):
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        self.send({
            'type': 'EFFECT-TOGGLE',
            'bank': bank.index,
            'pedalboard': pedalboard.index,
            'effect': effect.index
        }, token)

    def on_param_value_changed(self, param, token=None, **kwargs):
        effect = param.effect
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        self.send({
            'type': 'PARAM',
            'bank': bank.index,
            'pedalboard': pedalboard.index,
            'effect': effect.index,
            'param': param.index,
            'value': param.value,
        }, token)

    def on_connection_updated(self, connection, update_type, pedalboard, token=None, **kwargs):
        bank = pedalboard.bank

        self.send({
            'type': 'CONNECTION',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard.index,
            'value': connection.json,
        }, token)
