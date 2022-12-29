from argparse import ArgumentParser

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

from trajectorize.ephemeris.kerbol_system import (Body, BodyEnum,
                                                  state_vector_at_time)

if __name__ == "__main__":

    parser = ArgumentParser(description="Kerbol System Animation")

    '''
    Command Line Options

    --save: Save the animation to a file
    --length: Length of the animation in years (each year is 426.08 Kerbin days)
    '''
    parser.add_argument("--save", action="store_true",
                        help="Save the animation to a file")
    parser.add_argument(
        "--length",
        type=int,
        default=10,
        help="Length of the animation in years (each year is 426.08 Kerbin days)")

    args = parser.parse_args()

    years = args.length
    save_anim = args.save

    KERBIN_DAY = 21600
    KERBIN_YEAR = 426.08 * KERBIN_DAY

    # Generate animated frames
    t_ut = np.linspace(0, KERBIN_YEAR * years, 500)

    plt.style.use('dark_background')

    figsize = (3.5, 3.5) if save_anim else (8, 7)

    fig, ax = plt.subplots(figsize=figsize)

    planets = Body.planets()

    # place title inside the axes so it can blit
    title = ax.set_title(
        f"Kerbol System, UT = {round(t_ut[0]/KERBIN_DAY)}d",
        y=0.8, x=0.5, fontsize=10)

    ax.set_axis_off()
    ax.set_aspect('equal')
    fig.tight_layout()

    # Plot Kerbol and orbits of planets (static; no need to redraw)
    kerbol = Body.from_name("Kerbol")
    ax.plot(0, 0, 'o', markersize=5, color=kerbol.colour_hex)

    for body in planets:
        locus = body.orbit_locus(100)
        ax.plot(locus[:, 0], locus[:, 1],
                color=body.colour_hex,
                label=body.name)

    # Construct dynamic artists; these are the planets and their markers
    planet_ephemerides = [[None] * len(planets) for _ in range(len(t_ut))]

    for i, ut in enumerate(t_ut):
        for j, b in enumerate(planets):
            planet_ephemerides[i][j] = state_vector_at_time(ut,
                                                            BodyEnum.KERBOL,
                                                            b.body_id)

    planet_artists = [None for _ in range(len(planets))]

    for i, b in enumerate(planets):
        marker, = ax.plot(planet_ephemerides[0][i].position[0],
                          planet_ephemerides[0][i].position[1],
                          'o', markersize=5, color=b.colour_hex)
        planet_artists[i] = marker

    # Construct animation

    def animate(i):
        for j, b in enumerate(planets):
            planet_artists[j].set_data(planet_ephemerides[i][j].position[0],
                                       planet_ephemerides[i][j].position[1])

        title.set_text(f"Kerbol System, UT = {round(t_ut[i]/KERBIN_DAY)}d")

        return planet_artists + [title]

    animation = FuncAnimation(fig, animate, frames=len(
        t_ut) - 1, interval=30, blit=True)

    if plt.get_backend() == "agg":
        print("Non-GUI backend detected. Cannot show animation.")
    else:
        plt.show()

    if save_anim:
        # Write animation to file
        # TODO: optimize GIF to reduce file size
        writer = PillowWriter(fps=30,
                              metadata=dict(artist='Me'),
                              bitrate=50)
        animation.save('kerbol_system.gif', writer=writer)
