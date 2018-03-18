# Copyright 2018 SrMouraSilva
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

import datetime

import jwt
from application.controller.component_data_controller import ComponentDataController
from webservice.database.database import UsersDatabase
from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.properties import WSProperties
from webservice.util.auth import JWTAuth
from webservice.util.auth import RequiresAuthMixing
from webservice.util.handler_utils import exception


class AuthHandler(RequiresAuthMixing, AbstractRequestHandler):
    """
    Based on https://github.com/paulorodriguesxv/tornado-json-web-token-jwt
    """
    database = None

    def initialize(self, app, webservice):
        super(AuthHandler, self).initialize(app, webservice)
        self.database = UsersDatabase(app.controller(ComponentDataController))

    @exception(Exception, 500)
    def post(self):
        """
        :return The generated token
        """
        username = self.request_data["username"]
        password = self.request_data["password"]

        if not self.database.auth(username, password) \
        and not WSProperties.auth_client_component(username, password):
            self.unauthorized("Invalid username or password")
            return

        token = jwt.encode(
            {'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)},
            JWTAuth.SECRET_KEY,
            algorithm='HS256'
        )

        self.write({'token': token.decode('ascii')})
