#include <stdio.h>
#include <emscripten.h>

#include "transfer_orbit.h"
#include "trajectory_optimizers.h"
#include "kerbol_system_bodies.h"
#include "conic_kepler.h"
#include "delta_v_estimate.h"
#include "vec_math.h"
#include "ksp_time.h"

void EMSCRIPTEN_KEEPALIVE calculate_transfer(
    double t1_min, int body1_id, int body2_id,
    int n_grid_t1, int n_grid_tof, 
    double r_pe_1, double r_pe_2, int include_capture)
{

    // turn this into a form that transfer_dv can use
    Body body1 = kerbol_system_bodies[body1_id];
    Body body2 = kerbol_system_bodies[body2_id];

    // use orbital period of body 1 as a heuristic for max time
    double t1_max = orbital_period(body1.orbit.semi_major_axis, body1.mu) * 2 + t1_min;

    // Use Hohmann transfer time as a heuristic for time of flight
    double tof_approx = approximate_time_of_flight(body1, body2);
    double tof_min = tof_approx * 0.5;
    double tof_max = tof_approx * 2;

    GridSearchProblem gs_problem = {
        .body1 = body1,
        .body2 = body2,
        .t1_min = t1_min,
        .t1_max = t1_max,
        .tof_min = tof_min,
        .tof_max = tof_max,
        .n_grid_t1 = n_grid_t1,
        .n_grid_tof = n_grid_tof,
        .r_pe_1 = r_pe_1,
        .r_pe_2 = r_pe_2,
        .include_capture = (bool)include_capture};

    GridSearchResult gs_result = transfer_dv(gs_problem);

    // find minimum dv point
    int min_idx = 0;
    for (int i = 0; i < n_grid_t1 * n_grid_tof; i++)
    {
        if (gs_result.dv_ejection[i] < gs_result.dv_ejection[min_idx])
        {
            min_idx = i;
        }
    }

    KSPTime t1_opt = ksp_time_from_ut(gs_result.t1[min_idx], KERBIN_TIME);
    KSPTime tof_opt = ksp_time_from_ut(gs_result.tof[min_idx], KERBIN_TIME);
    KSPTime t2_opt = ksp_time_from_ut(gs_result.t1[min_idx] + gs_result.tof[min_idx], KERBIN_TIME);

    // Char buffers
    char t1_opt_str[100];
    char tof_opt_str[100];
    char t2_opt_str[100];

    get_ut_time_string(t1_opt, t1_opt_str, 100, false);
    get_delta_time_string(tof_opt, tof_opt_str, 100);
    get_ut_time_string(t2_opt, t2_opt_str, 100, false);

    // Print results
    printf("Optimal transfer from %s to %s:\n", body_names[body1_id], body_names[body2_id]);
    printf("Departure time: %s\n", t1_opt_str);
    printf("Time of flight: %s\n", tof_opt_str);
    printf("Arrival time: %s\n", t2_opt_str);
    printf("Delta-v to eject from %s: %.2f m/s\n", body_names[body1_id], gs_result.dv_ejection[min_idx]);

    free_GridSearchResult(gs_result);
}

int main(int argc, char *argv[])
{
    Body kerbin = kerbol_system_bodies[KERBIN];
    Body duna = kerbol_system_bodies[DUNA];
    double t1 = 5091552;
    double t2 = 10679760;
    TransferOrbit transfer_orbit = get_transfer_orbit(
        kerbin, duna, t1, t2);
    Vector3 excess_velocity_at_kerbin = excess_velocity_at_body(
        transfer_orbit, DEPARTURE);
    double r_pe = 70000 + kerbin.radius;
    double delta_v = ejection_capture_dv(
        kerbin, excess_velocity_at_kerbin, r_pe);

    printf("Delta-v to eject from Kerbin: %.2f m/s\n", delta_v);
    printf("Time of transfer: %.0f seconds\n", t2 - t1);
    return 0;
}
