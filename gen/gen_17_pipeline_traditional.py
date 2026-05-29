"""Figures for the 'Traditional pipeline' slide — TWO branches share the
same 7-vertex layout (focal i + 6 ring neighbours) so the slide can put
them side-by-side without scale mismatch.

Upper (mesh / cotangent) branch:
  pipeline_vertices.png        — just the vertices.
  pipeline_triangulation.png   — focal + 1-ring with all 6 triangle faces.
  pipeline_voronoi_cot.png     — same 1-ring with the Voronoi cell shaded
                                 (M_ii) and the cotangent angles (α, β)
                                 labelled on one edge ij (S_ij).

Lower (graph / Belkin–Niyogi) branch:
  pipeline_knn_graph.png       — same 7 vertices, but the connections are
                                 read as undirected graph edges (no faces).
  pipeline_heat_weights.png    — same graph with the focal–j edge
                                 highlighted, labelled with the heat-kernel
                                 weight W_ij = exp(-‖x_i − x_j‖² / t), and
                                 a D_ii label at the focal vertex (degree).
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Arc
from PIL import Image

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
TEAL = "#2B5876"
DARK = "#0f172a"
GREY = "#94a3b8"
EDGE_GREY = "#94a3b8"   # light grey for edges
RED = "#ef4444"          # focal reference point + highlighted edge
AMBER = "#b45309"
CELL_FILL = "#fecaca"   # red-200 (light red for the Voronoi cell)

POINT_SIZE = 110
FOCAL_SIZE = 170

# --- 1-ring: 6 neighbours around the centre, evenly spaced (regular vertex)
centre = np.array([0.0, 0.0])
angles = np.linspace(0, 2 * np.pi, 6, endpoint=False) + np.pi / 6  # offset so j sits to the right
R = 1.0
ring = R * np.column_stack([np.cos(angles), np.sin(angles)])
verts = np.vstack([centre[None, :], ring])   # index 0 = focal vertex i
focal = 0


def draw_edges(ax, edge_lw=2.6, edge_col=EDGE_GREY):
    # outer ring (hexagon perimeter)
    for k in range(6):
        a, b = 1 + k, 1 + (k + 1) % 6
        ax.plot([verts[a, 0], verts[b, 0]], [verts[a, 1], verts[b, 1]],
                color=edge_col, lw=edge_lw, zorder=3)
    # spokes from centre
    for k in range(6):
        a = 1 + k
        ax.plot([verts[focal, 0], verts[a, 0]],
                [verts[focal, 1], verts[a, 1]],
                color=edge_col, lw=edge_lw, zorder=3)


def draw_vertices(ax, pt_size=POINT_SIZE):
    # Non-focal vertices in black, no stroke.
    ring_idx = np.arange(1, len(verts))
    ax.scatter(verts[ring_idx, 0], verts[ring_idx, 1], s=pt_size,
               color=DARK, linewidths=0, zorder=6)
    # Focal reference vertex in red, slightly bigger, no stroke.
    ax.scatter([verts[focal, 0]], [verts[focal, 1]], s=FOCAL_SIZE,
               color=RED, linewidths=0, zorder=7)


def draw_one_ring(ax, edge_lw=2.6, edge_col=EDGE_GREY, pt_size=120):
    draw_edges(ax, edge_lw=edge_lw, edge_col=edge_col)
    draw_vertices(ax, pt_size=pt_size)


def style_axes(ax, pad=0.28):
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_xlim(verts[:, 0].min() - pad, verts[:, 0].max() + pad)
    ax.set_ylim(verts[:, 1].min() - pad, verts[:, 1].max() + pad)


def alpha_crop(path):
    im = Image.open(path)
    bbox = im.getchannel("A").getbbox()
    if bbox is not None:
        im.crop(bbox).save(path)


# All three pipeline figures (vertices, triangulation, voronoi+cot) MUST
# share identical pixel dimensions so the slide can overlay them and so
# the mesh appears at the same physical size across the row. We save the
# full canvas (no bbox=tight) for all of them, with the same figsize,
# axis limits, and DPI — single shared renderer below.
def render_share(name, build_fn):
    fig, ax = plt.subplots(figsize=(4.8, 4.8))
    build_fn(ax)
    style_axes(ax)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.savefig(OUT_DIR / f"{name}.png", dpi=220, transparent=True)
    plt.close()
    print(f"[ok] {name}.png")


render_share("pipeline_vertices", draw_vertices)
render_share("pipeline_triangulation", draw_one_ring)


# ============================================================ figure 2
def circumcenter(p1, p2, p3):
    a1, a2 = p1; b1, b2 = p2; c1, c2 = p3
    d = 2 * (a1 * (b2 - c2) + b1 * (c2 - a2) + c1 * (a2 - b2))
    ux = ((a1 ** 2 + a2 ** 2) * (b2 - c2)
          + (b1 ** 2 + b2 ** 2) * (c2 - a2)
          + (c1 ** 2 + c2 ** 2) * (a2 - b2)) / d
    uy = ((a1 ** 2 + a2 ** 2) * (c1 - b1)
          + (b1 ** 2 + b2 ** 2) * (a1 - c1)
          + (c1 ** 2 + c2 ** 2) * (b1 - a1)) / d
    return np.array([ux, uy])


# Voronoi cell = polygon of circumcenters of the 6 triangles, ordered ccw
cell = np.array([circumcenter(verts[focal], verts[1 + k], verts[1 + (k + 1) % 6])
                 for k in range(6)])

# Pick j = neighbour to the right (the first ring vertex, lowest |y|).
j = 1 + int(np.argmin(np.abs(ring[:, 1])))   # neighbour closest to the +x axis
# The two triangles sharing edge (i, j) have the two adjacent neighbours
# as their third vertices.
k_idx_in_ring = j - 1
k_alpha_ring = (k_idx_in_ring + 1) % 6
k_beta_ring  = (k_idx_in_ring - 1) % 6
k_alpha = 1 + k_alpha_ring   # upper opposite vertex
k_beta  = 1 + k_beta_ring    # lower opposite vertex

def draw_arc_label(ax, k, sym, col, r=0.24, label_off=0.12):
    v1 = verts[focal] - verts[k]
    v2 = verts[j] - verts[k]
    a1 = np.degrees(np.arctan2(v1[1], v1[0]))
    a2 = np.degrees(np.arctan2(v2[1], v2[0]))
    d = (a2 - a1) % 360
    if d > 180:
        a1, a2 = a2, a1
    arc = Arc(verts[k], 2 * r, 2 * r, angle=0,
              theta1=min(a1, a2), theta2=max(a1, a2),
              color=col, lw=2.6, zorder=11)
    ax.add_patch(arc)
    mid = np.radians((min(a1, a2) + max(a1, a2)) / 2)
    pl = verts[k] + (r + label_off) * np.array([np.cos(mid), np.sin(mid)])
    ax.text(pl[0], pl[1], sym, fontsize=30, color=col,
            ha="center", va="center", zorder=12, fontweight="bold")


def build_voronoi_cot(ax):
    # Shaded Voronoi cell — light red fill + red outline.
    ax.add_patch(Polygon(cell, closed=True, facecolor=CELL_FILL,
                         edgecolor=RED, lw=2.2, alpha=0.92, zorder=2))
    # Same mesh as the triangulation figure — shared draw_one_ring()
    draw_one_ring(ax)
    # Highlight edge (i, j) in red.
    ax.plot([verts[focal, 0], verts[j, 0]],
            [verts[focal, 1], verts[j, 1]],
            color=RED, lw=3.6, zorder=5)
    # Re-draw focal & j on top — focal red (bigger), j plain black.
    ax.scatter([verts[focal, 0]], [verts[focal, 1]], s=FOCAL_SIZE,
               color=RED, linewidths=0, zorder=10)
    ax.scatter([verts[j, 0]], [verts[j, 1]], s=POINT_SIZE,
               color=DARK, linewidths=0, zorder=10)
    # i / j vertex labels — offset i perpendicular to ij so it doesn't
    # sit on the edge; j outward along ij past the j vertex.
    ij = verts[j] - verts[focal]
    ij_unit = ij / np.linalg.norm(ij)
    perp = np.array([-ij_unit[1], ij_unit[0]])   # 90° ccw
    i_label_pos = verts[focal] + 0.22 * perp
    j_label_pos = verts[j] + 0.24 * ij_unit
    ax.text(i_label_pos[0], i_label_pos[1], r"$i$",
            fontsize=30, fontweight="bold", color=RED,
            ha="center", va="center", zorder=12)
    ax.text(j_label_pos[0], j_label_pos[1], r"$j$",
            fontsize=30, fontweight="bold", color=DARK,
            ha="center", va="center", zorder=12)
    # α / β arc labels on the two opposite vertices — drawn in black.
    draw_arc_label(ax, k_alpha, r"$\alpha$", DARK)
    draw_arc_label(ax, k_beta, r"$\beta$", DARK)
    # M_ii label inside the cell — placed inside the sector BETWEEN two
    # spokes (not on a spoke). Sector at 240° (lower-left), well away from
    # the i label which sits in the 120° sector (upper-left).
    sector_dir = np.array([np.cos(np.radians(240)), np.sin(np.radians(240))])
    m_pos = verts[focal] + 0.32 * sector_dir
    ax.text(m_pos[0], m_pos[1], r"$M_{ii}$", fontsize=30, color=AMBER,
            ha="center", va="center", fontweight="bold", zorder=12)


render_share("pipeline_voronoi_cot", build_voronoi_cot)


# ============================================================ Lower branch
# SAME 7 vertices as the upper branch (focal + 6 ring) — drawn now as a
# point cloud, and connected with k-NN edges. We use k=2 from each
# vertex's perspective and we DO NOT add the ring-to-ring closure that
# completes a triangulation, so the result is visibly NOT a triangle mesh:
# six spokes + the two ring-to-ring edges that each ring vertex picks as
# its second neighbour (excluding the focal).

# Each ring vertex's 2 nearest neighbours = {focal, next ring vertex going
# CCW}. The union (undirected) is the 6 spokes + 6 perimeter edges, which
# IS the triangulation. So instead we use k=1 from each ring vertex: every
# ring vertex's single nearest is the focal — giving a star-graph of just
# the 6 spokes. Perimeter edges are dropped on purpose.
pc_edges = [(focal, 1 + k) for k in range(6)]   # 6 spokes only


def draw_knn_edges(ax, edge_lw=2.6, edge_col=EDGE_GREY):
    for a, b in pc_edges:
        ax.plot([verts[a, 0], verts[b, 0]], [verts[a, 1], verts[b, 1]],
                color=edge_col, lw=edge_lw, zorder=3)


def build_knn_graph(ax):
    draw_knn_edges(ax)
    draw_vertices(ax)


def build_heat_weights(ax):
    draw_knn_edges(ax)
    # Highlight focal–j edge in red.
    ax.plot([verts[focal, 0], verts[j, 0]],
            [verts[focal, 1], verts[j, 1]],
            color=RED, lw=3.6, zorder=5)
    # Ring vertices in black (no stroke), focal in red (bigger, no stroke).
    ax.scatter(verts[1:, 0], verts[1:, 1], s=POINT_SIZE, color=DARK,
               linewidths=0, zorder=6)
    ax.scatter([verts[focal, 0]], [verts[focal, 1]], s=FOCAL_SIZE,
               color=RED, linewidths=0, zorder=10)
    ax.scatter([verts[j, 0]], [verts[j, 1]], s=POINT_SIZE, color=DARK,
               linewidths=0, zorder=10)
    ij = verts[j] - verts[focal]
    ij_unit = ij / np.linalg.norm(ij)
    perp = np.array([-ij_unit[1], ij_unit[0]])
    ax.text(*(verts[focal] + 0.22 * perp), r"$i$",
            fontsize=30, fontweight="bold", color=RED,
            ha="center", va="center", zorder=12)
    ax.text(*(verts[j] + 0.24 * ij_unit), r"$j$",
            fontsize=30, fontweight="bold", color=DARK,
            ha="center", va="center", zorder=12)
    mid_ij = 0.5 * (verts[focal] + verts[j])
    # W_ij below the red edge — far enough that it doesn't touch the edge.
    ax.text(*(mid_ij - 0.24 * perp), r"$W_{ij}$",
            fontsize=30, color=RED,
            ha="center", va="center", fontweight="bold", zorder=12)
    ax.text(*(verts[focal] - 0.32 * perp), r"$D_{ii}$",
            fontsize=30, color=AMBER,
            ha="center", va="center", fontweight="bold", zorder=12)


render_share("pipeline_knn_graph", build_knn_graph)
render_share("pipeline_heat_weights", build_heat_weights)


# All five pipeline images share the same canvas, so to keep them visually
# aligned across the slide we crop them ALL to the union of their alpha
# bounding boxes (i.e. the tightest box that fits the most-extensive image,
# which is pipeline_voronoi_cot). This removes the transparent padding
# without losing the per-image alignment.
_pipeline_names = [
    "pipeline_vertices",
    "pipeline_triangulation",
    "pipeline_voronoi_cot",
    "pipeline_knn_graph",
    "pipeline_heat_weights",
]
_bboxes = []
for _n in _pipeline_names:
    _im = Image.open(OUT_DIR / f"{_n}.png")
    _b = _im.getchannel("A").getbbox()
    if _b is not None:
        _bboxes.append(_b)
if _bboxes:
    _union = (
        min(b[0] for b in _bboxes),
        min(b[1] for b in _bboxes),
        max(b[2] for b in _bboxes),
        max(b[3] for b in _bboxes),
    )
    for _n in _pipeline_names:
        _p = OUT_DIR / f"{_n}.png"
        Image.open(_p).crop(_union).save(_p)
    print(f"[ok] cropped all 5 pipeline pngs to {_union}")
