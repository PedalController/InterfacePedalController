import tornado.ioloop
import tornado.web

import sys
folder = 'application'
sys.path.append(folder)

from handler.BanksHandler import BanksHandler
from handler.BankHandler import BankHandler
from handler.EffectHandler import EffectHandler
from handler.ParamHandler import ParamHandler
from handler.PatchHandler import PatchHandler

from handler.PluginsHandler import PluginsHandler
from handler.PluginHandler import PluginHandler

from handler.SetStatusHandler import SetStatusHandler

from application.Application import Application


def make_app(app):
    return tornado.web.Application([
        (r"/effects", PluginsHandler, dict(app=app)),
        (r"/effect/([^/]+)", PluginHandler, dict(app=app)),

        (r"/banks", BanksHandler, dict(app=app)),

        # Bank
        (r"/bank", BankHandler, dict(app=app)),
        (r"/bank/(?P<bankIndex>[0-9]+)", BankHandler, dict(app=app)),

        # Patch
        (r"/bank/(?P<bankIndex>[0-9]+)/patch", PatchHandler, dict(app=app)),
        (r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)", PatchHandler, dict(app=app)),

        # Effect
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect", EffectHandler, dict(app=app)),
        (r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)", EffectHandler, dict(app=app)),

        # Param
        (r"/bank/(?P<bankIndex>[0-9]+)/patch/(?P<patchIndex>[0-9]+)/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)",ParamHandler, dict(app=app)),

        # Current
        (r"/current/bank/(?P<bankIndex>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/patch/(?P<patchIndex>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/effect/(?P<effectIndex>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/effect/(?P<effectIndex>[0-9]+)/param/(?P<paramIndex>[0-9]+)", SetStatusHandler, dict(app=app)),

        # Connections

        # Peripheral
    ])

if __name__ == "__main__":
    app = make_app(Application(True, dataPatch="application/data/"))
    app.listen(3000)

    print("PedalController API localhost:3000")
    tornado.ioloop.IOLoop.current().start()
