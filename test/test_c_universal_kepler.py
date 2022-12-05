from trajectorize.orbit.universal_kepler import UniversalKeplerOrbit
from trajectorize.ephemeris.kerbol_system import Body
import numpy as np


def test_universal_kepler():
    r0 = np.array([7000e3, -12124e3, 0])
    v0 = np.array([2.6679e3, 4.6210e3, 0])
    t = 3600

    orb = UniversalKeplerOrbit(r0, v0, 0, 3.986e14)

    orb2 = orb.propagate(t)

    print(orb2.position)
    print(orb2.velocity)

    assert np.allclose(orb2.position, np.array(
        [-3297.7686252e3, 7413.39664579e3, 0]))
    assert np.allclose(orb2.velocity, np.array(
        [-8.29760302e3, -0.96404494e3, -0.]))