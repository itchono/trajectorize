import numpy as np
from matplotlib import pyplot as plt

from trajectorize.ephemeris.kerbol_system import Body
from trajectorize.ksp_time.time_conversion import ut_to_ut_string
from trajectorize.orbit.conic_kepler import KeplerianOrbit
from trajectorize.trajectory.transfer_orbit import approximate_time_of_flight
from trajectorize.visualizers.display_utils import display_or_save_plot
from trajectorize.visualizers.planetary_transfer_plot import plot_transfer
from trajectorize.visualizers.porkchop_plot import porkchop_plot_ejection

if __name__ == "__main__":
    body1 = Body.from_name("Kerbin")
    body2 = Body.from_name("Duna")

    # Use orbital period as heuristic for departure time look range
    t1_min = 0
    t1_max = t1_min + KeplerianOrbit.from_celestial_body(body1, 0).T * 2
    
    # Use Hohmann transfer heuristic for transfer time
    tof_approx = approximate_time_of_flight(body1, body2)
    tof_min = tof_approx/2
    tof_max = tof_approx*2
    n_grid = 300

    plt.style.use('dark_background')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    (dv, t1, tof) = porkchop_plot_ejection(ax1, body1, body2,
                                           (t1_min, t1_max),
                                           (tof_min, tof_max),
                                           100000, n_grid)

    # Mark minimum dv point
    min_dv_idx = np.unravel_index(np.nanargmin(dv), dv.shape)
    cursor_vline = ax1.axvline(t1[min_dv_idx], color='w', linestyle='--', lw=1)
    cursor_hline = ax1.axhline(
        tof[min_dv_idx], color='w', linestyle='--', lw=1)
    
    def find_index_from_t1_tof(event_t1: float, event_tof: float) -> np.ndarray:
        '''
        Return 2-index corresponding to a certain t1 and tof value.
        '''
        grid_spacing_t1 = (t1_max-t1_min)/n_grid
        grid_spacing_tof = (tof_max - tof_min) / n_grid
        return np.argwhere((np.abs(t1 - event_t1) < grid_spacing_t1)
                                & (np.abs(tof - event_tof) < grid_spacing_tof))[0]

    def draw_transfer_plot(event_t1: float, event_tof: float):
        # ax1: Move cursor lines
        # vline, hline are 2 points
        cursor_hline.set_ydata([event_tof, event_tof])
        cursor_vline.set_xdata([event_t1, event_t1])

        # ax2: plot interplanetary transfer
        ax2.clear()
        plot_transfer(
            body1, body2, event_t1, event_t1 + event_tof, ax2)
        
        dv_idx = find_index_from_t1_tof(event_t1, event_tof)
        traj_dv = dv[dv_idx[0], dv_idx[1]]
        traj_t1 = t1[dv_idx[0], dv_idx[1]]
        traj_tof = tof[dv_idx[0], dv_idx[1]] 
        ax2.set_title(f"$\Delta v$: {traj_dv:.2f} m/s\n"
                      f"Departure: {ut_to_ut_string(traj_t1)}\n"
                      f"Arrival: {ut_to_ut_string(traj_t1+traj_tof)}\n"
                      f"Time of Flight: {traj_tof / 21600:.0f} Kerbin Days")
        fig.canvas.draw_idle()

    # Call the drawing function once for minimum energy trajectory
    draw_transfer_plot(t1[min_dv_idx], tof[min_dv_idx])

    # Handler for clicking on the plot
    def onclick(event):
        if event.inaxes == ax1:
            draw_transfer_plot(event.xdata, event.ydata)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    
    fig.tight_layout()
    fig.subplots_adjust(top=0.8)

    display_or_save_plot("kerbin_duna_porkchop.png")
