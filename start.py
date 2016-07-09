import tornado.ioloop
import tornado.web

from load_module import load_module

load_module('application')
#load_module('webservice')


from application.Application import Application
from WebService import WebService

application = Application(True, dataPatch="application/data/")
webService = WebService(application)
#physical = Physical(application)
   
app = webService.prepare()
app.listen(3000)

print("PedalController API REST      localhost:3000")
print("PedalController API WebSocket localhost:3000/ws")

tornado.ioloop.IOLoop.current().start()
