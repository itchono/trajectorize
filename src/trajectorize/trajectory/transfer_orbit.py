from enum import IntEnum

import numpy as np

from trajectorize._c_extension import lib
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)
from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.orbit.conic_kepler import KeplerianOrbit, KeplerianElements


class TrajectoryDirection(IntEnum):
    PROGRADE = lib.PROGRADE
    RETROGRADE = lib.RETROGRADE


def planetary_transfer_orbit(body1: Body, body2: Body, t1: float, t2: float) \
        -> KeplerianOrbit:
    parent = Body.from_identifier(body1.parent_id)
    sol = lib.planetary_transfer_orbit(body1.c_data, body2.c_data, t1, t2)

    ke = KeplerianElements.from_c_data(sol)
    orbit = KeplerianOrbit(ke, parent)
    return orbit


def solve_lambert_problem(r1: np.ndarray, r2: np.ndarray,
                          dt: float, mu: float,
                          direction: TrajectoryDirection) \
        -> "tuple(np.ndarray, np.ndarray)":
    r1_c = vec3_from_np_array(r1)
    r2_c = vec3_from_np_array(r2)
    sol = lib.lambert(r1_c, r2_c, dt, mu, int(direction))
    v1 = np_array_from_vec3(sol.v1)
    v2 = np_array_from_vec3(sol.v2)
    return v1, v2
