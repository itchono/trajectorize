trajectorize/_c_extension.so: trajectorize/c_ext_utils/build_c_extension.py
	python $<

autoformat:
	autopep8 --in-place --recursive --aggressive --aggressive trajectorize/ -v

clean:
# Remove all .o and .so files under trajectorize/
# Also remove CFFI generated C files with name like _c_kerbol_system.c
	find trajectorize/ -name "*.o" -delete
	find trajectorize/ -name "*.so" -delete
	find trajectorize/ -name "_c_*.c" -delete