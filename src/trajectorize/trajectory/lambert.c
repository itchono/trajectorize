#include "lambert.h"
#include "stumpuff_functions.h"
#include "vec_math.h"

#define _USE_MATH_DEFINES
#include <math.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif // M_PI

#define ATOL (1e-12)
#define MAX_ITER (150)
#define NEWTON_SWITCHOVER_POINT (1e-4)

double func_y(double z, double r1, double r2, double A)
{
    // Equation 5.36 from Curtis
    double y = r1 + r2 + A * (z * stumpS(z) - 1) / sqrt(stumpC(z));
    // reject negative values of y
    if (y < 0)
    {
        return 0;
    }
    return y;
}

double func_F(double z, double t, double r1, double r2, double A, double mu)
{
    // Equation 5.40 from Curtis
    double y = func_y(z, r1, r2, A);
    double F = pow(y / stumpC(z), 1.5) * stumpS(z) + A * sqrt(y) - sqrt(mu) * t;
    return F;
}

double deriv_F_z(double z, double r1, double r2, double A, double mu)
{
    double y0 = func_y(0, r1, r2, A);
    // Equation 5.43 from Curtis
    if (z == 0)
    {
        return sqrt(2) / 40 * pow(y0, 1.5) + A / 8 * (sqrt(y0)) + A * sqrt(1 / 2 / y0);
    }
    double y = func_y(z, r1, r2, A);
    return pow(y / stumpC(z), 1.5) * (1 / 2 / z * (stumpC(z) - 3 * stumpS(z) / 2 / stumpC(z)) + 3 * pow(stumpS(z), 2) / 4 / stumpC(z)) + A / 8 * (3 * stumpS(z) / stumpC(z) * sqrt(y) + A * sqrt(stumpC(z) / y));
}

LambertSolution lambert(Vector3 R1, Vector3 R2, double dt, double mu, enum TrajectoryType type)
{
    // Implementing algorithm D.25 from Curtis

    double r1 = vec_norm(R1);
    double r2 = vec_norm(R2);

    Vector3 c12 = vec_cross(R1, R2);
    double theta = acos(vec_dot(R1, R2) / (r1 * r2));

    // Invert direction of transfer if:
    // 1. direction is prograde but c12.z <= 0
    // 2. direction is retrograde but c12.z >= 0
    if ((type == PROGRADE && c12.z <= 0) || (type == RETROGRADE && c12.z >= 0))
    {
        theta = 2 * M_PI - theta;
    }

    // Calculate A
    double A = sin(theta) * sqrt(r1 * r2 / (1 - cos(theta)));

    // find approximate sign change point of F(z, t) in z using
    // Hybrid Newton-Bisection method

    // Strategy
    // 1. Find a bracket for the sign change point
    // 2. Switch over to Newton's method when the bracket is sufficiently small
    double a = -100;
    double b = 100;
    double z = (a + b) / 2;

    for (int i = 0; i < MAX_ITER; i++)
    {
        double F = func_F(z, dt, r1, r2, A, mu);

        // collect information for bisection
        if (F > 0)
            b = z;
        else
            a = z;

        // decide if we want to use bisection or newton for next iteration
        if ((b - a) > NEWTON_SWITCHOVER_POINT)
        {
            // Bisection iteration
            z = (a + b) / 2;
        }
        else
        {
            // Newton Iteration
            double F_z = deriv_F_z(z, r1, r2, A, mu);
            z -= F / F_z;
        }

        if (fabs(F) < ATOL)
        {
            break;
        }
    }

    // Calculate orbit using lagrange f and g functions
    double y = func_y(z, r1, r2, A);
    double f = 1 - y / r1;
    double g = A * sqrt(y / mu);
    double gdot = 1 - y / r2;

    // V1 = 1/g * (R2 - f*R1)
    Vector3 V1 = vec_mul_scalar(1 / g, vec_sub(R2, vec_mul_scalar(f, R1)));

    // V2 = 1/g * (gdot*R2 - R1)
    Vector3 V2 = vec_mul_scalar(1 / g, vec_sub(vec_mul_scalar(gdot, R2), R1));

    LambertSolution solution = {V1, V2, dt};
    return solution;
}