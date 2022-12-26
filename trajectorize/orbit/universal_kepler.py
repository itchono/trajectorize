# Wrapper for C code

from dataclasses import dataclass

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.math_lib.math_interfaces import vec3_from_np_array


@dataclass
class UniversalKeplerOrbit:
    position: np.ndarray
    velocity: np.ndarray
    time: float
    mu: float

    def propagate(self, dt: float) -> "UniversalKeplerOrbit":
        new_position = np.zeros(3)
        new_velocity = np.zeros(3)

        orbit_c = ffi.new("struct StateVector *", {
            "position": vec3_from_np_array(self.position),
            "velocity": vec3_from_np_array(self.velocity),
            "time": self.time
        })

        new_orbit = lib.orbitAtTime(self.time + dt, orbit_c[0], self.mu)

        for i in range(3):
            new_position[i] = new_orbit.position.v[i]
            new_velocity[i] = new_orbit.velocity.v[i]

        return UniversalKeplerOrbit(new_position, new_velocity, self.time + dt, self.mu)
