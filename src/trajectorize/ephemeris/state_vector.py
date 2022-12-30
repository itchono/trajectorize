from dataclasses import dataclass

import numpy as np

from trajectorize.math_lib.math_interfaces import np_array_from_vec3


@dataclass
class StateVector:
    position: np.ndarray
    velocity: np.ndarray
    time: float

    @classmethod
    def from_c_data(cls: "StateVector", cdata):
        return cls(np_array_from_vec3(cdata.position),
                   np_array_from_vec3(cdata.velocity),
                   time=cdata.time)
