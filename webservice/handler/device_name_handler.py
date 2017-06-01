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


from application.controller.component_data_controller import ComponentDataController
from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.properties import WSProperties


class DeviceNameHandler(AbstractRequestHandler):
    data_controller = None

    def initialize(self, app, webservice):
        super(DeviceNameHandler, self).initialize(app, webservice)

        self.data_controller = self.app.controller(ComponentDataController)

    @property
    def data(self):
        return self.data_controller[WSProperties.DATA_KEY]

    @data.setter
    def data(self, new_data):
        self.data_controller[WSProperties.DATA_KEY] = new_data

    @property
    def device_name(self):
        return self.data[WSProperties.DEVICE_NAME]

    @device_name.setter
    def device_name(self, new_name):
        data = self.data
        data[WSProperties.DEVICE_NAME] = new_name
        self.data = data

    def get(self):
        self.send(200, {'name': self.device_name})

    def put(self, new_name):
        self.device_name = new_name
        self.ws.restart_zeroconf(new_name)
        self.send(200)
