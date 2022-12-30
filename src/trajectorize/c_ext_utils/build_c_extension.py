import sys

from cffi import FFI

include_dir = "include" if __name__ != "__main__" else "../include"
src_path = "src/trajectorize" if __name__ != "__main__" else "trajectorize"


def read_and_cleanse_header(filename: str) -> str:
    '''
    Reads a header file (.h) and removes macros,
    returning the contents as a string.
    '''
    filepath = f"{include_dir}/{filename}"

    with open(str(filepath), "r", encoding="utf-8") as f:
        lines = f.readlines()
        clean_lines = [line for line in lines if not line.startswith("#")]
        return ''.join(clean_lines)


def read_and_cleanse_many_headers(*filenames: str) -> str:
    '''
    Utility function for reading and cleansing multiple header files,
    joining them into a single string suitable for cffi.cdef().
    '''
    return ''.join([read_and_cleanse_header(filename)
                   for filename in filenames])


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
ffi.cdef(read_and_cleanse_many_headers("vec_math_types.h",
                                       "state_vector_types.h",
                                       "keplerian_element_types.h",
                                       "kerbol_system_types.h",
                                       "kerbol_system_bodies.h",
                                       "kerbol_system_ephemeris.h",
                                       "conic_kepler.h",
                                       "universal_kepler.h",
                                       "lambert.h",
                                       "transfer_orbit.h",
                                       "delta_v_estimate.h"))

'''
Determine compiler flags and linker args depending on platform.

GCC options
-std=c99: Use C99 standard
-lm: Link math library
-lc: Link C standard library
-march=native: Optimize for the current CPU
-O3: Optimize for speed

MSVC options


Compiler type is determined by the value of sys.platform.
'''
if sys.platform == "linux" or sys.platform == "linux2":
    # linux
    extra_compile_args = ["-std=c99", "-lm", "-lc", "-O3"]
else:
    # MSVC is already c99 compliant, so no need to specify
    extra_compile_args = None

# Include only the top-level header files.
ffi.set_source("trajectorize._c_extension",
               '''
               #include "kerbol_system_bodies.h"
               #include "kerbol_system_ephemeris.h"
               #include "conic_kepler.h"
               #include "universal_kepler.h"
               #include "lambert.h"
               #include "transfer_orbit.h"
               #include "delta_v_estimate.h"
               ''',
               sources=[f"{src_path}/math_lib/orbit_math.c",
                        f"{src_path}/math_lib/rotations.c",
                        f"{src_path}/math_lib/stumpuff_functions.c",
                        f"{src_path}/ephemeris/kerbol_system_bodies.c",
                        f"{src_path}/ephemeris/kerbol_system_ephemeris.c",
                        f"{src_path}/orbit/conic_kepler.c",
                        f"{src_path}/orbit/universal_kepler.c",
                        f"{src_path}/trajectory/lambert.c",
                        f"{src_path}/trajectory/transfer_orbit.c",
                        f"{src_path}/trajectory/delta_v_estimate.c"],
               include_dirs=[include_dir],
               extra_compile_args=extra_compile_args)

if __name__ == "__main__":
    # For debug building
    ffi.compile(verbose=True)
