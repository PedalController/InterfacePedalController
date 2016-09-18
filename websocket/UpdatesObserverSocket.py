from application.model.UpdatesObserver import UpdatesObserver

from websocket.WebSocketConnections import WebSocketConnections


class UpdatesObserverSocket(UpdatesObserver):

    def send(self, json_data, token=None):
        WebSocketConnections.sendBroadcast(json_data, token)

    def onCurrentPatchChange(self, patch, token=None):
        bank = patch.bank

        self.send({
            'type': 'CURRENT',
            'bank': bank.index,
            'patch': patch.index,
            'value': patch.json
        }, token)

    def onBankUpdate(self, bank, update_type, token=None):
        self.send({
            'type': 'BANK',
            'updateType': update_type.name,
            'bank': bank.index,
            'value': bank.json
        }, token)

    def onPatchUpdated(self, patch, update_type, token=None):
        bank = patch.bank

        self.send({
            'type': 'PATCH',
            'updateType': update_type.name,
            'bank': bank.index,
            'patch': patch.index,
            'value': patch.json
        }, token)

    def onEffectUpdated(self, effect, update_type, token=None):
        bank = effect.patch.bank
        patch = effect.patch

        self.send({
            'type': 'EFFECT',
            'updateType': update_type.name,
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index,
            'value': effect.json
        }, token)

    def onEffectStatusToggled(self, effect, token=None):
        bank = effect.patch.bank
        patch = effect.patch

        self.send({
            'type': 'EFFECT-TOGGLE',
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index
        }, token)

    def onParamValueChange(self, param, token=None):
        bank = param.effect.patch.bank
        patch = param.effect.patch
        effect = param.effect

        self.send({
            'type': 'PARAM',
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index,
            'param': param.index,
            'value': param.value,
        }, token)
