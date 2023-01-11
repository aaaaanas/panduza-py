import io
from collections import ChainMap
from panduza_platform.meta_drivers.psu import MetaDriverPsu
from panduza_platform.connectors.serial_tty import ConnectorSerialTty

from panduza_platform.connectors.udev_tty import HuntUsbDevs

IPS4303S_USBID_VENDOR="0403" # /!\ This is the VendorID and ProductID of the FT232 chip. Not a custome one!
IPS4303S_USBID_MODEL="6001"
IPS4303S_SERIAL_BAUDRATE=9600 # User manual indicates bullshit
IPS4303S_TTY_BASE="/dev/ttyUSB"

STATE_VALUE_ENUM = { "on": True, "off": False }
VOLTS_BOUNDS     = { "min": 0, "max": 30 }
AMPS_BOUNDS      = { "min": 0, "max":  5 }


class DriverIPS4303S(MetaDriverPsu):
    """Driver for the device IPS4303S from RS Pro.

    At this time only the channel 1 is supported.
    Also note that the ProductID and VendorID returned by the PSU
    are the ones for a basic FT232RL chip.
    """
    
    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        # Extend the common psu config
        return ChainMap(super()._PZADRV_config(), {
            "name": "Py_Psu_IPS4303S",
            "description": "Power Supply IPS4303S",
            "compatible": [
                "ips4303s",
                "rspro.ips4303s",
                "psu.rspro.ips4303s",
                "py.psu.rspro.ips4303s"
            ]
        })

    def __tgen(serial_short, name_suffix):
        return {
            "name": "IPS4303S:" + name_suffix,
            "driver": "py.psu.rspro.ips4303s",
            "settings": {
                "serial_short": serial_short
            }
        }

    def _PZADRV_tree_template(self):
        return DriverIPS4303S.__tgen("USB: Short Serial ID", "template")

    def _PZADRV_hunt_instances(self):
        instances = []
        usb_pieces = HuntUsbDevs(vendor=IPS4303S_USBID_VENDOR, model=IPS4303S_USBID_MODEL, subsystem="tty")
        for p in usb_pieces:
            iss = p["ID_SERIAL_SHORT"]
            instances.append(DriverIPS4303S.__tgen(iss, iss))
        return instances

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_ini(self, tree):

        # Get settings from tree and append constant settings for this device
        settings = dict() if "settings" not in tree else tree["settings"]
        settings["vendor"] = IPS4303S_USBID_VENDOR
        settings["model"] = IPS4303S_USBID_MODEL
        settings["baudrate"] = IPS4303S_SERIAL_BAUDRATE
        settings["base_devname"] = IPS4303S_TTY_BASE
        
        # Get the connector
        self.serp = ConnectorSerialTty.Get(**settings)

        # TODO : Bad pratice "get_internal_driver" but used to speed up
        # https://stackoverflow.com/questions/10222788/line-buffered-serial-input
        self.io  = io.TextIOWrapper(
            self.serp.get_internal_driver(),
            encoding       = "ascii",
            newline        = None,
            line_buffering = False
        )
        self.io._CHUNK_SIZE= 1
        

        # TODO :Bad pratice with loopback variable instead of reading the value back
        self.state = "off"
        self.volts = 0
        self.amps = 0

        # Constants Fields settings
        self._pzadrv_psu_update_volts_min_max(VOLTS_BOUNDS["min"], VOLTS_BOUNDS["max"])
        self._pzadrv_psu_update_amps_min_max(AMPS_BOUNDS["min"], AMPS_BOUNDS["max"])

        # Misc
        self._pzadrv_psu_update_misc("model", "IPS4303S (RS Pro)")

        # Call meta class PSU ini
        super()._PZADRV_loop_ini(tree)


    ###########################################################################
    ###########################################################################

    def __write(self, *cmds):
        # Append new line terminator to all commands
        txt = "".join( map(lambda x: f"{x}\r\n", cmds) )

        self.log.debug(f"TX: {txt!r}")
        self.io.write(txt)
        self.io.flush()

    ###########################################################################
    ###########################################################################

    def _PZADRV_PSU_read_state_value(self):
        return self.state

    def _PZADRV_PSU_write_state_value(self, v):
        self.state = v
        cmd = STATE_VALUE_ENUM[v]
        self.__write(f"OUT{int(cmd)}")

    def _PZADRV_PSU_read_volts_value(self):
        return self.volts

    def _PZADRV_PSU_write_volts_value(self, v):
        self.volts = v
        self.__write(f"VSET1:{v:.3f}")

    def _PZADRV_PSU_read_amps_value(self):
        return self.amps
    
    def _PZADRV_PSU_write_amps_value(self, v):
        self.amps = v
        self.__write(f"ISET1:{v:.3f}")

    ###########################################################################
    ###########################################################################

    def PZADRV_hunt():
        """
        """
        return None

