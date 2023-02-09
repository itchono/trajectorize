/*
Trajectorize

Transfer Orbit Calculator

Header file for functions to calculate transfer orbits between two bodies in the Kerbol system.
*/

#ifndef TRANSFER_ORBIT_H
#define TRANSFER_ORBIT_H

#include "keplerian_element_types.h"
#include "kerbol_system_types.h"
#include "vec_math_types.h"

#include <stdbool.h>


typedef struct TransferOrbit
{
    KeplerianElements ke;
    bool valid;
} TransferOrbit;

/**
 * @brief Computes a planetary transfer orbit between two bodies orbiting a common parent.
 * Solves Lambert's problem to find an orbit starting at body 1 and t1, going to
 * body 2 at t2
 * @param body1 departing body
 * @param body2 arriving body
 * @param t1 time of departure, ut (s)
 * @param t2 time of arrival, ut (s)
 * @return TransferOrbit struct, containing KeplerianElements if the solution obtained is valid.
 */
TransferOrbit planetary_transfer_orbit(Body body1, Body body2, double t1, double t2);

/**
 * @brief Computes excess hyperbolic velocity (v_infinity) at SOI interface
 * @param body body to compare with
 * @param transfer_orbit transfer orbit to compare with
 * @param ut universal timestamp - should be either the t1 or t2 value used to generate the transfer orbit
 * @return excess velocity vector (m/s)
 */
Vector3 excess_velocity_at_body(Body body, KeplerianElements transfer_orbit, double ut);

/**
 * @brief Gets heurisitic time of flight from body1 to body2 using an ideal Hohmann transfer.
 * Actual time of flight will vary. This is a good starting point for grid-searching.
 * @param body1 first body
 * @param body2 second body
 * @return time of flight in seconds
 * 
 * @note formula used: half-period of Hohmann transfer orbit
 */
double approximate_time_of_flight(Body body1, Body body2);

#endif // TRANSFER_ORBIT_H