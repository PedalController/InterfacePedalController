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
try:
    import pybonjour
except ImportError:
    from unittest.mock import MagicMock
    pybonjour = MagicMock()


class PybonjourService(object):
    """
    sudo apt-get install libavahi-compat-libdnssd1
    pip install git+https://github.com/depl0y/pybonjour-python3

    Examples:
    https://gist.github.com/nickcoutsos/7714711
    """

    def __init__(self, port):
        hostname = socket.gethostname().split('.')[0]

        self.name = hostname
        self.type = '_pedalpi._tcp'
        self.port = port

        self.registered = False

    def _log(self, *args, **kwargs):
        print('[' + time.strftime('%Y-%m-%d %H:%M:%S') + ']', *args, **kwargs)

    def register_callback(self, sdRef, flags, error_code, name, regtype, domain):
        if error_code == pybonjour.kDNSServiceErr_NoError:
            self.registered = True
            self._log('Zeroconf - Registered service:', 'name='+name, 'regtype='+regtype, 'domain='+domain)
        else:
            self._log('zeroconf is not workings')

    def start(self):
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

        return register

    def close(self, register):
        register.close()


if __name__ == '__main__':
    from signal import pause

    zeroconf = Zeroconf(3000)
    register = zeroconf.start()
    print('I am wating')

    try:
        pause()
    except KeyboardInterrupt:
        pass
    finally:
        print('closing')
        zeroconf.close(register)
