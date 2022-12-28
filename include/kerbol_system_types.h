/*
Trajectorize

KSP Kerbol System Types

This file contains type definitions for the Kerbol system bodies.
*/

#ifndef EPHEMERIS_KERBOL_SYSTEM_TYPES_H
#define EPHEMERIS_KERBOL_SYSTEM_TYPES_H
#include "keplerian_element_types.h"

enum BodyEnum
{
    KERBOL,
    MOHO,
    EVE,
    GILLY,
    KERBIN,
    MUN,
    MINMUS,
    DUNA,
    IKE,
    DRES,
    JOOL,
    LAYTHE,
    VALL,
    TYLO,
    BOP,
    POL,
    EELOO,
};

typedef struct Body
{
    enum BodyEnum body_id;
    enum BodyEnum parent_id;
    double mass;
    double mu;
    double radius;
    double atmosphere_height;
    PlanetaryKeplerianElements orbit;
    double soi_radius;
    int colour; // stored as a hex value (3 bytes)
} Body;

#endif // EPHEMERIS_KERBOL_SYSTEM_TYPES_H