import tornado.ioloop
import tornado.web

from load_module import load_module

load_module('application')

from application.Application import Application
from application.controller.NotificationController import NotificationController

from handler.BanksHandler import BanksHandler
from handler.BankHandler import BankHandler
from handler.EffectHandler import EffectHandler
from handler.ParamHandler import ParamHandler
from handler.PatchHandler import PatchHandler

from handler.PluginsHandler import PluginsHandler
from handler.PluginHandler import PluginHandler

from handler.SetStatusHandler import SetStatusHandler

from websocket.WebSocketConnectionHandler import WebSocketConnectionHandler
from websocket.UpdatesObserverSocket import UpdatesObserverSocket


class WebService(object):
    application = None
    handlers = None
    observer = None

    def __init__(self, application):
        self.application = application
        self.handlers = []

        self.registerHandlers()

        self.observer = UpdatesObserverSocket()
        self.application.controller(NotificationController).register(self.observer)

    def prepare(self):
        return tornado.web.Application(self.handlers)

    def registerHandlers(self):
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

        # Current
        self.forHandler(SetStatusHandler) \
            .register(r"/current/bank/(?P<bankIndex>[0-9]+)") \
            .register(r"/current/patch/(?P<patchIndex>[0-9]+)") \
            .register(r"/current/effect/(?P<effectIndex>[0-9]+)") \
            .register(r"/current/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)")

        # Connections

        # Peripheral

        # WebSocket
        self.forHandler(WebSocketConnectionHandler) \
            .register(r"/ws/?$")

    def forHandler(self, handlerClass):
        return HandlerRegister(self, handlerClass)

    def register(self, uri, classHandler):
        handler = (uri, classHandler, dict(app=self.application))
        self.handlers.append(handler)


class HandlerRegister(object):

    def __init__(self, webService, handlerClass):
        self.ws = webService
        self.handlerClass = handlerClass
    
    def register(self, uri):
        self.ws.register(uri, self.handlerClass)
        return self

