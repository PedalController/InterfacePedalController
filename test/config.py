if __name__ == "__main__":
    import sys
    import tornado

    sys.path.append('webservice')

    from application.application import Application
    from webservice.webservice import WebService

    address = 'localhost'
    port = 3000

    application = Application(path_data="Application/test/data/", address=address, test=True)
    application.register(WebService(application, port))

    application.start()

    tornado.ioloop.IOLoop.current().start()
