from trajectorize.setup_utils.c_parsing import (include_dir,
                                                read_and_cleanse_many_headers)
from cffi import FFI

ffi = FFI()


ffi.cdef(read_and_cleanse_many_headers("planetary_keplerian_elements.h",
                                       "kerbol_system_types.h",
                                       "kerbol_system_bodies.h"))

ffi.set_source("trajectorize.ephemeris._c_kerbol_system",
               '''
               #include "kerbol_system_bodies.h"
               ''',
               sources=["trajectorize/ephemeris/kerbol_system_bodies.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile(verbose=True)
