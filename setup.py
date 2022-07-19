# -*- coding: utf-8 -*-
"""
@author: Vladya
"""

from setuptools import setup

setup(
    name="RenPyDecomp",
    version="1.0.4",
    author="Vladya",
    packages=["RenPyDecomp"],
    install_requires=["unrpa>=2.3.0"],
    python_requires=">=3.9",
    entry_points={
        "console_scripts":
            [
                "decompileRenPy = RenPyDecomp.main:Decompiler.run_from_console"
            ]
    }
)
