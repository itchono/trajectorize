import numpy as np
from matplotlib.axes import Axes
from matplotlib.artist import Artist

from trajectorize.ksp_time.mpl_formatters import DeltaFormatter, UTFormatter
from trajectorize.trajectory.interplanetary_transfer import \
    InterplanetaryTransferResult
from trajectorize.visualizers.parula_colourmap import parula_map


def transfer_porkchop_plot(ax: Axes, dv_info: InterplanetaryTransferResult,
                           plot_type: str = "ejection") -> "tuple(Artist)":
    '''
    Plots a porkchop plot of the ejection times from body1 to body2.

    Parameters
    ----------
    ax: Axes
        The axes on which to plot the porkchop plot.
    dv_info: InterplanetaryTransferResult
        The result of the interplanetary transfer calculation.
    plot_type: str
        The type of porkchop plot to plot. One of "ejection", "capture", or
        "combined".

    Returns
    -------
    tuple(Artist):
        The artists that were plotted.
    '''

    if plot_type == "ejection":
        dv = dv_info.dv_ejection
        dv_title = "Ejection"
    elif plot_type == "capture":
        dv = dv_info.dv_capture
        dv_title = "Capture"
    elif plot_type == "combined":
        dv = dv_info.dv_ejection + dv_info.dv_capture
        dv_title = "Ejection + Capture"
    else:
        raise ValueError("Unrecognized plot_type. Must be one of 'ejection', "
                         "'capture', or 'combined'")

    dvs = dv.ravel()

    disp_percentile_max = 90

    # plot the porkchop plot
    mesh = ax.pcolormesh(dv_info.t1, dv_info.tof, dv, cmap="jet",
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
                                  label=f"$\\Delta v$ cost (m/s)")
    colorbar.set_ticks(tick_marks)

    # set the labels
    ax.set_title(
        f'{dv_title} $\\Delta v$ from {dv_info.body1.name}'
        f' to {dv_info.body2.name} (m/s)')
    ax.set_xlabel('Departure Time')
    ax.set_ylabel('Time of Flight')

    return (mesh, colorbar)
