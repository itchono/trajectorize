from matplotlib import pyplot as plt


def display_or_save_plot(filename: str):
    # Determine backend; if GUI, show plot, else save to file

    # Agg backend is used for non-GUI environments
    if plt.get_backend() == "agg":
        plt.savefig(filename)
        print(f"Non-GUI backend detected. Plot saved to {filename}")
    else:
        plt.show()
