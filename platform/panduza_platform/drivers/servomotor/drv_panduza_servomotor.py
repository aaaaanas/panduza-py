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
        
        #self.__task_increment = loop.create_task(self.__increment_task())

        # Get the gate connector
        self.uart_connector = await ConnectorUartFtdiSerial.Get(**settings)
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
        
        self.__fakes["position"]["value"] = await self.__round_value(self.__fakes["position"]["value"])

        return self.__fakes["position"]["value"]
                
    
    
    async def _PZA_DRV_SERVOMOTOR_set_position_value(self,value):
        
        value = await self.__round_value(value)
        print(f"command set {self.servo_id} {value}")
        await self.uart_connector.write_read_uart(f"set {self.servo_id} {value}")
        
        self.__fakes["position"]["value"] = value
            
        
    async def __round_value(self,value):      
        return ((value + 2) // 5) * 5
    
    
    # ---

    # async def __increment_task(self):
    #     while True:
    #         await asyncio.sleep(0.2)
    #         self.__fakes["position"]["value"] += 0.001
