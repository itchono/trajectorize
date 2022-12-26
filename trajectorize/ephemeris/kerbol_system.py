# Wrapper for C code
from enum import IntEnum

from trajectorize._c_extension import ffi, lib
from trajectorize.ephemeris.state_vector import StateVector

# Path: trajectorize/ephemeris/kerbol_system_bodies.c

# Enums


class KerbolSystemBodyEnum(IntEnum):
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

# Planets


class Body:
    def __init__(self, body_id: KerbolSystemBodyEnum):
        body_dict = {
            KerbolSystemBodyEnum.KERBOL: lib.Kerbol,
            KerbolSystemBodyEnum.MOHO: lib.Moho,
            KerbolSystemBodyEnum.EVE: lib.Eve,
            KerbolSystemBodyEnum.GILLY: lib.Gilly,
            KerbolSystemBodyEnum.KERBIN: lib.Kerbin,
            KerbolSystemBodyEnum.MUN: lib.Mun,
            KerbolSystemBodyEnum.MINMUS: lib.Minmus,
            KerbolSystemBodyEnum.DUNA: lib.Duna,
            KerbolSystemBodyEnum.IKE: lib.Ike,
            KerbolSystemBodyEnum.DRES: lib.Dres,
            KerbolSystemBodyEnum.JOOL: lib.Jool,
            KerbolSystemBodyEnum.LAYTHE: lib.Laythe,
            KerbolSystemBodyEnum.VALL: lib.Vall,
            KerbolSystemBodyEnum.TYLO: lib.Tylo,
            KerbolSystemBodyEnum.BOP: lib.Bop,
            KerbolSystemBodyEnum.POL: lib.Pol,
            KerbolSystemBodyEnum.EELOO: lib.Eeloo
        }

        if body_id not in body_dict:
            raise ValueError("Invalid planet")
        self._body = body_dict[body_id]
        self.name = KerbolSystemBodyEnum(body_id).name

    @property
    def body(self):
        return self._body.body_id

    @property
    def parent(self):
        return self._body.parent_id.body_id

    @property
    def mass(self):
        return self._body.mass

    @property
    def mu(self):
        return self._body.mu

    @property
    def radius(self):
        return self._body.radius

    @property
    def atmosphere_height(self):
        return self._body.atmosphere_height

    @property
    def orbit(self):
        return self._body.orbit

    @property
    def soi_radius(self):
        return self._body.soi_radius

    def __repr__(self):
        return f"Body({self.name})"

    def __str__(self):
        return (f"Body: {self.name}\n"
                f"Parent: {KerbolSystemBodyEnum(self.parent_id).name}\n"
                f"Mass: {self.mass} kg\n"
                f"Mu: {self.mu} m^3/s^2\n"
                f"Radius: {self.radius} m\n"
                f"Atmosphere Height: {self.atmosphere_height} m\n"
                f"Orbit:\n\t"
                f"Semi-major Axis: {self.orbit.semi_major_axis} m\n\t"
                f"Eccentricity: {self.orbit.eccentricity}\n\t"
                f"Inclination: {self.orbit.inclination} rad\n\t"
                f"Longitude of the Ascending Node: {self.orbit.longitude_of_the_ascending_node} rad\n\t"
                f"Argument of Periapsis: {self.orbit.argument_of_periapsis} rad\n\t"
                f"Mean Anomaly at Epoch: {self.orbit.mean_anomaly_at_epoch} rad\n\t"
                f"SOI Radius: {self.soi_radius} m")

    @classmethod
    def from_name(cls, name: str):
        '''
        Create a Body object from a string
        '''
        name_dict = {
            "Kerbol": KerbolSystemBodyEnum.KERBOL,
            "Moho": KerbolSystemBodyEnum.MOHO,
            "Eve": KerbolSystemBodyEnum.EVE,
            "Gilly": KerbolSystemBodyEnum.GILLY,
            "Kerbin": KerbolSystemBodyEnum.KERBIN,
            "Mun": KerbolSystemBodyEnum.MUN,
            "Minmus": KerbolSystemBodyEnum.MINMUS,
            "Duna": KerbolSystemBodyEnum.DUNA,
            "Ike": KerbolSystemBodyEnum.IKE,
            "Dres": KerbolSystemBodyEnum.DRES,
            "Jool": KerbolSystemBodyEnum.JOOL,
            "Laythe": KerbolSystemBodyEnum.LAYTHE,
            "Vall": KerbolSystemBodyEnum.VALL,
            "Tylo": KerbolSystemBodyEnum.TYLO,
            "Bop": KerbolSystemBodyEnum.BOP,
            "Pol": KerbolSystemBodyEnum.POL,
            "Eeloo": KerbolSystemBodyEnum.EELOO
        }

        if name not in name_dict:
            raise ValueError("Invalid planet")

        return cls(name_dict[name])


def state_vector_at_time(t: float, parent: KerbolSystemBodyEnum,
                         child: KerbolSystemBodyEnum) -> StateVector:
    cdata = lib.get_rel_state_at_time(t, parent.value, child.value)
    return StateVector.from_cdata(cdata)
