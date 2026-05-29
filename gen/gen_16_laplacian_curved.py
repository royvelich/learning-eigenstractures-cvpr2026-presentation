"""Intro primer — the Laplacian on a curved 2-D domain.

Same visual story as gen_14's 2D figure (flat (u,v) plane), but the domain
is now a smoothly curved sheet M in R^3. The function f : M -> R is rendered
as a second sheet floating ABOVE M along the surface normal — for each
point p in M we plot p + (lift + scale * f(p)) * n(p).

Three foci sit on M, each shown with its geodesic disk in the tangent
plane and a dotted connector up to the corresponding point on the f-sheet:

    red  — Δf > 0  (hill peak)
    blue — Δf < 0  (valley)
    grey — Δf ≈ 0  (far from both bumps)

Staged like gen_14 so the slide can reveal click-by-click:

    stage 0 — manifold M + f-sheet only
    stage 1 — + red focal point
    stage 2 — + red unit-ball (geodesic disk)
    stage 3 — + Δf > 0 label
    stage 4 — + blue focal point
    stage 5 — + blue unit-ball
    stage 6 — + Δf < 0 label
    stage 7 — + grey focal point
    stage 8 — + grey unit-ball
    stage 9 — + Δf ≈ 0 label

Output: lap_curved_2d_stage_{0..9}.png (all cropped to the same alpha bbox).
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
import math

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
DARK = "#0f172a"
GREY = "#cbd5e1"     # light slate (matches gen_14)
RED = "#ef4444"
BLUE = "#3b82f6"
GREEN = "#4ade80"    # light green for Δf ≈ 0

N_STAGES = 10

# ---------------------------------------------------------------- domain M
edge = 2.5
n = 90
g = np.linspace(-edge, edge, n)
Uu, Vv = np.meshgrid(g, g)

A_H, B_H, C_H = 0.40, 0.55, 0.55


def h(u, v):
    return A_H * np.sin(B_H * u) * np.cos(C_H * v)


def h_grad(u, v):
    hu = A_H * B_H * np.cos(B_H * u) * np.cos(C_H * v)
    hv = -A_H * C_H * np.sin(B_H * u) * np.sin(C_H * v)
    return hu, hv


def normal(u, v):
    hu, hv = h_grad(u, v)
    nx, ny, nz = -hu, -hv, np.ones_like(np.atleast_1d(u))
    L = np.sqrt(nx * nx + ny * ny + nz * nz)
    return nx / L, ny / L, nz / L


def tangent_frame(u, v):
    hu, hv = h_grad(u, v)
    t1 = np.array([1.0, 0.0, hu]);  t1 /= np.linalg.norm(t1)
    nrm = np.array(normal(u, v)).reshape(3)
    t2 = np.cross(nrm, t1);          t2 /= np.linalg.norm(t2)
    return t1, t2


Zh = h(Uu, Vv)


# ---------------------------------------------------------------- function f
def f(u, v):
    return 0.85 * np.exp(-((u + 1.0) ** 2 + (v + 0.5) ** 2) / 1.0) \
        - 0.80 * np.exp(-((u - 1.0) ** 2 + (v - 0.5) ** 2) / 1.0)


F_vals = f(Uu, Vv)
NX, NY, NZ = normal(Uu, Vv)
NORMAL_SCALE = 1.6   # visual exaggeration of f
NORMAL_LIFT = 1.6    # baseline lift so the f-sheet stays entirely above M
Xg = Uu + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NX
Yg = Vv + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NY
Zg = Zh + (NORMAL_LIFT + NORMAL_SCALE * F_vals) * NZ
m = float(np.abs(F_vals).max())

# ---------------------------------------------------------------- foci
r_disk = 0.275      # half-size unit ball, matching gen_14
theta_d = np.linspace(0, 2 * np.pi, 240)

foci_red = (-1.0, -0.5, RED)
foci_blue = (1.0, 0.5, BLUE)
GREY_UV = (-1.8, 1.5)   # roughly Δf ≈ 0 (far from both Gaussian centres)


def _focal_ground_curved(ax, uc, vc, col):
    """Coloured dot on M + dotted vertical-along-normal connector. Both
    pinned to a low sort z-position so the f-sheet always renders on top."""
    p0 = np.array([uc, vc, h(uc, vc)])
    nrm = np.array(normal(uc, vc)).reshape(3)
    pF = p0 + (NORMAL_LIFT + NORMAL_SCALE * f(uc, vc)) * nrm
    direction = pF - p0
    line_length = float(np.linalg.norm(direction))
    DASH_LEN = 0.08
    GAP_LEN = 0.08
    PERIOD = DASH_LEN + GAP_LEN
    dot_pairs = []
    i = 0
    while i * PERIOD < line_length:
        d_start = i * PERIOD
        d_end = min(d_start + DASH_LEN, line_length)
        t_start = d_start / line_length
        t_end = d_end / line_length
        dot_pairs.append((p0 + t_start * direction,
                          p0 + t_end * direction))
        i += 1
    line_col = Line3DCollection(dot_pairs, color=col, lw=2.0)
    ax.add_collection3d(line_col)
    ax.scatter([p0[0]], [p0[1]], [p0[2]], color=DARK, s=30,
               linewidths=0, zorder=6)


def _focal_top_curved(ax, uc, vc):
    """Black dot ON the f-sheet."""
    p0 = np.array([uc, vc, h(uc, vc)])
    nrm = np.array(normal(uc, vc)).reshape(3)
    pF = p0 + (NORMAL_LIFT + NORMAL_SCALE * f(uc, vc)) * nrm
    ax.scatter([pF[0]], [pF[1]], [pF[2]], color=DARK, s=45,
               linewidths=0, zorder=20)


def _unit_disk_curved(ax, uc, vc, col):
    """Geodesic-style disk in the tangent plane at (uc, vc, h(uc, vc))."""
    p0 = np.array([uc, vc, h(uc, vc)])
    nrm = np.array(normal(uc, vc)).reshape(3)
    t1, t2 = tangent_frame(uc, vc)
    lift = 0.012
    pts = (p0 + lift * nrm)[None, :] \
        + r_disk * (np.cos(theta_d)[:, None] * t1[None, :]
                    + np.sin(theta_d)[:, None] * t2[None, :])
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    outline = Line3DCollection(segs, color=col, lw=3.4, zorder=5)
    ax.add_collection3d(outline)
    poly = Poly3DCollection([list(map(tuple, pts))], color=col, alpha=0.45,
                            zorder=4)
    ax.add_collection3d(poly)


def _unit_patch_on_sheet_curved(ax, uc, vc, col, zorder, r=None):
    """The portion of the f-sheet above the unit ball as a separate
    polar-parametrised sub-surface. (u, v) inside the unit-ball circle is
    lifted via the normal to its position on the f-sheet — same formula as
    the main f-sheet, just over the disk parametrisation."""
    if r is None:
        r = r_disk
    n_r = 28
    n_t = 96
    r_g = np.linspace(0, r, n_r)
    t_g = np.linspace(0, 2 * np.pi, n_t)
    Rg, Tg = np.meshgrid(r_g, t_g)
    u_patch = uc + Rg * np.cos(Tg)
    v_patch = vc + Rg * np.sin(Tg)
    nx_, ny_, nz_ = normal(u_patch, v_patch)
    lift = NORMAL_LIFT + NORMAL_SCALE * f(u_patch, v_patch)
    x_patch = u_patch + lift * nx_
    y_patch = v_patch + lift * ny_
    z_patch = h(u_patch, v_patch) + lift * nz_
    ax.plot_surface(x_patch, y_patch, z_patch, color=col,
                    rcount=n_t, ccount=n_r, linewidth=0,
                    antialiased=True, shade=True, alpha=1.0,
                    zorder=zorder)


def _delta_label_curved(ax, uc, vc, text, col):
    """Label sitting above the f-sheet bump along the focal normal."""
    nrm = np.array(normal(uc, vc)).reshape(3)
    p0 = np.array([uc, vc, h(uc, vc)])
    pL = p0 + (NORMAL_LIFT + NORMAL_SCALE * abs(f(uc, vc)) + 0.55) * nrm
    ax.text(pL[0], pL[1], pL[2], text, color=col, fontsize=20,
            ha="center", va="bottom", fontweight="bold", zorder=25)


def build_stage(stage):
    fig = plt.figure(figsize=(7.2, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    # Render order is controlled by explicit zorder values — matplotlib's
    # 3D depth sort can't reliably layer multiple surfaces with patches.
    ax.computed_zorder = False
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Domain M — translucent light-grey sheet + light wireframe.
    ax.plot_surface(Uu, Vv, Zh, color=GREY, rcount=n, ccount=n,
                    linewidth=0, antialiased=True, shade=True, alpha=0.45,
                    zorder=1)
    ax.plot_wireframe(Uu, Vv, Zh, rcount=10, ccount=10,
                      color="#64748b", lw=0.4, alpha=0.5, zorder=2)

    # Domain boundary outline.
    bdry_u = np.concatenate([g, np.full(n, edge), g[::-1], np.full(n, -edge)])
    bdry_v = np.concatenate([np.full(n, -edge), g, np.full(n, edge), g[::-1]])
    bdry_z = h(bdry_u, bdry_v)
    ax.plot(bdry_u, bdry_v, bdry_z, color="#64748b", lw=1.2, zorder=3)

    # ----- Below the f-sheet (disks on M, dotted connectors, ground dots) -
    if stage >= 2:
        _unit_disk_curved(ax, foci_red[0], foci_red[1], foci_red[2])
    if stage >= 5:
        _unit_disk_curved(ax, foci_blue[0], foci_blue[1], foci_blue[2])
    if stage >= 8:
        _unit_disk_curved(ax, GREY_UV[0], GREY_UV[1], GREEN)
    if stage >= 1:
        _focal_ground_curved(ax, foci_red[0], foci_red[1], foci_red[2])
    if stage >= 4:
        _focal_ground_curved(ax, foci_blue[0], foci_blue[1], foci_blue[2])
    if stage >= 7:
        _focal_ground_curved(ax, GREY_UV[0], GREY_UV[1], GREEN)

    # ----- Main f-sheet (solid light grey) --------------------------------
    ax.plot_surface(Xg, Yg, Zg, color=GREY, rcount=n, ccount=n,
                    linewidth=0, antialiased=True, shade=True, alpha=0.88,
                    zorder=10)

    # ----- Coloured polar patches above each revealed unit ball -----------
    if stage >= 2:
        _unit_patch_on_sheet_curved(ax, foci_red[0], foci_red[1],
                                    foci_red[2], zorder=15)
    if stage >= 5:
        _unit_patch_on_sheet_curved(ax, foci_blue[0], foci_blue[1],
                                    foci_blue[2], zorder=15)
    if stage >= 8:
        _unit_patch_on_sheet_curved(ax, GREY_UV[0], GREY_UV[1],
                                    GREEN, zorder=15)

    # Lock the 3D extents so the projection is identical across stages.
    z_top_label = (Zh.max()
                   + NORMAL_LIFT + NORMAL_SCALE * m + 0.7)
    ax.set_xlim3d(-edge, edge)
    ax.set_ylim3d(-edge, edge)
    ax.set_zlim3d(Zh.min() - 0.1, z_top_label)
    ax.set_autoscale_on(False)

    # ----- Above-the-f-sheet artists --------------------------------------
    if stage >= 1:
        _focal_top_curved(ax, foci_red[0], foci_red[1])
    if stage >= 4:
        _focal_top_curved(ax, foci_blue[0], foci_blue[1])
    if stage >= 7:
        _focal_top_curved(ax, GREY_UV[0], GREY_UV[1])
    if stage >= 3:
        _delta_label_curved(ax, foci_red[0], foci_red[1],
                            r"$\Delta f > 0$", RED)
    if stage >= 6:
        _delta_label_curved(ax, foci_blue[0], foci_blue[1],
                            r"$\Delta f < 0$", BLUE)
    if stage >= 9:
        _delta_label_curved(ax, GREY_UV[0], GREY_UV[1],
                            r"$\Delta f \approx 0$", GREEN)

    ax.set_axis_off()
    ax.view_init(elev=28, azim=-30)
    ax.set_box_aspect((1, 1, 0.85))

    # "manifold M" label along the front edge of M (figure-coord text, like
    # the "uv plane" label in gen_14's old version).
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
    fig.text(label_pos[0], label_pos[1], r"manifold $M$", fontsize=13,
             color=DARK, ha="center", va="center", rotation=edge_angle)
    return fig


# Render all stages with FIXED figsize so pixel dimensions match across
# stages; then crop them all to the FULL stage's alpha bbox for a uniform
# tight crop (and no layout shift when the slide swaps the src).
for stage in range(N_STAGES):
    fig = build_stage(stage)
    plt.savefig(str(OUT_DIR / f"lap_curved_2d_stage_{stage}.png"),
                dpi=220, transparent=True)
    plt.close()

_full = Image.open(str(OUT_DIR / f"lap_curved_2d_stage_{N_STAGES - 1}.png"))
_bbox = _full.getchannel("A").getbbox()
if _bbox:
    for stage in range(N_STAGES):
        p = OUT_DIR / f"lap_curved_2d_stage_{stage}.png"
        Image.open(str(p)).crop(_bbox).save(str(p))
print(f"[ok] lap_curved_2d_stage_0..{N_STAGES - 1}.png")
