all: trajectorize/ephemeris/_c_kerbol_system.so trajectorize/orbit/_c_kepler_equation_solver.so


trajectorize/ephemeris/_c_kerbol_system.so: trajectorize/ephemeris/build_c_kerbol_system.py
	python $<


trajectorize/orbit/_c_kepler_equation_solver.so: trajectorize/orbit/build_c_kepler_equation_solver.py
	python $<


clean:
# Remove all .o and .so files under trajectorize/
# Also remove CFFI generated C files with name like _c_kerbol_system.c
	find trajectorize/ -name "*.o" -delete
	find trajectorize/ -name "*.so" -delete
	find trajectorize/ -name "_c_*.c" -delete