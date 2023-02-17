/*
Trajectorize

Delta v estimator
*/

#ifndef DELTA_V_ESTIMATE_H
#define DELTA_V_ESTIMATE_H

#include "kerbol_system_types.h"
#include "vec_math_types.h"

/**
 * @brief Estimate the delta-v required to eject from/capture into a body
 *
 * @param body
 * @param v_inf velocity vector in m [3]
 * @param periapsis radius of periapsis in m
 * @return double
 */
double ejection_capture_dv(Body body, Vector3 v_inf, double periapsis);

#endif // DELTA_V_ESTIMATE_H