from robotlibcore import DynamicCore, keyword

from robot.libraries.BuiltIn import BuiltIn

from ..core.core import Core
from .psu import KeywordsPsu
from ..interfaces.generator import GenerateAllInterfacesFromAliases

class Keywords(DynamicCore):

    def __init__(self):
        libraries = [KeywordsPsu()]
        DynamicCore.__init__(self, libraries)

    @keyword
    def load_pza_interfaces_from_aliases(self, connections):
        """
        """
        interfaces = GenerateAllInterfacesFromAliases(connections=connections)
        # print(interfaces)

        BuiltIn().set_suite_variable("${__pza__}", interfaces)
        # BuiltIn().set_test_variable("${pza}", aliases)

