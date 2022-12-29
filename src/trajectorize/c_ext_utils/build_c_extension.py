import sys
import pathlib
from cffi import FFI

# Hack: change working directory to be inside the src/ dir
# So that the trajectorize package can be imported
if __name__ != "__main__":
    # For normal building
    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent.resolve()))
    from trajectorize.c_ext_utils.c_parsing import \
        (read_and_cleanse_many_headers, include_dir, abs_src_path)
else:
    # For debug building
    from c_parsing import \
        (read_and_cleanse_many_headers, include_dir)
    abs_src_path = "trajectorize"


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
               ''',
               sources=[f"{abs_src_path}/math_lib/orbit_math.c",
                        f"{abs_src_path}/math_lib/rotations.c",
                        f"{abs_src_path}/math_lib/stumpuff_functions.c",
                        f"{abs_src_path}/ephemeris/kerbol_system_bodies.c",
                        f"{abs_src_path}/ephemeris/kerbol_system_ephemeris.c",
                        f"{abs_src_path}/orbit/conic_kepler.c",
                        f"{abs_src_path}/orbit/universal_kepler.c",
                        f"{abs_src_path}/trajectory/lambert.c"],
               include_dirs=[include_dir],
               extra_compile_args=extra_compile_args)

if __name__ == "__main__":
    # For debug building
    ffi.compile(verbose=True)
