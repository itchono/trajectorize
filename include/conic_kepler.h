/*
Trajectorize

Conic (classical) Keplerian orbit library

This file contains definitions for functions related to Keplerian orbits.
*/

#ifndef CONIC_KEPLER_H
#define CONIC_KEPLER_H

#include "keplerian_element_types.h"
#include "state_vector_types.h"

/**
 * @brief Get orbital period of a Keplerian orbit
 *
 * @param semi_major_axis *ASSUMES orbit is elliptical, so that a > 0
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @return double orbital period in seconds
 */
double orbital_period(double semi_major_axis, double mu);

/**
 * @brief True anomaly given elliptical anomaly
 *
 * @param E
 * @param e
 * @return double
 */
double theta_from_E(double E, double e);

/**
 * @brief Elliptical anomaly given mean anomaly
 * Solves Kepler's equation (iterative solution)
 *
 * @param M
 * @param e
 * @return double
 */
double E_from_M(double M, double e);

/**
 * @brief True anomaly given mean anomaly
 * Solves Kepler's equation
 *
 * @param M
 * @param e
 * @return double
 */
double theta_from_M(double M, double e);

/**
 * @brief Elliptical anomaly given true anomaly
 *
 * @param theta
 * @param e
 * @return double
 */
double E_from_theta(double theta, double e);

/**
 * @brief Mean anomaly given true anomaly
 *
 * @param theta
 * @param e
 * @return double
 */
double M_from_theta(double theta, double e);

/**
 * @brief Mean anomaly given true anomaly
 *
 * @param E
 * @param e
 * @return double
 */
double M_from_E(double E, double e);

/**
 * @brief Convert a state vector to a set of Keplerian elements
 * the state vector is provided at a specific instant in time.
 *
 * @param state_vector
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @return KeplerianElements
 */
KeplerianElements ke_from_state_vector(StateVector state_vector, double mu);

/**
 * @brief Convert a set of Keplerian elements to a state vector, evaluated
 * at a specific true anomaly.
 *
 * @param orbit
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @param theta
 * @return StateVector
 */
StateVector state_vector_at_true_anomaly(KeplerianElements orbit, double mu, double theta);

/**
 * @brief Convert a set of Keplerian elements to a state vector
 * the orbit is provided at a specific instant in time.
 *
 * @param orbit
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @return StateVector
 */
StateVector state_vector_from_ke(KeplerianElements orbit, double mu);

/**
 * @brief Returns an array of points corresponding to the locus of points
 * in an elliptical orbit
 *
 * @param orbit
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @param n
 * @return StateVectorArray
 */
StateVectorArray ke_state_locus(KeplerianElements orbit, double mu, int n);

/**
 * @brief Evaluate a Keplerian orbit at a future or past point in time,
 * returning Keplerian elements at that time
 *
 * @param t universal time, in seconds since epoch
 * @param orbit
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @return KeplerianElements
 */
KeplerianElements ke_orbit_prop(double t, KeplerianElements orbit, double mu);

/**
 * @brief Evaluate a Keplerian orbit at many points in time, returning a
 * state vector array
 *
 * @param n
 * @param times universal time, in seconds since epoch
 * @param orbit
 * @param mu standard gravitational parameter of the parent body (GM) in m^3/s^2
 * @return StateVectorArray
 */
StateVectorArray ke_orbit_prop_many(int n, double times[], KeplerianElements orbit, double mu);

/**
 * @brief Returns a hyperbolic trajectory given a velocity vector at infinity
 * around a body with GM = mu
 *
 * @param v_inf
 * @param r_pe
 * @param mu
 * @return KeplerianElements
 */
KeplerianElements fit_hyperbolic_trajectory(Vector3 v_inf, double r_pe, double mu);

/**
 * @brief Returns the state vector of a hyperbolic orbit at 99% of infinity
 *
 * @param orbit
 * @param mu
 * @return StateVector
 */
StateVector ke_hyperbolic_at_infinity(KeplerianElements orbit, double mu);

#endif // CONIC_KEPLER_H