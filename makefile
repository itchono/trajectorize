all: trajectorize/ephemeris/_c_kerbol_system.so


trajectorize/ephemeris/_c_kerbol_system.so: trajectorize/ephemeris/build_c_kerbol_system.py
	python $<


clean:
	rm trajectorize/*.o trajectorize/*.so