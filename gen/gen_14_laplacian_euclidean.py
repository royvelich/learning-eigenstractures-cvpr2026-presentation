"""Intro primer — the Laplacian on Euclidean domains, with two foci
(one where Δf > 0, one where Δf < 0) each shown with its unit-ball neighbourhood.

  lap_euclidean_1d.png  — f(x) on R, two foci on the hill / valley
  lap_euclidean_2d.png  — z = f(u,v) as a 3-D surface above the (u,v) plane,
                          with the two unit balls drawn on the plane
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import math

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
DARK = "#0f172a"
RED = "#b91c1c"
BLUE = "#1d4ed8"

# Convention: graph-Laplacian sign — Δf = f(x_0) − mean(f over neighbours).
#   hill peak  → focal is ABOVE its neighbours → Δf > 0 → red
#   valley    → focal is BELOW its neighbours → Δf < 0 → blue

# ============================== 1D ==============================
xs = np.linspace(-3.5, 3.5, 800)


def f1(x):
    return 1.0 * np.exp(-((x + 1.5) ** 2) / (2 * 0.62 ** 2)) \
        - 0.92 * np.exp(-((x - 1.5) ** 2) / (2 * 0.72 ** 2))


ys = f1(xs)
r1 = 0.55
foci_1d = [(-1.5, RED), (1.5, BLUE)]

fig, ax = plt.subplots(figsize=(5.8, 3.6))
ax.plot(xs, ys, color=INDIGO, lw=3.0, zorder=3)

for x0, col in foci_1d:
    y0 = f1(x0)
    mask = (xs >= x0 - r1) & (xs <= x0 + r1)
    ax.plot(xs[mask], ys[mask], color=col, lw=3.6, zorder=4)
    ax.plot([x0 - r1, x0 + r1], [0, 0], color=col, lw=5.0, zorder=5,
            solid_capstyle="round")
    for x_end in [x0 - r1, x0 + r1]:
        ax.plot([x_end, x_end], [-0.06, 0.06], color=col, lw=2.4, zorder=5)
    ax.plot([x0, x0], [0, y0], color=col, lw=1.2, ls=":", zorder=4)
    ax.scatter([x0], [y0], color=col, s=140, zorder=6,
               edgecolors="white", linewidths=2.0)
    ax.scatter([x0], [0], color=col, s=45, zorder=6)

# Δf-sign labels
ax.text(-1.5, f1(-1.5) + 0.22, r"$\Delta f > 0$", color=RED, fontsize=13,
        ha="center", fontweight="bold")
ax.text(1.5, f1(1.5) - 0.22, r"$\Delta f < 0$", color=BLUE, fontsize=13,
        ha="center", va="top", fontweight="bold")

# Axes
ax.annotate("", xy=(3.85, 0), xytext=(-3.6, 0),
            arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.5), zorder=2)
ax.text(3.93, 0, "$x$", fontsize=14, va="center")
ax.annotate("", xy=(-3.5, ys.max() + 0.20), xytext=(-3.5, ys.min() - 0.36),
            arrowprops=dict(arrowstyle="-|>", color=DARK, lw=1.5), zorder=2)
ax.text(-3.5, ys.max() + 0.36, "$f(x)$", fontsize=14, ha="center")

ax.set_xlim(-4.0, 4.3)
ax.set_ylim(ys.min() - 0.55, ys.max() + 0.62)
ax.axis("off")
plt.tight_layout()
plt.savefig(str(OUT_DIR / "lap_euclidean_1d.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.05)
plt.close()
print("[ok] lap_euclidean_1d.png")

# ============================== 2D (3-D plot) ==============================
n2 = 100
edge = 2.5
g = np.linspace(-edge, edge, n2)
Xg, Yg = np.meshgrid(g, g)


def f2(u, v):
    return 1.0 * np.exp(-((u + 1.0) ** 2 + (v + 0.5) ** 2) / 1.0) \
        - 0.95 * np.exp(-((u - 1.0) ** 2 + (v - 0.5) ** 2) / 1.0)


Z = f2(Xg, Yg)
m = float(np.abs(Z).max())
facecolors = cm.coolwarm(colors.Normalize(vmin=-m, vmax=m)(Z))

fig = plt.figure(figsize=(5.8, 5.0))
ax = fig.add_subplot(111, projection="3d")
ax.plot_surface(Xg, Yg, Z, facecolors=facecolors, rcount=n2, ccount=n2,
                linewidth=0, antialiased=True, shade=False, alpha=0.85)

z_base = Z.min() - 0.85

# (u,v) plane — translucent grey fill + light grid + outline, mirroring the
# curved-domain figure so the two slides feel like the same drawing system.
GREY_FILL = "#94a3b8"
quad_x = np.array([[-edge, edge], [-edge, edge]])
quad_y = np.array([[-edge, -edge], [edge, edge]])
quad_z = np.full_like(quad_x, z_base)
ax.plot_surface(quad_x, quad_y, quad_z, color=GREY_FILL, alpha=0.45,
                linewidth=0, antialiased=True, shade=False)

GRID_LINES = 10
Up = np.linspace(-edge, edge, GRID_LINES + 1)
for s in Up:
    ax.plot([-edge, edge], [s, s], [z_base, z_base],
            color="#64748b", lw=0.4, alpha=0.5, zorder=1)
    ax.plot([s, s], [-edge, edge], [z_base, z_base],
            color="#64748b", lw=0.4, alpha=0.5, zorder=1)
for s in [-edge, edge]:
    ax.plot([-edge, edge], [s, s], [z_base, z_base], color="#64748b", lw=1.2)
    ax.plot([s, s], [-edge, edge], [z_base, z_base], color="#64748b", lw=1.2)

r2 = 0.7
theta = np.linspace(0, 2 * np.pi, 240)
foci_2d = [(-1.0, -0.5, RED), (1.0, 0.5, BLUE)]

for uc, vc, col in foci_2d:
    cx = uc + r2 * np.cos(theta)
    cy = vc + r2 * np.sin(theta)
    cz = np.full_like(cx, z_base)
    ax.plot(cx, cy, cz, color=col, lw=3.0, zorder=3)
    disk = Poly3DCollection([list(zip(cx, cy, cz))], color=col, alpha=0.30)
    ax.add_collection3d(disk)
    zf = f2(uc, vc)
    ax.plot([uc, uc], [vc, vc], [z_base, zf], color=col, lw=1.6, ls=":")
    ax.scatter([uc], [vc], [zf], color=DARK, s=85,
               edgecolors="white", linewidths=2.0, zorder=6)
    ax.scatter([uc], [vc], [z_base], color=col, s=50, zorder=5)

# Δf-sign labels — both above the surface at the same z height for visibility
LABEL_Z = m + 0.7
ax.text(-1.0, -0.5, LABEL_Z, r"$\Delta f > 0$", color=RED, fontsize=14,
        ha="center", va="bottom", fontweight="bold")
ax.text(1.0, 0.5, LABEL_Z, r"$\Delta f < 0$", color=BLUE, fontsize=14,
        ha="center", va="bottom", fontweight="bold")

ax.set_axis_off()
ax.view_init(elev=30, azim=-60)
ax.set_box_aspect((1, 1, 0.7))
plt.tight_layout()
# Force the projection matrix to settle, then project the front-edge endpoints
# into figure coordinates so we can place a rotated 2D label along the edge.
fig.canvas.draw()


def _to_fig(x, y, z):
    xs, ys, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    px, py = ax.transData.transform((xs, ys))
    return fig.transFigure.inverted().transform((px, py))


fl = _to_fig(-edge, -edge, z_base)
fr = _to_fig(edge, -edge, z_base)
dl = fig.transFigure.transform(fl)
dr = fig.transFigure.transform(fr)
edge_angle = math.degrees(math.atan2(dr[1] - dl[1], dr[0] - dl[0]))
# Midpoint, dropped slightly outside the plane along the edge normal
mid = ((fl[0] + fr[0]) / 2, (fl[1] + fr[1]) / 2)
nx, ny = -math.sin(math.radians(edge_angle)), math.cos(math.radians(edge_angle))
label_pos = (mid[0] - 0.03 * nx, mid[1] - 0.03 * ny)
fig.text(label_pos[0], label_pos[1], "$uv$ plane", fontsize=13, color=DARK,
         ha="center", va="center", rotation=edge_angle)

plt.savefig(str(OUT_DIR / "lap_euclidean_2d.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.05)
plt.close()
print("[ok] lap_euclidean_2d.png")
