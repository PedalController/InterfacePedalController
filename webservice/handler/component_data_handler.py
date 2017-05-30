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

from webservice.handler.abstract_request_handler import AbstractRequestHandler

from application.controller.component_data_controller import ComponentDataController


class ComponentDataHandler(AbstractRequestHandler):
    controller = None

    def initialize(self, app, webservice):
        super(ComponentDataHandler, self).initialize(app, webservice)
        self.controller = app.controller(ComponentDataController)

    def get(self, key):
        self.send(200, self.controller[key])

    def post(self, key):
        self.controller[key] = self.request_data

        self.success()

    def delete(self, key):
        del self.controller[key]

        self.success()
