from matplotlib import pyplot as plt

from trajectorize.visualizers.celestial_body_plot import kerbol_system_plot
from trajectorize.visualizers.display_utils import display_or_save_plot

if __name__ == "__main__":

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(8, 7))

    kerbol_system_plot(0, ax)
    display_or_save_plot("kerbol_system.png")
