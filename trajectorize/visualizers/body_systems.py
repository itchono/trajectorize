import numpy as np
from matplotlib import pyplot as plt
from matplotlib.artist import Artist

from trajectorize.ephemeris.kerbol_system import Body, state_vector_at_time


def plot_body(
        body: Body,
        jd: float,
        ax: plt.Axes,
        mu: float,
        plot_orbit: bool = True,
        num_ellipse_samples: int = 1000) -> "tuple(Artist)":
    '''
    Plots a celestial body on a matplotlib axes object.

    Plot is in the barycentric ecliptic frame.

    Parameters
    ----------
    body: CelestialBody
        The body to plot.
    jd: float
        The Julian date at which to plot the body.
    ax: plt.Axes
        The axes on which to plot the body.
    mu: float
        The gravitational parameter of the central body.
    plot_orbit: bool
        Whether to plot the orbit of the body.
    num_ellipse_samples: int
        The number of samples to use when plotting the orbit ellipse.
    '''
    r, v = de440[0, body.ephemeris_id].compute_and_differentiate(jd)

    if frame == "ecliptic":
        C = ecliptic_from_J2000(jd)
    elif frame == "J2000":
        C = np.eye(3)

    r = C @ r * 1e3
    v = C @ v * 1e3

    orbit = KeplerianOrbit.from_state(
        r, v / 86400, mu)

    orbit_r = orbit.get_state_space_orbit(num_ellipse_samples)

    marker, = ax.plot(r[0], r[1], 'o', markersize=5,
                      color=f"#{body.color:X}", label=body.name)

    if plot_orbit:
        path, = ax.plot(orbit_r[0], orbit_r[1], color=f"#{body.color:X}")
        return marker, path
    else:
        return marker
