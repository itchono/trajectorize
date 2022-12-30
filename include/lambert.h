/*
Trajectorize

Lambert's Problem

This header file contains definitions for Lambert's Problem
*/

#ifndef LAMBERT_H
#define LAMBERT_H

#include "vec_math_types.h"

typedef struct LambertSolution
{
    Vector3 v1;
    Vector3 v2;
    double dt;
} LambertSolution;

// Lambert's Problem

enum TrajectoryType
{
    PROGRADE,
    RETROGRADE
};

LambertSolution lambert(Vector3 R1, Vector3 R2, double dt, double mu, enum TrajectoryType type);

#endif // LAMBERT_H