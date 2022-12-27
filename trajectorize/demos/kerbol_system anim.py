import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from tqdm import tqdm

from trajectorize.ephemeris.kerbol_system import Body, KerbolSystemBodyEnum
from trajectorize.visualizers.celestial_body_plot import plot_body_rel_kerbol

# Generate animated frames
t_ut = np.linspace(0, 86400*106.5*10, 500)  # 10 kerbin years

artist_lists = [[] for _ in range(len(t_ut))]

plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(8, 7))

all_bodies: "list[Body]" = \
    [Body(i) for i in KerbolSystemBodyEnum.__members__.values()]
planets = [body for body in all_bodies if body.parent_id ==
           KerbolSystemBodyEnum.KERBOL
           and body.body_id != KerbolSystemBodyEnum.KERBOL]

kerbol = Body.from_name("Kerbol")

ax.plot(0, 0, 'o', markersize=5, color=f"#{kerbol.colour}")

# place title inside the axes so it can blit
title = ax.set_title(f"UT = {round(t_ut[0]/86400)} d", y=0.9, x=0.5)

ax.set_axis_off()
ax.set_aspect('equal')

fig.suptitle("Kerbol System Animation", fontsize=16)
fig.tight_layout()

# Construct artist lists
with tqdm(total=len(t_ut), desc="Generating Animation Frames") as pbar:
    for i, ut in enumerate(t_ut):
        for b in planets:
            artist_lists[i].extend(
                plot_body_rel_kerbol(b, ut, ax, num_ellipse_samples=500))

        pbar.update(1)

# Construct animation

for artist_list in artist_lists:
    for artist in artist_list:
        artist.set_visible(False)


def animate(i):
    for artist in artist_lists[i]:
        artist.set_visible(True)

    if i > 0:
        for artist in artist_lists[i-1]:
            artist.set_visible(False)

    title.set_text(f"UT = {round(t_ut[i]/86400)} d")
    return artist_lists[i] + [title]


animation = FuncAnimation(fig, animate, frames=len(
    t_ut) - 1, interval=30, blit=True)

plt.show()

# Write animation to file
# writer = PillowWriter(fps=15,
#                       metadata=dict(artist='Me'),
#                       bitrate=1800)
# animation.save('kerbol_system.gif', writer=writer)
