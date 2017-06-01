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

    def __init__(self, name, port):
        super(ZeroconfService, self).__init__(name, port)

        self._zeroconf = None
        self._infos = []

    @classmethod
    def has_support(cls):
        return support

    def start(self):
        self._zeroconf = Zeroconf()
        for index, ip in enumerate(self.ips):
            info = self._gerenate_service_info(index, ip)
            self._infos.append(info)

            self._zeroconf.register_service(info)
            self._log('Zeroconf {} - Registered service: name={}, regtype={}, domain={}', self.__class__.__name__,
                      self.name, self.type, 'local.')
            self._log('         Network: {}', ip)

    def _gerenate_service_info(self, index, ip):
        name = '{}-{}.{}.local.'.format(self.name.lower(), index, self.type, '.local.')

        return ServiceInfo(
            self.type + '.local.',
            name,
            socket.inet_aton(ip),
            self.port,
            0,
            0,
            {}
        )

    def close(self):
        for info in self._infos:
            self._zeroconf.unregister_service(info)

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
