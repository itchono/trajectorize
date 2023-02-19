from matplotlib import pyplot as plt
import numpy as np

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.visualizers.display_utils import display_or_save_plot
from trajectorize.trajectory.transfer_orbit import \
    get_transfer_orbit, get_excess_velocity, ArrivalDeparture
from trajectorize.visualizers.transfer_orbit_plot import plot_transfer
from trajectorize.orbit.conic_kepler import fit_hyperbolic_trajectory
from trajectorize.visualizers.local_to_body_plot import \
    plot_trajectory_local_to_body, plot_infinity_vector,\
    plot_prograde_line

if __name__ == "__main__":
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1 = 5091552
    t2 = 10679760

    plt.style.use('dark_background')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    transfer_orbit = get_transfer_orbit(kerbin, duna, t1, t2)
    inf_velocity = get_excess_velocity(
        transfer_orbit, ArrivalDeparture.DEPARTURE)

    departure_trajectory = fit_hyperbolic_trajectory(inf_velocity,
                                                     70000 + kerbin.radius,
                                                     kerbin)
    traj_points = departure_trajectory.get_locus(500)

    plot_transfer(kerbin, duna, t1, t2, ax1)

    ax1.set_title("Ballistic Transfer from Kerbin to Duna\n"
                  f"Departure: UT = {t1} seconds\n"
                  f"Time of Flight: {t2 - t1} seconds\n")

    plot_trajectory_local_to_body(ax2, kerbin, traj_points)
    plot_infinity_vector(ax2, inf_velocity)
    plot_prograde_line(ax2, kerbin, t1)

    ax2.set_title("Departure from Kerbin\nEjection Inclination:"
                  f"{np.degrees(departure_trajectory.ke.inclination):.2f} degrees")

    fig.subplots_adjust(top=0.8)
    fig.tight_layout()
    display_or_save_plot("kerbin_duna_transfer.png")
