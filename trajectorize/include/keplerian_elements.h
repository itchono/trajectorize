/*
Trajectorize

Keplerian Elements Struct

This header file contains a struct for storing Keplerian elements.
*/

#ifndef TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H
#define TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H

#include "kerbol_system_types.h"

typedef struct KeplerianElements
{
    Body body;
    double semi_major_axis;
    double eccentricity;
    double inclination;
    double longitude_of_ascending_node;
    double argument_of_periapsis;
    double true_anomaly;
} KeplerianElements;

#endif // TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H