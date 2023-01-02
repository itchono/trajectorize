from matplotlib import pyplot as plt

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.visualizers.display_utils import display_or_save_plot
from trajectorize.visualizers.porkchop_plot import porkchop_plot_ejection, \
    porkchop_plot_ejection_v2
from time import perf_counter

if __name__ == "__main__":
    kerbin = Body.from_name("Kerbin")
    duna = Body.from_name("Duna")

    t1_min = 0
    t1_max = 852 * 86400 / 4

    tof_min = 151 * 86400 / 4
    tof_max = 453 * 86400 / 4

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(8, 7))
    start = perf_counter()
    porkchop_plot_ejection_v2(kerbin, duna, ax, t1_min,
                              t1_max, tof_min, tof_max, 70000)
    print(f"Time: {perf_counter() - start:.3f} s")

    display_or_save_plot("kerbin_duna_porkchop.png")