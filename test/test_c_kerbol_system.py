import pytest

from trajectorize.ephemeris.kerbol_system import Body


def test_kerbin_parameters():
    kerbin = Body.from_name("Kerbin")

    assert kerbin.mass == pytest.approx(5.2915158e22)
    assert kerbin.radius == pytest.approx(600000)
