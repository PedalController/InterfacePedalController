from zeroconf import ServiceBrowser, Zeroconf
import socket

class MyListener(object):

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print()
        print("Service %s added, service info: %s" % (name, info))

        if info:
            print("  Address is %s:%d" % (socket.inet_ntoa(info.address), info.port))
            print("  Weight is %d, Priority is %d" % (info.weight, info.priority))
            print("  Server is", info.server)
            if info.properties:
                print("  Properties are")
                for key, value in info.properties.items():
                    print("    %s: %s" % (key, value))
        else:
            print("  No info")

zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
try:
    input("Press enter to exit...\n\n")
finally:
    zeroconf.close()
