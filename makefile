all: trajectorize/ephemeris/_c_kerbol_system.so trajectorize/orbit/_c_conic_kepler.so trajectorize/orbit/_c_universal_kepler.so


trajectorize/ephemeris/_c_kerbol_system.so: trajectorize/ephemeris/build_c_kerbol_system.py
	python $<


trajectorize/orbit/_c_conic_kepler.so: trajectorize/orbit/build_c_conic_kepler.py
	python $<

trajectorize/orbit/_c_universal_kepler.so: trajectorize/orbit/build_c_universal_kepler.py
	python $<


clean:
# Remove all .o and .so files under trajectorize/
# Also remove CFFI generated C files with name like _c_kerbol_system.c
	find trajectorize/ -name "*.o" -delete
	find trajectorize/ -name "*.so" -delete
	find trajectorize/ -name "_c_*.c" -delete