from dataclasses import dataclass
from ..core import Interface, Attribute, RwField

@dataclass
class Dio(Interface):
    """Interface to manage DIO
    """

    interface:Interface = None

    def __post_init__(self):

        if self.alias:
            pass
        elif self.interface:
            # Build from an other interface
            self.alias = self.interface.alias
            self.addr = self.interface.addr
            self.port = self.interface.port
            self.topic = self.interface.topic
            self.client = self.interface.client

        super().__post_init__()

        # === DIRECTION ===
        self.add_attribute(
            Attribute( name_ = "direction" )
        ).add_field(
            RwField( name_ = "value")
        ).add_field(
            RwField( name_ = "pull")
        ).add_field(
            RwField( name_ = "polling_cycle")
        )

        # === STATE ===
        self.add_attribute(
            Attribute( name_ = "state" )
        ).add_field(
            RwField( name_ = "active" )
        ).add_field(
            RwField( name_ = "active_low" )
        ).add_field(
            RwField( name_ = "polling_cycle" )
        )

        if self.ensure:
            self.ensure_init()
