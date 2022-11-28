import os

include_dir = os.path.join(os.path.dirname(__file__), '../../include')


def read_header_file_and_cleanse_macros(filename: str):
    with open(os.path.join(include_dir, filename)) as f:
        lines = f.readlines()
        clean_lines = [line for line in lines if not line.startswith("#")]
        return ''.join(clean_lines)
