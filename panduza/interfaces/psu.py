import json
import threading
from ..core import Interface
from ..core import Attribute_JSON
from ..core import Interface, Attribute, EnsureError

# -----------------------------------------------------------------------------

class PsuNumericAttribute(Attribute):
    """! This attribute manage volts and amps attributes because they are very similar
    """

    def __init__(self, b_topic, pza_client, name):
        """! Constructor
        """
        super().__init__(client=pza_client, base_topic=b_topic, name=name)
        self.__trigger = threading.Event()
        self.__value = None
        self.__min = None
        self.__max = None
        self.__scale = None

    def __post_init__(self):
        """! Post Constructor
        """
        super().__post_init__()
        self.client.subscribe(self._topic_atts_get, callback=self.__update)

    def __update(self, topic, payload):
        """! Callback triggered on reception of an mqtt messsage for this attribute
        """
        # Fill internal data from payload
        if payload is None:
            self.__value = None
            self.__min = None
            self.__max = None
            self.__scale = None
        else:
            data = json.loads(payload.decode("utf-8"))
            self.__value = data[self.name]
            self._log.debug(f"NEW value : {self.__value}")
            if "min" in data:
                self.__min = data["min"]
                self._log.debug(f"NEW min : {self.__min}")
            if "max" in data:
                self.__max = data["max"]
                self._log.debug(f"NEW max : {self.__max}")
            if "scale" in data:
                self.__scale = data["scale"]
                self._log.debug(f"NEW scale : {self.__scale}")
            self.__trigger.set()

    def get(self):
        """! getter for the value property
        """
        return self.__value

    def get_min(self):
        """! getter for the min property
        """
        return self.__min

    def get_max(self):
        """! getter for the max property
        """
        return self.__max

    def get_scale(self):
        """! getter for the scale property
        """
        return self.__scale

    def set(self, v, ensure=False):
        """! getter for the scale property
        """
        # Init
        retry=3
        if ensure:
            self.trigger_arm()

        # Send the message
        self.client.publish(self._topic_cmds_set, self.payload_factory(v))

        if ensure:
            # It is possible that you catch some initialization message with the previous dir value
            # To manage this case, just wait for the correct value
            while self.__value != v or not retry:
                self.trigger_wait(timeout=3)
                if self.__value != v:
                    self.trigger_arm()
                    retry-=1

            if self.__value != v:
                raise RuntimeError(f"Attribute {self.name} for {self.base_topic}: cannot set to '{v}', got '{self.__value}'")

# -----------------------------------------------------------------------------

class Psu(Interface):
    """! Interface to manage power supplies
    """

    def __init__(self, alias=None, url=None, port=None, b_topic=None, pza_client=None):
        """! Constructor
        """
        super().__init__(alias, url, port, b_topic, pza_client)

    def _post_initialization(self):
        """! Declare attributes here
        """

        self.state = Attribute_JSON(
            client          = self.client,
            base_topic      = self.base_topic,
            name            = "state",

            payload_factory = lambda v: json.dumps({"state": bool(v)}).encode("utf-8"),
            payload_parser  = lambda v: bool(json.loads(v.decode("utf-8"))["state"])
        )

        self.volts = PsuNumericAttribute(
            pza_client      = self.client,
            b_topic         = self.base_topic,
            name            = "volts"
        )

        self.amps = PsuNumericAttribute(
            pza_client      = self.client,
            b_topic         = self.base_topic,
            name            = "amps"
        )
