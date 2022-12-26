from dataclasses import dataclass

import numpy as np


@dataclass
class StateVector:
    position: np.ndarray
    velocity: np.ndarray
    time: float

    @classmethod
    def from_cdata(cls: "StateVector", cdata):
        
        position = np.zeros(3)
        velocity = np.zeros(3)
        
        for i in range(3):
            position[i] = cdata.position.v[i]
            velocity[i] = cdata.velocity.v[i]
        
        return StateVector(position,
                           velocity,
                           time=cdata.time)