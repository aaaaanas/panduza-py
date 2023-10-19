from dataclasses import dataclass
from ..core import Interface, Attribute, RoField, RwField

@dataclass
class Platform(Interface):
    """Interface to manage power supplies
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

        # === CONFIG ===
        self.add_attribute(
            Attribute( name_ = "dtree" )
        ).add_field(
            RwField( name_ = "name" )
        ).add_field(
            RwField( name_ = "saved" )
        ).add_field(
            RwField( name_ = "list" )
        ).add_field(
            RwField( name_ = "content" )
        )

        # === CONFIG ===
        self.add_attribute(
            Attribute( name_ = "devices" )
        ).add_field(
            RwField( name_ = "hunting" )
        ).add_field(
            RwField( name_ = "max" )
        ).add_field(
            RwField( name_ = "hunted" )
        ).add_field(
            RwField( name_ = "store" )
        )

        if self.ensure:
            self.ensure_init()



