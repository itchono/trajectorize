/*
Trajectorize

Conic (classical) Keplerian orbit library

This file contains definitions for functions related to Keplerian orbits.
*/

#ifndef CONIC_KEPLER_H
#define CONIC_KEPLER_H

#include "keplerian_element_types.h"
#include "state_vector_types.h"

double orbital_period(double semi_major_axis, double mu);
double theta_from_E(double E, double e);
double E_from_M(double M, double e);     // Kepler's equation
double theta_from_M(double M, double e); // Kepler's equation, but with theta instead of E
double E_from_theta(double theta, double e);
double M_from_theta(double theta, double e);
double M_from_E(double E, double e);

KeplerianElements ke_from_state_vector(StateVector state_vector, double mu);
StateVector state_vector_from_ke(KeplerianElements orbit, double mu);
StateVectorArray ke_state_locus(KeplerianElements orbit, double mu, int n);
KeplerianElements ke_orbit_prop(double t, KeplerianElements orbit, double mu);
StateVectorArray ke_orbit_prop_many(int n, double times[], KeplerianElements orbit, double mu);

#endif // CONIC_KEPLER_H