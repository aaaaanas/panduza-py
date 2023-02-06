from .driver_platform import DriverPlatform
from .driver_modbus_client import DriverModbusClient
from .driver_serial import DriverSerial
from .ftdi-spi import FtdiSpi

PZA_DRIVERS_LIST=[
    DriverPlatform,
    DriverModbusClient,
    DriverSerial,
    FtdiSpi
]
