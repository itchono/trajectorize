/*
Trajectorize

Keplerian Elements Struct

This header file contains a struct for storing Keplerian elements.
*/

#ifndef TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H
#define TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H

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

typedef struct KeplerianElements
{
    double semi_major_axis;
    double eccentricity;
    double inclination;
    double longitude_of_ascending_node;
    double argument_of_periapsis;
    double true_anomaly;
} KeplerianElements;

typedef struct UniversalKeplerianElements
{
    double alpha;
    double eccentricity;
    double inclination;
    double longitude_of_ascending_node;
    double argument_of_periapsis;
    double universal_anomaly;
} UniversalKeplerianElements;

#endif // TRAJECTORIZE_ORBIT_KEPLERIAN_ELEMENTS_H