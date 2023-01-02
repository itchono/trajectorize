#!/bin/bash

# Make sure trajectorize is installed
# Also: have gifsicle installed for gif compression;
# you can comment out the line if you don't want to compress the gifs

# Temporarily set env to make matplotlib use Agg backend
export MPLBACKEND=Agg

# Generate plots
echo "Generating plots..."
python -m trajectorize.demos.orbit
python -m trajectorize.demos.kerbin_duna_transfer
python -m trajectorize.demos.kerbin_duna_porkchop
python -m trajectorize.demos.kerbol_system_anim --save
echo "Optimizing kerbol_system.gif"
gifsicle -O3 --colors 256 kerbol_system_raw.gif -o kerbol_system.gif
rm kerbol_system_raw.gif
echo "Done!"
