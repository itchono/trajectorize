from enum import IntEnum

import numpy as np

from trajectorize._c_extension import lib
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)


class TrajectoryDirection(IntEnum):
    PROGRADE = lib.PROGRADE
    RETROGRADE = lib.RETROGRADE


def solve_lambert_problem(r1: np.ndarray, r2: np.ndarray,
                          dt: float, mu: float,
                          direction: TrajectoryDirection) \
        -> "tuple(np.ndarray, np.ndarray)":
    r1_c = vec3_from_np_array(r1)
    r2_c = vec3_from_np_array(r2)
    sol = lib.lambert(r1_c, r2_c, mu, dt, int(direction))
    v1 = np_array_from_vec3(sol.v1)
    v2 = np_array_from_vec3(sol.v2)
    return v1, v2
