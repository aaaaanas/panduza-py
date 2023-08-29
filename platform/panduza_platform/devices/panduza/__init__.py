from .fake_dio_controller   import DevicePanduzaFakeDioController
from .fake_bps_controller   import DevicePanduzaFakeBps
from .fake_relay_controller import DevicePanduzaFakeRelayController
from .machine               import DevicePanduzaMachine

PZA_DEVICES_LIST= [ 
    DevicePanduzaFakeDioController,
    DevicePanduzaFakeBps,
    DevicePanduzaFakeRelayController,
    DevicePanduzaMachine
]

