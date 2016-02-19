import tornado.ioloop
import tornado.web

from handlers.BanksHandler import BanksHandler
from handlers.BankHandler import BankHandler

from handlers.EffectsHandler import EffectsHandler
from handlers.EffectHandler import EffectHandler

from Application import Application

def make_app(app):
    return tornado.web.Application([
        (r"/effects", EffectsHandler, dict(app=app)),
        (r"/effect/([^/]+)", EffectHandler, dict(app=app)),

        (r"/banks", BanksHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect/(?P<effect>[0-9]+)/param/(?P<param>[0-9]+)", BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)/effect/(?P<effect>[0-9]+)", BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)/patch/(?P<patch>[0-9]+)", BankHandler, dict(app=app)),
        (r"/bank/(?P<bank>[0-9]+)", BankHandler, dict(app=app)),
    ])

if __name__ == "__main__":
    app = make_app(Application())
    print("PedalController API works!")
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()