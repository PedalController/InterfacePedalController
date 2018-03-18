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

from pluginsmanager.model.param import ParamError
from tornado import gen
from webservice.handler.abstract_request_handler import AbstractRequestHandler
from webservice.util.auth import RequiresAuthMixing
from webservice.util.handler_utils import integer, exception


class LibsListHandler(RequiresAuthMixing, AbstractRequestHandler):

    def prepare(self):
        #self.auth()
        pass

    @gen.coroutine
    def get(self):
        import pip
        distributions = pip.get_installed_distributions()

        return self.write({'libs': {lib.project_name: lib.version for lib in distributions}})
