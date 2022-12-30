# Wrapper for C code

from dataclasses import dataclass

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.c_ext_utils.process_sva_buffer import process_sva_buffer
from trajectorize.math_lib.math_interfaces import (np_array_from_vec3,
                                                   vec3_from_np_array)


@dataclass
class UniversalKeplerOrbit:
    position: np.ndarray       # Either a single position or list of positions
    velocity: np.ndarray       # Either a single velocity or list of velocities
    time: "float|np.ndarray"   # used when called vectorized
    mu: float

    def propagate(self, t: float) -> "UniversalKeplerOrbit":
        orbit_c = ffi.new("struct StateVector *", {
            "position": vec3_from_np_array(self.position),
            "velocity": vec3_from_np_array(self.velocity),
            "time": self.time
        })[0]

        new_orbit = lib.state_vec_orbit_prop(t, orbit_c, self.mu)

        new_position = np_array_from_vec3(new_orbit.position)
        new_velocity = np_array_from_vec3(new_orbit.velocity)

        return UniversalKeplerOrbit(new_position, new_velocity,
                                    self.time + t, self.mu)

    def propagate_vec(self, times: np.ndarray) -> "UniversalKeplerOrbit":
        orbit_c = ffi.new("struct StateVector *", {
            "position": vec3_from_np_array(self.position),
            "velocity": vec3_from_np_array(self.velocity),
            "time": self.time
        })[0]

        c_times = ffi.new("double[]", times.tolist())
        prop_orbit = lib.state_vec_orbit_prop_many(
            len(times), c_times, orbit_c, self.mu)

        arr = process_sva_buffer(prop_orbit, len(times))

        positions = arr[:, :3]
        velocities = arr[:, 3:6]

        return UniversalKeplerOrbit(positions, velocities,
                                    times, self.mu)
