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
