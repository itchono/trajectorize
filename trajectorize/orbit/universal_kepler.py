# Wrapper for C code

from ._c_universal_kepler import ffi, lib
import numpy as np


def _vec3_from_np_array(np_array: np.ndarray) -> ffi.CData:
    return ffi.new("Vector3*", {"v": np_array.tolist()})[0]


class UniversalKeplerOrbit:
    def __init__(self, position: np.ndarray, velocity: np.ndarray,
                 time: float, mu: float):
        self.position = position
        self.velocity = velocity
        self.time = time
        self.mu = mu

    def propagate(self, dt: float) -> "UniversalKeplerOrbit":
        new_position = np.zeros(3)
        new_velocity = np.zeros(3)

        orbit_c = ffi.new("struct UniversalKeplerOrbit *", {
            "position": _vec3_from_np_array(self.position),
            "velocity": _vec3_from_np_array(self.velocity),
            "time": self.time,
            "mu": self.mu
        })

        new_orbit = lib.orbitAtTime(self.time + dt, orbit_c[0])

        for i in range(3):
            new_position[i] = new_orbit.position.v[i]
            new_velocity[i] = new_orbit.velocity.v[i]

        return UniversalKeplerOrbit(new_position, new_velocity, self.time + dt, self.mu)
