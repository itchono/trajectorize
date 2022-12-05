/*
Trajectorize

Universal Keplerian Orbit

This header file contains definitions for the Universal Keplerian Orbit
*/

#ifndef UNIVERSAL_KEPLER_H
#define UNIVERSAL_KEPLER_H

#include "orbit_math.h"

typedef struct UniversalKeplerOrbit {
    Vector3 position;
    Vector3 velocity;
    double time;
    double mu;
} UniversalKeplerOrbit;


double stumpS(double z);
double stumpC(double z);

double universalAnomaly(double t, UniversalKeplerOrbit orbit);
UniversalKeplerOrbit orbitAtTime(double t, UniversalKeplerOrbit orbit);

#endif // UNIVERSAL_KEPLER_H