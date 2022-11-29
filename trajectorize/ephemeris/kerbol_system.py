# Wrapper for C code
from ._c_kerbol_system import ffi, lib
from enum import IntEnum

# Path: trajectorize/ephemeris/kerbol_system_bodies.c

# Planets
Kerbol = lib.Kerbol
Moho = lib.Moho
Eve = lib.Eve
Gilly = lib.Gilly
Kerbin = lib.Kerbin
Mun = lib.Mun
Minmus = lib.Minmus
Duna = lib.Duna
Ike = lib.Ike
Dres = lib.Dres
Jool = lib.Jool
Laythe = lib.Laythe
Vall = lib.Vall
Tylo = lib.Tylo
Bop = lib.Bop
Pol = lib.Pol
Eeloo = lib.Eeloo

# Enums


class KerbolSystemID(IntEnum):
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
