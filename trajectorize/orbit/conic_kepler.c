#include "conic_kepler.h"

// Path: trajectorize/orbit/conic_kepler.c

#define _USE_MATH_DEFINES // for M_PI
#include <math.h>
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

    double M = E - e * sin(E);
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
