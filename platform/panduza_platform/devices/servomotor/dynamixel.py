
from core.platform_device import PlatformDevice


TTY_BASE="/dev/ttyUSB0"

class DeviceDynamixel(PlatformDevice):
    """Servomotor
    """

    def _PZA_DEV_config(self):
        """
        """
        return {
            "model": "ax12-a",
            "manufacturer": "Dynamixel"
        }

    def _PZA_DEV_interfaces(self):
        """
        """
        interfaces = []

        serial_port_name = self._initial_settings.get("serial_port_name",TTY_BASE)
        serial_baudrate = self._initial_settings.get("serial_baudrate",115200)
        number_of_servo = self._initial_settings.get("number_of_servo")
        
        for servo_id in range (0,number_of_servo):
            interfaces.append({
            "name": f"servo_ID_{servo_id}",
            "driver": "panduza.servomotor",
            "settings": {
                "serial_port_name": serial_port_name,
                "serial_baudrate": serial_baudrate,
                "number_of_servo" : number_of_servo,
                "servo_id" : servo_id
            }
        })

        return interfaces

