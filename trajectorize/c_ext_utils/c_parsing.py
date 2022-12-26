import os

include_dir = os.path.join(os.path.dirname(__file__), '../../include')


def read_and_cleanse_header(filename: str) -> str:
    '''
    Reads a header file (.h) and removes macros,
    returning the contents as a string.
    '''
    with open(os.path.join(include_dir, filename), "r", encoding="utf-8") as f:
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
