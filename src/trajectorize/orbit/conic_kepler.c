#include "conic_kepler.h"

// Path: trajectorize/orbit/conic_kepler.c

#define _USE_MATH_DEFINES // for M_PI
#include <math.h>

#ifndef M_PI
// This macro is here for when the linter doesn't see M_PI defined from math.h
#define M_PI (3.14159265358979323846)
#endif // M_PI

#include <stdlib.h>

#include "vec_math.h"
#include "rotations.h"

#define ATOL 1e-12
#define MAX_ITER 10 // convergence is usually reached in 2 iterations on low eccentricity orbits

double E_from_M(double M, double e)
// cubic convergent Kepler solver
{
    // Use initial guess from Battin's paper
    double E = M + e * sin(M) / (1 - sin(M + e) + sin(M));

    // Use Halley's method to solve Kepler's equation
    double f, f_prime, f_prime_prime; // f = E - e * sin(E) - M
    double delta;

    for (int i = 0; i < MAX_ITER; i++)
    {
        f = E - e * sin(E) - M;
        f_prime = 1 - e * cos(E);
        f_prime_prime = e * sin(E);
        delta = -2 * f * f_prime / (2 * f_prime * f_prime - f * f_prime_prime);
        E += delta;
        if (fabs(delta) < 1e-12)
            break;
    }
    return E;
}

double orbital_period(double semi_major_axis, double mu)
{
    return 2 * M_PI / sqrt(mu) * pow(semi_major_axis, 1.5);
}

double theta_from_E(double E, double e)
{
    return 2 * atan(sqrt((1 + e) / (1 - e)) * tan(E / 2));
}

double theta_from_M(double M, double e)
{
    return theta_from_E(E_from_M(M, e), e);
}

double E_from_theta(double theta, double e)
{
    return 2 * atan(sqrt((1 - e) / (1 + e)) * tan(theta / 2));
}
double M_from_theta(double theta, double e)
{
    return M_from_E(E_from_theta(theta, e), e);
}
double M_from_E(double E, double e)
{
    return E - e * sin(E);
}

KeplerianElements ke_orbit_prop(double t, KeplerianElements orbit, double mu)
{
    double dt = t - orbit.epoch;
    if (dt < 0)
    {
        return (KeplerianElements){0};
    }
    else if (dt == 0)
    {
        return orbit;
    }
    double M_at_epoch = M_from_theta(orbit.true_anomaly, orbit.eccentricity);

    // Compute mean anomaly
    double T = orbital_period(orbit.semi_major_axis, mu);
    double M = remainder(2 * M_PI * dt / T + M_at_epoch, 2 * M_PI);
    // Use E_from_M to solve Kepler's equation
    double E = E_from_M(M, orbit.eccentricity);
    // Calculate true anomaly
    double theta = theta_from_E(E, orbit.eccentricity);

    // Return new orbit
    KeplerianElements orbit_propagated = {
        .semi_major_axis = orbit.semi_major_axis,
        .eccentricity = orbit.eccentricity,
        .inclination = orbit.inclination,
        .longitude_of_ascending_node = orbit.longitude_of_ascending_node,
        .argument_of_periapsis = orbit.argument_of_periapsis,
        .true_anomaly = theta,
        .epoch = orbit.epoch + dt};

    return orbit_propagated;
}

StateVector state_vector_from_ke(KeplerianElements orbit, double mu)
{
    double r = orbit.semi_major_axis * (1 - orbit.eccentricity * orbit.eccentricity) / (1 + orbit.eccentricity * cos(orbit.true_anomaly));
    double x = r * cos(orbit.true_anomaly);
    double y = r * sin(orbit.true_anomaly);

    double h = sqrt(mu * orbit.semi_major_axis * (1 - orbit.eccentricity * orbit.eccentricity));
    double vx = -mu / h * sin(orbit.true_anomaly);
    double vy = mu / h * (orbit.eccentricity + cos(orbit.true_anomaly));

    Vector3 perifocal_position = {.v = {x, y, 0}};
    Vector3 perifocal_velocity = {.v = {vx, vy, 0}};

    // Rotation matrix from perifocal to inertial frame
    Matrix3 R = perifocal_to_eci(orbit.longitude_of_ascending_node,
                                 orbit.inclination,
                                 orbit.argument_of_periapsis);

    StateVector state_vector = {
        mat_mul_vec(R, perifocal_position),
        mat_mul_vec(R, perifocal_velocity),
        orbit.epoch};

    return state_vector;
}

StateVectorArray ke_state_locus(KeplerianElements orbit, double mu, int n)
{
    StateVector *mem_buffer = (StateVector *)malloc(n * sizeof(StateVector));
    // Format: x, y, z, vx, vy, vz, t; t is set to the epoch of the orbit (invariant)
    // we're doing some crazy struct-packing hackery here

    double d_theta = 2 * M_PI / (n - 1); // guarantees full cover
    for (int i = 0; i < n; i++)
    {
        double theta = i * d_theta;
        KeplerianElements orbit_i = {
            .semi_major_axis = orbit.semi_major_axis,
            .eccentricity = orbit.eccentricity,
            .inclination = orbit.inclination,
            .longitude_of_ascending_node = orbit.longitude_of_ascending_node,
            .argument_of_periapsis = orbit.argument_of_periapsis,
            .true_anomaly = theta,
            .epoch = orbit.epoch};
        mem_buffer[i] = state_vector_from_ke(orbit_i, mu);
    }

    StateVectorArray result;
    // Cast the pointer to a (Nx7) double array
    result.mem_buffer = (double *)mem_buffer; // C is so crazy lol
    result.n = n;
    result.states = mem_buffer;

    return result;
}

StateVectorArray ke_orbit_prop_many(int n, double times[n], KeplerianElements orbit, double mu)
{
    StateVector *mem_buffer = (StateVector *)malloc(n * sizeof(StateVector));
    // Format: x, y, z, vx, vy, vz, t; t is set to the epoch of the orbit (invariant)
    for (int i = 0; i < n; i++)
    {
        mem_buffer[i] = state_vector_from_ke(ke_orbit_prop(times[i], orbit, mu), mu);
    }
    StateVectorArray result;
    // Cast the pointer to a (Nx7) double array
    result.mem_buffer = (double *)mem_buffer;
    result.n = n;
    result.states = mem_buffer;

    return result;
}

KeplerianElements ke_from_state_vector(StateVector state_vector, double mu)
{
    // angular momentum
    Vector3 h = vec_cross(state_vector.position, state_vector.velocity);
    double h_norm = vec_norm(h);
    double r = vec_norm(state_vector.position);
    double v = vec_norm(state_vector.velocity);

    // semi-major axis
    double a = 1 / (2 / r - v * v / mu);

    // compute eccentricity vector
    double e_vec_x = (v * v - mu / r) * state_vector.position.x / mu - vec_dot(state_vector.position, state_vector.velocity) * state_vector.velocity.x / mu;
    double e_vec_y = (v * v - mu / r) * state_vector.position.y / mu - vec_dot(state_vector.position, state_vector.velocity) * state_vector.velocity.y / mu;
    double e_vec_z = (v * v - mu / r) * state_vector.position.z / mu - vec_dot(state_vector.position, state_vector.velocity) * state_vector.velocity.z / mu;
    Vector3 e_vec = {.v = {e_vec_x, e_vec_y, e_vec_z}};
    double e = vec_norm(e_vec);

    // compute inclination
    double n_vec_x = -h.y;
    double n_vec_y = h.x;
    double n_vec_z = 0;
    Vector3 n_vec = {.v = {n_vec_x, n_vec_y, n_vec_z}};
    double n = vec_norm(n_vec);

    double i = acos(h.z / h_norm);

    // compute longitude of ascending node
    double Omega = acos(n_vec.x / n);
    if (n_vec.y < 0)
        Omega = 2 * M_PI - Omega;

    // compute argument of periapsis
    double omega = acos(vec_dot(n_vec, e_vec) / (n * e));
    if (e_vec.z < 0)
        omega = 2 * M_PI - omega;

    // compute true anomaly, correcting for quadrant
    double E = acos((1 / e) * (1 - r / a));
    if (vec_dot(state_vector.position, state_vector.velocity) < 0)
        E = 2 * M_PI - E;

    double nu = acos((cos(E) - e) / (1 - e * cos(E)));
    if (E > M_PI)
        nu = 2 * M_PI - nu;

    KeplerianElements orbit = {
        a,
        e,
        i,
        Omega,
        omega,
        nu,
        state_vector.time};

    return orbit;
}
