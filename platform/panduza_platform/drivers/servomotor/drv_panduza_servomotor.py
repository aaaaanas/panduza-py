import asyncio

from hamcrest import assert_that, has_key, instance_of
from meta_drivers.servomotor import MetaDriverServomotor
from connectors.uart_ftdi_serial import ConnectorUartFtdiSerial


class DriverServomotor(MetaDriverServomotor):
    """Servomotor driver
    """

    # =============================================================================
    # FROM MetaDriverServomotor

    def _PZA_DRV_SERVOMOTOR_config(self):
        """
        """
        return {
            "name": "panduza.servomotor",
            "description": "SERVOMOTOR"
        }

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """Init function
        Reset fake parameters
        """

        settings = tree.get("settings", {})
        # self.log.info(settings)

        # Checks
        assert_that(settings, has_key("serial_port_name"))
        assert_that(settings, has_key("serial_baudrate"))
        assert_that(settings, has_key("number_of_servo"))
        assert_that(settings, has_key("servo_id"))

        self.number_of_servo = settings["number_of_servo"]
        self.servo_id  = settings["servo_id"]
        
        # Get the gate connector
        self.uart_connector = await ConnectorUartFtdiSerial.Get(**settings)

        # We need to wait for the serial connection
        await asyncio.sleep(2.2)

        self.__fakes = {
            "position": {
                "value": 0
            }
        }

        # Call meta class BPC ini
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_SERVOMOTOR_get_position_value(self):
        
        response = await self.uart_connector.write_read_uart(f"get {self.servo_id}")
        self.__fakes["position"]["value"] = int(response)

        return self.__fakes["position"]["value"]
                
    
    
    async def _PZA_DRV_SERVOMOTOR_set_position_value(self,value):
        
        # print(f"command set {self.servo_id} {value}")
        await self.uart_connector.write_read_uart(f"set {self.servo_id} {value}")
        
        self.__fakes["position"]["value"] = value
            




 
    # async def __round_value(self,value):      
    #     return ((value + 2) // 5) * 5
    
    # async def change_to_even_nuber(self,number):
    #     if number % 2 != 0: 
    #         number += 1     
    #     return number