import pytest

from trajectorize.orbit import kepler_equation_solver


def test_kepler_equation_solver():
    # From Curtis Orbital Mechanics Appendix D
    M = 3.6029
    e = 0.37255
    result = kepler_equation_solver.solve_kepler_equation(M, e)
    assert result == pytest.approx(3.479422)
