import logging
import asyncio
import serial_asyncio
import serial

from .uart_ftdi_base import ConnectorUartFtdiBase
from log.driver import driver_logger

class ConnectorUartFtdiSerial(ConnectorUartFtdiBase):
    """
    """

    # Hold instances mutex
    __MUTEX = asyncio.Lock()

    # Contains instances
    __INSTANCES = {}

    # Local logs
    log = driver_logger("ConnectorUartFtdiSerial")

    ###########################################################################
    ###########################################################################

    @staticmethod
    async def Get(**kwargs):
        """Singleton main getter

        
        :Keyword Arguments:
        * *serial_port_name* (``str``) --
            serial port name
    
        * *serial_baudrate* (``int``) --
            serial baudrate

        """
        # Log
        ConnectorUartFtdiSerial.log.debug(f"Get connector for {kwargs}")

        async with ConnectorUartFtdiSerial.__MUTEX:

            # Log
            ConnectorUartFtdiSerial.log.debug(f"Lock acquired !")


            # Get the serial port name
            serial_port_name = None
            if "serial_port_name" in kwargs:
                serial_port_name = kwargs["serial_port_name"]
        
            else:
                raise Exception("no way to identify the serial port")

            # Create the new connector
            if not (serial_port_name in ConnectorUartFtdiSerial.__INSTANCES):
                ConnectorUartFtdiSerial.__INSTANCES[serial_port_name] = None
                try:
                    new_instance = ConnectorUartFtdiSerial(**kwargs)
                    await new_instance.connect()
                    
                    ConnectorUartFtdiSerial.__INSTANCES[serial_port_name] = new_instance
                    ConnectorUartFtdiSerial.log.info("connector created")
                except Exception as e:
                    ConnectorUartFtdiSerial.__INSTANCES.pop(serial_port_name)
                    raise Exception('Error during initialization').with_traceback(e.__traceback__)

            # Return the previously created
            return ConnectorUartFtdiSerial.__INSTANCES[serial_port_name]

    ###########################################################################
    ###########################################################################

    def __init__(self,**kwargs):
        """Constructor
        """
        # Init local mutex
        self._mutex = asyncio.Lock()
        
        key = kwargs["serial_port_name"]
        
        self.loop = asyncio.get_event_loop()
        

        if not (key in ConnectorUartFtdiSerial.__INSTANCES):
            raise Exception("You need to pass through Get method to create an instance")
        else:
            self.log = logging.getLogger(key)
            self.log.info(f"attached to the UART Serial Connector")
            
            # Configuration for UART communication

            self.port_name = kwargs.get("serial_port_name", "/dev/ttyUSB0")
            self.baudrate = kwargs.get("serial_baudrate", 115200)


    # ---

    async def connect(self):
        """Start the serial connection
        """
        
        self.reader,_ = await serial_asyncio.open_serial_connection(loop = self.loop,url=self.port_name, baudrate=self.baudrate)

    ###########################################################################
    ###########################################################################


    async def read_uart(self):
        async with self._mutex:
            try:
                
                #data = await self.reader.readline()
                await asyncio.sleep(1)
                data = await asyncio.wait_for(self.reader.readuntil(b'\n'), timeout=2.0) 
                decoded_data = data.decode('utf-8').strip()
            
                return decoded_data
            
            except asyncio.TimeoutError as e: 
                raise Exception('Error during reading uart').with_traceback(e.__traceback__)

            
                
    ###########################################################################
    ###########################################################################

    ######## tester asyncio.wait_for(write message) ou tester si on recoit le meme message plusieurs fois -> ne pas prendre en compte

    async def write_uart(self,message):
        async with self._mutex:
            _, self.writer = await serial_asyncio.open_serial_connection(loop = self.loop,url=self.port_name, baudrate=self.baudrate)
            await asyncio.sleep(1)
            
            self.writer.write(message.encode())
            await self.writer.drain()
            self.writer.close() 







    ###########################################################################
    # SERIAL SYNCHRONOUS
    ###########################################################################



    # async def connect(self):
    #         """Start the serial connection
    #         """

    #         self.uart = serial.Serial(self.port_name, baudrate=self.baudrate, timeout=1)




    # async def read_uart(self):
    #     async with self._mutex:
    
    #         data = self.uart.readline()[:-2]

    #         decoded_data = data.decode('utf-8')
    #         if decoded_data :
    #             return decoded_data
    


    # async def write_uart(self,message):
    #     async with self._mutex:
    #         print(message.encode())
           
    #         self.uart.write(message.encode())