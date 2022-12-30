#include "delta_v_estimate.h"
#include "vec_math.h"

#include <math.h>

double delta_v_req(Body body, double excess_velocity, double periapsis)
{
    // Estimate the delta-v required to eject from a body
    // starting from a circular orbit at periapsis

    // Calculate the velocity of the circular orbit
    double v_circ = sqrt(body.mu / periapsis);

    double v_peri = sqrt(excess_velocity * excess_velocity + 2 * body.mu / periapsis);

    return v_peri - v_circ;
}