# Wrapper for C code
from ._c_conic_kepler import ffi, lib


def solve_kepler_equation(M: float, e: float) -> float:
    result: float = lib.kepler_solver(M, e)
    return result
