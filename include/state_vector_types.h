/*
Trajectorize

State Vector Types

This file contains typedefs related to state vector types.
*/

#ifndef STATE_VECTOR_TYPES_H
#define STATE_VECTOR_TYPES_H

#include "orbit_math_types.h"

typedef struct StateVector
{
    Vector3 position;
    Vector3 velocity;
    double time;
} StateVector;

#endif // STATE_VECTOR_TYPES_H