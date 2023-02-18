from matplotlib import pyplot as plt

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.visualizers.display_utils import display_or_save_plot
from trajectorize.trajectory.transfer_orbit import \
    get_transfer_orbit, get_excess_velocity, ArrivalDeparture
from trajectorize.visualizers.transfer_orbit_plot import plot_transfer
from trajectorize.visualizers.local_to_body_plot import \
    plot_trajectory_local_to_body, plot_infinity_vector

if __name__ == "__main__":
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1 = 5091552
    t2 = 10679760

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(8, 7))

    transfer_orbit = get_transfer_orbit(kerbin, duna, t1, t2)
    inf_velocity = get_excess_velocity(
        transfer_orbit, ArrivalDeparture.DEPARTURE)

    plot_transfer(kerbin, duna, t1, t2, ax)

    ax.set_title("Ballistic Transfer from Kerbin to Duna\n"
                 f"Departure: UT = {t1} seconds\n"
                 f"Time of Flight: {t2 - t1} seconds\n")
    fig.tight_layout()
    display_or_save_plot("kerbin_duna_transfer.png")
