/*
Trajectorize

Planetary Keplerian Elements

This header file contains a struct for storing planetary Keplerian elements.

*/

#ifndef PLANETARY_KEPLERIAN_ELEMENTS_H
#define PLANETARY_KEPLERIAN_ELEMENTS_H

// Used for planets because they are expressed with an initial mean anomaly
typedef struct PlanetaryKeplerianElements
{
    double semi_major_axis;
    double eccentricity;
    double inclination;
    double longitude_of_ascending_node;
    double argument_of_periapsis;
    double mean_anomaly_at_epoch;
} PlanetaryKeplerianElements;

#endif // PLANETARY_KEPLERIAN_ELEMENTS_H