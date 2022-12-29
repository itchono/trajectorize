import numpy as np
import pytest

from trajectorize.trajectory.lambert import solve_lambert_problem, \
    TrajectoryDirection
from trajectorize._c_extension import ffi, lib


def test_orbit_determination():
    # Test case from Curtis for Earth orbit determination
    r1 = np.array([5000, 10000, 2100])
    r2 = np.array([-14600, 2500, 7000])

    dt = 3600
    direction = TrajectoryDirection.PROGRADE
    mu = 398600  # km^3/s^2; Earth

    v1, v2 = solve_lambert_problem(r1, r2, dt, mu, direction)

    assert np.allclose(v1, np.array([-5.99249, 1.92536, 3.24564]), atol=1e-3)
    assert np.allclose(v2, np.array([-3.31246, -4.19662, -0.385288]),
                       atol=1e-3)
