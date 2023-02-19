import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.patches import Circle

from trajectorize.ephemeris.kerbol_system import Body, state_vector_at_time


def _2d_view_index(view: str) -> "tuple(int, int)":
    '''
    Returns the indices of the 2D view.

    Parameters
    ----------
    view: str
        The view to plot. One of "xy", "xz", "yz".

    Returns
    -------
    tuple(int, int):
        The indices of the 2D view.
    '''
    if view == "xy":
        return 0, 1
    elif view == "xz":
        return 0, 2
    elif view == "yz":
        return 1, 2
    else:
        raise ValueError(
            f"Invalid view: {view}. Must be one of 'xy', 'xz', 'yz'")


def plot_trajectory_local_to_body(ax: Axes, body: Body, trajectory: np.ndarray,
                                  view: str = "xy",
                                  path_colour: str = "C1") -> "tuple(Artist)":
    '''
    Plots xy, xz, yz views of the trajectory

    Parameters
    ----------
    ax: Axes
        The axes on which to plot the trajectory.
    body: Body
        The body to plot the trajectory relative to.
    trajectory: np.ndarray
        The trajectory to plot (n x 3)
    view: str
        The view to plot. One of "xy", "xz", "yz".
    path_colour: str
        The colour of the trajectory path.

    Returns
    -------
    tuple(Artist):
        The artists that were plotted.
    '''
    # Plot the patch for the body
    body_patch = Circle((0, 0), body.radius, color=body.colour_hex)

    ax.add_patch(body_patch)

    # Plot the trajectory
    ind_x, ind_y = _2d_view_index(view)

    x = trajectory[:, ind_x]
    y = trajectory[:, ind_y]

    ax.set_aspect("equal")
    ax.set_xlabel(f"{view[0]} position (mm)")
    ax.set_ylabel(f"{view[1]} position (mm)")
    ax.set_axis_off()

    traj_path = ax.plot(x, y, color=path_colour)

    # Plot arrow at end of trajectory
    arrow = ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-2], y[-2]),
                        color=path_colour, arrowprops=dict(arrowstyle="->"))

    return (body_patch, traj_path, arrow)


def plot_prograde_line(ax: Axes, body: Body, ut: float,
                       view: str = "xy") -> "tuple(Artist)":
    '''
    Plots a line in the direction of the prograde vector.

    Parameters
    ----------
    ax: Axes
        The axes on which to plot the trajectory.
    body: Body
        The body to plot the trajectory relative to.
    ut: float
        The universal time at which to plot the prograde vector.
    view: str
        The view to plot. One of "xy", "xz", "yz".
    '''

    body_vel = state_vector_at_time(ut, body.parent_id, body.body_id).velocity

    ind_x, ind_y = _2d_view_index(view)

    # Plot line in direction of velocity vector
    return ax.axline((0, 0), slope=body_vel[ind_y] /
                     body_vel[ind_x], color=body.colour_hex, ls="--", alpha=0.5,
                     label=f"{body.name} prograde")


def plot_infinity_vector(ax: Axes, vector: np.ndarray,
                         offset: np.ndarray = np.zeros(3),
                         view: str = "xy") -> "tuple(Artist)":
    '''
    Plots velocity vector at infinity, if applicable.

    Parameters
    ----------
    ax: Axes
        The axes on which to plot the vector.
    vector: np.ndarray
        The vector to plot.
    offset: np.ndarray
        The offset to apply to the vector.
    view: str
        The view to plot. One of "xy", "xz", "yz".
    '''
    ind_x, ind_y = _2d_view_index(view)

    # Plot a quiver in the direction of the velocity vector, starting
    # at the offset point
    x = offset[ind_x]
    y = offset[ind_y]
    u = vector[ind_x]
    v = vector[ind_y]

    return ax.quiver(x, y, u, v)
