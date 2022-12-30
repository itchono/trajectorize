import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.trajectory.transfer_orbit import planetary_transfer_orbit
from trajectorize.visualizers.celestial_body_plot import plot_body_rel_kerbol


def plot_transfer_orbit(body1: Body, body2: Body, t1: float, t2: float,
                        ax: Axes,
                        plot_full_orbit: bool = False) -> "tuple(Artist)":
    '''
    Plots a transfer orbit between two bodies on a matplotlib axes object.

    Parameters
    ----------
    body1: Body
        The first body.
    body2: Body
        The second body.
    t1: float
        The departure time in seconds.
    t2: float
        The arrival time in seconds.
    ax: Axes
        The axes on which to plot the transfer orbit.
    plot_full_orbit: bool
        Whether or not to plot the full ellipse of the orbit. Plots only
        the portion of the orbit between t1 and t2 if False.
    '''
    # Get transfer orbit
    transfer_orbit = planetary_transfer_orbit(body1, body2, t1, t2)

    if plot_full_orbit:
        transfer_locus = transfer_orbit.get_locus(500)
    else:
        eval_times = np.linspace(t1, t2, 500)
        transfer_locus = transfer_orbit.propagate_vec(eval_times)

    path, = ax.plot(transfer_locus[:, 0],
                    transfer_locus[:, 1], color="C1", lw=2)
    return path


def plot_interplanetary_transfer(body1: Body, body2: Body, t1: float,
                                 t2: float, ax: Axes) -> None:

    # Get transfer orbit
    plot_transfer_orbit(body1, body2, t1, t2, ax)

    # Plot planets
    plot_body_rel_kerbol(body1, t1, ax, plot_orbit=True,
                         marker_str="o", markersize=10)
    plot_body_rel_kerbol(body1, t2, ax, plot_orbit=False,
                         marker_str="D", markersize=10)
    plot_body_rel_kerbol(body2, t1, ax, plot_orbit=True,
                         marker_str="o", markersize=10)
    plot_body_rel_kerbol(body2, t2, ax, plot_orbit=False,
                         marker_str="D", markersize=10)
    plot_body_rel_kerbol(body1.parent, t1, ax, markersize=10)

    # Styling
    ax.set_axis_off()
    ax.set_aspect("equal")
