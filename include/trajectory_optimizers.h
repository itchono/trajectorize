/*
Trajectorize

Trajectory optimizers

This header contains definitions for optimization methods related to
planning trajectories.
*/

#ifndef TRAJECTORY_OPTIMIZERS_H
#define TRAJECTORY_OPTIMIZERS_H

#include <stdbool.h>
#include "kerbol_system_types.h"
typedef struct GridSearchResult
{
    int n_grid_t1;
    int n_grid_tof;
    double *t1;
    double *tof;
    double *dv_ejection;
    double *dv_capture;
} GridSearchResult;

typedef struct GridSearchProblem
{
    Body body1;
    Body body2;
    bool include_capture; // whether or not to include capture burn dv
    double r_pe_1;        // body 1 periapsis RADIUS (m)
    double r_pe_2;        // body 2 periapsis RADIUS (m)
    double t1_min;
    double t1_max;
    double tof_min;
    double tof_max;
    int n_grid_t1;
    int n_grid_tof;
} GridSearchProblem;

void free_GridSearchResult(GridSearchResult result);
GridSearchResult transfer_dv(GridSearchProblem problem);

#endif // TRAJECTORY_OPTIMIZERS_H