/*
Trajectorize

Lambert's Problem

This header file contains definitions for Lambert's Problem
*/

#ifndef LAMBERT_H
#define LAMBERT_H

#include "orbit_math_types.h"

typedef struct LambertSolution {
    double v1[3];
    double v2[3];
    double dt;
} LambertSolution;

// Lambert's Problem

LambertSolution lambert(Vector3 r1, Vector3 r2, double dt, double mu);


#endif // LAMBERT_H