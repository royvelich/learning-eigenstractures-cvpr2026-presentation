"""Intro primer — a small 'data manifold' point cloud for the Laplacian slide.

Four figures with identical point positions:
  data_manifold_grey.png       — all points grey, no values yet
  data_manifold_coloured.png   — same points, coloured by a smooth scalar f
  data_manifold_focal.png      — one point emphasised at its own colour (f value)
  data_manifold_laplacian.png  — same point recoloured to Δf = focal − mean(neighbours)
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

plt.rcParams["mathtext.fontset"] = "cm"

rng = np.random.default_rng(7)
n = 650

# Sample from a wavy strip — reads as "data on a low-d manifold in the plane".
xs = rng.uniform(-2.5, 2.5, n)
yc = 0.55 * np.sin(1.15 * xs) - 0.05 * xs            # gently curved centerline
thick = 0.55 * (1.0 - 0.18 * (xs / 2.5) ** 2)        # tapered thickness
yoff = rng.uniform(-1, 1, n) * thick
X = xs
Y = yc + yoff


def f(x, y):
    # Slightly sharper Gaussians so the gradient (and Δf) near the boundary is non-trivial.
    return 1.0 * np.exp(-((x + 1.1) ** 2 + (y + 0.45) ** 2) / 0.75) \
        - 0.95 * np.exp(-((x - 1.1) ** 2 + (y - 0.45) ** 2) / 0.75)


vals = f(X, Y)
m = float(np.abs(vals).max())


def setup_ax(ax):
    ax.set_aspect("equal")
    ax.axis("off")
    pad = 0.18
    ax.set_xlim(X.min() - pad, X.max() + pad)
    ax.set_ylim(Y.min() - pad, Y.max() + pad)


GREY = "#94a3b8"

fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.scatter(X, Y, c=GREY, s=26, edgecolors="white", linewidths=0.6, zorder=2)
setup_ax(ax)
plt.savefig(str(OUT_DIR / "data_manifold_grey.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.02)
plt.close()
print("[ok] data_manifold_grey.png")

fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.scatter(X, Y, c=vals, cmap="coolwarm", s=26, edgecolors="white",
           linewidths=0.6, vmin=-m, vmax=m, zorder=2)
setup_ax(ax)
plt.savefig(str(OUT_DIR / "data_manifold_coloured.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.02)
plt.close()
print("[ok] data_manifold_coloured.png")

# --- Choose focal: a clear local maximum of f (hill peak in the cloud).
# Putting the focal at a local extremum makes the visual computation transparent:
# eye sees the focal as the deepest red in its disk, neighbours slightly cooler,
# so Δf = focal − avg(neighbours) is naturally a moderate red — i.e. the
# recoloured colour is exactly what the eye expects.
R_NBHD = 0.60
tree = cKDTree(np.c_[X, Y])
nbrs_list = [tree.query_ball_point([X[i], Y[i]], r=R_NBHD) for i in range(n)]

delta_f = np.zeros(n)
for i in range(n):
    js = [j for j in nbrs_list[i] if j != i]
    if js:
        delta_f[i] = vals[i] - np.mean(vals[js])     # focal − mean(neighbours)

interior = (np.abs(X) < 1.7) & (np.abs(Y) < 0.8)
best = np.where(interior, delta_f, -np.inf).argmax()

xf, yf = X[best], Y[best]
print(f"[focal] idx={best}  pos=({xf:.2f},{yf:.2f})  f={vals[best]:.3f}  dF={delta_f[best]:.3f}")


def render_focal(focal_color_value, out_name):
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.scatter(X, Y, c=vals, cmap="coolwarm", s=26, edgecolors="white",
               linewidths=0.6, vmin=-m, vmax=m, zorder=2)
    circ = plt.Circle((xf, yf), R_NBHD, color="#0f172a", lw=1.8, ls="--",
                      fill=False, zorder=4)
    ax.add_patch(circ)
    ax.scatter([xf], [yf], c=[focal_color_value], cmap="coolwarm",
               s=220, edgecolors="#0f172a", linewidths=2.6,
               vmin=-m, vmax=m, zorder=5)
    setup_ax(ax)
    plt.savefig(str(OUT_DIR / out_name), dpi=200, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close()
    print(f"[ok] {out_name}")


render_focal(vals[best], "data_manifold_focal.png")
# Recolour focal to its Δf value on the same [-m, m] coolwarm scale (no boost):
# at a local maximum Δf is already a clean moderate red, naturally readable.
render_focal(delta_f[best], "data_manifold_laplacian.png")

# Δf-coloured cloud — every point recoloured by its discrete Δf value, used
# for the "Δ eats f and returns Δf" operator demo. Self-scaled colour range
# so the Laplacian output reads clearly (|Δf| < |f| for smooth functions).
mdf = float(np.abs(delta_f).max())
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.scatter(X, Y, c=delta_f, cmap="coolwarm", s=26, edgecolors="white",
           linewidths=0.6, vmin=-mdf, vmax=mdf, zorder=2)
setup_ax(ax)
plt.savefig(str(OUT_DIR / "data_manifold_laplacian_full.png"), dpi=200,
            transparent=True, bbox_inches="tight", pad_inches=0.02)
plt.close()
print("[ok] data_manifold_laplacian_full.png")
