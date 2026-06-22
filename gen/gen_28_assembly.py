"""How the cotangent stiffness L and mass M are assembled (schematics).

Outputs (public/applications/):
  asm_onering.png    1-ring of vertex i with the two opposite angles a, b
  asm_row.png        row i of L: diagonal = sum of weights, off-diag = -w_ij
  asm_mass.png       barycentric vertex area A_i = M_ii
  asm_sampling.png   coarse vs fine: dividing by A_i cancels sampling density
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Polygon

plt.rcParams["mathtext.fontset"] = "cm"

I_COL = "#e6194B"      # vertex i
J_COL = "#2B5876"      # the highlighted neighbour j
NB = "#64748b"         # other neighbours
EDGE = "#94a3b8"
FILL = "#eef2f7"
HILITE = "#fde68a"
FG = "#0f172a"
WARM = "#f59e0b"
COOL = "#3b82f6"

# centre vertex i and its 1-ring (slightly irregular), ordered around i
I = np.array([0.0, 0.0])
RING = np.array([
    [1.15, 0.12],    # j0  (highlighted edge i–j0)
    [0.55, 1.05],    # j1  -> angle alpha (opposite i–j0)
    [-0.62, 0.98],   # j2
    [-1.10, -0.08],  # j3
    [-0.58, -1.02],  # j4
    [0.62, -0.98],   # j5  -> angle beta (opposite i–j0)
])


def _angle_arc(ax, V, A, B, r, color, label, lab_r=None):
    a1 = np.degrees(np.arctan2(A[1] - V[1], A[0] - V[0]))
    a2 = np.degrees(np.arctan2(B[1] - V[1], B[0] - V[0]))
    lo, hi = sorted([a1, a2])
    if hi - lo > 180:
        lo, hi = hi, lo + 360
    ax.add_patch(Arc(V, 2 * r, 2 * r, angle=0, theta1=lo, theta2=hi,
                     color=color, lw=2.4, zorder=6))
    mid = np.radians((lo + hi) / 2)
    lr = lab_r if lab_r is not None else r + 0.16
    ax.text(V[0] + lr * np.cos(mid), V[1] + lr * np.sin(mid), label,
            color=color, fontsize=17, ha="center", va="center", zorder=7)


def build_onering(with_angles=True, out="asm_onering.png"):
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    n = len(RING)
    # triangle fans (tint the two triangles on edge i–j0 only when showing angles)
    for k in range(n):
        tri = np.array([I, RING[k], RING[(k + 1) % n]])
        hot = with_angles and ((k == 0) or (k == n - 1))
        ax.add_patch(Polygon(tri, closed=True, facecolor=HILITE if hot else FILL,
                             edgecolor=EDGE, lw=1.6, zorder=1))
    # spokes + ring edges already drawn by polygons; redraw highlighted edge i–j0
    ax.plot([I[0], RING[0][0]], [I[1], RING[0][1]], color=J_COL, lw=3.5, zorder=4)

    if with_angles:
        # opposite angles: alpha at j1 (tri i,j0,j1), beta at j5 (tri i,j5,j0)
        _angle_arc(ax, RING[1], I, RING[0], 0.30, WARM, r"$\alpha_{ij}$")
        _angle_arc(ax, RING[5], RING[0], I, 0.30, COOL, r"$\beta_{ij}$")
    else:
        # generic weight label on the highlighted edge
        mid = 0.5 * (I + RING[0])
        ax.text(mid[0], mid[1] + 0.16, r"$w_{ij}$", color=J_COL, fontsize=18,
                ha="center", zorder=9)

    # vertices
    ax.scatter(*I, s=190, color=I_COL, zorder=8)
    ax.text(I[0] - 0.02, I[1] - 0.22, "$i$", color=I_COL, fontsize=20, ha="center", zorder=9)
    ax.scatter(*RING[0], s=150, color=J_COL, zorder=8)
    ax.text(RING[0][0] + 0.18, RING[0][1] + 0.02, "$j$", color=J_COL, fontsize=20, zorder=9)
    for k in [1, 2, 3, 4, 5]:
        ax.scatter(*RING[k], s=70, color=NB, zorder=8)

    ax.text(0.5 * (I[0] + RING[0][0]), 0.5 * (I[1] + RING[0][1]) - 0.17,
            "edge $ij$", color=J_COL, fontsize=12, ha="center", zorder=9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.4, 1.7); ax.set_ylim(-1.35, 1.4)
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / out), dpi=160, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close()
    print(f"[ok] {out}")


def build_row():
    """Row i of L as a strip of cells: diagonal +Σw, neighbours −w_ij, else 0."""
    cells = [("$-w_{ij_1}$", COOL), ("0", None), ("$-w_{ij_2}$", COOL),
             (r"$+\sum_j w_{ij}$", WARM), ("$-w_{ij_3}$", COOL), ("0", None),
             ("$-w_{ij_4}$", COOL)]
    fig, ax = plt.subplots(figsize=(9.2, 1.7))
    w = 1.0
    for c, (txt, col) in enumerate(cells):
        face = "#ffffff" if col is None else col
        alpha = 1.0 if col is None else 0.22
        ax.add_patch(plt.Rectangle((c * w, 0), w, 1, facecolor=(face if col is None else col),
                                   edgecolor="#cbd5e1", lw=1.4, alpha=(1 if col is None else 0.22)))
        ax.text(c * w + w / 2, 0.5, txt, ha="center", va="center", fontsize=15,
                color=(FG if col is None else col))
    diag = 3
    ax.text(diag * w + w / 2, 1.28, "diagonal", ha="center", color=WARM, fontsize=13)
    ax.annotate("", xy=(diag * w + w / 2, 1.04), xytext=(diag * w + w / 2, 1.22),
                arrowprops=dict(arrowstyle="-|>", color=WARM, lw=2))
    ax.text(0.5 * w, -0.32, "off-diagonal: one $-w_{ij}$ per neighbour", ha="left",
            color=COOL, fontsize=13)
    ax.text(len(cells) * w + 0.15, 0.5, "← row $i$ of $L$", va="center", fontsize=14, color=FG)
    ax.set_xlim(0, len(cells) * w + 2.0); ax.set_ylim(-0.6, 1.5)
    ax.set_aspect("equal"); ax.axis("off")
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / "asm_row.png"), dpi=160, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close()
    print("[ok] asm_row.png")


def build_mass():
    """Barycentric vertex area: edge midpoints + triangle centroids around i."""
    fig, ax = plt.subplots(figsize=(6.4, 6.0))
    n = len(RING)
    for k in range(n):
        tri = np.array([I, RING[k], RING[(k + 1) % n]])
        ax.add_patch(Polygon(tri, closed=True, facecolor=FILL, edgecolor=EDGE, lw=1.6, zorder=1))
    # barycentric dual cell: midpoint(i,jk) -> centroid(i,jk,j(k+1)) -> midpoint(i,j(k+1)) ...
    cell = []
    for k in range(n):
        mid = (I + RING[k]) / 2
        cen = (I + RING[k] + RING[(k + 1) % n]) / 3
        cell.append(mid); cell.append(cen)
    ax.add_patch(Polygon(np.array(cell), closed=True, facecolor="#34d399",
                         edgecolor="#059669", lw=2.2, alpha=0.45, zorder=3))
    ax.scatter(*I, s=190, color=I_COL, zorder=8)
    ax.text(I[0], I[1] - 0.24, "$i$", color=I_COL, fontsize=20, ha="center", zorder=9)
    for k in range(n):
        ax.scatter(*RING[k], s=70, color=NB, zorder=8)
    ax.text(0.18, 0.30, "$A_i = M_{ii}$", color="#047857", fontsize=18, zorder=9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_xlim(-1.4, 1.7); ax.set_ylim(-1.35, 1.4)
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / "asm_mass.png"), dpi=160, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close()
    print("[ok] asm_mass.png")


def build_sampling():
    """Coarse vs fine triangulation of the same patch; ÷A_i cancels density."""
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
    rng = np.random.default_rng(3)
    for ax, (ncol, title) in zip(axes, [(4, "coarse"), (8, "fine")]):
        xs = np.linspace(0, 1, ncol)
        X, Y = np.meshgrid(xs, xs)
        P = np.c_[X.ravel(), Y.ravel()]
        from matplotlib.tri import Triangulation
        tri = Triangulation(P[:, 0], P[:, 1])
        ax.triplot(tri, color=EDGE, lw=1.1)
        # highlight a central vertex and its cell (approx: small square)
        ci = np.argmin(np.sum((P - 0.5) ** 2, axis=1))
        h = (xs[1] - xs[0]) / 2
        ax.add_patch(plt.Rectangle((P[ci, 0] - h, P[ci, 1] - h), 2 * h, 2 * h,
                                   facecolor="#34d399", edgecolor="#059669", lw=2, alpha=0.5))
        ax.scatter(*P[ci], s=120, color=I_COL, zorder=6)
        ax.set_title(f"{title}  ·  cell area $A_i$ "
                     + ("large" if title == "coarse" else "small"),
                     fontsize=13, color=FG)
        ax.set_aspect("equal"); ax.axis("off")
    fig.suptitle(r"$(Lf)_i \propto A_i$, but $\;(M^{-1}Lf)_i = (Lf)_i / A_i\;$ is the same",
                 fontsize=15, color=FG, y=0.04)
    plt.tight_layout(rect=[0, 0.07, 1, 1])
    plt.savefig(str(OUT_DIR / "asm_sampling.png"), dpi=160, transparent=True,
                bbox_inches="tight", pad_inches=0.05)
    plt.close()
    print("[ok] asm_sampling.png")


if __name__ == "__main__":
    build_onering(with_angles=False, out="asm_onering_plain.png")
    build_onering(with_angles=True, out="asm_onering.png")
    build_row()
    build_mass()
    build_sampling()
