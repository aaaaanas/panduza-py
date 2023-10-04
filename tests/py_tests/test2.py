import time
from panduza import Bpc

ADDR="localhost"
PORT=1883

# power_channel = Bpc(addr=ADDR, port=PORT, topic="pza/default/Hanmatek_Hm310t/bpc")
# power_channel = Bpc(addr=ADDR, port=PORT, topic="pza/default/Panduza_FakeBps/channel_1")
power_channel = Bpc(addr=ADDR, port=PORT, topic="pza/default/Tenma_722710/bpc")

power_channel.voltage.value.set(0.29)
power_channel.current.value.set(2.5)

power_channel.enable.value.set(True)
time.sleep(5)
power_channel.enable.value.set(False)

