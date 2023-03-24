import sys
import pathlib
import argparse
from panduza_platform import MetaPlatform

import logging

# Initialize log file
pathlib.Path("/etc/panduza/log").mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename="/etc/panduza/log/py.log", 
					format='%(asctime)s | %(name)s | %(message)s', 
					filemode='w') 


parser = argparse.ArgumentParser()
parser.add_argument('tree', nargs='?', default=None)
args = parser.parse_args()


srv = MetaPlatform()
srv.force_log = True
srv.register_driver_plugin_discovery()
if args.tree != None:
    srv.load_tree_overide(args.tree)
srv.run()
logging.warning("Platform stopped !")
