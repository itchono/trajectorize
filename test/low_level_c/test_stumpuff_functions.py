import pytest

from trajectorize._c_extension import ffi, lib


@pytest.mark.parametrize("z, S",
                         [(10, 0.10065407),
                          (1, 0.15852902),
                          (0, 1/6),
                          (-1, 0.17520119),
                          (-10, 0.27286438)])
def test_stumpuff_S(z, S):
    S_lib = lib.stumpS(z)

    assert S == pytest.approx(S_lib)


@pytest.mark.parametrize("z, C",
                         [(10, 0.19997861),
                          (1, 0.45969769),
                          (0, 0.5),
                          (-1, 0.54308063),
                          (-10, 1.0833336)])
def test_stumpuff_C(z, C):
    C_lib = lib.stumpC(z)

    assert C == pytest.approx(C_lib)
