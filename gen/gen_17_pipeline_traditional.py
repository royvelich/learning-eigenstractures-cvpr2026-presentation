"""Two figures for the 'Traditional pipeline' slide:

  pipeline_triangulation.png   — a regular interior vertex of a triangle
                                 mesh: six triangles around a single point.
  pipeline_voronoi_cot.png     — the same 1-ring with the Voronoi cell
                                 shaded (M_ii) and the cotangent angles
                                 (α, β) labelled on one edge ij (S_ij).
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
EDGE_GREY = "#334155"
AMBER = "#b45309"
CELL_FILL = "#fef3c7"   # amber-100

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


def draw_vertices(ax, pt_size=120):
    ax.scatter(verts[:, 0], verts[:, 1], s=pt_size, color=DARK,
               edgecolors="white", linewidths=2.0, zorder=6)


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

def draw_arc_label(ax, k, sym, col, r=0.24, label_off=0.18):
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
    ax.text(pl[0], pl[1], sym, fontsize=22, color=col,
            ha="center", va="center", zorder=12, fontweight="bold")


def build_voronoi_cot(ax):
    # Shaded Voronoi cell (background)
    ax.add_patch(Polygon(cell, closed=True, facecolor=CELL_FILL,
                         edgecolor=AMBER, lw=2.2, alpha=0.92, zorder=2))
    # Same mesh as the triangulation figure — shared draw_one_ring()
    draw_one_ring(ax)
    # Highlight edge (i, j)
    ax.plot([verts[focal, 0], verts[j, 0]],
            [verts[focal, 1], verts[j, 1]],
            color=INDIGO, lw=3.6, zorder=5)
    # Re-draw focal & j on top
    ax.scatter([verts[focal, 0]], [verts[focal, 1]], s=170, color=DARK,
               edgecolors="white", linewidths=2.6, zorder=10)
    ax.scatter([verts[j, 0]], [verts[j, 1]], s=140, color=INDIGO,
               edgecolors="white", linewidths=2.4, zorder=10)
    # i / j vertex labels — offset i perpendicular to ij so it doesn't
    # sit on the edge; j outward along ij past the j vertex.
    ij = verts[j] - verts[focal]
    ij_unit = ij / np.linalg.norm(ij)
    perp = np.array([-ij_unit[1], ij_unit[0]])   # 90° ccw
    i_label_pos = verts[focal] + 0.22 * perp
    j_label_pos = verts[j] + 0.24 * ij_unit
    ax.text(i_label_pos[0], i_label_pos[1], r"$i$",
            fontsize=22, fontweight="bold", color=DARK,
            ha="center", va="center", zorder=12)
    ax.text(j_label_pos[0], j_label_pos[1], r"$j$",
            fontsize=22, fontweight="bold", color=INDIGO,
            ha="center", va="center", zorder=12)
    # α / β arc labels on the two opposite vertices
    draw_arc_label(ax, k_alpha, r"$\alpha$", TEAL)
    draw_arc_label(ax, k_beta, r"$\beta$", TEAL)
    # M_ii label inside the cell — place it OPPOSITE the i label across the
    # focal point so the two never collide.
    m_pos = verts[focal] - 0.32 * perp
    ax.text(m_pos[0], m_pos[1], r"$M_{ii}$", fontsize=22, color=AMBER,
            ha="center", va="center", fontweight="bold", zorder=12)


render_share("pipeline_voronoi_cot", build_voronoi_cot)
