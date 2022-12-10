from trajectorize.setup_utils.c_parsing import (include_dir,
                                                read_and_cleanse_many_headers)
from cffi import FFI

ffi = FFI()


ffi.cdef(read_and_cleanse_many_headers("keplerian_elements.h",
                                       "orbit_math_types.h",
                                       "state_vector_types.h",
                                       "stumpuff_functions.h",
                                       "universal_kepler.h"))

ffi.set_source("trajectorize.orbit._c_universal_kepler",
               '''
               #include "kerbol_system_types.h"
               #include "orbit_math_types.h"
               #include "universal_kepler.h"
               #include "stumpuff_functions.h"
               ''',
               sources=["trajectorize/orbit/universal_kepler.c",
                        "trajectorize/math_lib/orbit_math.c",
                        "trajectorize/math_lib/stumpuff_functions.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile(verbose=True)
