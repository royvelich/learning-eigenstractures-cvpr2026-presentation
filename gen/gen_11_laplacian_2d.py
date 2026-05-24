"""Intro primer — the Laplacian in 2D.

A height field z = f(x,y) over the plane (a bump + a dip), shown as a surface
coloured by its Laplacian Δf = f_xx + f_yy.
Rendered from several camera angles on a solid white background:
  lap_2d_<elev>_<azim>.png
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors

plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern — the LaTeX look

n = 220
g = np.linspace(-3.0, 3.0, n)
X, Y = np.meshgrid(g, g)


def gauss(cx, cy, s):
    return np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s ** 2))


Z = 1.0 * gauss(-1.1, -0.7, 0.8) - 0.9 * gauss(1.2, 0.8, 0.9)

dx = g[1] - g[0]
fxx = np.gradient(np.gradient(Z, dx, axis=1), dx, axis=1)
fyy = np.gradient(np.gradient(Z, dx, axis=0), dx, axis=0)
lap = fxx + fyy

m = np.abs(lap).max()
facecolors = cm.coolwarm(colors.Normalize(vmin=-m, vmax=m)(lap))

# (elevation, azimuth) views to try
VIEWS = [(40, -120), (40, -75), (40, -30), (40, 20), (55, -60), (22, -60)]

AXc = "#0f172a"
# axis triad anchored at a corner just outside the surface
O = np.array([-3.4, -3.4, 0.0])
arrows = [((6.9, 0, 0), "$x$"),
          ((0, 6.9, 0), "$y$"),
          ((0, 0, 1.7), "$f(x,y)$")]

for elev, azim in VIEWS:
    fig = plt.figure(figsize=(6.4, 5.2))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, facecolors=facecolors, rcount=n, ccount=n,
                    linewidth=0, antialiased=True, shade=False)
    for (u, v, w), lbl in arrows:
        ax.quiver(*O, u, v, w, color=AXc, lw=1.8, arrow_length_ratio=0.12)
        tip = O + np.array([u, v, w]) * 1.07
        ax.text(*tip, lbl, fontsize=14, color=AXc, ha="center", va="center")
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1, 1, 0.55))
    name = f"lap_2d_{elev:03d}_{azim:+04d}.png"
    plt.savefig(str(OUT_DIR / name), dpi=200, transparent=False,
                facecolor="white", bbox_inches="tight", pad_inches=0.05)
    plt.close()
    print(f"[ok] {name}")
