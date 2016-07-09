from application.model.UpdatesObserver import UpdatesObserver

from websocket.WebSocketConnections import WebSocketConnections


class UpdatesObserverSocket(UpdatesObserver):

    def send(self, jsonData):
        WebSocketConnections.sendBroadcast(jsonData)

    def onCurrentPatchChange(self, patch):
        bank = patch.bank

        self.send({
            'type': 'CURRENT',
            'bank': bank.index,
            'patch': patch.index,
            'value': patch.json
        })

    def onBankUpdate(self, bank, updateType):
        self.send({
            'type': 'BANK',
            'updateType': updateType,
            'bank': bank.index,
            'value': bank.json
        })

    def onPatchUpdated(self, patch, updateType):
        bank = patch.bank

        self.send({
            'type': 'PATCH',
            'updateType': updateType,
            'bank': bank.index,
            'patch': patch.index,
            'value': patch.json
        })

    def onEffectUpdated(self, effect, updateType):
        bank = effect.patch.bank
        patch = effect.patch

        self.send({
            'type': 'EFFECT',
            'updateType': updateType,
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index,
            'value': effect.json
        })

    def onEffectStatusToggled(self, effect):
        bank = effect.patch.bank
        patch = effect.patch

        self.send({
            'type': 'EFFECT-TOGGLE',
            'bank': bank.index,
            'patch': patch.index,
            'effect': effect.index
        })

    def onParamValueChange(self, param):
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
        })
