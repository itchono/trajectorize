#include "../../include/kepler_equation_solver.h"

// Path: trajectorize/orbit/kepler_equation_solver.c

#define _USE_MATH_DEFINES // for M_PI
#include <math.h>

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
