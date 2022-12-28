/*
Trajectorize

Universal Keplerian Orbit

This header file contains definitions for the Universal Keplerian Orbit
*/

#ifndef UNIVERSAL_KEPLER_H
#define UNIVERSAL_KEPLER_H

#include "state_vector_types.h"

double univeral_anomaly_at_time(double t, StateVector orbit, double mu);
StateVector state_vec_orbit_prop(double t, StateVector orbit, double mu);
StateVectorArray state_vec_orbit_prop_many(int n, double times[], StateVector orbit, double mu);

#endif // UNIVERSAL_KEPLER_H