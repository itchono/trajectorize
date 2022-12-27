# Wrapper for C code
from dataclasses import dataclass

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.math_lib.math_interfaces import vec3_from_np_array


@dataclass
class KeplerianElements:
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
        Creates a KeplerianElements object from a celestial body and a
        universal time.
        '''
        # Body orbits are stored as PlanetaryKeplerianElements, which differ
        # in that they store mean anomaly at epoch instead of true anomaly.

        # Run kepler solver to get true anomaly

        E = solve_kepler_equation(
            body.orbit.mean_anomaly_at_epoch, body.orbit.eccentricity)
        theta = lib.theta_from_E(
            E, body.orbit.eccentricity)

        return cls(body.orbit.semi_major_axis,
                   body.orbit.eccentricity,
                   body.orbit.inclination,
                   body.orbit.longitude_of_ascending_node,
                   body.orbit.argument_of_periapsis,
                   theta,
                   ut)


@dataclass
class KeplerianOrbit:
    orbit: KeplerianElements
    body: Body

    def get_locus(self, n: int) -> np.ndarray:
        '''
        Returns the locus of the orbit in state space.
        '''
        orbit = ffi.new('struct KeplerianElements *', self.orbit.__dict__)[0]

        state_vec_arr = lib.stateVectorLocus(orbit, self.body.mu, n)

        # process memory buffer
        # Format: [x, y, z, vx, vy, vz, t] x n
        arr = np.frombuffer(ffi.buffer(state_vec_arr.mem_buffer, 7 *
                                       8 * n), dtype=np.float64)
        arr.shape = (n, 7)
        positions = np.copy(arr[:, :3])  # copy to avoid memory leak

        # Free memory
        lib.freeStateVectorArray(state_vec_arr)

        return positions

    @property
    def T(self) -> float:
        '''
        Orbital period
        '''
        return lib.orbital_period(self.orbit.semi_major_axis, self.body.mu)

    @classmethod
    def from_state_vector(cls, position: np.ndarray, velocity: np.ndarray,
                          epoch: float, body: Body) -> "KeplerianOrbit":
        '''
        Returns the orbit from a state vector.
        '''
        state_vec = ffi.new('struct StateVector *', {
            'position': vec3_from_np_array(position),
            'velocity': vec3_from_np_array(velocity),
            'time': epoch
        })[0]

        orbit = lib.orbitFromStateVector(state_vec, body.mu)

        return cls(orbit, body)


def solve_kepler_equation(M: float, e: float) -> float:
    result: float = lib.kepler_solver(M, e)
    return result
