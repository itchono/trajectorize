#!/usr/bin/env python

import os
import sys

from setuptools import find_packages, setup

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
    license="LGPLv3",
    author="Mingde Yin",
    author_email="mdsuper@hotmail.com",
    packages=find_packages(),
    install_requires=["cffi>=1.15.0",
                      "numpy>=1.24.0",
                      "matplotlib>=3.6.0",
                      "mayavi",
                      "tqdm"],
    setup_requires=["cffi>=1.15.0"],
    python_requires=">=3.8",
    classifiers=["Development Status :: 3 - Alpha",
                 "Programming Language :: Python :: 3",
                 "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
                 "Operating System :: OS Independent",
                 "Programming Language :: C",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Intended Audience :: Science/Research"],
    cffi_modules=[
        "./trajectorize/c_ext_utils/build_c_extension.py:ffi"
    ],
)
