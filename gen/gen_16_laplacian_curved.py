"""Intro primer — the Laplacian on a curved 2-D domain.

Mirrors gen_14's 2D figure, but the domain is no longer the flat (u,v) plane:
it's a smoothly curved sheet M in R^3. The function f : M -> R is rendered as
a second sheet floating ABOVE M along the surface normal — i.e. for each
point p in M we plot p + f(p) * n(p).

Two foci sit on M, each with a small geodesic disk in its tangent plane,
and a dotted line up to the corresponding point on the f-sheet.

  lap_curved_2d.png
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
DARK = "#0f172a"
GREY = "#94a3b8"
RED = "#b91c1c"
BLUE = "#1d4ed8"

# ---------------------------------------------------------------- domain M
# A gentle wavy patch — clearly non-flat, but doesn't dominate the figure.
edge = 2.5
n = 90
g = np.linspace(-edge, edge, n)
Uu, Vv = np.meshgrid(g, g)

A_H, B_H, C_H = 0.40, 0.55, 0.55


def h(u, v):
    """Height of the domain sheet above the (u,v) reference plane."""
    return A_H * np.sin(B_H * u) * np.cos(C_H * v)


def h_grad(u, v):
    hu = A_H * B_H * np.cos(B_H * u) * np.cos(C_H * v)
    hv = -A_H * C_H * np.sin(B_H * u) * np.sin(C_H * v)
    return hu, hv


def normal(u, v):
    """Unit normal to z = h(u,v) at (u,v)."""
    hu, hv = h_grad(u, v)
    nx, ny, nz = -hu, -hv, np.ones_like(np.atleast_1d(u))
    L = np.sqrt(nx * nx + ny * ny + nz * nz)
    return nx / L, ny / L, nz / L


def tangent_frame(u, v):
    """Orthonormal (e1, e2) spanning the tangent plane at (u, v, h(u,v))."""
    hu, hv = h_grad(u, v)
    t1 = np.array([1.0, 0.0, hu]);  t1 /= np.linalg.norm(t1)
    nrm = np.array(normal(u, v)).reshape(3)
    t2 = np.cross(nrm, t1);          t2 /= np.linalg.norm(t2)
    return t1, t2


# domain sheet
Zh = h(Uu, Vv)

# ---------------------------------------------------------------- function f
def f(u, v):
    return 0.85 * np.exp(-((u + 1.0) ** 2 + (v + 0.5) ** 2) / 1.0) \
        - 0.80 * np.exp(-((u - 1.0) ** 2 + (v - 0.5) ** 2) / 1.0)


# graph of f over M: p + f(p) * n(p)
F_vals = f(Uu, Vv)
NX, NY, NZ = normal(Uu, Vv)
NORMAL_SCALE = 1.6  # visual exaggeration of f for height-above-M
NORMAL_LIFT = 1.6   # baseline lift so the f-sheet stays entirely above M
Xg = Uu + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NX
Yg = Vv + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NY
Zg = Zh + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NZ

m = float(np.abs(F_vals).max())
facecolors = cm.coolwarm(colors.Normalize(vmin=-m, vmax=m)(F_vals))

# ---------------------------------------------------------------- plot
fig = plt.figure(figsize=(7.2, 5.6))
ax = fig.add_subplot(111, projection="3d")
# Let the 3D axes fill the figure — matplotlib's default 3D margins are huge
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

# domain M — translucent grey sheet so it reads clearly as the base manifold
ax.plot_surface(Uu, Vv, Zh, color=GREY, rcount=n, ccount=n,
                linewidth=0, antialiased=True, shade=True, alpha=0.45)
ax.plot_wireframe(Uu, Vv, Zh, rcount=10, ccount=10,
                  color="#64748b", lw=0.4, alpha=0.5)

# the f-sheet
ax.plot_surface(Xg, Yg, Zg, facecolors=facecolors, rcount=n, ccount=n,
                linewidth=0, antialiased=True, shade=False, alpha=0.88)

# outline of M's boundary so the domain is unambiguous
bdry_u = np.concatenate([g, np.full(n, edge), g[::-1], np.full(n, -edge)])
bdry_v = np.concatenate([np.full(n, -edge), g, np.full(n, edge), g[::-1]])
bdry_z = h(bdry_u, bdry_v)
ax.plot(bdry_u, bdry_v, bdry_z, color="#64748b", lw=1.2)

# ---------------------------------------------------------------- foci
foci = [(-1.0, -0.5, RED), (1.0, 0.5, BLUE)]
r_disk = 0.55
theta = np.linspace(0, 2 * np.pi, 240)

for uc, vc, col in foci:
    p0 = np.array([uc, vc, h(uc, vc)])
    t1, t2 = tangent_frame(uc, vc)

    # geodesic disk in the tangent plane at p0 (drawn slightly above M to
    # avoid z-fighting with the wireframe)
    nrm = np.array(normal(uc, vc)).reshape(3)
    lift = 0.012
    disk_pts = (p0 + lift * nrm)[None, :] \
        + r_disk * (np.cos(theta)[:, None] * t1[None, :]
                    + np.sin(theta)[:, None] * t2[None, :])
    ax.plot(disk_pts[:, 0], disk_pts[:, 1], disk_pts[:, 2],
            color=col, lw=3.4, zorder=10)
    poly = Poly3DCollection([list(map(tuple, disk_pts))], color=col, alpha=0.45)
    poly.set_zorder(9)
    ax.add_collection3d(poly)

    # point on f-sheet directly above p0 along the surface normal
    pF = p0 + (NORMAL_LIFT + NORMAL_SCALE * f(uc, vc)) * nrm
    # dotted connector — draw a few segments with explicit zorder so it shows
    ts = np.linspace(0, 1, 60)
    seg = np.outer(1 - ts, p0) + np.outer(ts, pF)
    ax.plot(seg[:, 0], seg[:, 1], seg[:, 2],
            color=col, lw=2.0, ls=(0, (1, 1.5)), zorder=11)
    ax.scatter([pF[0]], [pF[1]], [pF[2]], color=DARK, s=110,
               edgecolors="white", linewidths=2.4, zorder=12)
    ax.scatter([p0[0]], [p0[1]], [p0[2]], color=col, s=70,
               edgecolors="white", linewidths=1.6, zorder=12)

# Δf-sign labels — always above the f-sheet bump along the focal normal
for uc, vc, col, sign in [(-1.0, -0.5, RED, r"$\Delta f > 0$"),
                          (1.0, 0.5, BLUE, r"$\Delta f < 0$")]:
    nrm = np.array(normal(uc, vc)).reshape(3)
    p0 = np.array([uc, vc, h(uc, vc)])
    # peak of the red hill / floor of the blue valley on the f-sheet
    pF = p0 + (NORMAL_LIFT + NORMAL_SCALE * f(uc, vc)) * nrm
    # always lift the label well above the entire f-sheet so it's never occluded
    pL = p0 + (NORMAL_LIFT + NORMAL_SCALE * abs(f(uc, vc)) + 0.55) * nrm
    ax.text(pL[0], pL[1], pL[2], sign, color=col, fontsize=14,
            ha="center", va="bottom", fontweight="bold")

ax.set_axis_off()
ax.view_init(elev=28, azim=-30)
ax.set_box_aspect((1, 1, 0.85))

# Domain label (drawn in figure coords, like gen_14's "uv plane" label)
from mpl_toolkits.mplot3d import proj3d

fig.canvas.draw()


def _to_fig(x, y, z):
    xs, ys, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
    px, py = ax.transData.transform((xs, ys))
    return fig.transFigure.inverted().transform((px, py))


fl = _to_fig(-edge, -edge, h(-edge, -edge))
fr = _to_fig(edge, -edge, h(edge, -edge))
dl = fig.transFigure.transform(fl)
dr = fig.transFigure.transform(fr)
edge_angle = math.degrees(math.atan2(dr[1] - dl[1], dr[0] - dl[0]))
mid = ((fl[0] + fr[0]) / 2, (fl[1] + fr[1]) / 2)
nx_, ny_ = -math.sin(math.radians(edge_angle)), math.cos(math.radians(edge_angle))
label_pos = (mid[0] - 0.03 * nx_, mid[1] - 0.03 * ny_)
fig.text(label_pos[0], label_pos[1], r"manifold $M$", fontsize=13, color=DARK,
         ha="center", va="center", rotation=edge_angle)

out_path = OUT_DIR / "lap_curved_2d.png"
plt.savefig(str(out_path), dpi=220, transparent=True,
            bbox_inches="tight", pad_inches=0.0)
plt.close()

# Post-crop: matplotlib 3D still leaves a fully-transparent border around the
# content. Crop to the alpha-channel bounding box for a truly tight image.
from PIL import Image
im = Image.open(out_path)
bbox = im.getchannel("A").getbbox()
if bbox is not None:
    im.crop(bbox).save(out_path)
print(f"[ok] lap_curved_2d.png  ({im.crop(bbox).size if bbox else im.size})")
