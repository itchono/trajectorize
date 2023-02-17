#include "trajectory_optimizers.h"
#include "transfer_orbit.h"
#include "delta_v_estimate.h"
#include "vec_math.h"
#include <stdlib.h>

void free_GridSearchResult(GridSearchResult result)
{
    free(result.dv);
    free(result.t1);
    free(result.tof);
}

GridSearchResult transfer_dv(GridSearchProblem problem)
{

    double d_t1 = (problem.t1_max - problem.t1_min) / problem.n_grid_t1;
    double d_tof = (problem.tof_max - problem.tof_min) / problem.n_grid_tof;

    int n2_grid = problem.n_grid_t1 * problem.n_grid_tof;

    double *t1_arr = malloc(sizeof(double) * n2_grid);
    double *tof_arr = malloc(sizeof(double) * n2_grid);
    double *dv_arr = malloc(sizeof(double) * n2_grid);

    // Init arrays
    for (int i = 0; i < problem.n_grid_t1; i++)
    {
        for (int j = 0; j < problem.n_grid_tof; j++)
        {
            int idx = i * problem.n_grid_tof + j;

            double t1 = problem.t1_min + d_t1 * i;
            t1_arr[idx] = t1;

            double tof = problem.tof_min + d_tof * j;
            tof_arr[idx] = tof;

            double t2 = t1 + tof;

            TransferOrbit to = planetary_transfer_orbit(problem.body1,
                                                        problem.body2,
                                                        t1, t2);
            Vector3 dep_xs_vel = excess_velocity_at_body(to, DEPARTURE);
            dv_arr[idx] = ejection_capture_dv(problem.body1, dep_xs_vel, problem.r_pe_1);

            // Calculate arrival dv if needed
            if (problem.include_capture)
            {
                Vector3 arr_xs_vel = excess_velocity_at_body(to, ARRIVAL);
                dv_arr[idx] += ejection_capture_dv(problem.body2, arr_xs_vel, problem.r_pe_2);
            }
        }
    }

    GridSearchResult sol = {.dv = dv_arr,
                            .t1 = t1_arr,
                            .tof = tof_arr,
                            .n_grid_t1 = problem.n_grid_t1,
                            .n_grid_tof = problem.n_grid_tof};
    return sol;
}
