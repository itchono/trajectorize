#include "transfer_orbit.h"
#include "kerbol_system_ephemeris.h"
#include "kerbol_system_bodies.h"
#include "lambert.h"
#include "conic_kepler.h"
#include "vec_math.h"

#include <stdio.h>

#define _USE_MATH_DEFINES
#include <math.h>
#ifndef M_PI
// This macro is here for when the linter doesn't see M_PI defined from math.h
#define M_PI (3.14159265358979323846)
#endif // M_PI

TransferOrbit get_transfer_orbit(Body body1, Body body2, double t1, double t2)
{
    // Calculates a transfer orbit from body1 to body2 at time t1 to arrive at body2 at time t2
    // Keplerian elements are given in terms of the common parent body at time t1

    // Ensure bodies have a common parent
    if (body1.parent_id != body2.parent_id)
    {
        fprintf(stderr, "Error: Bodies do not have a common parent.\n");
        return (TransferOrbit){.valid = false, .ke = {0}, .t1 = 0, .t2 = 0, .body1 = body1, .body2 = body2};
    }

    Body parent = kerbol_system_bodies[body1.parent_id];

    // Calculate the state vectors at time t1 and t2
    StateVector b1t1 = get_rel_state_at_time(t1, body1.parent_id, body1.body_id);
    StateVector b2t2 = get_rel_state_at_time(t2, body2.parent_id, body2.body_id);

    // Solve Lambert's problem to find the transfer orbit
    enum TrajectoryType type = PROGRADE;
    LambertSolution sol = lambert(b1t1.position, b2t2.position, t2 - t1, parent.mu, type);

    if (!sol.valid)
    {
        return (TransferOrbit){.valid = false, .ke = {0}, .t1 = 0, .t2 = 0, .body1 = body1, .body2 = body2};
    }

    // Get velocity at time t1 and construct state vector of transfer orbit at t1

    StateVector b1t1_transfer = {.position = b1t1.position,
                                 .velocity = sol.v1,
                                 .time = t1};

    // Generate the transfer orbit
    KeplerianElements ke = ke_from_state_vector(b1t1_transfer, parent.mu);
    return (TransferOrbit){.valid = true, .ke = ke, .t1 = t1, .t2 = t2, .body1 = body1, .body2 = body2};
}

Vector3 excess_velocity_at_body(TransferOrbit transfer_orbit,
                                enum ArrivalDepartureEnum arrival_or_departure)
{
    Body parent = kerbol_system_bodies[transfer_orbit.body1.parent_id];

    double ut;

    StateVector body_state;
    if (arrival_or_departure == DEPARTURE)
    {
        ut = transfer_orbit.t1;
        body_state = get_rel_state_at_time(ut,
                                           transfer_orbit.body1.parent_id,
                                           transfer_orbit.body1.body_id);
    }
    else
    {
        ut = transfer_orbit.t2;
        body_state = get_rel_state_at_time(ut,
                                           transfer_orbit.body2.parent_id,
                                           transfer_orbit.body2.body_id);
    }

    // Calculate the excess velocity at a body given a transfer orbit
    // Excess velocity is the velocity of the transfer orbit relative to the body

    // Ensure that we are evaluating state at time ut
    KeplerianElements orbit_ke = ke_orbit_prop(ut, transfer_orbit.ke, parent.mu);
    StateVector transfer_state = state_vector_from_ke(orbit_ke, parent.mu);

    Vector3 excess_velocity = vec_sub(transfer_state.velocity, body_state.velocity);
    return excess_velocity;
}

double approximate_time_of_flight(Body body1, Body body2)
{
    // Approximates radii of bodies using SMA; this means that the eccentricity of the bodies
    // is assumed to be almost zero. (This is true for most of KSP)

    // Ensure bodies have a common parent
    if (body1.parent_id != body2.parent_id)
    {
        fprintf(stderr, "Error: Bodies do not have a common parent.\n");
        return 0;
    }

    // Get parent body
    Body parent = kerbol_system_bodies[body1.parent_id];

    return M_PI * sqrt(pow(body1.orbit.semi_major_axis + body2.orbit.semi_major_axis, 3) / (8 * parent.mu));
}
