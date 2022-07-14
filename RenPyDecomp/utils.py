# -*- coding: utf-8 -*-
"""
@author: Vladya
"""

import os
import sys
import logging
import subprocess
from os import path


def _get_module_logger(name, _format=None, debug_level=False):

    if _format is None:
        _format = "%(levelname)s:%(name)s\n%(message)s\n"

    _formatter = logging.Formatter(_format)

    logger = logging.getLogger(name)

    _handler = logging.StreamHandler()
    _handler.setFormatter(_formatter)

    logger.addHandler(_handler)

    level = logging.INFO
    if debug_level:
        level = logging.DEBUG

    logger.setLevel(level)

    return logger


def create_directories_for(name):
    name = path.abspath(name)
    directory = path.dirname(name)
    if not path.isdir(directory):
        os.makedirs(directory)


def assert_run_in_python3():
    if sys.version_info.major != 3:
        raise RuntimeError("Current Python isn't 3.")


def check_and_return_python2_exe(executable, _logger=None):

    if not isinstance(executable, str):
        raise TypeError("Path should be a str.")

    executable = path.abspath(executable)
    if not path.isfile(executable):
        raise ValueError("\"{0}\" is not valid path.".format(executable))

    with subprocess.Popen(
        (
            executable,
            "-c",
            (
                "import sys\n"
                "print(\"python{0}\".format(sys.version_info.major))"
            )
        ),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ) as process:
        stdout_data, stderr_data = process.communicate(timeout=30.)

    if stderr_data:
        raise OSError(stderr_data)

    stdout_data = stdout_data.decode("utf_8", "ignore")
    stdout_data = stdout_data.lower().strip()

    if "python" not in stdout_data:
        raise RuntimeError("File is not Python executable.")

    if stdout_data != "python2":
        raise RuntimeError("File is not Python 2 executable.")

    if _logger:
        _logger.info("Python 2 executable \"%s\".", executable)

    return executable
