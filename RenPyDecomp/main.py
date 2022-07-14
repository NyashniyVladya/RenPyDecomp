# -*- coding: utf-8 -*-
"""
@author: Vladya
"""

import os
import argparse
import subprocess
import threading
import shutil
import unrpa
from os import path
from . import (
    PY2EXE,
    LOGGER as parent_logger
)


class Decompiler(threading.Thread):

    __author__ = "Vladya"

    LOGGER = parent_logger.getChild("Decompiler")
    DECOMP_FORMATS = {
        "compiled": (".rpyc", ".rpymc"),
        "archive": (".rpa", ".rpi")
    }

    def __init__(self, input_path):

        super().__init__()
        self.daemon = True

        input_path = path.abspath(input_path)
        if not path.exists(input_path):
            raise ValueError("Path \"{0}\" is not exists.".format(input_path))

        self._input_path = input_path

    @classmethod
    def run_from_console(cls):
        parser = argparse.ArgumentParser(
            prog="RenPyDecomp",
            description="Ren'Py decompiler."
        )
        parser.add_argument("files_or_folders", nargs='*')
        namespace = parser.parse_args()
        for name in map(path.abspath, namespace.files_or_folders):
            decompile_object = cls(name)
            cls.LOGGER.info("Start decompiling \"%s\".", name)
            decompile_object.run()

    def get_files_from_dir(self, directory):

        directory = path.abspath(directory)
        if not path.isdir(directory):
            raise ValueError("\"{0}\" is not a directory.".format(directory))

        def _get_exts():
            for exts in self.DECOMP_FORMATS.values():
                yield from exts

        _exts = frozenset(_get_exts())
        for dirpath, _, filenames in os.walk(directory):
            for filename in filenames:
                filename = path.abspath(path.join(dirpath, filename))
                _, _ext = path.splitext(filename)
                _ext = _ext.lower().strip()
                if _ext in _exts:
                    yield filename

    def _decomp_file(self, filename, _ignore_other_ext=True):

        filename = path.abspath(filename)
        if not path.isfile(filename):
            raise ValueError("\"{0}\" is not file.".format(filename))

        _, _ext = path.splitext(filename)
        _ext = _ext.lower().strip()

        if _ext in self.DECOMP_FORMATS["archive"]:

            out_folder_name = path.abspath(
                path.join(
                    path.dirname(filename),
                    "depacked {0}".format(path.basename(filename))
                )
            )

            if path.isdir(out_folder_name):
                shutil.rmtree(out_folder_name)
            elif path.isfile(out_folder_name):
                os.remove(out_folder_name)

            os.makedirs(out_folder_name)
            depacker = unrpa.UnRPA(
                filename,
                path=out_folder_name,
                mkdir=True,
                continue_on_error=True
            )
            depacker.extract_files()
            new_files = frozenset(self.get_files_from_dir(out_folder_name))
            for new_filename in new_files:
                self._decomp_file(new_filename)

            return

        elif _ext in self.DECOMP_FORMATS["compiled"]:

            with subprocess.Popen(
                (
                    PY2EXE,
                    "-m", "unrpyc",
                    "--clobber",
                    filename
                ),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ) as process:
                stdout_data, stderr_data = process.communicate(timeout=30.)

            if stderr_data:
                self.LOGGER.error(stderr_data)
                raise SystemError(stderr_data)

            self.LOGGER.info(stdout_data)
            return

        elif not _ignore_other_ext:
            raise ValueError("Incorrect file extension \"{0}\".".format(_ext))

    def run(self):

        if path.isfile(self._input_path):
            work_data = frozenset((self._input_path,))
        elif path.isdir(self._input_path):
            work_data = frozenset(self.get_files_from_dir(self._input_path))
        else:
            raise ValueError("\"{0}\" is not exists.".format(self._input_path))

        for filename in work_data:
            self._decomp_file(filename)
