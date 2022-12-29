#include "universal_kepler.h"
#include "vec_math.h"
#include "stumpuff_functions.h"
#include <math.h>
#include <stdlib.h>

#define ATOL (1e-12)
#define MAX_ITER (50)

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
    double r = vec_norm(orbit.position);
    double v = vec_norm(orbit.velocity);

    return 2.0 / r - v * v / mu;
}

double univeral_anomaly_at_time(double t, StateVector orbit, double mu)
{
    double dt = t - orbit.time;
    double x = sqrt(mu) * fabs(alpha(orbit, mu)) * dt; // initial guess for x

    // Solve iteratively using Newton's method
    double ratio = 1.0;

    double r = vec_norm(orbit.position);
    double vr = vec_dot(orbit.position, orbit.velocity) / r;

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
    double x = univeral_anomaly_at_time(t, orbit, mu);

    double r = vec_norm(orbit.position);

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
    double x = univeral_anomaly_at_time(t, orbit, mu);

    double r = vec_norm(orbit.position);

    double z = x * x * alpha(orbit, mu);
    double C = stumpC(z);
    double S = stumpS(z);

    LagrangeDerivatives result;
    result.fdot = sqrt(mu) / (r * r_new) * (z * S - 1) * x;
    result.gdot = 1 - C / r_new * x * x;
    return result;
}

StateVector state_vec_orbit_prop(double t, StateVector orbit, double mu)
{
    LagrangeCoefficients lc = lagrangeFG(t, orbit, mu);
    Vector3 position = vec_add(vec_mul_scalar(lc.f, orbit.position),
                               vec_mul_scalar(lc.g, orbit.velocity));
    double r_new = vec_norm(position);

    LagrangeDerivatives ldc = lagrangeFGdot(t, orbit, mu, r_new);
    Vector3 velocity = vec_add(vec_mul_scalar(ldc.fdot, orbit.position),
                               vec_mul_scalar(ldc.gdot, orbit.velocity));

    StateVector result;
    result.position = position;
    result.velocity = velocity;
    result.time = t;
    return result;
}

StateVectorArray state_vec_orbit_prop_many(int n, double times[], StateVector orbit, double mu)
// RETURNS HEAP ALLOCATED MEMORY; CALLER MUST FREE
{
    // We're gonna do some hacker shit here
    // a (Nx7) double [56 bytes] is equivalent to a (N) StateVector [also 56 bytes]
    // so we're gonna allocate a (N) StateVector array,
    // and then cast it to a (Nx7) double array later
    StateVector *mem_buffer = (StateVector *)malloc(n * sizeof(StateVector));
    // Format: x, y, z, vx, vy, vz, t

    for (int i = 0; i < n; i++)
    {
        StateVector state = state_vec_orbit_prop(times[i], orbit, mu);
        mem_buffer[i] = state;
    }

    StateVectorArray result;
    // Cast the pointer to a (Nx7) double array
    result.mem_buffer = (double *)mem_buffer; // C is so crazy lol
    result.n = n;
    result.states = mem_buffer;

    return result;
}

void free_StateVectorArray(StateVectorArray sva)
// TODO: This lives here for now, but should be moved to a separate file
{
    free(sva.mem_buffer);
}
