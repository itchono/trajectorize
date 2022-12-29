/*
Trajectorize

Transfer Orbit Calculator

Header file for functions to calculate transfer orbits between two bodies in the Kerbol system.
*/

#ifndef TRANSFER_ORBIT_H
#define TRANSFER_ORBIT_H

#include "keplerian_element_types.h"
#include "kerbol_system_types.h"

KeplerianElements planetary_transfer_orbit(Body body1, Body body2, double t1, double t2);

#endif // TRANSFER_ORBIT_H