from application.component.application_observer import ApplicationObserver

from websocket.web_socket_connections import WebSocketConnections


class UpdatesObserverSocket(ApplicationObserver):

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

    def on_bank_updated(self, bank, update_type, token=None, **kwargs):
        self.send({
            'type': 'BANK',
            'updateType': update_type.name,
            'bank': bank.index,
            'value': bank.json
        }, token)

    def on_pedalboard_updated(self, pedalboard, update_type, token=None, **kwargs):
        bank = kwargs['origin']
        pedalboard_index = kwargs['index']

        self.send({
            'type': 'PATCH',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'value': pedalboard.json
        }, token)

    def on_effect_updated(self, effect, update_type, token=None, **kwargs):
        pedalboard = kwargs['origin']
        bank = pedalboard.bank
        effect_index = kwargs['index']
        pedalboard_index = bank.pedalboards.index(pedalboard)

        self.send({
            'type': 'EFFECT',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'effect': effect_index,
            'value': effect.json
        }, token)

    def on_effect_status_toggled(self, effect, token=None):
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        effect_index = pedalboard.effects.index(effect)
        pedalboard_index = bank.pedalboards.index(pedalboard)

        self.send({
            'type': 'EFFECT-TOGGLE',
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'effect': effect_index
        }, token)

    def on_param_value_changed(self, param, token=None):
        effect = param.effect
        pedalboard = effect.pedalboard
        bank = pedalboard.bank

        param_index = effect.params.index(param)
        effect_index = pedalboard.effects.index(effect)
        pedalboard_index = bank.pedalboards.index(pedalboard)

        self.send({
            'type': 'PARAM',
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'effect': effect_index,
            'param': param_index,
            'value': param.value,
        }, token)

    def on_connection_updated(self, pedalboard, connection, update_type, token=None):
        bank = pedalboard.bank
        pedalboard_index = bank.pedalboards.index(pedalboard)

        self.send({
            'type': 'CONNECTION',
            'updateType': update_type.name,
            'bank': bank.index,
            'pedalboard': pedalboard_index,
            'value': connection,
        }, token)