/*
Trajectorize

Conic (classical) Keplerian orbit library

This file contains definitions for functions related to Keplerian orbits.
*/

#ifndef CONIC_KEPLER_H
#define CONIC_KEPLER_H

#include "keplerian_element_types.h"
#include "state_vector_types.h"

double kepler_solver(double M, double e);

KeplerianElements orbitFromStateVector(StateVector state_vector, double mu);
StateVector stateVectorFromOrbit(KeplerianElements orbit, double mu);
StateVectorArray stateVectorLocus(KeplerianElements orbit, double mu, int n);
KeplerianElements propagateKeplerianOrbit(KeplerianElements orbit, double dt, double mu);

double orbital_period(double semi_major_axis, double mu);
double theta_from_E(double E, double e);

#endif // CONIC_KEPLER_H