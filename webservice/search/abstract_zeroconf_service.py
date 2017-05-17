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

import logging

from abc import ABCMeta, abstractmethod
from subprocess import check_output


class AbstractZeroconfService(object, metaclass=ABCMeta):

    def __init__(self, name, port):
        self.port = port
        self.name = name

    @property
    def type(self):
        return '_pedalpi._tcp'

    @property
    def ips(self):
        output = check_output(['hostname', '--all-ip-addresses']).decode("utf-8")
        output_no_linebreak = output[0:-2]
        return output_no_linebreak.split(' ')

    @classmethod
    @abstractmethod
    def has_support(cls):
        """
        :return bool: Does the device support this Zeroconf implementation?
                      It can usually be checked by verifying that the required libraries
                      are installed.
        """
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def close(self):
        pass

    def _log(self, message, *args, error=False, **kwargs):
        if error:
            logging.error(msg=message.format(*args, **kwargs))
        else:
            logging.info(msg=message.format(*args, **kwargs))