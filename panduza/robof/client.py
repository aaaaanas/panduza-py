from panduza import Client

from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn

class KeywordsClient(object):

    # ---

    @keyword
    def panduza_scan_all_interfaces(self, addr, port, duration=1):
        """Scan all the interface of the given broker
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_all_interfaces(duration)

    # ---

    @keyword
    def panduza_scan_all_platforms(self, addr, port, duration=1):
        """Scan all the platform interfaces of the given broker
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_all_platform_interfaces(duration)

    # ---

    @keyword
    def panduza_scan_all_devices(self, addr, port, expected_device_nb=1):
        """Scan all the device interfaces of the given broker
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_all_device_interfaces(expected_device_nb)

    # ---

    @keyword
    def panduza_scan_device(self, addr, port, topic, expected_device_nb=1):
        """Scan a device interfaces of the given broker
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_device_interfaces(topic, expected_device_nb)













    # ---

    @keyword
    def panduza_scan_server(self, addr, port):
        """
        """
        c = Client(url=addr, port=port)
        c.connect()
        return c.scan_interfaces()

