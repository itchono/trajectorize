#include "../include/universal_kepler.h"
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

double stumpS(double z)
{
    if (z > 0)
    {
        return (sqrt(z) - sin(sqrt(z))) / pow(sqrt(z), 3);
    }
    else if (z < 0)
    {
        return (sinh(sqrt(-z)) - sqrt(-z)) / pow(sqrt(-z), 3);
    }
    else
    {
        return 1.0 / 6.0;
    }
}

double stumpC(double z)
{
    if (z > 0)
    {
        return (1 - cos(sqrt(z))) / z;
    }
    else if (z < 0)
    {
        return (cosh(sqrt(-z)) - 1) / (-z);
    }
    else
    {
        return 1.0 / 2.0;
    }
}

double alpha(UniversalKeplerOrbit orbit)
{
    double r = norm(orbit.position);
    double v = norm(orbit.velocity);

    return 2.0 / r - v * v / orbit.mu;
}

double universalAnomaly(double t, UniversalKeplerOrbit orbit)
{
    double dt = t - orbit.time;
    double x = sqrt(orbit.mu) * fabs(alpha(orbit)) * dt; // initial guess for x

    // Solve iteratively using Newton's method
    double ratio = 1.0;

    double r = norm(orbit.position);
    double v = norm(orbit.velocity);
    double vr = dot(orbit.position, orbit.velocity) / r;

    for (int i = 0; i < MAX_ITER; i++)
    {
        double z = x * x * alpha(orbit);
        double C = stumpC(z);
        double S = stumpS(z);

        double f = r * vr / sqrt(orbit.mu) * x * x * C +
                   (1 - r * alpha(orbit)) * x * x * x * S +
                   r * x - sqrt(orbit.mu) * dt;
        double f_prime = r * vr / sqrt(orbit.mu) * x * (1 - z * S) +
                         (1 - r * alpha(orbit)) * x * x * C +
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

LagrangeCoefficients lagrangeFG(double t, UniversalKeplerOrbit orbit)
{
    double dt = t - orbit.time;
    double x = universalAnomaly(t, orbit);

    double r = norm(orbit.position);
    double v = norm(orbit.velocity);
    double vr = dot(orbit.position, orbit.velocity) / r;

    double z = x * x * alpha(orbit);
    double C = stumpC(z);
    double S = stumpS(z);

    LagrangeCoefficients result;
    result.f = 1 - C / r * x * x;
    result.g = dt - 1 / sqrt(orbit.mu) * x * x * x * S;
    return result;
}

LagrangeDerivatives lagrangeFGdot(double t, UniversalKeplerOrbit orbit, double r_new)
{
    double x = universalAnomaly(t, orbit);

    double r = norm(orbit.position);

    double z = x * x * alpha(orbit);
    double C = stumpC(z);
    double S = stumpS(z);

    LagrangeDerivatives result;
    result.fdot = sqrt(orbit.mu) / (r * r_new) * (z * S - 1) * x;
    result.gdot = 1 - C / r_new * x * x;
    return result;
}

UniversalKeplerOrbit orbitAtTime(double t, UniversalKeplerOrbit orbit)
{
    LagrangeCoefficients lc = lagrangeFG(t, orbit);
    Vector3 position = add_vec(mul_scalar_vec(lc.f, orbit.position),
                               mul_scalar_vec(lc.g, orbit.velocity));
    double r_new = norm(position);

    LagrangeDerivatives ldc = lagrangeFGdot(t, orbit, r_new);
    Vector3 velocity = add_vec(mul_scalar_vec(ldc.fdot, orbit.position),
                               mul_scalar_vec(ldc.gdot, orbit.velocity));

    UniversalKeplerOrbit result;
    result.position = position;
    result.velocity = velocity;
    result.time = t;
    result.mu = orbit.mu;
    return result;
}