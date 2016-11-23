import sys
import tornado

sys.path.append('webservice')

from application.application import Application
from webservice.WebService import WebService

address = 'localhost'
port = 3000

application = Application(data_patch="application/test/data/", address=address, test=True)
application.register(WebService(application, port))

application.start()

tornado.ioloop.IOLoop.current().start()
