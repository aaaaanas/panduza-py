import time
from loguru import logger
from ..meta_driver import MetaDriver

class DriverPlatform(MetaDriver):
    """
    """

    ###########################################################################
    ###########################################################################

    def _PZADRV_config(self):
        return {
            "info": {
                "type": "platform",
                "version": "0.0"
            },
            "compatible": [
                "py.platform"
            ]
        }

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_ini(self, tree):

        # self.log.debug(f"{tree}")
        # self.log.debug(f">>>>>>>>>{len(self._platform.interfaces)}")

        
        # Update the number of managed interface
        self.number_of_interfaces = len(self._platform.interfaces)
        self._update_attribute("info", "interfaces", self.number_of_interfaces)

        # Tell the platform that the init state end sucessfuly
        self._pzadrv_ini_success()


    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_run(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_loop_err(self):
        """
        """
        pass

    ###########################################################################
    ###########################################################################

    def _PZADRV_cmds_set(self, payload):
        """From MetaDriver
        """
        pass

