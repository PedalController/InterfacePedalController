""" Example of announcing a service (in this case, a fake HTTP server) """

import socket
from signal import pause


from zeroconf import ServiceInfo, Zeroconf

description = {
    'version': '0.0.1'
}

info = ServiceInfo(
    type_="_http._tcp.local.",
    name="_pedalpi._http._tcp.local.",
    address=socket.inet_aton("127.0.0.1"),
    port=80,
    weight=0,
    priority=0,
    properties=description,
    server="_pedalpi.local."
)

info2 = ServiceInfo("_http._tcp.local.",
                       "Paul's Test Web Site._http._tcp.local.",
                       socket.inet_aton("127.0.0.1"), 80, 0, 0,
                       {'path': '/~paulsm/'}, "ash-2.local.")

info3 = ServiceInfo(
    type_="_http._tcp.local.",
    name="Becvert\'s iPad I._http._tcp.local.",
    address=socket.inet_aton("127.0.0.1"),
    port=80,
    weight=0,
    priority=0,
    properties=description,
    server="pedalpi.local."
)

zeroconf = Zeroconf()
zeroconf.register_service(info)
zeroconf.register_service(info2)
zeroconf.register_service(info3)

print("Registration of a service, press Ctrl-C to exit...")

try:
    pause()
except KeyboardInterrupt:
    pass
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()