# Wrapper for C code
from dataclasses import dataclass

import numpy as np


from trajectorize._c_extension import ffi, lib


@dataclass
class KeplerianElements:
    semi_major_axis: float
    eccentricity: float
    inclination: float
    longitude_of_ascending_node: float
    argument_of_periapsis: float
    true_anomaly: float
    epoch: float

    def get_locus(self, n: int, mu: float) -> np.ndarray:
        '''
        Returns the locus of the orbit in state space.
        '''
        orbit = ffi.new('struct KeplerianElements *', self.__dict__)[0]

        # process memory buffer
        # Format: [x, y, z, vx, vy, vz, t] x n
        arr = np.frombuffer(ffi.buffer(orbit.mem_buffer, 7 *
                                       8 * n), dtype=np.float64)
        arr.shape = (n, 7)
        positions = np.copy(arr[:, :3])  # copy to avoid memory leak

        # Free memory
        lib.freeStateVectorArray(orbit)

        return positions


def solve_kepler_equation(M: float, e: float) -> float:
    result: float = lib.kepler_solver(M, e)
    return result
