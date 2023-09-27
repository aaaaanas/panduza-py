from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Servo(Interface):
    """Interface to manage Servomotor
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

        # === POSITION ===
        self.add_attribute(
            Attribute( name = "position" )
        ).add_field(
            RwField( name = "value")
        )

        if self.ensure:
            self.ensure_init()
