import numpy as np
import pytest

from trajectorize.orbit import conic_kepler
from trajectorize.tester_utils.fake_body import EARTH_SI


def test_orbital_period():
    # Create an example orbit of known period
    # Circular orbit with a = 7378.1 km
    # T = 01:45:07.12 (hh:mm:ss) = 6372.12 s

    elements = conic_kepler.KeplerianElements(
        semi_major_axis=7378.14e3,
        eccentricity=0,
        inclination=0,
        longitude_of_ascending_node=0,
        argument_of_periapsis=0,
        true_anomaly=0,
        epoch=0
    )

    orbit = conic_kepler.KeplerianOrbit(elements, EARTH_SI)

    # Assert that the orbital period is correct
    assert orbit.T == pytest.approx(6307.12, abs=1e-2)


def test_ke_from_state_vector():
    # Using Curtis example 4.3
    position = np.array([-6045, -3490, 2500])*1e3
    velocity = np.array([-3.457, 6.618, 2.533])*1e3

    orbit = conic_kepler.KeplerianOrbit.from_state_vector(position,
                                                          velocity,
                                                          0,
                                                          EARTH_SI)

    assert orbit.ke.semi_major_axis == pytest.approx(8788e3, rel=1e-3)
    assert orbit.ke.eccentricity == pytest.approx(0.1712, rel=1e-4)
    assert orbit.ke.inclination == pytest.approx(np.deg2rad(153.2), rel=1e-3)
    assert orbit.ke.longitude_of_ascending_node == pytest.approx(
        np.deg2rad(255.3), rel=1e-4)
    assert orbit.ke.argument_of_periapsis == pytest.approx(
        np.deg2rad(20.07), rel=1e-4)
    assert orbit.ke.true_anomaly == pytest.approx(np.deg2rad(28.45), rel=1e-3)


def test_state_vector_from_ke():
    # Using Curtis example 4.3
    position = np.array([-6045, -3490, 2500])*1e3
    velocity = np.array([-3.457, 6.618, 2.533])*1e3

    orbit = conic_kepler.KeplerianOrbit.from_state_vector(position,
                                                          velocity,
                                                          0,
                                                          EARTH_SI)

    sv = orbit.state_vector
    assert np.allclose(sv.position, position)
    assert np.allclose(sv.velocity, velocity)


def test_hyperbolic_fitter():
    # using Curtis example 2.10
    v_inf = np.array([4.4e3, 0, 0])
    r_pe = 6986e3

    hyp_traj = conic_kepler.fit_hyperbolic_trajectory(v_inf, r_pe, EARTH_SI)

    assert hyp_traj.ke.eccentricity == pytest.approx(1.3393, rel=1e-3)
    assert hyp_traj.ke.semi_major_axis == pytest.approx(20590e3, rel=1e-3)
