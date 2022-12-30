![Trajectorize Logo](https://raw.githubusercontent.com/itchono/trajectorize/assets/trajectorize_logo.png)
[![PyPi Version](https://img.shields.io/pypi/v/trajectorize?style=for-the-badge)](https://pypi.org/project/trajectorize/)
[![License](https://img.shields.io/github/license/itchono/trajectorize?style=for-the-badge)](https://github.com/itchono/trajectorize/blob/main/LICENSE)

---

KSP Trajectory Optimizer.

This project is a reduced-scope version of [one of my other (currently incomplete) projects](https://github.com/itchono/gravity-assist-flyby-optimizer), as an intermediate stepping stone.

This tool computes trajectories between celestial bodies in KSP based on on-rails two-body patched conics, incorporating trajectory correction maneuvers for a variety of mission scenarios, such as:

* Ballistic Hohmann transfers for other planets
* Gravity assist flyby routes

Computationally-intensive code is implemented in C, with a Python wrapper made using `cffi`.
C code follows mostly C89, with some C99 features used. It has been tested against the latest versions of GCC (on Linux) and MSVC (on Windows 10).

# Installation

The simplest way to install is from PyPI:

`pip install trajectorize`

This will install the latest stable version of the package, and may include pre-compiled binaries for your platform.

The package is still in development, so you may want to install from the latest commit on the `main` branch instead:

Run `pip install git+https://github.com/itchono/trajectorize` to install the package from source.

You will need to have Python 3.8+, and a **C compiler installed** to compile the C code if installing from source. You will also need a C compiler installed if there are no pre-compiled binaries for your platform. If you're on Windows, you can find details about installing a C compiler [here](https://wiki.python.org/moin/WindowsCompilers).

The following platforms/compilers have been tested:
|Platform         |Compiler   |
|-----------------|-----------|
|Windows 10       | MSVC 14.16 (Visual Studio 2017)|
|Ubuntu 20.04 LTS (Dev Machine) | GCC 9.4.0 |

# Demos

Right now, full functionality is incomplete. There are, however, some cool demos showing off the capabilities of the package.

## Full Model of KSP Planetary System and Ephemerides

`python -m trajectorize.demos.kerbol_system_anim`

![Kerbol System Animation](https://raw.githubusercontent.com/itchono/trajectorize/assets/kerbol_system.gif)

## Calculation of Ballistic Interplanetary Transfers Using Lambert's Problem

`python -m trajectorize.demos.kerbin_duna_transfer`

![Transfer](https://raw.githubusercontent.com/itchono/trajectorize/assets/kerbin_duna_transfer.png)

## Propagation of Two-Body Trajectories Using Universal Keplerian Elements

`python -m trajectorize.demos.orbit`

![Orbit Demo](https://raw.githubusercontent.com/itchono/trajectorize/assets/orbit_universal.png)

## Calculations of Optimal Transfers, Porkchop Plots

`python -m trajectorize.demos.kerbin_duna_porkchop`

![Porkchop](https://raw.githubusercontent.com/itchono/trajectorize/assets/kerbin_duna_porkchop.png)

# Inspirations

* [Interactive illustrated interplanetary guide and calculator for KSP](https://ksp.olex.biz/), by Olex
* [Launch Window Planner](https://alexmoon.github.io/ksp/), by AlexMoon
