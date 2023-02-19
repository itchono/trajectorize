#include "delta_v_estimate.h"
#include "vec_math.h"

#include <math.h>

double ejection_capture_dv(Body body, Vector3 v_inf, double periapsis)
{
    // Estimate the delta-v required to eject from/capture into a body
    // with a circular orbit at periapsis matching inclination and RAAN

    // Calculate the velocity of the circular orbit
    double v_circ = sqrt(body.mu / periapsis);

    double v_peri = sqrt(vec_dot(v_inf, v_inf) + 2 * body.mu / periapsis);

    return v_peri - v_circ;
}