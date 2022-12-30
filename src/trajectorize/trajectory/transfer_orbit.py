from enum import IntEnum

import numpy as np

from trajectorize._c_extension import lib
from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)
from trajectorize.orbit.conic_kepler import KeplerianElements, KeplerianOrbit


class TrajectoryDirection(IntEnum):
    PROGRADE = lib.PROGRADE
    RETROGRADE = lib.RETROGRADE


def planetary_transfer_orbit(body1: Body, body2: Body, t1: float, t2: float) \
        -> KeplerianOrbit:
    parent = Body.from_identifier(body1.parent_id)
    sol = lib.planetary_transfer_orbit(body1.c_data, body2.c_data, t1, t2)

    ke = KeplerianElements.from_c_data(sol)
    orbit = KeplerianOrbit(ke, parent)
    return orbit


def get_excess_velocity(body: Body, orbit: KeplerianOrbit, time: float) \
        -> np.ndarray:
    '''
    Gets the excess velocity between the transfer orbit and a celestial
    body at some time.
    Used to patch the transfer orbit into the body orbit.
    '''
    return np_array_from_vec3(
        lib.excess_velocity_at_body(body.c_data, orbit.ke.c_data, time))


def estimate_delta_v(body: Body, excess_velocity: float,
                     periapsis_radius: float) -> float:
    '''
    Estimates the delta-v required to patch the transfer orbit into the body orbit.
    '''
    return lib.delta_v_req(body.c_data, excess_velocity, periapsis_radius)


def solve_lambert_problem(r1: np.ndarray, r2: np.ndarray,
                          dt: float, mu: float,
                          direction: TrajectoryDirection) \
        -> "tuple(np.ndarray, np.ndarray)":
    r1_c = vec3_from_np_array(r1)
    r2_c = vec3_from_np_array(r2)
    sol = lib.lambert(r1_c, r2_c, dt, mu, int(direction))
    v1 = np_array_from_vec3(sol.v1)
    v2 = np_array_from_vec3(sol.v2)
    return v1, v2


def trajectory_ejection_dv(t1: float, t2: float,
                           body1: Body, body2: Body,
                           parking_orbit_alt: float = 100000):
    '''
    Delta-v required to eject from body1 and enter a transfer orbit to body2.

    Parameters
    ----------
    t1: float
        Time of departure from body1 (universal time, seconds)
    t2: float
        Time of arrival at body2 (universal time, seconds)
    body1: Body
        Departure body
    body2: Body
        Arrival body
    parking_orbit_alt: float
        Altitude of parking orbit (meters) above body1's surface.
        e.g. for Kerbin, it's about 70 km for an ideal orbit just outside
        the atmosphere.
    '''
    try:
        orbit = planetary_transfer_orbit(
            body1, body2, t1, t2)
        excess_velocity = get_excess_velocity(body1, orbit, t1)
        excess_speed = np.linalg.norm(excess_velocity)
        delta_v = estimate_delta_v(
            body1, excess_speed,
            orbit.ke.semi_major_axis + parking_orbit_alt)
        return delta_v
    except Exception:
        return np.nan


# standalone test
if __name__ == "__main__":
    # Test transfer from Kerbin to Duna
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1 = 5091552
    t2 = 10679760

    transfer_orbit = planetary_transfer_orbit(kerbin, duna, t1, t2)
    kerbin_excess_velocity = get_excess_velocity(kerbin, transfer_orbit, t1)

    v_inf_kerbin = np.linalg.norm(kerbin_excess_velocity)
    v_inf_duna = np.linalg.norm(get_excess_velocity(duna, transfer_orbit, t2))
    r_pe_kerbin = kerbin.radius + 70000  # 70 km parking orbit
    dv_est_kerbin = estimate_delta_v(kerbin, v_inf_kerbin, r_pe_kerbin)
    r_pe_duna = duna.radius + 50000  # 50 km target orbit
    dv_est_duna = estimate_delta_v(duna, v_inf_duna, r_pe_duna)

    print(f"Estimated ejection delta-v: {dv_est_kerbin:.2f} m/s")
    print(f"C3 wrt Kerbin: {v_inf_kerbin**2/1e6:.2f} km^2/s^2")
    print(f"Estimate capture delta-v: {dv_est_duna:.2f} m/s")
