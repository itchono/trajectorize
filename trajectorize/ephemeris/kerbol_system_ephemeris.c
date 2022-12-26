#include "kerbol_system_ephemeris.h"
#include "conic_kepler.h"
#include "kerbol_system_bodies.h"
#include "orbit_math.h"
#include <math.h>

KeplerianElements ke_from_pke(PlanetaryKeplerianElements pke, double t, double mu)
{
    // Compute mean anomaly
    double T = orbital_period(pke.semi_major_axis, mu);
    double M = remainder(2 * M_PI * t / T + pke.mean_anomaly_at_epoch, 2 * M_PI);

    double E = kepler_solver(M, pke.eccentricity);

    double true_anomaly = theta_from_E(E, pke.eccentricity);

    KeplerianElements ke = {.semi_major_axis = pke.semi_major_axis,
                            .eccentricity = pke.eccentricity,
                            .inclination = pke.inclination,
                            .longitude_of_ascending_node = pke.longitude_of_ascending_node,
                            .argument_of_periapsis = pke.argument_of_periapsis,
                            .true_anomaly = true_anomaly,
                            .epoch = t};

    return ke;
}

StateVector get_direct_state_at_time(double t, enum BodyEnum child_id)
{
    // Get direct state of child wrt its parent at some time
    Body body = bodies_list[child_id];
    Body parent = bodies_list[body.parent_id];

    KeplerianElements body_ke = ke_from_pke(body.orbit, t, parent.mu);

    return stateVectorFromOrbit(body_ke, parent.mu);
}

StateVector get_rel_state_at_time(double t, enum BodyEnum parent_id, enum BodyEnum child_id)
{
    // t is universal time in seconds
    // calculates relative ECI position of child body rel. to parent
    // ordering of bodies must be exclsively in descending order, i.e. parent
    // must be an ancestor of child (TODO: add a check for this)
    // performs recursive comparisons if needed

    Body child = bodies_list[child_id];

    if (parent_id == child.parent_id)
    {
        return get_direct_state_at_time(t, child_id);
    }
    else
    {
        StateVector parent_state = get_direct_state_at_time(t, parent_id);
        StateVector child_state = get_direct_state_at_time(t, child_id);

        StateVector true_rel_state = {
            .position = add_vec(parent_state.position, child_state.position),
            .velocity = add_vec(parent_state.velocity, child_state.velocity),
            .time = parent_state.time};
        return true_rel_state;
    }
}