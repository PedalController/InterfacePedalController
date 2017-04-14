import time

import tornado.ioloop
import tornado.web

from application.component.component import Component

from webservice.handler.banks_handler import BanksHandler
from webservice.handler.bank_handler import BankHandler
from webservice.handler.effect_handler import EffectHandler
from webservice.handler.param_handler import ParamHandler
from webservice.handler.pedalboard_handler import PedalboardHandler
from webservice.handler.pedalboard_data_handler import PedalboardDataHandler

from webservice.handler.plugins_handler import PluginsHandler
from webservice.handler.plugin_handler import PluginHandler

from webservice.handler.connection_handler import ConnectionHandler

from webservice.handler.current_handler import CurrentHandler
from webservice.handler.current_data_handler import CurrentDataHandler
from webservice.handler.current_effect_status_handler import CurrentEffectStatusHandler
from webservice.handler.current_pedalboard_handler import CurrentPedalboardHandler

from webservice.handler.swap_bank_handler import SwapBankHandler
from webservice.handler.swap_pedalboard_handler import SwapPedalboardHandler

from webservice.handler.component_data_handler import ComponentDataHandler

from websocket.web_socket_connection_handler import WebSocketConnectionHandler
from websocket.updates_observer_socket import UpdatesObserverSocket

from pybonjour_service.pybonjour_service import PybonjourService


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

        self._log("WebService - PedalPi API REST      localhost:" + str(self.port))
        self._log("WebService - PedalPi API WebSocket localhost:" + str(self.port) + "/ws")

        self._start_zeroconf(self.port)

    def register_handlers(self):
        self.for_handler(PluginsHandler) \
            .register(r"/v1/plugins")
        self.for_handler(PluginHandler) \
            .register(r"/v1/plugin/(?P<uri>[^^]+)")

        self.for_handler(BanksHandler)\
            .register(r"/v1/banks")

        # Bank
        self.for_handler(BankHandler) \
            .register(r"/v1/bank") \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)")

        # Pedalboard
        self.for_handler(PedalboardHandler) \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard") \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)")

        # Pedalboard data
        self.for_handler(PedalboardDataHandler) \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/data/(?P<key>[a-zA-Z_\-0-9]+)")

        # Effect
        self.for_handler(EffectHandler) \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/effect") \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/effect/(?P<effect_index>[0-9]+)")

        # Param
        self.for_handler(ParamHandler) \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/effect/(?P<effect_index>[0-9]+)/param/(?P<param_index>[0-9]+)")

        # Get current
        self.for_handler(CurrentHandler) \
            .register(r"/v1/current")
        self.for_handler(CurrentDataHandler) \
            .register(r"/v1/current/data")

        # Set current
        self.for_handler(CurrentEffectStatusHandler) \
            .register(r"/v1/current/effect/(?P<effect_index>[0-9]+)")
        self.for_handler(CurrentPedalboardHandler) \
            .register(r"/v1/current/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)")

        # Swap
        self.for_handler(SwapBankHandler) \
            .register(r"/v1/swap/bank-a/(?P<bank_a_index>[0-9]+)/bank-b/(?P<bank_b_index>[0-9]+)")
        self.for_handler(SwapPedalboardHandler) \
            .register(r"/v1/swap/pedalboard/bank/(?P<bank_index>[0-9]+)/pedalboard-a/(?P<pedalboard_a_index>[0-9]+)/pedalboard-b/(?P<pedalboard_b_index>[0-9]+)")

        # Connections
        self.for_handler(ConnectionHandler) \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/connect") \
            .register(r"/v1/bank/(?P<bank_index>[0-9]+)/pedalboard/(?P<pedalboard_index>[0-9]+)/disconnect")

        # Peripheral

        # ComponentDataHandler
        self.for_handler(ComponentDataHandler) \
            .register(r"/v1/data/(?P<key>[a-zA-Z\-0-9:]+)") \

        # WebSocket
        self.for_handler(WebSocketConnectionHandler) \
            .register(r"/ws/?$")

    def for_handler(self, handler_class):
        return HandlerRegister(self, handler_class)

    def register(self, uri, class_handler):
        handler = (uri, class_handler, dict(app=self.application))
        self.handlers.append(handler)

        self._log('WebService', '-', class_handler.__name__, uri)

    def prepare(self):
        return tornado.web.Application(self.handlers)

    def _log(self, *args, **kwargs):
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']', *args, **kwargs)

    def _start_zeroconf(self, port):
        try:
            zeroconf = PybonjourService(port)
            register = zeroconf.start()
        except:
            self._log('zeroconf is not instaled')
            pass


class HandlerRegister(object):

    def __init__(self, web_service, handler_class):
        self.web_service = web_service
        self.handler_class = handler_class

    def register(self, uri):
        self.web_service.register(uri, self.handler_class)
        return self
