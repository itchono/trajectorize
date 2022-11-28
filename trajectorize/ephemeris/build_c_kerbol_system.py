from trajectorize.setup_utils.c_parsing import include_dir, read_header_file_and_cleanse_macros
from cffi import FFI

ffi = FFI()


ffi.cdef(read_header_file_and_cleanse_macros('keplerian_elements.h') +
         read_header_file_and_cleanse_macros('kerbol_system_types.h') +
         read_header_file_and_cleanse_macros('kerbol_system_bodies.h'))

ffi.set_source("trajectorize.ephemeris._c_kerbol_system",
               '''
               #include "keplerian_elements.h"
               #include "kerbol_system_types.h"
               #include "kerbol_system_bodies.h"
               ''',
               sources=["trajectorize/ephemeris/kerbol_system_bodies.c"],
               include_dirs=[include_dir])

if __name__ == "__main__":
    ffi.compile()
