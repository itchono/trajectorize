# Trajectorize
KSP Trajectory Optimizer.

This project is a reduced-scope version of [one of my other (currently incomplete) projects](https://github.com/itchono/gravity-assist-flyby-optimizer), as an intermediate stepping stone.

This tool computes trajectories between celestial bodies in KSP based on on-rails two-body patched conics, incorporating trajectory correction maneuvers for a variety of mission scenarios, such as:
* Ballistic Hohmann transfers for other planets
* Gravity assist flyby routes

Computationally-intensive code is implemented in C, with a Python wrapper made using `cffi`.

# Installation
The package is still in development at this time, but you can install it from source.

Run `pip install git+https://github.com/itchono/trajectorize` to install the package.
You will need to have Python 3.8+, and a C compiler installed to compile the C code.

Other Python dependencies are included inside `pyproject.toml`, and will be installed automatically.

# Demos
Right now, full functionality is incomplete. There are, however, some cool demos showing off the capabilities of the package.

## Full Model of KSP Planetary System and Ephemerides
`python -m trajectorize.demos.kerbol_system_anim`
![Kerbol System Animation](https://github.com/itchono/trajectorize/raw/assets/kerbol_system.gif)

## Propagation of Two-Body Trajectories Using Universal Keplerian Elements
`python -m trajectorize.demos.orbit`
![Orbit Demo](https://github.com/itchono/trajectorize/raw/assets/orbit_universal.png)

# Inspirations
* [Interactive illustrated interplanetary guide and calculator for KSP](https://ksp.olex.biz/), by Olex
* [This tool](https://alexmoon.github.io/ksp/), by AlexMoon
