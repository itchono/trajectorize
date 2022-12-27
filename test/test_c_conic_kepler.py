import pytest

from trajectorize.orbit import conic_kepler


class MonkeyPatchedBody:
    '''
    Defines a body with a monkey-patched mu attribute which behaves like a
    Body from the kerbol_system module.
    '''

    def __init__(self, mu):
        self.mu = mu


EARTH = MonkeyPatchedBody(3.986004418e14)


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

    orbit = conic_kepler.KeplerianOrbit(elements, EARTH)

    # Assert that the orbital period is correct
    assert orbit.T == pytest.approx(6307.12, abs=1e-2)


def test_kepler_equation_solver():
    # From Curtis Orbital Mechanics Appendix D
    M = 3.6029
    e = 0.37255
    result = conic_kepler.solve_kepler_equation(M, e)
    assert result == pytest.approx(3.479422)
