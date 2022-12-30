# Wrapper for C code
from dataclasses import dataclass
from enum import IntEnum

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.ephemeris.state_vector import StateVector


class BodyEnum(IntEnum):
    KERBOL = lib.KERBOL
    MOHO = lib.MOHO
    EVE = lib.EVE
    GILLY = lib.GILLY
    KERBIN = lib.KERBIN
    MUN = lib.MUN
    MINMUS = lib.MINMUS
    DUNA = lib.DUNA
    IKE = lib.IKE
    DRES = lib.DRES
    JOOL = lib.JOOL
    LAYTHE = lib.LAYTHE
    VALL = lib.VALL
    TYLO = lib.TYLO
    BOP = lib.BOP
    POL = lib.POL
    EELOO = lib.EELOO

# PlanetaryKeplerianElements struct class


@dataclass
class PlanetaryKeplerianElements:
    '''
    Equivalent of C PlanetaryKeplerianElements struct.
    '''
    semi_major_axis: float
    eccentricity: float
    inclination: float
    longitude_of_ascending_node: float
    argument_of_periapsis: float
    mean_anomaly_at_epoch: float

    @classmethod
    def from_c_data(cls, cdata):
        return cls(cdata.semi_major_axis,
                   cdata.eccentricity,
                   cdata.inclination,
                   cdata.longitude_of_ascending_node,
                   cdata.argument_of_periapsis,
                   cdata.mean_anomaly_at_epoch)

    @property
    def c_data(self):
        '''
        Returns C struct compatible with library functions.
        '''
        return ffi.new('PlanetaryKeplerianElements *', self.__dict__)[0]


# Planets

@ dataclass
class Body:
    body_id: BodyEnum
    parent_id: BodyEnum
    mass: float
    mu: float
    radius: float
    atmosphere_height: float
    orbit: PlanetaryKeplerianElements
    soi_radius: float
    colour: int

    @ property
    def name(self) -> str:
        return BodyEnum(self.body_id).name.title()

    @ property
    def colour_hex(self) -> str:
        # returns as hex string
        return f"#{self.colour:06x}"

    @classmethod
    def from_identifier(cls, identifier: "BodyEnum|int") -> "Body":
        '''
        Create a Body object from an identifier
        '''
        if identifier not in BodyEnum:
            raise ValueError("Invalid planet")

        body = lib.kerbol_system_bodies[int(identifier)]

        return cls(BodyEnum(body.body_id),
                   BodyEnum(body.parent_id),
                   body.mass,
                   body.mu,
                   body.radius,
                   body.atmosphere_height,
                   PlanetaryKeplerianElements.from_c_data(body.orbit),
                   body.soi_radius,
                   body.colour)

    @ classmethod
    def from_name(cls, name: str) -> "Body":
        '''
        Create a Body object from a string
        '''
        name_dict = {k.casefold(): v for k, v in BodyEnum.__members__.items()}

        if name.casefold() not in name_dict:
            raise ValueError("Invalid planet")

        return cls.from_identifier(name_dict[name.casefold()])

    @ property
    def c_data(self):
        '''
        Returns C struct compatible with library functions.
        '''
        return lib.kerbol_system_bodies[self.body_id.value]

    def orbit_locus(self, num_points: int = 1000) -> np.ndarray:
        '''
        Return a (N, 3) array of points on the orbit of the body
        in state space relative to its parent.
        '''
        parent = Body.from_identifier(self.parent_id)
        state_vec_arr = lib.pke_state_locus(self.orbit.c_data, parent.mu,
                                            num_points)

        # process memory buffer
        # Format: [x, y, z, vx, vy, vz, t] x n
        arr = np.frombuffer(ffi.buffer(state_vec_arr.mem_buffer, 7 *
                                       8 * num_points), dtype=np.float64)
        arr.shape = (num_points, 7)
        positions = np.copy(arr[:, :3])  # copy to avoid memory leak

        lib.free_StateVectorArray(state_vec_arr)

        return positions

    @property
    def parent(self) -> "Body":
        '''
        Returns the parent body of this body.
        '''
        return Body.from_identifier(self.parent_id)

    @classmethod
    def all_bodies(cls) -> "list[Body]":
        '''
        Returns a list of all bodies in the system.
        '''
        return [cls.from_identifier(i) for i in BodyEnum]

    @classmethod
    def planets(cls) -> "list[Body]":
        '''
        Returns a list of all planets in the system
        (i.e. Kerbol is their parent)
        '''
        bodies = cls.all_bodies()
        return [body for body in bodies if body.parent_id == BodyEnum.KERBOL
                and body.body_id != BodyEnum.KERBOL]


def state_vector_at_time(t: float, parent: BodyEnum,
                         child: BodyEnum) -> StateVector:
    cdata = lib.get_rel_state_at_time(t, parent.value, child.value)
    return StateVector.from_c_data(cdata)
