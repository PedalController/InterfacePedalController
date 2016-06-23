import tornado.ioloop
import tornado.web

import sys
folder = 'application'
sys.path.append(folder)

from handler.BanksHandler import BanksHandler
from handler.BankHandler import BankHandler
from handler.PatchHandler import PatchHandler

from handler.EffectsHandler import EffectsHandler
from handler.EffectHandler import EffectHandler

from handler.SetStatusHandler import SetStatusHandler

from application.Application import Application


def make_app(app):
    return tornado.web.Application([
        (r"/effects", EffectsHandler, dict(app=app)),
        (r"/effect/([^/]+)", EffectHandler, dict(app=app)),

        # Read, update and delete
        (r"/banks", BanksHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect/(?P<effect>[0-9]+)/param/(?P<param>[0-9]+)",BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect/(?P<effect>[0-9]+)", BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)", PatchHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)", BankHandler, dict(app=app)),

        # Save new
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect", BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch", PatchHandler, dict(app=app)),
        (r"/bank", BankHandler, dict(app=app)),

        # Current
        (r"/current/bank/(?P<bank>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/patch/(?P<patch>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/effect/(?P<effect>[0-9]+)", SetStatusHandler, dict(app=app)),
        (r"/current/effect/(?P<effect>[0-9]+)/param/(?P<param>[0-9]+)", SetStatusHandler, dict(app=app)),

        # Connections

        # Peripheral
    ])

if __name__ == "__main__":
    app = make_app(Application(True, dataPatch="application/data/"))
    app.listen(3000)

    print("PedalController API localhost:3000")
    tornado.ioloop.IOLoop.current().start()
