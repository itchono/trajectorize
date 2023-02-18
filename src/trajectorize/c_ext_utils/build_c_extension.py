import glob
import sys

from cffi import FFI

include_dir = "include" if __name__ != "__main__" else "../include"
src_path = "src/trajectorize" if __name__ != "__main__" else "trajectorize"


def process_and_join_headers(*filenames: str) -> str:
    '''
    Used to join into a cdef string.

    Header files are sorted to ensure that the order of
    declarations is consistent.
    i.e. if we read a header file and see that it #includes another
    header, then the other header needs to be read first.

    Removes all preprocessor directives, and joins the contents of the headers
    together in topological order.
    '''
    already_processed = set()

    def process_single_file(filename: str) -> str:
        # Processes and cleans a file, recursively processing any #includes
        if filename in already_processed:
            return ""

        with open(f"{include_dir}/{filename}", "r") as f:
            lines = f.readlines()

            clean_lines: "list[str]" = []
            include_lines: "list[str]" = []

            for line in lines:
                if line.startswith("#"):
                    include_lines.append(line)
                else:
                    clean_lines.append(line)

            clean_string = "\n".join(clean_lines)

            for line in include_lines:
                # First find all #include statements and process them
                if line.startswith("#include"):
                    try:
                        include_filename = line.split('"')[1]
                        clean_string = process_single_file(
                            include_filename) + clean_string
                    except IndexError:  # e.g. system header
                        pass

            # Now, process the current file
            already_processed.add(filename)
        return clean_string

    return " ".join(process_single_file(filename) for filename in filenames)


ffi = FFI()


# Sniff out all the header files

# This exposes all symbols in the header files to the C extension
# it helps facilitate testing, but may be overwhelming for production
# (may want to change this in the future)

# remove anything in front of a slash, e.g. "include/vec_math.h" ->
# "vec_math.h"

# delimiter for windows vs unix
delimiter = "\\" if sys.platform.startswith("win") else "/"

header_files = [header_file.split(delimiter)[-1]
                for header_file in glob.glob(f"{include_dir}/*.h")]

ffi.cdef(process_and_join_headers(*header_files))

if sys.platform.startswith("linux"):
    # linux
    extra_compile_args = ["-std=c99", "-lm", "-lc", "-O3"]
else:
    # MSVC is already c99 compliant, so no need to specify
    extra_compile_args = None

# Include all source files under src/trajectorize
# except those starting with "_" (generated code files)
sources = glob.glob(f"{src_path}/**/[!_]*.c")


ffi.set_source("trajectorize._c_extension",
               "\n".join([f'#include "{header}"' for header in header_files]),
               sources=sources,
               include_dirs=[include_dir],
               extra_compile_args=extra_compile_args)

if __name__ == "__main__":
    # For debug building
    ffi.compile(verbose=True)
