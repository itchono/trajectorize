#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages

os.chdir(os.path.dirname(sys.argv[0]) or ".")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="trajectorize",
    version="0.1",
    description="KSP Trajectory Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itchono/trajectorize",
    author="Mingde Yin",
    author_email="mdsuper@hotmail.com",
    packages=find_packages(),
    install_requires=["cffi>=1.15.0"],
    setup_requires=["cffi>=1.15.0"],
    cffi_modules=[
        "./trajectorize/ephemeris/build_c_kerbol_system.py:ffi",
        "./trajectorize/orbit/build_c_kepler_equation_solver.py:ffi",
    ],
)
