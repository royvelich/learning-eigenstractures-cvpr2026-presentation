"""Intuition image for the 'Recover the eigenbasis…' slide.

Seven cumulative APNG stages, each a full rendered scene at the current
rotation phase, so the slide can swap between them via $clicks while the
camera oscillates gently around the z-axis:

  optimal_basis_stage1.png  — 3D axes + the basis plane
  optimal_basis_stage2.png  + the basis vectors b1, b2
  optimal_basis_stage3.png  + the 3D vector v
  optimal_basis_stage4.png  + projection of v onto b1  (c1·b1, dashed drop)
  optimal_basis_stage5.png  + projection of v onto b2  (c2·b2, dashed drop)
  optimal_basis_stage6.png  + the sum v_proj = c1·b1 + c2·b2 (parallelogram)
  optimal_basis_stage7.png  + the residual v - v_proj
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
TEAL = "#2B5876"
DARK = "#0f172a"
GREY = "#94a3b8"
EMERALD = "#047857"
RED = "#b91c1c"

# ---------------- the scene
# Rotated basis (30° in the plane) — so b1, b2 and their c·b projections all
# live in the *interior* of the first quadrant, NOT on the x/y axes. This
# avoids the basis arrows visually colliding with the projection arrows.
ROT_DEG = 30.0
_rot = np.radians(ROT_DEG)
b1 = np.array([np.cos(_rot),  np.sin(_rot), 0.0])   # unit
b2 = np.array([-np.sin(_rot), np.cos(_rot), 0.0])   # unit, perp to b1 in the plane
B_LEN = 0.9                         # drawn length of the basis arrows
# v chosen so its in-plane component aligns with the (b1, b2) bisector
# → c1 ≈ c2, so the two c·b projections appear visually balanced and BOTH
# clearly extend past the basis arrows.
v = np.array([0.45, 1.70, 0.95])
c1 = float(v @ b1)
c2 = float(v @ b2)
v_proj = c1 * b1 + c2 * b2

LABEL_OFFSET = 0.22       # perpendicular offset for the b1, b2 labels
CB_TIP_EXTRA = 0.40       # distance past c·b's tip (along the b-direction) where the c·b label sits
ARROW_LW = 1.6            # uniform line-width for every vector / axis arrow

# -------- "better" basis: same b1, but b2 tilted out of the xy-plane around b1
# so the spanned plane sits closer to v → smaller reconstruction residual.
TILT_DEG = 25.0   # less tilt → slightly larger residual so the red v-v_proj line is visible
_tilt = np.radians(TILT_DEG)
b1B = b1                                         # unchanged
b2B = b2 * np.cos(_tilt) + np.array([0.0, 0.0, 1.0]) * np.sin(_tilt)
c1B = float(v @ b1B)
c2B = float(v @ b2B)
v_projB = c1B * b1B + c2B * b2B
S = 1.85          # half-extent of the plane patch
AX = 2.40         # length of x, y axis arrows (stretch a bit past the grid)
AZ_LEN = 1.55     # length of the z axis (shorter so it stays inside the frame)
LIM = 2.65        # axis limits — must include axis-label positions


def arrow(ax, p0, p1, color, lw=1.6, mut=18, ls="-", zorder=5,
          head_world=0.15, head_width_ratio=0.28, head_n_sides=18):
    """A 3D arrow with a true triangulated cone arrowhead.

    Shaft: an `ax.plot` line from p0 to where the cone's base sits.
    Head:  a `Poly3DCollection` of triangles (a cone), with its tip at p1
           and base at p1 - head_world * direction. Since the cone is built
           in world coordinates and rendered through the 3D pipeline, it
           transforms correctly under camera rotation — no screen-space
           hack like FancyArrowPatch.

    The shaft stops at the cone's base, so the line never visually
    "pokes out" past the head.

    `mut` is accepted but unused (kept for call-site compatibility).
    """
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    if L < 1e-9:
        return
    head_dir = d / L
    head_len = min(head_world, L * 0.45)
    base_center = p1 - head_dir * head_len

    # Shaft (stops at the cone's base to avoid double-drawing)
    ax.plot([p0[0], base_center[0]],
            [p0[1], base_center[1]],
            [p0[2], base_center[2]],
            color=color, lw=lw, linestyle=ls, zorder=zorder,
            solid_capstyle="butt")

    # Two perpendicular unit vectors to head_dir
    ref = np.array([0.0, 0.0, 1.0]) if abs(head_dir[2]) < 0.95 \
        else np.array([1.0, 0.0, 0.0])
    perp1 = np.cross(head_dir, ref); perp1 /= np.linalg.norm(perp1)
    perp2 = np.cross(head_dir, perp1)   # already unit (head_dir ⟂ perp1, both unit)

    # Ring of points around the cone's base
    radius = head_len * head_width_ratio
    angs = np.linspace(0.0, 2 * np.pi, head_n_sides, endpoint=False)
    base_pts = np.array([
        base_center + radius * (np.cos(a) * perp1 + np.sin(a) * perp2)
        for a in angs
    ])

    # Side triangles (base ring → tip) AND the closing base disk (so the
    # cone doesn't look hollow from the rear).
    side_tris, disk_tris = [], []
    for i in range(head_n_sides):
        j = (i + 1) % head_n_sides
        side_tris.append([base_pts[i], base_pts[j], p1])
        disk_tris.append([base_center, base_pts[j], base_pts[i]])
    head = Poly3DCollection(side_tris + disk_tris, facecolor=color,
                            edgecolor="none", zorder=zorder + 1)
    ax.add_collection3d(head)


# ============== layer functions (each adds its own elements)
def draw_axes(ax):
    """xyz coordinate axes only (no plane, no basis)."""
    arrow(ax, [0, 0, 0], [AX, 0, 0], GREY, lw=ARROW_LW, mut=14, zorder=2)
    arrow(ax, [0, 0, 0], [0, AX, 0], GREY, lw=ARROW_LW, mut=14, zorder=2)
    arrow(ax, [0, 0, 0], [0, 0, AZ_LEN], GREY, lw=ARROW_LW, mut=14, zorder=2)
    ax.text(AX + 0.14, 0, 0, r"$x$", color=GREY, fontsize=18, fontweight="bold",
            ha="left", va="center")
    ax.text(0, AX + 0.14, 0, r"$y$", color=GREY, fontsize=18, fontweight="bold",
            ha="left", va="center")
    ax.text(0, 0, AZ_LEN + 0.16, r"$z$", color=GREY, fontsize=18, fontweight="bold",
            ha="left", va="bottom")


def draw_plane_xy(ax):
    """The flat xy-plane patch + grid lines (the span of the flat basis)."""
    corners = np.array([[-S, -S, 0], [S, -S, 0], [S, S, 0], [-S, S, 0]])
    ax.add_collection3d(Poly3DCollection([corners], facecolor=TEAL,
                                          edgecolor=TEAL, alpha=0.16, lw=1.0))
    GRID = 6
    for k in range(-GRID, GRID + 1):
        t = k / GRID * S
        ax.plot([-S, S], [t, t], [0, 0], color="#64748b", lw=0.4, alpha=0.55)
        ax.plot([t, t], [-S, S], [0, 0], color="#64748b", lw=0.4, alpha=0.55)


def draw_plane_tilted(ax):
    """The tilted plane patch + grid lines (the span of the better basis)."""
    corners = np.array([
        s1 * S * b1B + s2 * S * b2B
        for s1, s2 in [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    ])
    ax.add_collection3d(Poly3DCollection([corners], facecolor=TEAL,
                                          edgecolor=TEAL, alpha=0.16, lw=1.0))
    GRID = 6
    for k in range(-GRID, GRID + 1):
        t = k / GRID * S
        p1 = -S * b1B + t * b2B; p2 =  S * b1B + t * b2B
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                color="#64748b", lw=0.4, alpha=0.55)
        p1 =  t * b1B - S * b2B; p2 =  t * b1B + S * b2B
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]],
                color="#64748b", lw=0.4, alpha=0.55)


def draw_basis(ax):
    p1 = B_LEN * b1
    p2 = B_LEN * b2
    arrow(ax, [0, 0, 0], p1, INDIGO, lw=ARROW_LW, mut=16, zorder=6)
    arrow(ax, [0, 0, 0], p2, INDIGO, lw=ARROW_LW, mut=16, zorder=6)
    # labels offset perpendicular to each basis vector, in the plane.
    # b1 label sits "below" b1 (along -b2); b2 label sits "left of" b2 (along -b1).
    lp1 = p1 + (-b2) * LABEL_OFFSET
    lp2 = p2 + (-b1) * LABEL_OFFSET
    ax.text(lp1[0], lp1[1], 0, r"$b_1$",
            color=INDIGO, fontsize=17, fontweight="bold",
            ha="center", va="center")
    ax.text(lp2[0], lp2[1], 0, r"$b_2$",
            color=INDIGO, fontsize=17, fontweight="bold",
            ha="center", va="center")


def draw_v(ax):
    arrow(ax, [0, 0, 0], v, DARK, lw=ARROW_LW, mut=22, zorder=10)
    ax.text(v[0] + 0.05, v[1] + 0.05, v[2] + 0.13, r"$v$",
            color=DARK, fontsize=18, fontweight="bold")


def draw_proj_on_b1(ax):
    """Projection of v onto the b1-line: arrow c1·b1 + dashed perpendicular drop from v."""
    end = c1 * b1
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, mut=18, zorder=7)
    # label just past the c1·b1 tip, ALONG the b1 direction
    lp = end + CB_TIP_EXTRA * b1
    ax.text(lp[0], lp[1], 0, r"$c_1 b_1$",
            color=EMERALD, fontsize=14, fontweight="bold",
            ha="center", va="center")
    # dashed perpendicular drop from v down to c1·b1
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_proj_on_b2(ax):
    """Projection of v onto the b2-line: arrow c2·b2 + dashed perpendicular drop from v."""
    end = c2 * b2
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, mut=18, zorder=7)
    # label just past the c2·b2 tip, ALONG the b2 direction
    lp = end + CB_TIP_EXTRA * b2
    ax.text(lp[0], lp[1], 0, r"$c_2 b_2$",
            color=EMERALD, fontsize=14, fontweight="bold",
            ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_sum_vproj(ax):
    """Sum the two projections: parallelogram closure + the v_proj arrow."""
    p_b1 = c1 * b1
    p_b2 = c2 * b2
    # parallelogram closing lines: c1·b1 → v_proj  and  c2·b2 → v_proj
    ax.plot([p_b1[0], v_proj[0]], [p_b1[1], v_proj[1]], [0, 0],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    ax.plot([p_b2[0], v_proj[0]], [p_b2[1], v_proj[1]], [0, 0],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    # the v_proj arrow (sum of c1·b1 and c2·b2)
    arrow(ax, [0, 0, 0], v_proj, EMERALD, lw=ARROW_LW, mut=22, zorder=8)
    ax.text(v_proj[0] + 0.20, v_proj[1] + 0.05, 0,
            r"$v_{\text{proj}}$",
            color=EMERALD, fontsize=16, fontweight="bold",
            ha="left", va="center")


def draw_residual(ax):
    ax.plot([v_proj[0], v[0]], [v_proj[1], v[1]], [v_proj[2], v[2]],
            color=RED, lw=2.4, ls=(0, (4, 3)), zorder=12)
    mid_r = 0.5 * (v + v_proj)
    ax.text(mid_r[0] + 0.13, mid_r[1] + 0.06, mid_r[2],
            r"$v - v_{\text{proj}}$",
            color=RED, fontsize=13, fontweight="bold")


# ====================================================================
# "Better" basis — same v, same b1, but b2 tilted toward v so the plane
# spanned by (b1, b2) sits closer to v.
# ====================================================================


def draw_basis_better(ax):
    p1 = B_LEN * b1B
    p2 = B_LEN * b2B
    arrow(ax, [0, 0, 0], p1, INDIGO, lw=ARROW_LW, mut=16, zorder=6)
    arrow(ax, [0, 0, 0], p2, INDIGO, lw=ARROW_LW, mut=16, zorder=6)
    # offsets perpendicular to each basis vector, IN THE PLANE
    lp1 = p1 + (-b2B) * LABEL_OFFSET
    lp2 = p2 + (-b1B) * LABEL_OFFSET
    ax.text(lp1[0], lp1[1], lp1[2], r"$b_1$",
            color=INDIGO, fontsize=17, fontweight="bold",
            ha="center", va="center")
    ax.text(lp2[0], lp2[1], lp2[2], r"$b_2$",
            color=INDIGO, fontsize=17, fontweight="bold",
            ha="center", va="center")


def draw_proj_on_b1_better(ax):
    end = c1B * b1B
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, mut=18, zorder=7)
    lp = end + CB_TIP_EXTRA * b1B
    ax.text(lp[0], lp[1], lp[2], r"$c_1 b_1$",
            color=EMERALD, fontsize=14, fontweight="bold",
            ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_proj_on_b2_better(ax):
    end = c2B * b2B
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, mut=18, zorder=7)
    lp = end + CB_TIP_EXTRA * b2B
    ax.text(lp[0], lp[1], lp[2], r"$c_2 b_2$",
            color=EMERALD, fontsize=14, fontweight="bold",
            ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_sum_vproj_better(ax):
    p_b1 = c1B * b1B
    p_b2 = c2B * b2B
    ax.plot([p_b1[0], v_projB[0]], [p_b1[1], v_projB[1]], [p_b1[2], v_projB[2]],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    ax.plot([p_b2[0], v_projB[0]], [p_b2[1], v_projB[1]], [p_b2[2], v_projB[2]],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    arrow(ax, [0, 0, 0], v_projB, EMERALD, lw=ARROW_LW, mut=22, zorder=8)
    ax.text(v_projB[0] + 0.20, v_projB[1] + 0.05, v_projB[2] + 0.04,
            r"$v_{\text{proj}}$",
            color=EMERALD, fontsize=16, fontweight="bold",
            ha="left", va="center")


def draw_residual_better(ax):
    ax.plot([v_projB[0], v[0]], [v_projB[1], v[1]], [v_projB[2], v[2]],
            color=RED, lw=2.4, ls=(0, (4, 3)), zorder=12)
    mid_r = 0.5 * (v + v_projB)
    ax.text(mid_r[0] + 0.13, mid_r[1] + 0.06, mid_r[2] + 0.05,
            r"$v - v_{\text{proj}}$",
            color=RED, fontsize=13, fontweight="bold")


import io

# ---- Animation parameters: gentle CW/CCW oscillation around z (azimuth)
AZ_BASE = -55.0       # centre of the sweep
AZ_AMP = 14.0         # ± degrees from centre
N_FRAMES = 36          # frames per cycle
FRAME_MS = 90          # display duration per frame -> 36*90 ≈ 3.2s cycle
DPI = 220              # sharper APNGs (larger file, but the deck is local)


def render_frame(draw_layers, azim):
    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    for fn in draw_layers:
        fn(ax)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=22, azim=azim)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM * 0.3, LIM)
    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=DPI, transparent=True)
    plt.close()
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


def stage_layers(stage):
    """Cumulative layers for the flat basis.

    Reveal order:
      1. coordinate axes only
      2. + v (the 3D vector)
      3. + the basis AND the grid it spans
      4. + projection of v onto b1
      5. + projection of v onto b2
      6. + the sum (v_proj)
      7. + the residual
    """
    L = [[draw_axes]]
    L.append(L[-1] + [draw_v])
    L.append(L[-1] + [draw_plane_xy, draw_basis])
    L.append(L[-1] + [draw_proj_on_b1])
    L.append(L[-1] + [draw_proj_on_b2])
    L.append(L[-1] + [draw_sum_vproj])
    L.append(L[-1] + [draw_residual])
    return L[stage]


def stage_layers_better(stage):
    """Cumulative layers for the BETTER basis (tilted plane closer to v)."""
    L = [[draw_axes]]
    L.append(L[-1] + [draw_v])
    L.append(L[-1] + [draw_plane_tilted, draw_basis_better])
    L.append(L[-1] + [draw_proj_on_b1_better])
    L.append(L[-1] + [draw_proj_on_b2_better])
    L.append(L[-1] + [draw_sum_vproj_better])
    L.append(L[-1] + [draw_residual_better])
    return L[stage]


# Pre-compute the shared crop bbox by sampling EVERY frame of the densest
# stage. Sampling only the extreme angles misses where the x/y axis tips
# swing furthest in screen space (since projection isn't monotonic in azim).
print(f"[..] computing shared bbox over {N_FRAMES} frames (both bases)")
bb_x0, bb_y0, bb_x1, bb_y1 = 10**9, 10**9, 0, 0
DENSEST = 6   # zero-indexed; stage 7 = index 6 has the most content
for layers_fn in (stage_layers, stage_layers_better):
    for i in range(N_FRAMES):
        azim = AZ_BASE + AZ_AMP * np.sin(2 * np.pi * i / N_FRAMES)
        im = render_frame(layers_fn(DENSEST), azim)
        b = im.getchannel("A").getbbox()
        if b is not None:
            bb_x0 = min(bb_x0, b[0]); bb_y0 = min(bb_y0, b[1])
            bb_x1 = max(bb_x1, b[2]); bb_y1 = max(bb_y1, b[3])
PAD = 8  # a few extra pixels of safety
bbox = (max(0, bb_x0 - PAD), max(0, bb_y0 - PAD), bb_x1 + PAD, bb_y1 + PAD)
print(f"[ok] bbox={bbox}")


def render_stage_apng(stage_idx, out_name, layers_fn):
    frames = []
    for i in range(N_FRAMES):
        # smooth sin oscillation
        azim = AZ_BASE + AZ_AMP * np.sin(2 * np.pi * i / N_FRAMES)
        im = render_frame(layers_fn(stage_idx), azim)
        frames.append(im.crop(bbox))
    out = OUT_DIR / f"{out_name}.png"
    # disposal=1 (clear to transparent) + blend=0 (replace, don't composite)
    # guarantees each frame is a FULL picture instead of a diff over the
    # previous — otherwise Pillow saves deltas and the z-axis gets "lost"
    # in frames where it didn't move from the previous frame.
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=FRAME_MS, loop=0, disposal=1, blend=0)
    print(f"[ok] {out.name}  ({len(frames)} frames)")


for stage in range(7):
    render_stage_apng(stage, f"optimal_basis_stage{stage + 1}", stage_layers)
for stage in range(7):
    render_stage_apng(stage, f"optimal_basis_better_stage{stage + 1}",
                      stage_layers_better)

# Clean up any old static overlays + scratch.
for old in OUT_DIR.glob("optimal_basis_bg.png"):
    old.unlink(); print(f"[rm] {old.name}")
for old in OUT_DIR.glob("optimal_basis_ov_*.png"):
    old.unlink(); print(f"[rm] {old.name}")
shared_path = OUT_DIR / "_optimal_basis_all.png"
if shared_path.exists():
    shared_path.unlink()
