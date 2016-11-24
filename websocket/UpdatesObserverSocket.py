from pluginsmanager.model.updates_observer import UpdatesObserver

from websocket.WebSocketConnections import WebSocketConnections


class UpdatesObserverSocket(UpdatesObserver):

    def send(self, json_data, token=None):
        WebSocketConnections.send_broadcast(json_data, token)

    def on_current_patch_change(self, patch, token=None):
        bank = patch.bank

        self.send({
            'type': 'CURRENT',
            'bank': bank.index,
            'patch': patch.index,
            'value': patch.json
        }, token)

    def on_bank_updated(self, bank, update_type, token=None, **kwargs):
        self.send({
            'type': 'BANK',
            'updateType': update_type.name,
            'bank': bank.index,
            'value': bank.json
        }, token)

    def on_patch_updated(self, patch, update_type, token=None, **kwargs):
        bank = kwargs['origin']
        patch_index = kwargs['index']

        self.send({
            'type': 'PATCH',
            'updateType': update_type.name,
            'bank': bank.index,
            'patch': patch_index,
            'value': patch.json
        }, token)

    def on_effect_updated(self, effect, update_type, token=None, **kwargs):
        patch = kwargs['origin']
        bank = patch.bank
        effect_index = kwargs['index']
        patch_index = bank.patches.index(patch)

        self.send({
            'type': 'EFFECT',
            'updateType': update_type.name,
            'bank': bank.index,
            'patch': patch_index,
            'effect': effect_index,
            'value': effect.json
        }, token)

    def on_effect_status_toggled(self, effect, token=None):
        bank = effect.patch.bank
        patch = effect.patch

        self.send({
            'type': 'EFFECT-TOGGLE',
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index
        }, token)

    def on_param_value_changed(self, param, token=None):
        effect = param.effect
        patch = effect.patch
        bank = patch.bank

        param_index = effect.params.index(param)
        effect_index = patch.effects.index(effect)
        patch_index = bank.patches.index(patch)

        self.send({
            'type': 'PARAM',
            'bank': bank.index,
            'patch': patch_index,
            'effect': effect_index,
            'param': param_index,
            'value': param.value,
        }, token)

    def on_connection_updated(self):
        pass
