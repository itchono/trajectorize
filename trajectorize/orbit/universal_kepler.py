# Wrapper for C code

from ._c_universal_kepler import ffi, lib
import numpy as np

class UniversalKeplerOrbit:
    def __init__(self, position: np.ndarray, velocity: np.ndarray, time: float, mu: float):
        self.position = position
        self.velocity = velocity
        self.time = time
        self.mu = mu
    def propagate(self, dt: float) -> "UniversalKeplerOrbit":
        new_position = np.zeros(3)
        new_velocity = np.zeros(3)

        # Convert to C arrays
        position_c = ffi.new("double[3]", self.position.tolist())
        velocity_c = ffi.new("double[3]", self.velocity.tolist())

        orbit_c = ffi.new("struct UniversalKeplerOrbit *", {
            "position": lib.vec_from_double_array(position_c),
            "velocity": lib.vec_from_double_array(velocity_c),
            "time": self.time,
            "mu": self.mu
        })

        new_orbit = lib.universalOrbitatTime(self.time + dt, orbit_c[0])

        for i in range(3):
            new_position[i] = new_orbit.position.v[i]
            new_velocity[i] = new_orbit.velocity.v[i]

        return UniversalKeplerOrbit(new_position, new_velocity, self.time + dt, self.mu)