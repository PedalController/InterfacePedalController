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

import traceback
import sys


class integer(object):
    """
    Convert the informed args to integer
    """
    def __init__(self, *args):
        self.args = args

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            for arg in self.args:
                kwargs[arg] = int(kwargs[arg])
            f(*args, **kwargs)

        return wrapped


class exception(object):
    """
    Envelopes the method so that if an exception occurs
    as specified in error, a response is sent with the status
    code and defined error message

    :param class error: Class error
    :param int status_code: HTTP status code
    :param string message: error message
    :param bool error_message: Show raised error instead a defined message
    """

    def __init__(self, error, status_code, message=None, error_message=False):
        self.error = error
        self.status_code = status_code
        self.message = message
        self.error_message = error_message

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            this = args[0]

            try:
                f(*args, **kwargs)

            except self.error as e:
                print(traceback.format_exc(), file=sys.stderr, flush=True)

                if self.message is not None:
                    this.send(self.status_code, {"error": self.message})
                elif self.error_message:
                    this.send(self.status_code, {"error": str(e)})
                else:
                    this.send(self.status_code)

        return wrapped
