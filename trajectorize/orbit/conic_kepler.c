#include "conic_kepler.h"

// Path: trajectorize/orbit/conic_kepler.c

#define _USE_MATH_DEFINES // for M_PI
#include <math.h>

#ifndef M_PI
// This macro is here for when the linter doesn't see M_PI defined from math.h
#define M_PI 3.14159265358979323846
#endif // M_PI

#include <stdlib.h>

#include "orbit_math.h"
#include "rotations.h"

#define ATOL 1e-12
#define MAX_ITER 10 // convergence is usually reached in 2 iterations on low eccentricity orbits

double kepler_solver(double M, double e)
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

KeplerianElements propagateKeplerianOrbit(KeplerianElements orbit, double dt, double mu)
{
    // Compute mean anomaly
    double T = orbital_period(orbit.semi_major_axis, mu);
    double M = remainder(2 * M_PI * dt / T, 2 * M_PI);
    // Use kepler_solver to solve Kepler's equation
    double E = kepler_solver(M, orbit.eccentricity);
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

StateVector stateVectorFromOrbit(KeplerianElements orbit, double mu)
{
    double r = orbit.semi_major_axis * (1 - orbit.eccentricity * orbit.eccentricity) / (1 + orbit.eccentricity * cos(orbit.true_anomaly));
    double x = r * cos(orbit.true_anomaly);
    double y = r * sin(orbit.true_anomaly);

    double v = sqrt(mu * (2 / r - 1 / orbit.semi_major_axis));
    double vx = -v * sin(orbit.true_anomaly);
    double vy = v * (orbit.eccentricity + cos(orbit.true_anomaly));

    Vector3 perifocal_position = {.v = {x, y, 0}};
    Vector3 perifocal_velocity = {.v = {vx, vy, 0}};

    // Rotation matrix from perifocal to inertial frame
    Matrix3 R = perifocal_to_eci(orbit.longitude_of_ascending_node,
                                 orbit.inclination,
                                 orbit.argument_of_periapsis);

    StateVector state_vector = {
        mul_mat_vec(R, perifocal_position),
        mul_mat_vec(R, perifocal_velocity),
        orbit.epoch};

    return state_vector;
}

StateVectorArray stateVectorLocus(KeplerianElements orbit, double mu, int n)
{
    StateVector *mem_buffer = (StateVector *)malloc(n * sizeof(StateVector));
    // Format: x, y, z, vx, vy, vz, t
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
        mem_buffer[i] = stateVectorFromOrbit(orbit_i, mu);
    }

    StateVectorArray result;
    // Cast the pointer to a (Nx7) double array
    result.mem_buffer = (double *)mem_buffer; // C is so crazy lol
    result.n = n;
    result.states = mem_buffer;

    return result;
}

KeplerianElements orbitFromStateVector(StateVector state_vector, double mu)
{
    Vector3 h = cross(state_vector.position, state_vector.velocity);
    double h_norm = norm(h);
    double r = norm(state_vector.position);
    double v = norm(state_vector.velocity);

    double e_vec_x = (v * v - mu / r) * state_vector.position.x / mu - dot(state_vector.position, state_vector.velocity) * state_vector.velocity.x / mu;
    double e_vec_y = (v * v - mu / r) * state_vector.position.y / mu - dot(state_vector.position, state_vector.velocity) * state_vector.velocity.y / mu;
    double e_vec_z = (v * v - mu / r) * state_vector.position.z / mu - dot(state_vector.position, state_vector.velocity) * state_vector.velocity.z / mu;
    Vector3 e_vec = {.v = {e_vec_x, e_vec_y, e_vec_z}};
    double e = norm(e_vec);

    double n_vec_x = -h.y;
    double n_vec_y = h.x;
    double n_vec_z = 0;
    Vector3 n_vec = {.v = {n_vec_x, n_vec_y, n_vec_z}};
    double n = norm(n_vec);

    double i = acos(h.z / h_norm);
    double Omega = acos(n_vec.x / n);
    if (n_vec.y < 0)
        Omega = 2 * M_PI - Omega;
    double omega = acos(dot(n_vec, e_vec) / (n * e));
    if (e_vec.z < 0)
        omega = 2 * M_PI - omega;

    double E = acos((1 / e) * (1 - r / norm(h)) * dot(e_vec, state_vector.position) + (1 / e) * dot(state_vector.velocity, state_vector.position) / sqrt(mu));
    if (dot(state_vector.position, state_vector.velocity) < 0)
        E = 2 * M_PI - E;

    double nu = acos((cos(E) - e) / (1 - e * cos(E)));
    if (E > M_PI)
        nu = 2 * M_PI - nu;

    double a = 1 / (2 / r - v * v / mu);

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

double orbital_period(double semi_major_axis, double mu)
{
    return 2 * M_PI / sqrt(mu) * pow(semi_major_axis, 1.5);
}

double theta_from_E(double E, double e)
{
    return 2 * atan(sqrt((1 + e) / (1 - e)) * tan(E / 2));
}
