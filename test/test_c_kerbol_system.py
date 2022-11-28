import pytest

from trajectorize.ephemeris import kerbol_system


def test_kerbin_parameters():
    assert kerbol_system.Kerbin.mass == pytest.approx(5.2915158e22)
    assert kerbol_system.Kerbin.radius == pytest.approx(600000)
