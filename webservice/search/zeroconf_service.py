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

import time

import select
import socket

from webservice.search.abstract_zeroconf_service import AbstractZeroconfService

try:
    from zeroconf import ServiceInfo, Zeroconf
    support = True
except ImportError:
    from unittest.mock import MagicMock
    zeroconf = MagicMock()
    support = False


class ZeroconfService(AbstractZeroconfService):
    """
    :class:`ZeroconfService` uses `python zeroconf`_

    .. _python zeroconf: https://pypi.org/project/zeroconf/

    Install::

    .. code-block:: bash

        pip install zeroconf
    """

    def __init__(self, port):
        super(ZeroconfService, self).__init__(port)
        self._zeroconf = None
        self._info = None

    @classmethod
    def has_support(cls):
        return support

    def start(self):
        self._zeroconf = Zeroconf()
        self._info = ServiceInfo(
            self.type + '.local.',
            self.name + '.' + self.type + '.local.',
            socket.inet_aton(self.ip),
            self.port,
            0,
            0,
            {}
        )

        self._zeroconf.register_service(self._info)
        self._log('Zeroconf', self.__class__.__name__, '- Registered service:', 'name=' + self.name, 'regtype=' + self.type, 'domain=local.')

    def close(self):
        self._zeroconf.unregister_service(self._info)

    def _log(self, *args, **kwargs):
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']', *args, **kwargs)

if __name__ == '__main__':
    from signal import pause

    service = ZeroconfService(3000)
    service = zeroconf.start()
    print('I am waiting')

    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        print('closing')
        service.close()
