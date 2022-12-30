/*
Trajectorize

Delta v estimator
*/

#ifndef DELTA_V_ESTIMATE_H
#define DELTA_V_ESTIMATE_H

#include "kerbol_system_types.h"
#include "vec_math_types.h"

double delta_v_req(Body body, double excess_velocity, double periapsis);

#endif // DELTA_V_ESTIMATE_H