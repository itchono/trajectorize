from functools import partial
from multiprocessing import Pool, cpu_count
from typing import NamedTuple

import numpy as np

from trajectorize._c_extension import ffi, lib
from trajectorize.c_ext_utils.extract_arrays import extract_double_array
from trajectorize.ephemeris.kerbol_system import Body


class InterplanetaryTransferResult(NamedTuple):
    body1: Body
    body2: Body
    dv_ejection: np.ndarray
    dv_capture: np.ndarray
    t1: np.ndarray
    tof: np.ndarray
    include_capture: bool

    @property
    def dv(self):
        return self.dv_ejection + self.dv_capture \
            if self.include_capture else self.dv_ejection


def _process_chunked_dv(t1_min: float, t1_max: float,
                        tof_lim: "tuple(float, float)",
                        body1: Body, body2: Body,
                        parking_orbit_alt: float,
                        capture_orbit_alt: float,
                        include_capture: bool,
                        n_grid_t1: int = 100,
                        n_grid_tof: int = 100) -> np.ndarray:

    r_pe_1 = parking_orbit_alt + body1.radius
    if include_capture:
        r_pe_2 = capture_orbit_alt + body2.radius
    else:
        r_pe_2 = 0

    gs_prob = ffi.new("struct GridSearchProblem *",
                      {"body1": body1.c_data,
                       "body2": body2.c_data,
                       "include_capture": include_capture,
                       "r_pe_1": r_pe_1,
                       "r_pe_2": r_pe_2,
                       "t1_min": t1_min,
                       "t1_max": t1_max,
                       "tof_min": tof_lim[0],
                       "tof_max": tof_lim[1],
                       "n_grid_t1": n_grid_t1,
                       "n_grid_tof": n_grid_tof})[0]

    gs_sol = lib.transfer_dv(gs_prob)

    # parse arrays
    arr_shape = (gs_prob.n_grid_t1, gs_prob.n_grid_tof)

    dv_ejection = extract_double_array(gs_sol.dv_ejection, arr_shape)
    dv_capture = extract_double_array(gs_sol.dv_capture, arr_shape)
    t1 = extract_double_array(gs_sol.t1, arr_shape)
    tof = extract_double_array(gs_sol.tof, arr_shape)

    lib.free_GridSearchResult(gs_sol)

    return np.stack((dv_ejection, dv_capture, t1, tof), -1)


def interplanetary_transfer_dv(body1: Body, body2: Body,
                               t1_lim: "tuple(float, float)",
                               tof_lim: "tuple(float, float)",
                               parking_orbit_alt: float,
                               capture_orbit_alt: float,
                               include_capture: bool,
                               n_grid: int = 200,
                               process_count: int = cpu_count()) \
        -> InterplanetaryTransferResult:

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
                                       capture_orbit_alt=capture_orbit_alt,
                                       include_capture=include_capture,
                                       n_grid_t1=n_grid_t1, n_grid_tof=n_grid),
                               t1_limit_zip)

    big_arr = np.concatenate(arr_seq, 0)

    dv_ejection = big_arr[:, :, 0]
    dv_capture = big_arr[:, :, 1]
    t1 = big_arr[:, :, 2]
    tof = big_arr[:, :, 3]

    return InterplanetaryTransferResult(body1, body2,
                                        dv_ejection, dv_capture,
                                        t1, tof,
                                        include_capture)
