# -*- coding: utf-8 -*-
"""
@author: Vladya
"""

import configparser
from os import path
from . import utils

__author__ = "Vladya"
__version__ = "1.0.3"

utils.assert_run_in_python3()

LOGGER = utils._get_module_logger("RenPyDecomp")
LOGGER.info("Module is started. Version %s.", __version__)

CONFIG_FILE = path.abspath(path.join(path.expanduser('~'), "RenPyDecomp.ini"))
DEFAULT_CONFIG = {
    "DEFAULT": {
        "Python 2 executable": "python2"
    }
}

config = configparser.ConfigParser()
config.read_dict(DEFAULT_CONFIG)
if path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, 'r', encoding="utf_8") as _config_file:
        config.read_file(_config_file)

utils.create_directories_for(CONFIG_FILE)
with open(CONFIG_FILE, 'w', encoding="utf_8") as _config_file:
    config.write(_config_file)

PY2EXE = utils.check_and_return_python2_exe(
    config.get("DEFAULT", "Python 2 executable"),
    LOGGER
)
