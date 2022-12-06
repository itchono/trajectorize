/*
Trajectorize

Universal Keplerian Orbit

This header file contains definitions for the Universal Keplerian Orbit
*/

#ifndef UNIVERSAL_KEPLER_H
#define UNIVERSAL_KEPLER_H

#include "state_vector_types.h"

double stumpS(double z);
double stumpC(double z);

double universalAnomaly(double t, StateVector orbit, double mu);
StateVector orbitAtTime(double t, StateVector orbit, double mu);

#endif // UNIVERSAL_KEPLER_H