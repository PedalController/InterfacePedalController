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
import select

from webservice.search.abstract_zeroconf_service import AbstractZeroconfService

try:
    import pybonjour
    support = True
except ImportError:
    from unittest.mock import MagicMock
    pybonjour = MagicMock()
    support = False


class PybonjourService(AbstractZeroconfService):
    """
    :class:`PybonjourService` uses pybonjour-python for python 3

    Install::

    .. code-block:: bash

        sudo apt-get install libavahi-compat-libdnssd1
        pip install git+https://github.com/depl0y/pybonjour-python3
    """

    def __init__(self, name, port):
        super(PybonjourService, self).__init__(name, port)

        self.registered = False
        self.register = None

    @classmethod
    def has_support(cls):
        return support

    def register_callback(self, sdRef, flags, error_code, name, regtype, domain):
        if error_code == pybonjour.kDNSServiceErr_NoError:
            self.registered = True
            self._log('Zeroconf {} - Registered service: name={}, regtype={}, domain={}', self.__class__.__name__, name, regtype, domain)
        else:
            self._log('Zeroconf is not workings', error=True)

    def start(self):
        self.registered = False
        register = pybonjour.DNSServiceRegister(
            name=self.name,
            regtype=self.type,
            port=self.port,
            callBack=self.register_callback
        )

        while not self.registered:
            readable, writable, exceptional = select.select([register], [], [])
            if register in readable:
                pybonjour.DNSServiceProcessResult(register)

        self.register = register

    def close(self):
        self.register.close()


if __name__ == '__main__':
    from signal import pause

    service = PybonjourService(3000)
    service.start()
    print('I am waiting')

    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        print('closing')
        service.close()
