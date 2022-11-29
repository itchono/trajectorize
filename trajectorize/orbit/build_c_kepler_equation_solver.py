from trajectorize.setup_utils.c_parsing import (include_dir,
                                                read_and_cleanse_header)
from cffi import FFI

ffi = FFI()


ffi.cdef(read_and_cleanse_header("kepler_equation_solver.h"))

ffi.set_source("trajectorize.orbit._c_kepler_equation_solver",
               '''
               #include "kepler_equation_solver.h"
               ''',
               sources=["trajectorize/orbit/kepler_equation_solver.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile()
