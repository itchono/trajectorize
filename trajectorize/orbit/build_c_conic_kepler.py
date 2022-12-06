from trajectorize.setup_utils.c_parsing import (include_dir,
                                                read_and_cleanse_many_headers)
from cffi import FFI

ffi = FFI()


ffi.cdef(read_and_cleanse_many_headers("orbit_math_types.h",
                                       "keplerian_elements.h",
                                       "state_vector_types.h",
                                       "conic_kepler.h"))

ffi.set_source("trajectorize.orbit._c_conic_kepler",
               '''
               #include "conic_kepler.h"
               ''',
               sources=["trajectorize/orbit/conic_kepler.c",
                        "trajectorize/math_lib/orbit_math.c",
                        "trajectorize/math_lib/rotations.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile(verbose=True)
