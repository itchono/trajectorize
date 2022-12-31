import sys
import glob

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
    # Used to join into a cdef string
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

if sys.platform.startswith("linux"):
    # linux
    extra_compile_args = ["-std=c99", "-lm", "-lc", "-O3"]
else:
    # MSVC is already c99 compliant, so no need to specify
    extra_compile_args = None

# Include all source files under src/trajectorize
# except those starting with "_" (generated code files)
sources = glob.glob(f"{src_path}/**/[!_]*.c")

# This exposes all symbols in the header files to the C extension
# it helps facilitate testing, but may be overwhelming for production
# (may want to change this in the future)

# remove anything in front of a slash, e.g. "include/vec_math.h" -> "vec_math.h"
# delimiter for windows vs unix
delimiter = "\\" if sys.platform.startswith("win") else "/"

include_statements = [f'#include "{include_file.split(delimiter)[-1]}"'
                      for include_file in glob.glob(f"{include_dir}/*.h")]

ffi.set_source("trajectorize._c_extension",
               "\n".join(include_statements),
               sources=sources,
               include_dirs=[include_dir],
               extra_compile_args=extra_compile_args)

if __name__ == "__main__":
    # For debug building
    ffi.compile(verbose=True)
