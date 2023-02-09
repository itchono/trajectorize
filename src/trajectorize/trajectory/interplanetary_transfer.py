from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.c_ext_utils.extract_arrays import extract_double_array
from trajectorize.ephemeris.kerbol_system import Body


def _process_chunked_dv(t1_min: float, t1_max: float,
                        tof_lim: "tuple(float, float)",
                        body1: Body, body2: Body,
                        parking_orbit_alt: float,
                        n_grid_t1: int = 100,
                        n_grid_tof: int = 100) -> np.ndarray:
    gs_prob = ffi.new("struct GridSearchProblem *",
                      {"body1": body1.c_data,
                       "body2": body2.c_data,
                       "r_pe_1": parking_orbit_alt,
                       "t1_min": t1_min,
                       "t1_max": t1_max,
                       "tof_min": tof_lim[0],
                       "tof_max": tof_lim[1],
                       "n_grid_t1": n_grid_t1,
                       "n_grid_tof": n_grid_tof})[0]

    gs_sol = lib.ejection_dv(gs_prob)

    # parse arrays
    arr_shape = (gs_prob.n_grid_t1, gs_prob.n_grid_tof)

    dv = extract_double_array(gs_sol.dv, arr_shape)
    t1 = extract_double_array(gs_sol.t1, arr_shape)
    tof = extract_double_array(gs_sol.tof, arr_shape)

    lib.free_GridSearchResult(gs_sol)

    return np.stack((dv, t1, tof), -1)


def interplanetary_transfer_dv(body1: Body, body2: Body,
                               t1_lim: "tuple(float, float)",
                               tof_lim: "tuple(float, float)",
                               parking_orbit_alt: float,
                               n_grid: int = 200,
                               process_count: int = cpu_count()) \
        -> "tuple(np.ndarray, np.ndarray, np.ndarray)":
    if process_count > n_grid:
        raise ValueError(f"process_count of {process_count} is greater"
                         f" than grid size of {n_grid}, cannot slice"
                         " problem so finely. Use fewer processes.")
        
    if body1.parent != body2.parent:
        raise ValueError("body1 and body2 must have the same parent.")

    # Chunk the problem into multiple "strips" of t1 to be solve
    n_grid_t1 = round(n_grid / process_count)

    t1_limit_vals = np.linspace(*t1_lim, process_count + 1)
    t1_limit_zip = zip(t1_limit_vals[:-1], t1_limit_vals[1:])

    with Pool(process_count) as pool:
        arr_seq = pool.starmap(partial(_process_chunked_dv,
                                       body1=body1, body2=body2,
                                       tof_lim=tof_lim,
                                       parking_orbit_alt=parking_orbit_alt,
                                       n_grid_t1=n_grid_t1, n_grid_tof=n_grid),
                               t1_limit_zip)

    big_arr = np.concatenate(arr_seq, 0)

    dv = big_arr[:, :, 0]
    t1 = big_arr[:, :, 1]
    tof = big_arr[:, :, 2]

    return (dv, t1, tof)
