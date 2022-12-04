from trajectorize.setup_utils.c_parsing import (include_dir,
                                                read_and_cleanse_many_headers)
from cffi import FFI

ffi = FFI()


ffi.cdef(read_and_cleanse_many_headers("planetary_keplerian_elements.h",
                                       "kerbol_system_types.h",
                                       "orbit_math_types.h",
                                       "universal_kepler.h"))

ffi.set_source("trajectorize.orbit._c_universal_kepler",
               '''
               #include "kerbol_system_types.h"
               #include "orbit_math_types.h"
               #include "universal_kepler.h"
               ''',
               sources=["trajectorize/orbit/universal_kepler.c",
                        "trajectorize/math_lib/orbit_math.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile(verbose=True)
