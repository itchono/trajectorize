/*
Trajectorize

State Vector Types

This file contains typedefs related to state vector types.
*/

#ifndef STATE_VECTOR_TYPES_H
#define STATE_VECTOR_TYPES_H

#include "vec_math_types.h"

typedef struct StateVector
{
    Vector3 position;
    Vector3 velocity;
    double time;
} StateVector;

typedef struct StateVectorArray
{
    int n;
    StateVector *states;
    double *mem_buffer;
    // stores underlying states as a (N x 7) matrix, which can be
    // re-interpreted as a set of StateVectors
} StateVectorArray;

void free_StateVectorArray(StateVectorArray sva);

#endif // STATE_VECTOR_TYPES_H