#include "transfer_orbit.h"
#include "kerbol_system_ephemeris.h"
#include "kerbol_system_bodies.h"
#include "lambert.h"
#include "conic_kepler.h"

#include <stdio.h>

KeplerianElements planetary_transfer_orbit(Body body1, Body body2, double t1, double t2)
{
    // Calculates a transfer orbit from body1 to body2 at time t1 to arrive at body2 at time t2
    // Keplerian elements are given in terms of the common parent body at time t1

    // Ensure bodies have a common parent
    if (body1.parent_id != body2.parent_id)
    {
        fprintf(stderr, "Error: Bodies do not have a common parent.\n");
        return (KeplerianElements){0};
    }

    Body parent = kerbol_system_bodies[body1.parent_id];

    // Calculate the state vectors at time t1 and t2
    StateVector b1t1 = get_rel_state_at_time(t1, body1.parent_id, body1.body_id);
    StateVector b2t2 = get_rel_state_at_time(t2, body2.parent_id, body2.body_id);

    // Solve Lambert's problem to find the transfer orbit
    enum TrajectoryType type = PROGRADE;
    LambertSolution sol = lambert(b1t1.position, b2t2.position, t2 - t1, parent.mu, type);

    // Get velocity at time t1 and construct state vector of transfer orbit at t1

    StateVector b1t1_transfer = {.position = b1t1.position,
                                 .velocity = sol.v1,
                                 .time = t1};

    // Generate the transfer orbit
    KeplerianElements ke = ke_from_state_vector(b1t1_transfer, parent.mu);
    return ke;
}
