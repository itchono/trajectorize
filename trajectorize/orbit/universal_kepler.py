# Wrapper for C code

from dataclasses import dataclass

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)


@dataclass
class UniversalKeplerOrbit:
    position: np.ndarray       # Either a single position or list of positions
    velocity: np.ndarray       # Either a single velocity or list of velocities
    time: "float|np.ndarray"   # used when called vectorized
    mu: float

    def propagate(self, dt: float) -> "UniversalKeplerOrbit":
        orbit_c = ffi.new("struct StateVector *", {
            "position": vec3_from_np_array(self.position),
            "velocity": vec3_from_np_array(self.velocity),
            "time": self.time
        })[0]

        new_orbit = lib.state_vec_orbit_prop(self.time + dt, orbit_c, self.mu)

        new_position = np_array_from_vec3(new_orbit.position)
        new_velocity = np_array_from_vec3(new_orbit.velocity)

        return UniversalKeplerOrbit(new_position, new_velocity,
                                    self.time + dt, self.mu)

    def propagate_vec(self, delta_times: np.ndarray) -> "UniversalKeplerOrbit":
        orbit_c = ffi.new("struct StateVector *", {
            "position": vec3_from_np_array(self.position),
            "velocity": vec3_from_np_array(self.velocity),
            "time": self.time
        })[0]

        c_times = ffi.new("double[]", delta_times.tolist())
        prop_orbit = lib.state_vec_orbit_prop_many(
            len(delta_times), c_times, orbit_c, self.mu)

        # Process memory buffer
        # Format: [x, y, z, vx, vy, vz, t] x n
        arr = np.frombuffer(ffi.buffer(prop_orbit.mem_buffer, 7 *
                                       8 * len(delta_times)), dtype=np.float64)
        arr.shape = (len(delta_times), 7)
        positions = np.copy(arr[:, :3])  # copy to avoid memory leak
        velocities = np.copy(arr[:, 3:6])

        # Free memory
        lib.free_StateVectorArray(prop_orbit)

        return UniversalKeplerOrbit(positions, velocities,
                                    self.time + delta_times, self.mu)
