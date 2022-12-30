from functools import partial
from multiprocessing import Pool, cpu_count

import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from tqdm import tqdm

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.trajectory.transfer_orbit import trajectory_ejection_dv
from trajectorize.visualizers.parula_colourmap import parula_map


def porkchop_plot_ejection(body1: Body, body2: Body, ax: Axes,
                           t1_min: float, t1_max: float,
                           tof_min: float, tof_max: float,
                           parking_orbit_alt: float) -> Artist:
    '''
    Plots a porkchop plot of the ejection times from body1 to body2.
    '''

    t1 = np.linspace(t1_min, t1_max, 200)

    tof = np.linspace(tof_min, tof_max, 200)

    g_t1, g_tof = np.meshgrid(t1, tof)

    # construct iterable of arguments for the pool
    t1t2_vals = zip(g_t1.ravel(), g_t1.ravel() + g_tof.ravel())

    # make a partial function to pass to the pool for a given t1 and t2
    # using star map to unpack the arguments

    with Pool(cpu_count() - 1) as pool:
        dvs = pool.starmap(partial(trajectory_ejection_dv,
                                   body1=body1,
                                   body2=body2,
                                   parking_orbit_alt=parking_orbit_alt),
                           tqdm(t1t2_vals, total=len(t1) * len(tof),
                                desc="Calculating Porkchop Plot"))

    # convert the time values to kerbin days

    t1_kerbin_days = g_t1 / 86400 * 4
    tof_kerbin_days = g_tof / 86400 * 4
    # reshape dv to match t1_kerbin_days and tof_kerbin_days
    dv = np.array(dvs).reshape(t1_kerbin_days.shape)

    # plot the porkchop plot
    mesh = ax.pcolormesh(t1_kerbin_days, tof_kerbin_days, dv, cmap="jet",
                         shading='gouraud', vmin=min(dvs),
                         vmax=np.percentile(dvs, 99))

    # add colorbar
    tick_marks = np.linspace(np.percentile(
        dvs, 0.5), np.percentile(dvs, 99), 10)
    colorbar = ax.figure.colorbar(mesh, ax=ax, fraction=0.05, extend='max')
    colorbar.set_ticks(tick_marks)

    # show min dv point using lines
    min_dv_idx = np.unravel_index(np.argmin(dv), dv.shape)
    t1_min_dv = t1_kerbin_days[min_dv_idx]
    tof_min_dv = tof_kerbin_days[min_dv_idx]
    ax.axvline(t1_min_dv, color='w', linestyle='--')
    ax.axhline(tof_min_dv, color='w', linestyle='--')

    # set the labels
    ax.set_title(f'Porkchop Plot from {body1.name} to {body2.name}')
    ax.set_xlabel('Departure Time (Kerbin Days)')
    ax.set_ylabel('Time of Flight (Kerbin Days)')

    return (mesh, colorbar)
