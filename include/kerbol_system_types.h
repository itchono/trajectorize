/*
Trajectorize

KSP Kerbol System Types

This file contains type definitions for the Kerbol system bodies.
*/

#ifndef TRAJECTORIZE_EPHEMERIS_KERBOL_SYSTEM_TYPES_H
#define TRAJECTORIZE_EPHEMERIS_KERBOL_SYSTEM_TYPES_H
#include "keplerian_elements.h"

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
    enum BodyEnum body;
    enum BodyEnum parent;
    double mass;
    double mu;
    double radius;
    double atmosphere_height;
    PlanetaryKeplerianElements orbit;
    double soi_radius;
} Body;

#endif // TRAJECTORIZE_EPHEMERIS_KERBOL_SYSTEM_TYPES_H