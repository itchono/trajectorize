from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np

from trajectorize.orbit.universal_kepler import UniversalKeplerOrbit
from trajectorize.visualizers.display_utils import display_or_save_plot

if __name__ == "__main__":
    r0 = np.array([7000, -12124, 0])
    v0 = np.array([2.6679, 4.6210, 0])

    demo_orbit = UniversalKeplerOrbit(r0, v0, 0, 398600)

    t = np.linspace(0, 34000, 1000)

    start = perf_counter()

    orb = demo_orbit.propagate_vec(t)

    r = orb.position
    v = orb.velocity

    plt.style.use("dark_background")
    fig = plt.figure(figsize=(12, 5), tight_layout=True)

    earth = [plt.Circle((0, 0), 6378, color='#00a7a5') for _ in range(3)]
    axes = []

    for i in range(3):
        axes.append(fig.add_subplot(231 + i))
        axes[i].add_patch(earth[i])
        axes[i].set_aspect("equal")

    x = r[:, 0]
    y = r[:, 1]
    z = r[:, 2]
    axes[0].plot(x, y)
    axes[0].set_ylabel("y position (km)")
    axes[0].set_xlabel("x position (km)")
    axes[1].plot(y, z)
    axes[1].set_ylabel("z position (km)")
    axes[1].set_xlabel("y position (km)")
    axes[2].plot(x, z)
    axes[2].set_ylabel("z position (km)")
    axes[2].set_xlabel("x position (km)")
    axes[0].set_title("xy")
    axes[1].set_title("yz")
    axes[2].set_title("xz")

    axes.append(fig.add_subplot(212))
    # Plot altitude above each
    altitude = np.sqrt(x**2 + y**2 + z**2) - 6378
    axes[3].plot(t, altitude)
    axes[3].set_ylabel("Altitude (km)")
    axes[3].set_xlabel("Mission Time (s)")

    fig.suptitle("Universal Keplerian Elements Demo")
    display_or_save_plot("orbit.png")
