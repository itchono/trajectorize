import numpy as np
from matplotlib.axes import Axes

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.ksp_time.mpl_formatters import DeltaFormatter, UTFormatter
from trajectorize.trajectory.interplanetary_transfer import \
    interplanetary_transfer_dv
from trajectorize.visualizers.parula_colourmap import parula_map


def porkchop_plot_ejection(ax: Axes,
                           body1: Body, body2: Body,
                           t1_lim: "tuple(float, float)",
                           tof_lim: "tuple(float, float)",
                           parking_orbit_alt: float,
                           capture_orbit_alt: float,
                           include_capture: bool,
                           n_grid: int = 200) \
        -> "tuple(np.ndarray, np.ndarray, np.ndarray)":
    '''
    Plots a porkchop plot of the ejection times from body1 to body2.

    Returns the data arrays
    '''
    dv, t1, tof = interplanetary_transfer_dv(body1, body2,
                                             t1_lim, tof_lim,
                                             parking_orbit_alt,
                                             capture_orbit_alt,
                                             include_capture,
                                             n_grid)

    dvs = dv.ravel()

    disp_percentile_max = 90

    # plot the porkchop plot
    mesh = ax.pcolormesh(t1, tof, dv, cmap="jet",
                         shading="gouraud", vmin=np.nanmin(dvs),
                         vmax=np.nanpercentile(dvs, disp_percentile_max))
    ax.xaxis.set_major_formatter(UTFormatter())
    ax.yaxis.set_major_formatter(DeltaFormatter())
    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')

    # add colorbar
    tick_marks = np.linspace(
        np.nanmin(dvs), np.nanpercentile(dvs, disp_percentile_max), 10)
    colorbar = ax.figure.colorbar(mesh, ax=ax, fraction=0.05, extend='max',
                                  label=f"$\Delta v$ cost (m/s)")
    colorbar.set_ticks(tick_marks)

    # set the labels
    dv_title = "Ejection + Capture" if include_capture else "Ejection"

    ax.set_title(
        f'{dv_title} $\Delta v$ from {body1.name} to {body2.name} (m/s)')
    ax.set_xlabel('Departure Time')
    ax.set_ylabel('Time of Flight')

    return (dv, t1, tof)
