# Copyright 2017 SrMouraSilva
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import sys
EXIT_STATUS = 0

LOOP = None


def test_thread():
    discover_tests()
    stop()


def discover_tests():
    import os
    import sys

    import glob
    import unittest

    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    path = os.path.dirname(__file__)
    test_files = glob.glob(path + '/handler/*_test.py')
    module_strings = [test_file[0:len(test_file) - 3].replace('/', '.') for test_file in test_files]

    results = []
    for test_file in module_strings:
        tests = unittest.defaultTestLoader.loadTestsFromName(test_file)
        suite = unittest.TestSuite(tests)
        results.append(unittest.TextTestRunner().run(suite))

    global EXIT_STATUS
    for result in results:
        if result.errors or result.failures:
            EXIT_STATUS = -1

def stop():
    LOOP.add_callback(LOOP.stop)


if __name__ == "__main__":
    import tornado

    from application.application import Application
    from application.controller.plugins_controller import PluginsController
    from webservice.webservice import WebService


    application = Application(path_data="wstest/data/", address='localhost', test=True)
    application.register(WebService(application, 3000))

    application.start()
    controller = application.controller(PluginsController)

    for plugin_uri in controller.lv2_builder.plugins:
        print(plugin_uri)

    from _thread import start_new_thread
    start_new_thread(test_thread, ())
    LOOP = tornado.ioloop.IOLoop.current()
    tornado.ioloop.IOLoop.current().start()

    application.stop()

    sys.exit(EXIT_STATUS)
