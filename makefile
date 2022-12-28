src/trajectorize/_c_extension.so: src/trajectorize/c_ext_utils/build_c_extension.py
	python $<

autoformat:
	autopep8 --in-place --recursive --aggressive --aggressive src/trajectorize/ -v

clean:
# Remove all .o and .so files under trajectorize/
# Also remove CFFI generated C files with name like _c_kerbol_system.c
	find src/trajectorize/ -name "*.o" -delete
	find src/trajectorize/ -name "*.so" -delete
	find src/trajectorize/ -name "_c_*.c" -delete