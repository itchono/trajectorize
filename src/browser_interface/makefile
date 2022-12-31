# makefile for browser_interface using emcc toolchain
# define individual targets here

# define include directories
INCLUDES = -I../../include
SRCS = ../trajectorize/**/*.c browser_main.c

# target
trajectorize.js: browser_main.c
	emcc -o trajectorize.js $(INCLUDES) $(SRCS)
# create dist folder
	mkdir -p dist
# copy files to dist folder
	cp trajectorize.js dist
	cp trajectorize.wasm dist
	cp index.html dist
	cp -r scripts dist/scripts

browser_main.c:
# (placeholder)

clean:
	rm -rf dist
	rm trajectorize.js
	rm trajectorize.wasm
