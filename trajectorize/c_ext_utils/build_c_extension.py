from cffi import FFI

from trajectorize.c_ext_utils.c_parsing import (include_dir,
                                                read_and_cleanse_many_headers)
from sys import platform

ffi = FFI()

'''
Add files in dependency order.
Generally, the order is:
- "..._types.h"
- everything else that's called at the top level
- files "in the middle" need not be included e.g. math library functions

This is because header files further down the list may depend on types defined
upstream.
'''
ffi.cdef(read_and_cleanse_many_headers("orbit_math_types.h",
                                       "state_vector_types.h",
                                       "keplerian_element_types.h",
                                       "kerbol_system_types.h",
                                       "kerbol_system_bodies.h",
                                       "kerbol_system_ephemeris.h",
                                       "conic_kepler.h",
                                       "universal_kepler.h",
                                       "lambert.h"))

'''
Determine compiler flags and linker args depending on platform.

GCC options
-std=c99: Use C99 standard
-lm: Link math library
-lc: Link C standard library

MSVC options


Compiler type is determined by the value of sys.platform.
'''
if platform == "linux" or platform == "linux2":
    # linux
    extra_compile_args = ["-std=c99", "-lm", "-lc"]
else:
    extra_compile_args = []

# Include only the top-level header files.
ffi.set_source("trajectorize._c_extension",
               '''
               #include "kerbol_system_bodies.h"
               #include "kerbol_system_ephemeris.h"
               #include "conic_kepler.h"
               #include "universal_kepler.h"
               #include "lambert.h"
               ''',
               sources=["trajectorize/math_lib/orbit_math.c",
                        "trajectorize/math_lib/rotations.c",
                        "trajectorize/math_lib/stumpuff_functions.c",
                        "trajectorize/ephemeris/kerbol_system_bodies.c",
                        "trajectorize/ephemeris/kerbol_system_ephemeris.c",
                        "trajectorize/orbit/conic_kepler.c",
                        "trajectorize/orbit/universal_kepler.c",
                        "trajectorize/trajectory/lambert.c"],
               include_dirs=[include_dir],
               extra_compile_args=extra_compile_args)

if __name__ == "__main__":
    # For debug building
    ffi.compile(verbose=True)
