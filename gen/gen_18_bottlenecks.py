"""Three icon-like images for the 'unavoidable bottlenecks' slide.

  bottleneck_high_d_graph.png   — a dense, messy node-link graph, signalling
                                  the 'high-d data → graph Laplacian' heuristic
                                  that has no clean 2-manifold structure.
  bottleneck_no_grad.png        — a back-prop chain crossed out, signalling
                                  the eigensolver is not differentiable.

The intrinsic-dimension-2 panel reuses pipeline_triangulation.png from
gen_17 (a regular interior vertex with its 1-ring), so no new image is
generated for it here.
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

plt.rcParams["mathtext.fontset"] = "cm"

DARK = "#0f172a"
INDIGO = "#4E4376"
TEAL = "#2B5876"
GREY = "#94a3b8"
EDGE_GREY = "#475569"
RED = "#b91c1c"


def save(fig, name):
    plt.savefig(OUT_DIR / f"{name}.png", dpi=220, transparent=True,
                bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    print(f"[ok] {name}.png")


# ====================================================== high-d graph
rng = np.random.default_rng(11)
N = 36
pts = rng.normal(size=(N, 2))
# pull into a roughly circular cluster
norms = np.linalg.norm(pts, axis=1)
pts = pts / norms.max() * 1.6
# kNN edges (k=4) — directed dedup
K = 4
edges = set()
for i in range(N):
    d = np.linalg.norm(pts - pts[i], axis=1)
    d[i] = np.inf
    nbrs = np.argsort(d)[:K]
    for j in nbrs:
        edges.add(tuple(sorted((i, int(j)))))

fig, ax = plt.subplots(figsize=(4.8, 4.8))
for a, b in edges:
    ax.plot([pts[a, 0], pts[b, 0]], [pts[a, 1], pts[b, 1]],
            color=EDGE_GREY, lw=1.2, alpha=0.55, zorder=2)
ax.scatter(pts[:, 0], pts[:, 1], s=80, color=INDIGO,
           edgecolors="white", linewidths=1.6, zorder=5)
ax.set_aspect("equal")
ax.set_axis_off()
m = float(np.abs(pts).max()) + 0.25
ax.set_xlim(-m, m)
ax.set_ylim(-m, m)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
save(fig, "bottleneck_high_d_graph")


# ====================================================== no gradient
# Forward chain: input → block₁ → block₂ → block₃ → loss (right-pointing arrows)
# Backward chain underneath: loss → ... → input (left-pointing arrows)
# A bold red X is drawn over the BACKWARD arrows.

fig, ax = plt.subplots(figsize=(4.8, 4.8))

n_nodes = 4
xs = np.linspace(-1.8, 1.8, n_nodes)
y_fwd = 0.55
y_bwd = -0.55
node_r = 0.28

for x in xs:
    # forward node
    ax.add_patch(plt.Circle((x, y_fwd), node_r, facecolor="white",
                            edgecolor=INDIGO, lw=2.2, zorder=4))
    # backward node (greyed out — gradient cannot pass)
    ax.add_patch(plt.Circle((x, y_bwd), node_r, facecolor="white",
                            edgecolor=GREY, lw=1.8, zorder=4))

# forward arrows
for i in range(n_nodes - 1):
    ax.add_patch(FancyArrowPatch(
        (xs[i] + node_r + 0.04, y_fwd),
        (xs[i + 1] - node_r - 0.04, y_fwd),
        arrowstyle="-|>", mutation_scale=22,
        color=INDIGO, lw=2.4, zorder=3))

# backward arrows (greyed)
for i in range(n_nodes - 1):
    ax.add_patch(FancyArrowPatch(
        (xs[i + 1] - node_r - 0.04, y_bwd),
        (xs[i] + node_r + 0.04, y_bwd),
        arrowstyle="-|>", mutation_scale=22,
        color=GREY, lw=2.2, zorder=3))

# labels for the two rows
ax.text(xs[0] - 0.55, y_fwd, r"forward", color=INDIGO,
        fontsize=14, ha="right", va="center", fontweight="bold")
ax.text(xs[0] - 0.55, y_bwd, r"$\nabla$", color=GREY,
        fontsize=22, ha="right", va="center", fontweight="bold")

# big red X across the backward row
x_lo, x_hi = xs[0] - 0.55, xs[-1] + 0.55
y_lo, y_hi = y_bwd - 0.55, y_bwd + 0.55
ax.plot([x_lo, x_hi], [y_lo, y_hi], color=RED, lw=6, zorder=8,
        solid_capstyle="round")
ax.plot([x_lo, x_hi], [y_hi, y_lo], color=RED, lw=6, zorder=8,
        solid_capstyle="round")

ax.set_aspect("equal")
ax.set_axis_off()
ax.set_xlim(-3.2, 3.0)
ax.set_ylim(-2.0, 1.6)
fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
save(fig, "bottleneck_no_grad")
