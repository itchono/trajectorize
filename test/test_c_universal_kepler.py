from trajectorize.orbit.universal_kepler import UniversalKeplerOrbit
import numpy as np


def test_universal_kepler():
    r0 = np.array([7000, -12124, 0])
    v0 = np.array([2.6679, 4.6210, 0])
    mu = 398600
    t = 3600

    orb = UniversalKeplerOrbit(r0, v0, 0, mu)

    orb2 = orb.propagate(t)

    print(orb2.position)
    print(orb2.velocity)

    assert np.allclose(orb2.position, np.array([-3297.7686252, 7413.39664579, 0]))
    assert np.allclose(orb2.velocity, np.array([-8.29760302, -0.96404494, -0.]))
    
