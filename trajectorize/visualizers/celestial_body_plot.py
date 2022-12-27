from matplotlib import pyplot as plt
from matplotlib.artist import Artist

from trajectorize.ephemeris.kerbol_system import (Body, KerbolSystemBodyEnum,
                                                  state_vector_at_time)
from trajectorize.orbit.conic_kepler import KeplerianElements, KeplerianOrbit


def plot_body_rel_kerbol(body: Body, ut: float, ax: plt.Axes,
                         plot_orbit: bool = True,
                         num_ellipse_samples: int = 1000) -> "tuple(Artist)":
    '''
    Plots a celestial body on a matplotlib axes object.

    Plot centered around the Kerbol system origin.

    Parameters
    ----------
    body: CelestialBody
        The body to plot.
    ut: float
        Universal time in seconds. (Game Time)
    ax: plt.Axes
        The axes on which to plot the body.
    mu: float
        The gravitational parameter of the central body.
    plot_orbit: bool
        Whether to plot the orbit of the body.
    num_ellipse_samples: int
        The number of samples to use when plotting the orbit ellipse.
    '''
    obj_state_vec = state_vector_at_time(ut, KerbolSystemBodyEnum.KERBOL,
                                         body.body_id)

    kerbol = Body(KerbolSystemBodyEnum.KERBOL)

    elements = KeplerianElements.from_celestial_body(body, ut)

    marker, = ax.plot(obj_state_vec.position[0], obj_state_vec.position[1],
                      'o', markersize=5, color=f"#{body.colour}")

    if plot_orbit:
        obj_orbit = KeplerianOrbit(elements, kerbol)
        obj_locus = obj_orbit.get_locus(num_ellipse_samples)
        path, = ax.plot(obj_locus[:, 0], obj_locus[:, 1],
                        color=f"#{body.colour}",
                        label=body.name.title())
        return marker, path
    else:
        print(obj_state_vec)
        return marker


def kerbol_system_plot(ut: float, ax: plt.Axes,
                       num_ellipse_samples: int = 1000,
                       show_legend: bool = True) -> "tuple(Artist)":
    all_bodies: "list[Body]" = \
        [Body(i) for i in KerbolSystemBodyEnum.__members__.values()]
    planets = [body for body in all_bodies if body.parent_id ==
               KerbolSystemBodyEnum.KERBOL]  # (also includes Kerbol)

    for body in planets:
        plot_body_rel_kerbol(body, ut, ax, num_ellipse_samples)

    # Styling
    ax.set_axis_off()
    ax.set_aspect("equal")

    ax.set_title(f"Kerbol System at UT = {ut} seconds")

    if show_legend:
        ax.legend()
