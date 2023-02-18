import numpy as np
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.patches import Circle

from trajectorize.ephemeris.kerbol_system import Body


def plot_trajectory_local_to_body(body: Body, trajectory: np.ndarray,
                                  ax: Axes, view: str = "xy") -> "tuple(Artist)":
    '''
    Plots xy, xz, yz views of the trajectory

    Parameters
    ----------
    body: Body
        The body to plot the trajectory relative to.
    trajectory: np.ndarray
        The trajectory to plot (n x 6)
    ax: Axes
        The axes on which to plot the trajectory.
    view: str
        The view to plot. One of "xy", "xz", "yz".

    Returns
    -------
    tuple(Artist):
        The artists that were plotted.
    '''
    # Plot the patch for the body
    body_patch = Circle((0, 0), body.radius, color=body.colour)

    ax.add_patch(body_patch)

    # Plot the trajectory
    if view == "xy":
        ind_x = 0
        ind_y = 1
    elif view == "xz":
        ind_x = 0
        ind_y = 2
    elif view == "yz":
        ind_x = 1
        ind_y = 2
    else:
        raise ValueError(
            f"Unrecognized view {view}. Must be one of 'xy', 'xz', 'yz'")

    x = trajectory[:, ind_x]
    y = trajectory[:, ind_y]

    ax.set_aspect("equal")
    ax.set_xlabel(f"{view[0]} position (mm)")
    ax.set_ylabel(f"{view[1]} position (mm)")

    return (body_patch, ax.plot(x, y))


def plot_infinity_vector(vector: np.ndarray, ax: Axes,
                         offset: np.ndarray = np.zeros(3),
                         view: str = "xy") -> "tuple(Artist)":
    '''
    Plots velocity vector at infinity, if applicable.

    Parameters
    ----------
    vector: np.ndarray
        The vector to plot.
    ax: Axes
        The axes on which to plot the vector.
    offset: np.ndarray
        The offset to apply to the vector.
    view: str
        The view to plot. One of "xy", "xz", "yz".
    '''
    if view == "xy":
        ind_x = 0
        ind_y = 1
    elif view == "xz":
        ind_x = 0
        ind_y = 2
    elif view == "yz":
        ind_x = 1
        ind_y = 2
    else:
        raise ValueError(
            f"Unrecognized view {view}. Must be one of 'xy', 'xz', 'yz'")

    # Plot a quiver in the direction of the velocity vector, starting
    # at the offset point
    x = offset[ind_x]
    y = offset[ind_y]
    u = vector[ind_x]
    v = vector[ind_y]

    return ax.quiver(x, y, u, v)
