import abc
import time
import asyncio
import inspect
from collections import ChainMap
from core.platform_driver import PlatformDriver

class MetaDriverServomotor(PlatformDriver):
    """Abstract Driver with helper class to manage Servomotor interface
    """

    # =============================================================================
    # PLATFORM DRIVERS FUNCTIONS

    def _PZA_DRV_config(self):
        """Driver base configuration
        """
        base = {
            "info": {
                "type": "servomotor",
                "version": "0.0"
            }
        }
        return ChainMap(base, self._PZA_DRV_SERVOMOTOR_config())

    # ---

    async def _PZA_DRV_loop_init(self, loop, tree):
        """From PlatformDriver
        """
        # Set handers
        self.__cmd_handlers = {
            "position" : self.__handle_cmds_set_position
        }

        # 
        self.__polling_cycle = 3

        # first update
        await self.__update_attribute_initial()

        # Start polling task
        self.__task_polling = loop.create_task(self.__polling_task())
    
        # Init Success
        await super()._PZA_DRV_loop_init(loop, tree)

    # ---

    async def _PZA_DRV_cmds_set(self, loop, payload):
        cmds = self.payload_to_dict(payload)
        self.log.debug(f"cmds as json : {cmds}")
        for att in self.__cmd_handlers:
            if att in cmds:
                await self.__cmd_handlers[att](cmds[att])

    # =============================================================================
    # TO OVERRIDE IN DRIVER

    # ---

    @abc.abstractmethod
    def _PZA_DRV_SERVOMOTOR_config(self):
        """Driver base configuration
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # ---

    async def _PZA_DRV_SERVOMOTOR_get_position_value(self):
        """
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")
    
    
    async def _PZA_DRV_SERVOMOTOR_set_position_value(self,value):
        """
        """
        file_name = inspect.stack()[0][1]
        function_name = inspect.stack()[0][3]
        raise NotImplementedError(f"Function not implemented ! '{function_name}' => %{file_name}%")

    # =============================================================================
    # PRIVATE FUNCTIONS

    # ---

    async def __polling_task(self):
        """Task to poll the value
        """
        while self.alive:
            await asyncio.sleep(self.__polling_cycle)
            #await self._update_attribute("position", "value", await self._PZA_DRV_SERVOMOTOR_get_position_value(), 'always')
            await self._update_attribute("position", "value", await self._PZA_DRV_SERVOMOTOR_get_position_value(), 'on-change')
            # await self._update_attributes_from_dict({
            #     "position": {
            #         "value": await self._PZA_DRV_SERVOMOTOR_get_position_value()
            #     }
            # })

    # ---

    async def __update_attribute_initial(self):
        """Function to perform the initial init
        """
        await self.__att_position_full_update()

    # ---

    async def __handle_cmds_set_position(self, cmd_att):
        """
        """
        update_obj = {}
        await self._prepare_update(update_obj, 
                            "position", cmd_att,
                            "value", [int],
                            self._PZA_DRV_SERVOMOTOR_set_position_value,
                            self._PZA_DRV_SERVOMOTOR_get_position_value)
        await self._prepare_update(update_obj, 
                            "position", cmd_att,
                            "polling_cycle", [float, int], 
                            self.__set_poll_cycle, 
                            self.__get_poll_cycle)
        await self._update_attributes_from_dict(update_obj)

    # ---

    async def __set_poll_cycle(self, v):
        self.__polling_cycle = v

    # ---

    async def __get_poll_cycle(self):
        return self.__polling_cycle

    # ---

    async def __att_position_full_update(self):
        """
        """
        await self._update_attributes_from_dict({
            "position": {
                "value": await self._PZA_DRV_SERVOMOTOR_get_position_value(),
                "polling_cycle": await self.__get_poll_cycle()
            }
        })

    # ---

