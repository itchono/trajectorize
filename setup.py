#!/usr/bin/env python

import pathlib

from setuptools import setup

if __name__ == "__main__":
    # Make a relative path for the cffi module
    cffi_dir = pathlib.Path(__file__).parent / "src" / \
        "trajectorize" / "c_ext_utils"
    setup(cffi_modules=[str(cffi_dir / "build_c_extension.py:ffi")])
