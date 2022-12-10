#include "universal_kepler.h"
#include "orbit_math.h"
#include "stumpuff_functions.h"
#include <math.h>

#define ATOL 1e-12
#define MAX_ITER 50

typedef struct LagrangeCoefficients
{
    double f;
    double g;
} LagrangeCoefficients;

typedef struct LagrangeDerivatives
{
    double fdot;
    double gdot;
} LagrangeDerivatives;

double alpha(StateVector orbit, double mu)
{
    double r = norm(orbit.position);
    double v = norm(orbit.velocity);

    return 2.0 / r - v * v / mu;
}

double universalAnomaly(double t, StateVector orbit, double mu)
{
    double dt = t - orbit.time;
    double x = sqrt(mu) * fabs(alpha(orbit, mu)) * dt; // initial guess for x

    // Solve iteratively using Newton's method
    double ratio = 1.0;

    double r = norm(orbit.position);
    double vr = dot(orbit.position, orbit.velocity) / r;

    for (int i = 0; i < MAX_ITER; i++)
    {
        double z = x * x * alpha(orbit, mu);
        double C = stumpC(z);
        double S = stumpS(z);

        double f = r * vr / sqrt(mu) * x * x * C +
                   (1 - r * alpha(orbit, mu)) * x * x * x * S +
                   r * x - sqrt(mu) * dt;
        double f_prime = r * vr / sqrt(mu) * x * (1 - z * S) +
                         (1 - r * alpha(orbit, mu)) * x * x * C +
                         r;
        ratio = f / f_prime;
        x -= ratio;

        if (fabs(ratio) < ATOL)
        {
            break;
        }
    }
    return x;
}

LagrangeCoefficients lagrangeFG(double t, StateVector orbit, double mu)
{
    double dt = t - orbit.time;
    double x = universalAnomaly(t, orbit, mu);

    double r = norm(orbit.position);

    double z = x * x * alpha(orbit, mu);
    double C = stumpC(z);
    double S = stumpS(z);

    LagrangeCoefficients result;
    result.f = 1 - C / r * x * x;
    result.g = dt - 1 / sqrt(mu) * x * x * x * S;
    return result;
}

LagrangeDerivatives lagrangeFGdot(double t, StateVector orbit, double mu, double r_new)
{
    double x = universalAnomaly(t, orbit, mu);

    double r = norm(orbit.position);

    double z = x * x * alpha(orbit, mu);
    double C = stumpC(z);
    double S = stumpS(z);

    LagrangeDerivatives result;
    result.fdot = sqrt(mu) / (r * r_new) * (z * S - 1) * x;
    result.gdot = 1 - C / r_new * x * x;
    return result;
}

StateVector orbitAtTime(double t, StateVector orbit, double mu)
{
    LagrangeCoefficients lc = lagrangeFG(t, orbit, mu);
    Vector3 position = add_vec(mul_scalar_vec(lc.f, orbit.position),
                               mul_scalar_vec(lc.g, orbit.velocity));
    double r_new = norm(position);

    LagrangeDerivatives ldc = lagrangeFGdot(t, orbit, mu, r_new);
    Vector3 velocity = add_vec(mul_scalar_vec(ldc.fdot, orbit.position),
                               mul_scalar_vec(ldc.gdot, orbit.velocity));

    StateVector result;
    result.position = position;
    result.velocity = velocity;
    result.time = t;
    return result;
}