import numpy as np

from trajectorize.orbit.universal_kepler import UniversalKeplerOrbit


def test_universal_kepler():
    r0 = np.array([7000e3, -12124e3, 0])
    v0 = np.array([2.6679e3, 4.6210e3, 0])
    t = 3600

    orb = UniversalKeplerOrbit(r0, v0, 0, 3.986e14)

    orb2 = orb.propagate(t)

    assert np.allclose(orb2.position, np.array(
        [-3297.7686252e3, 7413.39664579e3, 0]))
    assert np.allclose(orb2.velocity, np.array(
        [-8.29760302e3, -0.96404494e3, -0.]))


def test_universal_kepler_vec():
    r0 = np.array([7000e3, -12124e3, 0])
    v0 = np.array([2.6679e3, 4.6210e3, 0])
    t = np.array([1800, 3600, 5400, 7200])

    orb = UniversalKeplerOrbit(r0, v0, 0, 3.986e14)

    orb2 = orb.propagate_vec(t)

    assert np.allclose(orb2.position[1, :], np.array(
        [-3297.7686252e3, 7413.39664579e3, 0]))
    assert np.allclose(orb2.velocity[1, :], np.array(
        [-8.29760302e3, -0.96404494e3, -0.]))
