"""Intro primer — the Laplacian on Euclidean domains, with two foci
(one where Δf > 0, one where Δf < 0) each shown with its unit-ball neighbourhood.

Produces progressive stages 0..6 of the same scene so the slide can reveal
the construction click-by-click:

    stage 0 — just the underlying function / surface
    stage 1 — + red focal point
    stage 2 — + red unit-ball neighbourhood
    stage 3 — + Δf > 0 label
    stage 4 — + blue focal point
    stage 5 — + blue unit-ball neighbourhood
    stage 6 — + Δf < 0 label
    stage 7 — + green focal point (Δf ≈ 0, at the inflection)
    stage 8 — + green unit-ball neighbourhood
    stage 9 — + Δf ≈ 0 label

Output:
    lap_euclidean_1d_stage_{0..6}.png
    lap_euclidean_2d_stage_{0..6}.png

All stages within a row share the SAME pixel dimensions (cropped to the
final stage's alpha bbox) so the slide can swap them without layout shift.
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
from PIL import Image
import math

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
DARK = "#0f172a"
GREY = "#cbd5e1"  # light slate
RED = "#ef4444"
BLUE = "#3b82f6"
GREEN = "#4ade80"  # green (Tailwind green-400)

# Convention: graph-Laplacian sign — Δf = f(x_0) − mean(f over neighbours).
#   hill peak  → focal is ABOVE its neighbours → Δf > 0 → red
#   valley    → focal is BELOW its neighbours → Δf < 0 → blue

N_STAGES = 10
GREEN_X_1D = 0.3
GREEN_UV_2D = (1.5, 1.5)

# ============================== 1D ==============================
xs = np.linspace(-3.5, 3.5, 800)


def f1(x):
    return 1.0 * np.exp(-((x + 1.5) ** 2) / (2 * 0.62 ** 2)) \
        - 0.92 * np.exp(-((x - 1.5) ** 2) / (2 * 0.72 ** 2))


ys = f1(xs)
r1 = 0.275  # half-size unit ball (was 0.55)
foci_1d_red = (-1.5, RED)
foci_1d_blue = (1.5, BLUE)


def _focal_dot_1d(ax, x0, col):
    y0 = f1(x0)
    ax.plot([x0, x0], [0, y0], color=col, lw=1.2, ls=":", zorder=4)
    # Dot ON the graph: black, no stroke, smaller (matches the 2D version).
    ax.scatter([x0], [y0], color=DARK, s=45, linewidths=0, zorder=6)
    # Dot on the x-axis: black (matches the 2D ground dot).
    ax.scatter([x0], [0], color=DARK, s=30, linewidths=0, zorder=6)


def _unit_ball_1d(ax, x0, col, r=None):
    if r is None:
        r = r1
    mask = (xs >= x0 - r) & (xs <= x0 + r)
    ax.plot(xs[mask], ys[mask], color=col, lw=1.8, zorder=4)
    ax.plot([x0 - r, x0 + r], [0, 0], color=col, lw=2.5, zorder=5,
            solid_capstyle="round")
    for x_end in [x0 - r, x0 + r]:
        ax.plot([x_end, x_end], [-0.06, 0.06], color=col, lw=1.2, zorder=5)


def build_1d_stage(stage):
    fig, ax = plt.subplots(figsize=(5.8, 3.6))
    ax.plot(xs, ys, color="#94a3b8", lw=3.0, zorder=3)

    if stage >= 1:
        _focal_dot_1d(ax, foci_1d_red[0], foci_1d_red[1])
    if stage >= 2:
        _unit_ball_1d(ax, foci_1d_red[0], foci_1d_red[1])
    if stage >= 3:
        ax.text(foci_1d_red[0], f1(foci_1d_red[0]) + 0.22,
                r"$\Delta f > 0$", color=RED, fontsize=20,
                ha="center", fontweight="bold")
    if stage >= 4:
        _focal_dot_1d(ax, foci_1d_blue[0], foci_1d_blue[1])
    if stage >= 5:
        _unit_ball_1d(ax, foci_1d_blue[0], foci_1d_blue[1])
    if stage >= 6:
        ax.text(foci_1d_blue[0], f1(foci_1d_blue[0]) - 0.22,
                r"$\Delta f < 0$", color=BLUE, fontsize=20,
                ha="center", va="top", fontweight="bold")
    if stage >= 7:
        _focal_dot_1d(ax, GREEN_X_1D, GREEN)
    if stage >= 8:
        _unit_ball_1d(ax, GREEN_X_1D, GREEN)
    if stage >= 9:
        ax.text(GREEN_X_1D, f1(GREEN_X_1D) + 0.4,
                r"$\Delta f \approx 0$", color=GREEN, fontsize=20,
                ha="center", fontweight="bold")

    ax.annotate("", xy=(3.85, 0), xytext=(-3.6, 0),
                arrowprops=dict(arrowstyle="-|>", color=DARK,
                                lw=2.8, mutation_scale=28),
                zorder=2)
    ax.text(4.05, 0, "$x$", fontsize=24, va="center")
    ax.annotate("", xy=(-3.5, ys.max() + 0.20), xytext=(-3.5, ys.min() - 0.36),
                arrowprops=dict(arrowstyle="-|>", color=DARK,
                                lw=2.8, mutation_scale=28),
                zorder=2)
    ax.text(-3.5, ys.max() + 0.42, "$f(x)$", fontsize=24, ha="center")

    ax.set_xlim(-4.0, 4.3)
    ax.set_ylim(ys.min() - 0.55, ys.max() + 0.62)
    ax.axis("off")
    plt.tight_layout()
    return fig


# Render all 1D stages with FIXED figsize (no bbox_inches="tight") so all
# stages share identical pixel dimensions, then crop them all to the FULL
# stage's alpha bbox for a uniform tight crop.
for stage in range(N_STAGES):
    fig = build_1d_stage(stage)
    plt.savefig(str(OUT_DIR / f"lap_euclidean_1d_stage_{stage}.png"),
                dpi=200, transparent=True)
    plt.close()

_full_1d = Image.open(str(OUT_DIR / f"lap_euclidean_1d_stage_{N_STAGES - 1}.png"))
_bbox_1d = _full_1d.getbbox()
if _bbox_1d:
    for stage in range(N_STAGES):
        p = OUT_DIR / f"lap_euclidean_1d_stage_{stage}.png"
        Image.open(str(p)).crop(_bbox_1d).save(str(p))
print(f"[ok] lap_euclidean_1d_stage_0..{N_STAGES - 1}.png")


# ============================== 2D (matplotlib, mirrors gen_16's style) ==============================
# Same visual treatment as the curved-domain slide (lap_curved_2d.png):
# translucent grey domain sheet + wireframe + boundary outline, function f
# rendered as a SECOND sheet floating above the domain along the normal,
# coloured by f, with foci sitting on the domain and connecting up to the
# f-sheet. Difference here: the "manifold" is flat — z = 0 everywhere and
# the normal is the constant (0, 0, 1).
edge = 2.5
n2 = 90
g2 = np.linspace(-edge, edge, n2)
Uu, Vv = np.meshgrid(g2, g2)

# Flat domain: h(u, v) ≡ 0. Normal = (0, 0, 1). Tangent frame = standard.
Zh = np.zeros_like(Uu)


def f2(u, v):
    return 0.85 * np.exp(-((u + 1.0) ** 2 + (v + 0.5) ** 2) / 1.0) \
        - 0.80 * np.exp(-((u - 1.0) ** 2 + (v - 0.5) ** 2) / 1.0)


F_vals = f2(Uu, Vv)
NORMAL_SCALE = 1.6  # visual exaggeration of f
NORMAL_LIFT = 1.6   # baseline lift so the f-sheet stays above the plane

# f-sheet vertices: (u, v) + (NORMAL_LIFT + NORMAL_SCALE * f) * n_hat
Xg = Uu
Yg = Vv
Zg = Zh + NORMAL_LIFT + NORMAL_SCALE * F_vals

m = float(np.abs(F_vals).max())

r2 = 0.275  # half-size unit ball (was 0.55)
theta = np.linspace(0, 2 * np.pi, 240)
foci_2d_red = (-1.0, -0.5, RED)
foci_2d_blue = (1.0, 0.5, BLUE)


from mpl_toolkits.mplot3d.art3d import Line3DCollection  # noqa: E402


def _focal_ground_2d(ax, uc, vc, col):
    """Coloured dot on the (u,v) plane + dotted vertical connector. Both
    pinned to a low sort z-position so the f-sheet always renders on top.
    Dash + gap lengths are FIXED in world units, independent of line length."""
    p0 = np.array([uc, vc, 0.0])
    pF = np.array([uc, vc, NORMAL_LIFT + NORMAL_SCALE * f2(uc, vc)])
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
    line_col.set_sort_zpos(-100.0)
    ax.add_collection3d(line_col)
    ax.scatter([p0[0]], [p0[1]], [p0[2]], color=DARK, s=30,
               linewidths=0, zorder=1)


def _focal_top_2d(ax, uc, vc):
    """Dark dot ON the f-sheet, drawn AFTER the f-sheet so it sits on top."""
    pF = np.array([uc, vc, NORMAL_LIFT + NORMAL_SCALE * f2(uc, vc)])
    ax.scatter([pF[0]], [pF[1]], [pF[2]], color=DARK, s=45,
               linewidths=0, zorder=20)


def _unit_disk_2d(ax, uc, vc, col, r=None):
    """Flat translucent disk + thin outline ring on the (u,v) plane —
    both pinned with set_sort_zpos so they always sort BEHIND the f-sheet."""
    if r is None:
        r = r2
    lift = 0.012
    px = uc + r * np.cos(theta)
    py = vc + r * np.sin(theta)
    pz = np.full_like(px, lift)
    # Outline ring as a Line3DCollection so we can sort_zpos it.
    pts = np.column_stack([px, py, pz])
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    outline = Line3DCollection(segs, color=col, lw=3.4)
    outline.set_sort_zpos(-100.0)
    ax.add_collection3d(outline)
    # Filled disk.
    poly = Poly3DCollection([list(zip(px, py, pz))], color=col, alpha=0.45)
    poly.set_sort_zpos(-100.0)
    ax.add_collection3d(poly)


def _delta_label_2d(ax, uc, vc, text, col, side="above", offset=0.55,
                    du=0.0, dv=0.0, dz=0.0, ha="center", va=None):
    """Δf-sign label, placed above or below the f-sheet bump along ẑ.
    `offset` = vertical gap (world units) bump↔label.  `du/dv/dz` = extra
    nudge in world units (camera projects them to a small image-pixel shift)."""
    z_bump = NORMAL_LIFT + NORMAL_SCALE * f2(uc, vc)
    if side == "below":
        # Sit just under the f-sheet dip — next to the (u,v)-plane unit ball.
        pL_z = z_bump - offset + dz
        default_va = "top"
    elif side == "at":
        # Sit at the bump level (use du/dv to nudge horizontally).
        pL_z = z_bump + dz
        default_va = "center"
    else:
        # Sit above the f-sheet peak.
        pL_z = NORMAL_LIFT + NORMAL_SCALE * abs(f2(uc, vc)) + offset + dz
        default_va = "bottom"
    if va is None:
        va = default_va
    ax.text(uc + du, vc + dv, pL_z, text, color=col, fontsize=20,
            ha=ha, va=va, fontweight="bold")


def _unit_patch_on_sheet_2d(ax, uc, vc, col, zorder, r=None):
    """The portion of the f-sheet above the unit ball, as a separate
    polar-parametrised sub-surface (smooth circular boundary). Drawn with
    explicit zorder — requires ax.computed_zorder = False on the axes."""
    if r is None:
        r = r2
    n_r = 30
    n_t = 96
    r_g = np.linspace(0, r, n_r)
    t_g = np.linspace(0, 2 * np.pi, n_t)
    Rg, Tg = np.meshgrid(r_g, t_g)
    u_patch = uc + Rg * np.cos(Tg)
    v_patch = vc + Rg * np.sin(Tg)
    z_patch = NORMAL_LIFT + NORMAL_SCALE * f2(u_patch, v_patch)
    ax.plot_surface(u_patch, v_patch, z_patch, color=col,
                    rcount=n_t, ccount=n_r, linewidth=0,
                    antialiased=True, shade=True, alpha=1.0,
                    zorder=zorder)


def build_2d_stage(stage):
    fig = plt.figure(figsize=(7.2, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    # Disable matplotlib's 3D depth-sort; we control rendering order with
    # explicit zorder values. The fixed iso-ish view keeps the order valid
    # across all stages.
    ax.computed_zorder = False
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Flat domain — translucent grey sheet + wireframe.
    ax.plot_surface(Uu, Vv, Zh, color=GREY, rcount=n2, ccount=n2,
                    linewidth=0, antialiased=True, shade=True, alpha=0.45,
                    zorder=1)
    ax.plot_wireframe(Uu, Vv, Zh, rcount=10, ccount=10,
                      color="#64748b", lw=0.4, alpha=0.5, zorder=2)

    # Domain boundary outline.
    bdry_u = np.concatenate([g2, np.full(n2, edge), g2[::-1], np.full(n2, -edge)])
    bdry_v = np.concatenate([np.full(n2, -edge), g2, np.full(n2, edge), g2[::-1]])
    bdry_z = np.zeros_like(bdry_u)
    ax.plot(bdry_u, bdry_v, bdry_z, color="#64748b", lw=1.2, zorder=3)

    # ----- Below the f-sheet (disks on plane, dotted connectors, ground dots).
    if stage >= 2:
        _unit_disk_2d(ax, foci_2d_red[0], foci_2d_red[1], foci_2d_red[2])
    if stage >= 5:
        _unit_disk_2d(ax, foci_2d_blue[0], foci_2d_blue[1], foci_2d_blue[2])
    if stage >= 8:
        _unit_disk_2d(ax, GREEN_UV_2D[0], GREEN_UV_2D[1], GREEN)
    if stage >= 1:
        _focal_ground_2d(ax, foci_2d_red[0], foci_2d_red[1], foci_2d_red[2])
    if stage >= 4:
        _focal_ground_2d(ax, foci_2d_blue[0], foci_2d_blue[1], foci_2d_blue[2])
    if stage >= 7:
        _focal_ground_2d(ax, GREEN_UV_2D[0], GREEN_UV_2D[1], GREEN)

    # ----- Main f-sheet (grey) ---------------------------------------------
    ax.plot_surface(Xg, Yg, Zg, color=GREY, rcount=n2, ccount=n2,
                    linewidth=0, antialiased=True, shade=True, alpha=0.88,
                    zorder=10)

    # ----- Coloured polar patches above each revealed unit ball ------------
    if stage >= 2:
        _unit_patch_on_sheet_2d(ax, foci_2d_red[0], foci_2d_red[1],
                                foci_2d_red[2], zorder=15)
    if stage >= 5:
        _unit_patch_on_sheet_2d(ax, foci_2d_blue[0], foci_2d_blue[1],
                                foci_2d_blue[2], zorder=15)
    if stage >= 8:
        _unit_patch_on_sheet_2d(ax, GREEN_UV_2D[0], GREEN_UV_2D[1],
                                GREEN, zorder=15)

    # Lock the 3D extents so the projection is identical across stages.
    z_top_label = NORMAL_LIFT + NORMAL_SCALE * m + 0.7
    ax.set_xlim3d(-edge, edge)
    ax.set_ylim3d(-edge, edge)
    ax.set_zlim3d(0, z_top_label)
    ax.set_autoscale_on(False)

    # ----- Above-the-sheet artists ------------------------------------------
    if stage >= 1:
        _focal_top_2d(ax, foci_2d_red[0], foci_2d_red[1])
    if stage >= 4:
        _focal_top_2d(ax, foci_2d_blue[0], foci_2d_blue[1])
    if stage >= 7:
        _focal_top_2d(ax, GREEN_UV_2D[0], GREEN_UV_2D[1])
    if stage >= 3:
        _delta_label_2d(ax, foci_2d_red[0], foci_2d_red[1],
                        r"$\Delta f > 0$", RED, offset=0.15)
    if stage >= 6:
        _delta_label_2d(ax, foci_2d_blue[0], foci_2d_blue[1],
                        r"$\Delta f < 0$", BLUE, side="below")
    if stage >= 9:
        # Sit at the bump level, just to the right of the green unit-ball patch.
        _delta_label_2d(ax, GREEN_UV_2D[0], GREEN_UV_2D[1],
                        r"$\Delta f \approx 0$", GREEN,
                        side="at", du=r2 + 0.15, ha="left")

    ax.set_axis_off()
    ax.view_init(elev=18, azim=-30)
    ax.set_proj_type("persp", focal_length=0.3)
    ax.set_box_aspect((1, 1, 0.85))

    # "uv plane" label running along the front edge of the (u,v) grid —
    # rotated to follow the projected edge in figure coordinates.
    fig.canvas.draw()

    def _to_fig(x, y, z):
        xs, ys, _ = proj3d.proj_transform(x, y, z, ax.get_proj())
        px, py = ax.transData.transform((xs, ys))
        return fig.transFigure.inverted().transform((px, py))

    fl = _to_fig(-edge, -edge, 0.0)
    fr = _to_fig( edge, -edge, 0.0)
    dl = fig.transFigure.transform(fl)
    dr = fig.transFigure.transform(fr)
    edge_angle = math.degrees(math.atan2(dr[1] - dl[1], dr[0] - dl[0]))
    mid = ((fl[0] + fr[0]) / 2, (fl[1] + fr[1]) / 2)
    nx_, ny_ = -math.sin(math.radians(edge_angle)), math.cos(math.radians(edge_angle))
    label_pos = (mid[0] - 0.03 * nx_, mid[1] - 0.03 * ny_)
    fig.text(label_pos[0], label_pos[1], r"$uv$ plane", fontsize=18,
             color=DARK, ha="center", va="center", rotation=edge_angle)
    return fig


for stage in range(N_STAGES):
    fig = build_2d_stage(stage)
    plt.savefig(str(OUT_DIR / f"lap_euclidean_2d_stage_{stage}.png"),
                dpi=220, transparent=True)
    plt.close()

_full_2d = Image.open(str(OUT_DIR / f"lap_euclidean_2d_stage_{N_STAGES - 1}.png"))
_bbox_2d = _full_2d.getchannel("A").getbbox()
if _bbox_2d:
    for stage in range(N_STAGES):
        p = OUT_DIR / f"lap_euclidean_2d_stage_{stage}.png"
        Image.open(str(p)).crop(_bbox_2d).save(str(p))
print(f"[ok] lap_euclidean_2d_stage_0..{N_STAGES - 1}.png")
