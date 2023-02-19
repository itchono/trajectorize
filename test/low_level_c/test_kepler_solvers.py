import numpy as np
import pytest

from trajectorize._c_extension import ffi, lib


@pytest.mark.parametrize("E, e",
                         np.vstack((np.linspace(0, 2*np.pi, 10),
                                   np.linspace(0, 0.999, 10))).T.tolist())
def test_kepler_equation_solver(E, e):
    M = E - e * np.sin(E)  # Calculate forwards kepler equation
    E_c = lib.E_from_M(M, e)

    assert E_c == pytest.approx(E)
