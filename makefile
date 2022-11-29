all: trajectorize/ephemeris/_c_kerbol_system.so trajectorize/orbit/_c_kepler_equation_solver.so


trajectorize/ephemeris/_c_kerbol_system.so: trajectorize/ephemeris/build_c_kerbol_system.py
	python $<


trajectorize/orbit/_c_kepler_equation_solver.so: trajectorize/orbit/build_c_kepler_equation_solver.py
	python $<


clean:
	rm trajectorize/*.o trajectorize/*.so