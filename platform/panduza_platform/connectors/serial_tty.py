import time
import asyncio
import logging
import serial_asyncio

from .serial_base import SerialBase
from log.driver import driver_logger

from .udev_tty import SerialPortFromUsbSetting

class SerialTty():
    """
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    # Local logs
    log = driver_logger("SerialTty")

    ###########################################################################
    ###########################################################################

    @staticmethod
    async def Get(loop,**kwargs):
        """Singleton main getter

        
        :Keyword Arguments:
        * *serial_port_name* (``str``) --
            serial port name
    
        * *serial_baudrate* (``int``) --
            serial baudrate
    
        * *usb_vendor* (``str``) --
            ID_VENDOR_ID
        * *usb_model* (``str``) --
            ID_MODEL_ID
        """
        # Log
        SerialTty.log.debug(f"Get connector for {kwargs}")

        async with SerialTty.__MUTEX:

            # Log
            SerialTty.log.debug(f"Lock acquired !")


            # Get the serial port name
            serial_port_name = None
            if "serial_port_name" in kwargs:
                serial_port_name = kwargs["serial_port_name"]
            elif "usb_vendor" in kwargs:
                # Get the serial port name using "usb_vendor"
                serial_port_name = SerialPortFromUsbSetting(**kwargs)
                kwargs["serial_port_name"] = serial_port_name
        
            else:
                raise Exception("no way to identify the serial port")

            # Create the new connector
            if not (serial_port_name in SerialTty.__INSTANCES):
                SerialTty.__INSTANCES[serial_port_name] = None
                try:
                    new_instance = SerialTty(loop,**kwargs)
                    await new_instance.connect()
                    
                    SerialTty.__INSTANCES[serial_port_name] = new_instance
                    SerialTty.log.info("connector created")
                except Exception as e:
                    SerialTty.__INSTANCES.pop(serial_port_name)
                    raise Exception('Error during initialization').with_traceback(e.__traceback__)
            else:
                SerialTty.log.info("connector already created, use existing instance")

            # Return the previously created
            return SerialTty.__INSTANCES[serial_port_name]

    ###########################################################################
    ###########################################################################

    def __init__(self, loop,**kwargs):
        """Constructor
        """

        # Init local mutex
        self._mutex = asyncio.Lock()

        # Init time lock
        self._time_lock_s = None
        
        key = kwargs["serial_port_name"]
        
        self.loop = loop
        
        if not (key in SerialTty.__INSTANCES):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = driver_logger(key)
            self.log.info(f"attached to the UART Serial Connector")

            
            # Configuration for UART communication

            self.port_name = kwargs.get("serial_port_name", "/dev/ttyUSB0")
            self.baudrate = kwargs.get("serial_baudrate", 9600)


    # ---

    async def connect(self):
        """Start the serial connection
        """

        self.reader,self.writer = await serial_asyncio.open_serial_connection(loop = self.loop,url=self.port_name, baudrate=self.baudrate)
        



    # =============================================================================
    # OVERRIDE FROM SERIAL_BASE

    async def _write(self, message, time_lock_s=None):
        """write to UART using asynchronous mode
        """
        try:
            # Manage time lock by waiting for the remaining duration
            if self._time_lock_s:
                elapsed = time.time() - self._time_lock_s["t0"]
                if elapsed < self._time_lock_s["duration"]:
                    wait_time = self._time_lock_s["duration"] - elapsed
                    self.log.debug(f"wait lock {wait_time}")
                    await asyncio.sleep(wait_time)
                self._time_lock_s = None
            # Start sending the message
            self.writer.write(message.encode())
            # Wait for the emittion completion
            await self.writer.drain()
            # Set the time lock if requested by the user
            if time_lock_s != None:
                self._time_lock_s = {
                    "duration": time_lock_s,
                    "t0": time.time()
                }
        except Exception as e:
            raise Exception('Error during writing to uart').with_traceback(e.__traceback__)
            
    async def _read(self, n_bytes_to_read):
        try:
            response = await asyncio.wait_for(self.reader.read(n_bytes_to_read), timeout=1)
            return response
        except Exception as e:
            raise Exception('Error during reading from uart').with_traceback(e.__traceback__)
        
        
    
    async def write(self, message, time_lock_s=None):
        async with self._mutex:
            await self._write(message, time_lock_s)

    async def read(self, n_bytes_to_read=10):
        async with self._mutex:
            return await self._read(n_bytes_to_read)
    
    async def write_and_read(self, message, time_lock_s=0, n_bytes_to_read=10):
        async with self._mutex:
            await self._write(message, time_lock_s)
            await asyncio.sleep(time_lock_s)
            return await self._read(n_bytes_to_read)