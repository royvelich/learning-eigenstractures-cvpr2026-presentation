"""Click-by-click stages for the 'Recover the eigenbasis…' slide.

Two sequential build-ups sharing the same camera and crop bbox.

  Sequence A — flat basis (b2 in the xy-plane):
    step 1   axes + v
    step 2   basis (b1, b2) + plane grid + v        (axes removed)
    step 3   + projections c1 b1, c2 b2
    step 4   + reconstructed v_proj
    step 5   + residual v - v_proj

  Sequence B — slightly tilted basis (b2 lifted out of xy toward v):
    step 6   axes + v                                (clean reset before B)
    step 7   tilted basis + tilted grid + v
    step 8   + tilted projections
    step 9   + tilted v_proj
    step 10  + tilted residual (visibly smaller)
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import io

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
TEAL = "#2B5876"
DARK = "#0f172a"
GREY = "#94a3b8"
EMERALD = "#047857"
RED = "#b91c1c"

# ---------------- the scene
ROT_DEG = 30.0
_rot = np.radians(ROT_DEG)
b1 = np.array([np.cos(_rot),  np.sin(_rot), 0.0])
b2 = np.array([-np.sin(_rot), np.cos(_rot), 0.0])
B_LEN = 0.9
v = np.array([0.45, 1.70, 0.95])
c1 = float(v @ b1)
c2 = float(v @ b2)
v_proj = c1 * b1 + c2 * b2

# Tilted ("better") basis: rotate b1, b2 around the global x-axis by a
# small angle so the spanned plane lifts slightly out of xy toward v.
TILT_DEG = 20.0


def _rot_x(vec, deg):
    """Rotate a 3-vector around the global x-axis by `deg` degrees."""
    t = np.radians(deg)
    c, s = np.cos(t), np.sin(t)
    x, y, z = vec
    return np.array([x, y * c - z * s, y * s + z * c])


b1B = _rot_x(b1, TILT_DEG)
b2B = _rot_x(b2, TILT_DEG)
c1B = float(v @ b1B)
c2B = float(v @ b2B)
v_projB = c1B * b1B + c2B * b2B

LABEL_OFFSET = 0.34
CB_TIP_EXTRA = 0.40
ARROW_LW = 1.6

S = 1.85
AX = 2.40
AZ_LEN = 1.55
LIM = 2.65

AZ_BASE = -45.0
ELEV = 22
DPI = 220


def arrow(ax, p0, p1, color, lw=1.6, zorder=5, ls="-",
          head_world=0.15, head_width_ratio=0.28, head_n_sides=18):
    p0 = np.asarray(p0, dtype=float)
    p1 = np.asarray(p1, dtype=float)
    d = p1 - p0
    L = float(np.linalg.norm(d))
    if L < 1e-9:
        return
    head_dir = d / L
    head_len = min(head_world, L * 0.45)
    base_center = p1 - head_dir * head_len
    ax.plot([p0[0], base_center[0]],
            [p0[1], base_center[1]],
            [p0[2], base_center[2]],
            color=color, lw=lw, linestyle=ls, zorder=zorder,
            solid_capstyle="butt")
    ref = np.array([0.0, 0.0, 1.0]) if abs(head_dir[2]) < 0.95 \
        else np.array([1.0, 0.0, 0.0])
    perp1 = np.cross(head_dir, ref); perp1 /= np.linalg.norm(perp1)
    perp2 = np.cross(head_dir, perp1)
    radius = head_len * head_width_ratio
    angs = np.linspace(0.0, 2 * np.pi, head_n_sides, endpoint=False)
    base_pts = np.array([
        base_center + radius * (np.cos(a) * perp1 + np.sin(a) * perp2)
        for a in angs
    ])
    side_tris, disk_tris = [], []
    for i in range(head_n_sides):
        j = (i + 1) % head_n_sides
        side_tris.append([base_pts[i], base_pts[j], p1])
        disk_tris.append([base_center, base_pts[j], base_pts[i]])
    head = Poly3DCollection(side_tris + disk_tris, facecolor=color,
                            edgecolor="none", zorder=zorder + 1)
    ax.add_collection3d(head)


# ============== layer functions — shared ===================================

def draw_axes(ax):
    arrow(ax, [0, 0, 0], [AX, 0, 0], GREY, lw=ARROW_LW, zorder=2)
    arrow(ax, [0, 0, 0], [0, AX, 0], GREY, lw=ARROW_LW, zorder=2)
    arrow(ax, [0, 0, 0], [0, 0, AZ_LEN], GREY, lw=ARROW_LW, zorder=2)
    ax.text(AX + 0.14, 0, 0, r"$x$", color=GREY, fontsize=18,
            fontweight="bold", ha="left", va="center")
    ax.text(0, AX + 0.14, 0, r"$y$", color=GREY, fontsize=18,
            fontweight="bold", ha="left", va="center")
    ax.text(0, 0, AZ_LEN + 0.16, r"$z$", color=GREY, fontsize=18,
            fontweight="bold", ha="left", va="bottom")


def draw_v(ax):
    arrow(ax, [0, 0, 0], v, DARK, lw=ARROW_LW, zorder=10)
    ax.text(v[0] + 0.05, v[1] + 0.05, v[2] + 0.13, r"$v$",
            color=DARK, fontsize=18, fontweight="bold")


# ---- flat basis -----------------------------------------------------------

def draw_plane_xy(ax):
    corners = np.array([[-S, -S, 0], [S, -S, 0], [S, S, 0], [-S, S, 0]])
    ax.add_collection3d(Poly3DCollection([corners], facecolor=TEAL,
                                          edgecolor=TEAL, alpha=0.16, lw=1.0))
    GRID = 6
    for k in range(-GRID, GRID + 1):
        t = k / GRID * S
        ax.plot([-S, S], [t, t], [0, 0], color="#64748b", lw=0.4, alpha=0.55)
        ax.plot([t, t], [-S, S], [0, 0], color="#64748b", lw=0.4, alpha=0.55)


def draw_basis(ax):
    p1 = B_LEN * b1
    p2 = B_LEN * b2
    arrow(ax, [0, 0, 0], p1, INDIGO, lw=ARROW_LW, zorder=6)
    arrow(ax, [0, 0, 0], p2, INDIGO, lw=ARROW_LW, zorder=6)
    lp1 = p1 + (-b2) * (LABEL_OFFSET + 0.18)   # b1 gets extra clearance
    lp2 = p2 + (-b1) * LABEL_OFFSET
    ax.text(lp1[0], lp1[1], 0, r"$b_1$", color=INDIGO,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.text(lp2[0], lp2[1], 0, r"$b_2$", color=INDIGO,
            fontsize=14, fontweight="bold", ha="center", va="center")


def draw_proj_on_b1(ax):
    end = c1 * b1
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, zorder=7)
    lp = end + CB_TIP_EXTRA * b1
    ax.text(lp[0], lp[1], 0, r"$c_1 b_1$", color=EMERALD,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_proj_on_b2(ax):
    end = c2 * b2
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, zorder=7)
    # Diagonally offset: past the tip along b2 AND perpendicular (-b1)
    # so the label sits clear of both the b2 arrow's own label and the
    # dashed perpendicular drop from v.
    lp = end + 0.45 * b2 - 0.5 * b1
    ax.text(lp[0], lp[1], 0, r"$c_2 b_2$", color=EMERALD,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_sum_vproj(ax):
    p_b1 = c1 * b1
    p_b2 = c2 * b2
    ax.plot([p_b1[0], v_proj[0]], [p_b1[1], v_proj[1]], [0, 0],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    ax.plot([p_b2[0], v_proj[0]], [p_b2[1], v_proj[1]], [0, 0],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    arrow(ax, [0, 0, 0], v_proj, EMERALD, lw=ARROW_LW, zorder=8)
    ax.text(v_proj[0] + 0.20, v_proj[1] + 0.05, 0,
            r"$v_{\text{proj}}$", color=EMERALD,
            fontsize=16, fontweight="bold", ha="left", va="center")


def draw_residual(ax):
    ax.plot([v_proj[0], v[0]], [v_proj[1], v[1]], [v_proj[2], v[2]],
            color=RED, lw=1.5, ls=(0, (4, 3)), zorder=12)
    mid_r = 0.5 * (v + v_proj)
    ax.text(mid_r[0] + 0.13, mid_r[1] + 0.06, mid_r[2],
            r"$v - v_{\text{proj}}$",
            color=RED, fontsize=13, fontweight="bold")


# ---- tilted ("better") basis ---------------------------------------------

def draw_plane_tilted(ax):
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


def draw_basis_better(ax):
    p1 = B_LEN * b1B
    p2 = B_LEN * b2B
    arrow(ax, [0, 0, 0], p1, INDIGO, lw=ARROW_LW, zorder=6)
    arrow(ax, [0, 0, 0], p2, INDIGO, lw=ARROW_LW, zorder=6)
    lp1 = p1 + (-b2B) * (LABEL_OFFSET + 0.18)   # b1 gets extra clearance
    lp2 = p2 + (-b1B) * LABEL_OFFSET
    ax.text(lp1[0], lp1[1], lp1[2], r"$b_1$", color=INDIGO,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.text(lp2[0], lp2[1], lp2[2], r"$b_2$", color=INDIGO,
            fontsize=14, fontweight="bold", ha="center", va="center")


def draw_proj_on_b1_better(ax):
    end = c1B * b1B
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, zorder=7)
    lp = end + CB_TIP_EXTRA * b1B
    ax.text(lp[0], lp[1], lp[2], r"$c_1 b_1$", color=EMERALD,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_proj_on_b2_better(ax):
    end = c2B * b2B
    arrow(ax, [0, 0, 0], end, EMERALD, lw=ARROW_LW, zorder=7)
    lp = end + CB_TIP_EXTRA * b2B
    ax.text(lp[0], lp[1], lp[2], r"$c_2 b_2$", color=EMERALD,
            fontsize=14, fontweight="bold", ha="center", va="center")
    ax.plot([v[0], end[0]], [v[1], end[1]], [v[2], end[2]],
            color=EMERALD, lw=1.5, ls=(0, (4, 3)), alpha=0.65, zorder=6)


def draw_sum_vproj_better(ax):
    p_b1 = c1B * b1B
    p_b2 = c2B * b2B
    ax.plot([p_b1[0], v_projB[0]], [p_b1[1], v_projB[1]], [p_b1[2], v_projB[2]],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    ax.plot([p_b2[0], v_projB[0]], [p_b2[1], v_projB[1]], [p_b2[2], v_projB[2]],
            color=EMERALD, lw=1.2, ls=(0, (3, 3)), alpha=0.75, zorder=6)
    arrow(ax, [0, 0, 0], v_projB, EMERALD, lw=ARROW_LW, zorder=8)
    ax.text(v_projB[0] + 0.20, v_projB[1] + 0.05, v_projB[2] + 0.04,
            r"$v_{\text{proj}}$", color=EMERALD,
            fontsize=16, fontweight="bold", ha="left", va="center")


def draw_residual_better(ax):
    ax.plot([v_projB[0], v[0]], [v_projB[1], v[1]], [v_projB[2], v[2]],
            color=RED, lw=1.5, ls=(0, (4, 3)), zorder=12)
    mid_r = 0.5 * (v + v_projB)
    ax.text(mid_r[0] + 0.13, mid_r[1] + 0.06, mid_r[2] + 0.05,
            r"$v - v_{\text{proj}}$",
            color=RED, fontsize=13, fontweight="bold")


# ============== render =====================================================

STAGES = [
    # Sequence A — flat basis
    [draw_axes, draw_v],
    [draw_plane_xy, draw_basis, draw_v],
    [draw_plane_xy, draw_basis, draw_v, draw_proj_on_b1, draw_proj_on_b2],
    [draw_plane_xy, draw_basis, draw_v, draw_proj_on_b1, draw_proj_on_b2,
     draw_sum_vproj],
    [draw_plane_xy, draw_basis, draw_v, draw_proj_on_b1, draw_proj_on_b2,
     draw_sum_vproj, draw_residual],
    # Sequence B — clean reset, then tilted basis
    [draw_axes, draw_v],
    [draw_plane_tilted, draw_basis_better, draw_v],
    [draw_plane_tilted, draw_basis_better, draw_v,
     draw_proj_on_b1_better, draw_proj_on_b2_better],
    [draw_plane_tilted, draw_basis_better, draw_v,
     draw_proj_on_b1_better, draw_proj_on_b2_better, draw_sum_vproj_better],
    [draw_plane_tilted, draw_basis_better, draw_v,
     draw_proj_on_b1_better, draw_proj_on_b2_better, draw_sum_vproj_better,
     draw_residual_better],
]


def render_to_image(layers):
    fig = plt.figure(figsize=(7.0, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    # Perspective projection (same focal_length as the other diagrams in
    # the deck — gen_14 / gen_16) so depth cues match the rest of the talk.
    ax.set_proj_type("persp", focal_length=0.3)
    for fn in layers:
        fn(ax)
    ax.set_axis_off()
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=ELEV, azim=AZ_BASE)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM * 0.3, LIM)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=DPI, transparent=True)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGBA")


print("[..] computing shared bbox across all stages")
bb_x0, bb_y0, bb_x1, bb_y1 = 10**9, 10**9, 0, 0
images = []
for stage in STAGES:
    im = render_to_image(stage)
    images.append(im)
    b = im.getchannel("A").getbbox()
    if b is not None:
        bb_x0 = min(bb_x0, b[0]); bb_y0 = min(bb_y0, b[1])
        bb_x1 = max(bb_x1, b[2]); bb_y1 = max(bb_y1, b[3])
PAD = 8
bbox = (max(0, bb_x0 - PAD), max(0, bb_y0 - PAD), bb_x1 + PAD, bb_y1 + PAD)
print(f"[ok] shared bbox = {bbox}")

for i, im in enumerate(images, start=1):
    out = OUT_DIR / f"optimal_basis_step{i}.png"
    im.crop(bbox).save(out)
    print(f"[ok] {out.name}")
