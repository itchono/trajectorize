from enum import IntEnum

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.ephemeris.kerbol_system import Body, BodyEnum
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)
from trajectorize.orbit.conic_kepler import KeplerianElements, KeplerianOrbit

from dataclasses import dataclass


class TrajectoryDirection(IntEnum):
    PROGRADE = lib.PROGRADE
    RETROGRADE = lib.RETROGRADE


class ArrivalDeparture(IntEnum):
    ARRIVAL = lib.ARRIVAL
    DEPARTURE = lib.DEPARTURE


@dataclass
class TransferOrbit:
    '''
    Equivalent to C TransferOrbit struct
    '''
    ke: KeplerianElements
    valid: bool
    t1: float
    t2: float
    body1: Body
    body2: Body

    @classmethod
    def from_c_data(cls, c_data):
        ke = KeplerianElements.from_c_data(c_data.ke)
        return cls(ke, c_data.valid, c_data.t1, c_data.t2,
                   Body.from_identifier(BodyEnum(c_data.body1.body_id)),
                   Body.from_identifier(BodyEnum(c_data.body2.body_id)))

    @property
    def c_data(self):
        return ffi.new("struct TransferOrbit *", {
            "ke": self.ke.c_data,
            "valid": self.valid,
            "t1": self.t1,
            "t2": self.t2,
            "body1": self.body1.c_data,
            "body2": self.body2.c_data
        })[0]


def planetary_transfer_orbit(body1: Body, body2: Body, t1: float, t2: float) \
        -> TransferOrbit:
    sol = lib.planetary_transfer_orbit(body1.c_data, body2.c_data, t1, t2)

    if not sol.valid:
        return None
    return TransferOrbit.from_c_data(sol)


def get_excess_velocity(transfer_orbit: TransferOrbit,
                        arrival_or_departure: ArrivalDeparture) \
        -> np.ndarray:
    '''
    Gets the excess velocity between the transfer orbit and a celestial
    body at some time.
    Used to patch the transfer orbit into the body orbit.
    '''
    return np_array_from_vec3(
        lib.excess_velocity_at_body(transfer_orbit.c_data,
                                    arrival_or_departure.value))


def ejection_capture_dv(body: Body, excess_velocity: np.ndarray,
                        periapsis_radius: float) -> float:
    '''
    Estimates the delta-v required to patch the transfer orbit into the body orbit.
    '''
    return lib.ejection_capture_dv(body.c_data,
                                   vec3_from_np_array(excess_velocity),
                                   periapsis_radius)


def approximate_time_of_flight(body1: Body, body2: Body) -> float:
    if body1.parent != body2.parent:
        raise ValueError("body1 and body2 must have the same parent.")
    return lib.approximate_time_of_flight(body1.c_data, body2.c_data)


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
    if body1.parent != body2.parent:
        raise ValueError("body1 and body2 must have the same parent.")
    transfer_orbit = planetary_transfer_orbit(
        body1, body2, t1, t2)

    if transfer_orbit is None:
        return np.nan

    excess_velocity = get_excess_velocity(body1, transfer_orbit, t1)
    delta_v = ejection_capture_dv(
        body1, excess_velocity,
        body1.radius + parking_orbit_alt)
    return delta_v


# standalone test
if __name__ == "__main__":
    # Test transfer from Kerbin to Duna
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1 = 5091552
    t2 = 10679760

    transfer_orbit = planetary_transfer_orbit(kerbin, duna, t1, t2)
    kerbin_excess_velocity = get_excess_velocity(
        transfer_orbit, ArrivalDeparture.DEPARTURE)

    v_inf_kerbin = np.linalg.norm(kerbin_excess_velocity)

    duna_excess_velocity = get_excess_velocity(
        transfer_orbit, ArrivalDeparture.ARRIVAL)

    v_inf_duna = np.linalg.norm(duna_excess_velocity)

    r_pe_kerbin = kerbin.radius + 70000  # 70 km parking orbit
    dv_est_kerbin = ejection_capture_dv(
        kerbin, kerbin_excess_velocity, r_pe_kerbin)
    r_pe_duna = duna.radius + 50000  # 50 km target orbit
    dv_est_duna = ejection_capture_dv(duna, duna_excess_velocity, r_pe_duna)

    print(f"Estimated ejection delta-v: {dv_est_kerbin:.2f} m/s")
    print(f"C3 wrt Kerbin: {v_inf_kerbin**2/1e6:.2f} km^2/s^2")
    print(f"Estimate capture delta-v: {dv_est_duna:.2f} m/s")
