/*
Trajectorize

Conic (classical) Keplerian orbit library

This file contains definitions for functions related to Keplerian orbits.
*/

#ifndef CONIC_KEPLER_H
#define CONIC_KEPLER_H

#include "keplerian_elements.h"
#include "state_vector_types.h"

double kepler_solver(double M, double e);

KeplerianElements orbitFromStateVector(StateVector state_vector, double mu);
StateVector stateVectorFromOrbit(KeplerianElements orbit, double mu);

#endif // CONIC_KEPLER_H