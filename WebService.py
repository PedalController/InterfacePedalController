import tornado.ioloop
import tornado.web

from application.architecture.Component import Component

from handler.BanksHandler import BanksHandler
from handler.BankHandler import BankHandler
from handler.EffectHandler import EffectHandler
from handler.ParamHandler import ParamHandler
from handler.PatchHandler import PatchHandler

from handler.PluginsHandler import PluginsHandler
from handler.PluginHandler import PluginHandler

from handler.CurrentHandler import CurrentHandler
from handler.CurrentDataHandler import CurrentDataHandler
from handler.SetStatusHandler import SetStatusHandler

from handler.SwapBankHandler import SwapBankHandler
from handler.SwapPatchHandler import SwapPatchHandler
from handler.SwapEffectHandler import SwapEffectHandler

from handler.ComponentDataHandler import ComponentDataHandler

from websocket.WebSocketConnectionHandler import WebSocketConnectionHandler
from websocket.UpdatesObserverSocket import UpdatesObserverSocket


class WebService(Component):
    """
    Exposes the :class:`Application` features in a _façade_ REST and
    notifies changes in a WebSocket connection.

    For more details, see http://pedalpi.github.io/WebService.
    """

    def __init__(self, application, port):
        super().__init__(application)

        self.handlers = []
        self.observer = None
        self.ws_app = None
        self.port = port

    def init(self):
        self.register_handlers()

        self.observer = UpdatesObserverSocket()
        self.register_observer(self.observer)

        self.ws_app = self.prepare()
        self.ws_app.listen(self.port)

        print("WebService - PedalPi API REST      localhost:" + str(self.port))
        print("WebService - PedalPi API WebSocket localhost:" + str(self.port) + "/ws")

    def register_handlers(self):
        self.forHandler(PluginsHandler) \
            .register(r"/effects")
        self.forHandler(PluginHandler) \
            .register(r"/effect/([^/]+)")

        self.forHandler(BanksHandler).register(r"/banks")

        # Bank
        self.forHandler(BankHandler) \
            .register(r"/bank") \
            .register(r"/bank/(?P<bankIndex>[0-9]+)")

        # Patch
        self.forHandler(PatchHandler) \
            .register(r"/bank/(?P<bankIndex>[0-9]+)/patch") \
            .register(r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)")

        # Effect
        self.forHandler(EffectHandler) \
            .register(r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect") \
            .register(r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)")

        # Param
        self.forHandler(ParamHandler) \
            .register(r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)")

        # Get current
        self.forHandler(CurrentHandler) \
            .register(r"/current")
        self.forHandler(CurrentDataHandler) \
            .register(r"/current/data")

        # Set current
        self.forHandler(SetStatusHandler) \
            .register(r"/current/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)") \
            .register(r"/current/effect/(?P<effectIndex>[0-9]+)") \
            .register(r"/current/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)")

        # Swap
        self.forHandler(SwapBankHandler) \
            .register(r"/swap/bank-a/(?P<bankAIndex>[0-9]+)/bank-b/(?P<bankBIndex>[0-9]+)")
        self.forHandler(SwapPatchHandler) \
            .register(r"/swap/patch/bank/(?P<bankIndex>[0-9]+)/patch-a/(?P<patchAIndex>[0-9]+)/patch-b/(?P<patchBIndex>[0-9]+)")
        self.forHandler(SwapEffectHandler) \
            .register(r"/swap/effect/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect-a/(?P<effectAIndex>[0-9]+)/effect-b/(?P<effectBIndex>[0-9]+)")

        # Connections

        # Peripheral

        # ComponentDataHandler
        self.forHandler(ComponentDataHandler) \
            .register(r"/data/(?P<key>[a-zA-Z\-0-9:]+)") \

        # WebSocket
        self.forHandler(WebSocketConnectionHandler) \
            .register(r"/ws/?$")

    def forHandler(self, handler_class):
        return HandlerRegister(self, handler_class)

    def register(self, uri, class_handler):
        handler = (uri, class_handler, dict(app=self.application))
        self.handlers.append(handler)

    def prepare(self):
        return tornado.web.Application(self.handlers)


class HandlerRegister(object):

    def __init__(self, web_service, handler_class):
        self.web_service = web_service
        self.handler_class = handler_class

    def register(self, uri):
        self.web_service.register(uri, self.handler_class)
        return self
