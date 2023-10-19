from panduza import Client, Platform

from robotlibcore import keyword
from robot.libraries.BuiltIn import BuiltIn

class KeywordsPlatform(object):

    # ---

    @keyword
    def panduza_platform_load_dtree(self, platform_alias, dtree):
        """
        """
        
        if dtree == '':
            dtree = {}

        p = Platform(alias=platform_alias)
        p.dtree.content.set(dtree)
        
    # ---





