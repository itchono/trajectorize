import numpy as np
import pytest

from trajectorize._c_extension import ffi, lib

from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)


def test_kerbin_ejection():
    # desired velocity at kerbin SOI exit
    v_inf = np.array([-193.78557954, 830.55066003, 36.9947657])
    v_inf_c = vec3_from_np_array(v_inf)

    kerbin = lib.kerbol_system_bodies[lib.KERBIN]

    hyperbolic_ke = lib.fit_hyperbolic_trajectory(
        v_inf_c, 70000+kerbin.radius, kerbin.mu)

    inf_sv = lib.ke_hyperbolic_at_infinity(hyperbolic_ke, kerbin.mu)

    print(hyperbolic_ke.eccentricity)

    pos = np_array_from_vec3(inf_sv.position)
    vel = np_array_from_vec3(inf_sv.velocity)

    print(pos)
    print(vel)

    assert vel == pytest.approx(v_inf, abs=1e-6)
