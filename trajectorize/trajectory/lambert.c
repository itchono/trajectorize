#include "lambert.h"
#include "stumpuff_functions.h"
#include "orbit_math.h"

#include <math.h>

// Path: trajectorize/trajectory/trajectory.c

LambertSolution lambert(Vector3 R1, Vector3 R2, double mu, double dt, enum TrajectoryType type)
{
    // Implementing algorithm D.25 from Curtis

    double r1 = vec_norm(R1);
    double r2 = vec_norm(R2);
}