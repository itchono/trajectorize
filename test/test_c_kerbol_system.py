import pytest

from trajectorize.ephemeris.kerbol_system import (Body, KerbolSystemBodyEnum,
                                                  state_vector_at_time)


def test_kerbin_parameters():
    kerbin = Body.from_name("Kerbin")

    assert kerbin.mass == pytest.approx(5.2915158e22)
    assert kerbin.radius == pytest.approx(600000)


def test_ephemeris_1():
    initial_kerbin_State = state_vector_at_time(0, KerbolSystemBodyEnum.KERBOL,
                                                KerbolSystemBodyEnum.KERBIN)

    assert initial_kerbin_State.time == 0
    print(initial_kerbin_State)
