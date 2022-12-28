from matplotlib import pyplot as plt

from trajectorize.visualizers.celestial_body_plot import kerbol_system_plot

if __name__ == "__main__":

    plt.style.use('dark_background')

    fig, ax = plt.subplots(figsize=(8, 7))

    kerbol_system_plot(0, ax)

    # Determine backend; if GUI, show plot, else save to file

    # Agg backend is used for non-GUI environments
    if plt.get_backend() == "agg":
        plt.savefig("kerbol_system.png")
        print("Non-GUI backend detected. Plot saved to orbit.png")
    else:
        plt.show()
