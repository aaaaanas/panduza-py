
from core.platform_device import PlatformDevice

USBID_VENDOR="0416"
USBID_MODEL="5011"
TTY_BASE="/dev/ttyACM0"

class DeviceTenma722710(PlatformDevice):
    """Power Supply From Tenma
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "722710",
            "manufacturer": "Tenma"
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        interfaces = []

        fake_mode = self._initial_settings.get("fake_mode", False)


        if fake_mode:
            pass
        else:
            interfaces.append({
                "name": f"bpc",
                "driver": "tenma.722710.bpc",
                "settings": {
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": 9600
                }
            })
            '''
            interfaces.append({
                "name": f"am",
                "driver": "tenma.722710.ammeter",
                "settings": {
                    "usb_vendor": USBID_VENDOR,
                    "usb_model": USBID_MODEL,
                    "serial_baudrate": 9600
                }
            })
	    '''
        return interfaces

