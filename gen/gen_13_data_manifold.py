"""Intro primer — a small 'data manifold' point cloud for the Laplacian slide.

Four figures with identical point positions:
  data_manifold_grey.png       — all points grey, no values yet
  data_manifold_coloured.png   — same points, coloured by a smooth scalar f
  data_manifold_focal.png      — one point emphasised at its own colour (f value)
  data_manifold_laplacian.png  — same point recoloured to Δf = f(focal) − mean(neighbours)
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


# Parameters of the field — two Gaussians of opposite sign, gently tapered
# at the strip rims so the discrete graph-Laplacian doesn't pick up a
# one-sided boundary artifact there.
A1, XC1, YC1 = 1.00, -1.1, -0.45
A2, XC2, YC2 = 0.95,  1.1,  0.45
SIGMA2       = 0.75            # σ² for both Gaussians
ENV_X0       = 2.15            # envelope inflection in |x|
ENV_S        = 0.20            # envelope ramp scale


def f(x, y):
    """Two opposite-sign Gaussians tapered to ≈ 0 at the strip's rims."""
    g1 = A1 * np.exp(-((x - XC1) ** 2 + (y - YC1) ** 2) / SIGMA2)
    g2 = A2 * np.exp(-((x - XC2) ** 2 + (y - YC2) ** 2) / SIGMA2)
    base = g1 - g2
    env  = 0.5 * (1.0 + np.tanh((ENV_X0 - np.abs(x)) / ENV_S))
    return base * env


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

# --- Discrete graph Laplacian using the positive (PSD) sign convention:
# Δf[i] ≈ f(i) − mean(f over neighbours within radius R), so Δf > 0 at
# peaks of f and < 0 at valleys, matching the continuous Δ = −div(grad f)
# and the "deviation from local average" framing used on slides 2–5.
R_NBHD = 0.60
tree = cKDTree(np.c_[X, Y])
nbrs_list = [tree.query_ball_point([X[i], Y[i]], r=R_NBHD) for i in range(n)]

delta_f = np.zeros(n)
for i in range(n):
    js = [j for j in nbrs_list[i] if j != i]
    if js:
        delta_f[i] = vals[i] - np.mean(vals[js])

# Focal point = a clear local maximum of f (the visible hill peak in the cloud).
interior = (np.abs(X) < 1.7) & (np.abs(Y) < 0.8)
best = np.where(interior, vals, -np.inf).argmax()

xf, yf = X[best], Y[best]
print(f"[focal] idx={best}  pos=({xf:.2f},{yf:.2f})  f={vals[best]:.3f}  dF={delta_f[best]:.3f}")

# Shared Δf normalization — used for BOTH the focal-recoloured image and the
# full Δf cloud, so the same point shows the same colour in both views.
mdf = float(np.abs(delta_f).max())

# Δf colour-scale half-range, shared by the focal image and the full Δf cloud
# so the same point reads the same in both. Chosen as a fraction of the SIGNAL
# scale m: tight enough to give visible contrast (the bulk of |Δf| ≈ 0.06–0.2),
# but wide enough that the peak (Δf ≈ 0.21) stays light-moderate red rather than
# saturating — conveying "a small, but real, local deviation". Tune DF_FRAC.
DF_FRAC = 0.40
df_vmax = DF_FRAC * m


def render_focal(focal_color_value, focal_vmin, focal_vmax, out_name):
    """Render the f-coloured cloud with one focal point recoloured by a
    different quantity (e.g. its Δf value) on its own scale."""
    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    # background: every point coloured by f on the [-m, m] scale
    ax.scatter(X, Y, c=vals, cmap="coolwarm", s=26, edgecolors="white",
               linewidths=0.6, vmin=-m, vmax=m, zorder=2)
    circ = plt.Circle((xf, yf), R_NBHD, color="#0f172a", lw=1.8, ls="--",
                      fill=False, zorder=4)
    ax.add_patch(circ)
    # focal: its own value on its own scale (so the same Δf reading matches
    # whatever scale the full-cloud Δf image uses).
    ax.scatter([xf], [yf], c=[focal_color_value], cmap="coolwarm",
               s=220, edgecolors="#0f172a", linewidths=2.6,
               vmin=focal_vmin, vmax=focal_vmax, zorder=5)
    setup_ax(ax)
    plt.savefig(str(OUT_DIR / out_name), dpi=200, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close()
    print(f"[ok] {out_name}")


# Focal coloured by its f-value (matches the background scale).
render_focal(vals[best], -m, m, "data_manifold_focal.png")
# Focal recoloured by its Δf value on the SIGNAL's [-m, m] scale (the SAME
# scale used for the f-colouring) — NOT the Δf cloud's own [-mdf, mdf] range.
# This way a small positive Laplacian reads as a *light* red, conveying that
# the peak sits only slightly above its neighbourhood average (rather than
# saturating to deep red just because it's the largest Laplacian in the cloud).
render_focal(delta_f[best], -df_vmax, df_vmax, "data_manifold_laplacian.png")

# Full Δf cloud — every point recoloured by Δf on the SIGNAL's [-m, m] scale
# (matching the focal image and the f-colouring), NOT the Δf cloud's own
# [-mdf, mdf] range. Laplacian values are small vs. the signal, so the whole
# cloud reads pale — light red at peaks, light blue at valleys — conveying
# "Δf measures only a small local deviation". Positive (PSD) sign convention.
fig, ax = plt.subplots(figsize=(5.6, 3.4))
ax.scatter(X, Y, c=delta_f, cmap="coolwarm", s=26, edgecolors="white",
           linewidths=0.6, vmin=-df_vmax, vmax=df_vmax, zorder=2)
setup_ax(ax)
plt.savefig(str(OUT_DIR / "data_manifold_laplacian_full.png"), dpi=200,
            transparent=True, bbox_inches="tight", pad_inches=0.02)
plt.close()
print("[ok] data_manifold_laplacian_full.png")
