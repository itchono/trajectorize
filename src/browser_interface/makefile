# makefile for browser_interface using emcc toolchain
# define individual targets here

# define include directories
INCLUDES = -I../../include
SRCS = ../trajectorize/**/*.c

dist: trajectorize.js index.html
# create dist folder
	mkdir -p dist
# copy files to dist folder
	cp trajectorize.js dist
	cp trajectorize.wasm dist
	cp -r scripts dist/scripts
	cp index.html dist

# target
trajectorize.js: browser_main.c
	emcc -sEXPORTED_RUNTIME_METHODS=ccall,cwrap browser_main.c -o trajectorize.js $(INCLUDES) $(SRCS)

index.html:
# (placeholder)

browser_main.c:
# (placeholder)

clean:
	rm -rf dist
	rm trajectorize.js
	rm trajectorize.wasm
