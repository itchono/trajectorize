/*
Trajectorize

Keplerian Elements Struct

This header file contains a struct for storing Keplerian elements.
*/

#ifndef KEPLERIAN_ELEMENT_TYPES_H
#define KEPLERIAN_ELEMENT_TYPES_H

typedef struct KeplerianElements
{
    double semi_major_axis;
    double eccentricity;
    double inclination;
    double longitude_of_ascending_node;
    double argument_of_periapsis;
    double true_anomaly;
    double epoch;
} KeplerianElements;

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

#endif // KEPLERIAN_ELEMENT_TYPES_H