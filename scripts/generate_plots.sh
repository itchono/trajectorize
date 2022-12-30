#!/bin/bash

# Make sure trajectorize is installed
# Temporarily set env to make matplotlib use Agg backend
export MPLBACKEND=Agg

# Generate plots
python -m trajectorize.demos.orbit
python -m trajectorize.demos.kerbin_duna_transfer
python -m trajectorize.demos.kerbin_duna_porkchop
python -m trajectorize.demos.kerbol_system_anim --save
