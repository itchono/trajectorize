from matplotlib import pyplot as plt

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.visualizers.display_utils import display_or_save_plot
from trajectorize.visualizers.planetary_transfer_plot import plot_transfer

if __name__ == "__main__":
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1 = 5091552
    t2 = 10679760

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(8, 7))

    plot_transfer(kerbin, duna, t1, t2, ax)

    ax.set_title("Ballistic Transfer from Kerbin to Duna\n"
                 f"Departure: UT = {t1} seconds\n"
                 f"Time of Flight: {t2 - t1} seconds\n")
    fig.tight_layout()
    display_or_save_plot("kerbin_duna_transfer.png")
