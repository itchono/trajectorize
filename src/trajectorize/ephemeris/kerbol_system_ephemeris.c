#include "kerbol_system_ephemeris.h"
#include "conic_kepler.h"
#include "kerbol_system_bodies.h"
#include "vec_math.h"

#define _USE_MATH_DEFINES
#include <math.h>
#include <stdlib.h>

#ifndef M_PI
// This macro is here for when the linter doesn't see M_PI defined from math.h
#define M_PI (3.14159265358979323846)
#endif // M_PI

KeplerianElements ke_from_pke(PlanetaryKeplerianElements pke, double t, double mu)
// Compute Keplerian elements at some time from planetary Keplerian elements
{
    // Compute mean anomaly
    double T = orbital_period(pke.semi_major_axis, mu);
    double M = remainder(2 * M_PI * t / T + pke.mean_anomaly_at_epoch, 2 * M_PI);

    double true_anomaly = theta_from_M(M, pke.eccentricity);

    KeplerianElements ke = {.semi_major_axis = pke.semi_major_axis,
                            .eccentricity = pke.eccentricity,
                            .inclination = pke.inclination,
                            .longitude_of_ascending_node = pke.longitude_of_ascending_node,
                            .argument_of_periapsis = pke.argument_of_periapsis,
                            .true_anomaly = true_anomaly,
                            .epoch = t};

    return ke;
}

StateVectorArray pke_state_locus(PlanetaryKeplerianElements pke, double mu, int n)
// CALLER MUST FREE RETURNED STRUCT
{
    // Generate state space locus of points representing the orbit of a body
    KeplerianElements ke = ke_from_pke(pke, 0, mu);
    return ke_state_locus(ke, mu, n);
}

StateVector get_direct_state_at_time(double t, enum BodyEnum child_id)
{
    // Get direct state of child wrt its parent at some time
    Body body = kerbol_system_bodies[child_id];
    Body parent = kerbol_system_bodies[body.parent_id];

    KeplerianElements body_ke = ke_from_pke(body.orbit, t, parent.mu);

    return state_vector_from_ke(body_ke, parent.mu);
}

StateVector get_rel_state_at_time(double t, enum BodyEnum parent_id, enum BodyEnum child_id)
{
    // t is universal time in seconds
    // calculates relative ECI position of child body rel. to parent
    // ordering of bodies must be exclsively in descending order, i.e. parent
    // must be an ancestor of child (TODO: add a check for this)

    Body child = kerbol_system_bodies[child_id];

    if (parent_id == child_id)
    {
        StateVector zero_state = {.position = {.x = 0,
                                               .y = 0,
                                               .z = 0},
                                  .velocity = {.x = 0,
                                               .y = 0,
                                               .z = 0},
                                  .time = t};
        return zero_state;
    }
    else if (parent_id == child.parent_id)
    {
        return get_direct_state_at_time(t, child_id);
    }
    else
    {
        StateVector parent_state = get_direct_state_at_time(t, parent_id);
        StateVector child_state = get_direct_state_at_time(t, child_id);

        StateVector true_rel_state = {
            .position = vec_add(parent_state.position, child_state.position),
            .velocity = vec_add(parent_state.velocity, child_state.velocity),
            .time = parent_state.time};
        return true_rel_state;
    }
}

StateVectorArray get_rel_state_at_many_times(int n, double times[], enum BodyEnum parent_id, enum BodyEnum child_id)
// CALLER MUST FREE RETURNED STRUCT
{
    StateVector *mem_buffer = (StateVector *)malloc(n * sizeof(StateVector));
    // Format: x, y, z, vx, vy, vz, t; t is left as 0

    for (int i = 0; i < n; i++)
    {
        StateVector state = get_rel_state_at_time(times[i], parent_id, child_id);
        mem_buffer[i] = state;
    }

    StateVectorArray result;
    // Cast the pointer to a (Nx7) double array
    result.mem_buffer = (double *)mem_buffer; // C is so crazy lol
    result.n = n;
    result.states = mem_buffer;

    return result;
}
