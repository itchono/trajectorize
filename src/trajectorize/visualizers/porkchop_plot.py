from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes

from trajectorize._c_extension import ffi, lib
from trajectorize.c_ext_utils.extract_arrays import extract_double_array
from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.ksp_time.mpl_formatters import DeltaFormatter, UTFormatter
from trajectorize.ksp_time.time_conversion import TimeType, ut_to_ut_string
from trajectorize.visualizers.parula_colourmap import parula_map


def process_chunked_dv(t1_min: float, t1_max: float,
                       tof_min: float, tof_max: float,
                       body1: Body, body2: Body, parking_orbit_alt: float,
                       n_grid_t1: int = 100,
                       n_grid_tof: int = 100) -> np.ndarray:
    gs_prob = ffi.new("struct GridSearchProblem *",
                      {"body1": body1.c_data,
                       "body2": body2.c_data,
                       "r_pe_1": parking_orbit_alt,
                       "t1_min": t1_min,
                       "t1_max": t1_max,
                       "tof_min": tof_min,
                       "tof_max": tof_max,
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


def porkchop_plot_ejection(body1: Body, body2: Body, ax: Axes,
                           t1_min: float, t1_max: float,
                           tof_min: float, tof_max: float,
                           parking_orbit_alt: float,
                           n_grid: int = 200,
                           process_count: int = cpu_count()) -> Artist:
    '''
    Plots a porkchop plot of the ejection times from body1 to body2.
    '''
    if process_count > n_grid:
        raise ValueError(f"process_count of {process_count} is greater"
                         f" than grid size of {n_grid}, cannot slice"
                         " problem so finely. Use fewer processes.")

    # Chunk the problem into multiple "strips" of t1 to be solve
    n_grid_t1 = round(n_grid / process_count)

    t1_limit_vals = np.linspace(t1_min, t1_max, process_count + 1)
    t1_limit_zip = zip(t1_limit_vals[:-1], t1_limit_vals[1:])

    with Pool(process_count) as pool:
        arr_seq = pool.starmap(partial(process_chunked_dv,
                                       body1=body1, body2=body2,
                                       tof_min=tof_min, tof_max=tof_max,
                                       parking_orbit_alt=parking_orbit_alt,
                                       n_grid_t1=n_grid_t1, n_grid_tof=n_grid),
                               t1_limit_zip)

    big_arr = np.concatenate(arr_seq, 0)

    dv = big_arr[:, :, 0]
    t1 = big_arr[:, :, 1]
    tof = big_arr[:, :, 2]

    dvs = dv.ravel()

    t1_kerbin_days = t1 / 21600
    tof_kerbin_days = tof / 21600

    disp_percentile_max = 95

    # plot the porkchop plot
    mesh = ax.pcolormesh(t1_kerbin_days, tof_kerbin_days, dv, cmap="jet",
                         shading="gouraud", vmin=min(dvs),
                         vmax=np.nanpercentile(dvs, disp_percentile_max))
    # ax.fmt_xdata = UTFormatter(TimeType.KERBIN_TIME)

    # add colorbar
    tick_marks = np.linspace(
        min(dvs), np.nanpercentile(dvs, disp_percentile_max), 10)
    colorbar = ax.figure.colorbar(mesh, ax=ax, fraction=0.05, extend='max')
    colorbar.set_ticks(tick_marks)

    # show min dv point using lines
    min_dv_idx = np.unravel_index(np.argmin(dv), dv.shape)
    t1_min_dv = t1_kerbin_days[min_dv_idx]
    tof_min_dv = tof_kerbin_days[min_dv_idx]
    ax.axvline(t1_min_dv, color='w', linestyle='--', lw=1)
    ax.axhline(tof_min_dv, color='w', linestyle='--', lw=1)

    # set the labels
    ax.set_title(f'Porkchop Plot from {body1.name} to {body2.name}\n'
                 f'Min. dv={min(dvs):.2f} m/s '
                 f'on {ut_to_ut_string(t1[min_dv_idx], TimeType.KERBIN_TIME)}')
    ax.set_xlabel('Departure Time (Kerbin Days)')
    ax.set_ylabel('Time of Flight (Kerbin Days)')

    return (mesh, colorbar)
