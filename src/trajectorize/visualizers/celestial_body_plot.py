from matplotlib.artist import Artist
from matplotlib.axes import Axes

from trajectorize.ephemeris.kerbol_system import (Body, BodyEnum,
                                                  state_vector_at_time)
from trajectorize.orbit.conic_kepler import KeplerianElements, KeplerianOrbit


def plot_body_rel_kerbol(body: Body, ut: float, ax: Axes,
                         plot_orbit: bool = True,
                         num_ellipse_samples: int = 1000,
                         marker_str: str = "o",
                         markersize: int = 5) -> "tuple(Artist)":
    '''
    Plots a celestial body on a matplotlib axes object.

    Plot centered around the Kerbol system origin.

    Parameters
    ----------
    body: CelestialBody
        The body to plot.
    ut: float
        Universal time in seconds. (Game Time)
    ax: Axes
        The axes on which to plot the body.
    mu: float
        The gravitational parameter of the central body.
    plot_orbit: bool
        Whether to plot the orbit of the body.
    num_ellipse_samples: int
        The number of samples to use when plotting the orbit ellipse.
    marker_str: str
        The marker to use when plotting the body. (see matplotlib docs)
    markersize: int
        The size of the marker to use when plotting the body.
    '''
    obj_state_vec = state_vector_at_time(ut, BodyEnum.KERBOL,
                                         body.body_id)
    marker, = ax.plot(obj_state_vec.position[0], obj_state_vec.position[1],
                      marker=marker_str, markersize=markersize,
                      color=body.colour_hex,
                      label=body.name)

    if plot_orbit:
        obj_locus = body.orbit_locus(num_ellipse_samples)
        path, = ax.plot(obj_locus[:, 0], obj_locus[:, 1],
                        color=body.colour_hex)
        return marker, path
    else:
        return marker


def kerbol_system_plot(ut: float, ax: Axes,
                       num_ellipse_samples: int = 1000,
                       show_legend: bool = True,
                       markersize: int = True) -> "tuple(Artist)":
    '''
    Higher level "prefab" function to generate a pretty looking plot
    of the Kerbol system.
    '''
    planets = Body.planets()
    for body in planets:
        plot_body_rel_kerbol(
            body, ut, ax, num_ellipse_samples=num_ellipse_samples,
            markersize=markersize)

    # Plot Kerbol
    kerbol = Body.from_name("Kerbol")
    ax.plot(0, 0, 'o', markersize=markersize, color=kerbol.colour_hex)

    # Styling
    ax.set_axis_off()
    ax.set_aspect("equal")

    ax.set_title(f"Kerbol System at UT = {ut} seconds")

    if show_legend:
        ax.legend()
