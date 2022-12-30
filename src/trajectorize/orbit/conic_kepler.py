# Wrapper for C code
from dataclasses import dataclass

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.c_ext_utils.process_sva_buffer import process_sva_buffer
from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.ephemeris.state_vector import StateVector
from trajectorize.math_lib.math_interfaces import vec3_from_np_array


@dataclass
class KeplerianElements:
    '''
    Equivalent of C KeplerianElements struct.
    '''
    semi_major_axis: float
    eccentricity: float
    inclination: float
    longitude_of_ascending_node: float
    argument_of_periapsis: float
    true_anomaly: float
    epoch: float

    @classmethod
    def from_celestial_body(cls, body: Body, ut: float):
        '''
        Creates a KeplerianElements object from a celestial body
        at some time.
        '''

        # Use library function: ke_from_pke
        pke_c = body.orbit.c_data

        ke_c = lib.ke_from_pke(pke_c, ut, body.mu)
        return cls.from_c_data(ke_c)

    @classmethod
    def from_c_data(cls, cdata):
        return cls(cdata.semi_major_axis,
                   cdata.eccentricity,
                   cdata.inclination,
                   cdata.longitude_of_ascending_node,
                   cdata.argument_of_periapsis,
                   cdata.true_anomaly,
                   cdata.epoch)

    @property
    def c_data(self):
        '''
        Returns C struct compatible with library functions.
        '''
        return ffi.new('struct KeplerianElements *', self.__dict__)[0]


@ dataclass
class KeplerianOrbit:
    '''
    Convenience class storing a KeplerianElements object and a Body object.

    Used to perform composite calculations that require both Keplerian
    Elements as well as a central body's properties (mass, radius, etc.)
    '''
    ke: KeplerianElements
    parent_body: Body

    def get_locus(self, n: int) -> np.ndarray:
        '''
        Returns the locus of the orbit in state space.
        '''
        state_vec_arr = lib.ke_state_locus(
            self.ke.c_data, self.parent_body.mu, n)
        arr = process_sva_buffer(state_vec_arr, n)

        return arr[:, 0:3]

    @ property
    def T(self) -> float:
        '''
        Orbital period
        '''
        return lib.orbital_period(self.ke.semi_major_axis, self.parent_body.mu)

    @ classmethod
    def from_state_vector(cls, position: np.ndarray, velocity: np.ndarray,
                          epoch: float, parent_body: Body) -> "KeplerianOrbit":
        '''
        Returns the orbit from a state vector.
        '''
        state_vec = ffi.new('struct StateVector *', {
            'position': vec3_from_np_array(position),
            'velocity': vec3_from_np_array(velocity),
            'time': epoch
        })[0]

        ke = KeplerianElements.from_c_data(
            lib.ke_from_state_vector(state_vec, parent_body.mu))

        return cls(ke, parent_body)

    @property
    def state_vector(self):
        sv_c = lib.state_vector_from_ke(self.ke.c_data, self.parent_body.mu)
        return StateVector.from_c_data(sv_c)

    def propagate(self, t: float) -> "KeplerianOrbit":
        sol = lib.ke_orbit_prop(t, self.ke.c_data, self.parent_body.mu)

        ke = KeplerianElements.from_c_data(sol.ke)
        return KeplerianOrbit(ke, self.parent_body)

    def propagate_vec(self, times: np.ndarray) -> np.ndarray:
        c_times = ffi.new("double[]", times.tolist())
        prop_orbit = lib.ke_orbit_prop_many(len(times),
                                            c_times,
                                            self.ke.c_data,
                                            self.parent_body.mu)

        arr = process_sva_buffer(prop_orbit, len(times))
        return arr[:, 0:3]


def solve_kepler_equation(M: float, e: float) -> float:
    result: float = lib.E_from_M(M, e)
    return result
