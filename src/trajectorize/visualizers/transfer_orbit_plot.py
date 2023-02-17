import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.trajectory.transfer_orbit import planetary_transfer_orbit
from trajectorize.visualizers.celestial_system_plot import plot_body_rel_parent
from trajectorize.orbit.conic_kepler import KeplerianOrbit


def plot_transfer_orbit_path(body1: Body, body2: Body, t1: float, t2: float,
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
    transfer_orbit_struct = planetary_transfer_orbit(body1, body2, t1, t2)
    transfer_orbit = KeplerianOrbit(transfer_orbit_struct.ke,
                                    transfer_orbit_struct.body1.parent)

    if plot_full_orbit:
        transfer_locus = transfer_orbit.get_locus(500)
    else:
        eval_times = np.linspace(t1, t2, 500)
        transfer_locus = transfer_orbit.propagate_vec(eval_times)

    path, = ax.plot(transfer_locus[:, 0],
                    transfer_locus[:, 1], color="C1", lw=2)
    return path


def plot_transfer(body1: Body, body2: Body, t1: float,
                  t2: float, ax: Axes) -> None:

    # Get transfer orbit
    plot_transfer_orbit_path(body1, body2, t1, t2, ax)

    # Plot planets
    plot_body_rel_parent(body1, t1, ax, plot_orbit=True,
                         marker_str="o", markersize=10)
    plot_body_rel_parent(body1, t2, ax, plot_orbit=False,
                         marker_str="D", markersize=10)
    plot_body_rel_parent(body2, t1, ax, plot_orbit=True,
                         marker_str="o", markersize=10)
    plot_body_rel_parent(body2, t2, ax, plot_orbit=False,
                         marker_str="D", markersize=10)

    # Plot central body
    ax.plot(0, 0, 'o', markersize=10, color=body1.parent.colour_hex)

    # Plot custom legend; label circle marker = t1, label diamond marker = t2
    legend_elements = [Line2D([0], [0], marker='o', markerfacecolor='w', lw=0,
                              label=f'Positions at {body1.name} Departure'),
                       Line2D([0], [0], marker='D', markerfacecolor='w', lw=0,
                              label=f'Positions at {body2.name} Arrival')]
    ax.legend(handles=legend_elements, loc=(0.5, -0.1))

    # Styling
    ax.set_axis_off()
    ax.set_aspect("equal")
