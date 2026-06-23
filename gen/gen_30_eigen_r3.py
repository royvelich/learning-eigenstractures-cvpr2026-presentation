"""Warm-up: reconstruction in the eigenbasis of a 3x3 symmetric PSD operator.

A = A^T >= 0 has an orthonormal eigenbasis {v1,v2,v3}. A vector b is the sum of
its projections; keeping K terms gives a better and better approximation.

Outputs (public/applications/):
  eig_r3_k1.png, eig_r3_k2.png, eig_r3_k3.png
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

plt.rcParams["mathtext.fontset"] = "cm"

GRAY = "#94a3b8"
CRIMSON = "#e6194B"
TEAL = "#2B5876"
FG = "#0f172a"


def orthonormal_frame():
    v1 = np.array([0.82, 0.46, 0.34]); v1 /= np.linalg.norm(v1)
    t = np.array([-0.35, 0.84, 0.10])
    v2 = t - (t @ v1) * v1; v2 /= np.linalg.norm(v2)
    v3 = np.cross(v1, v2)
    return np.array([v1, v2, v3])


def arrow(ax, vec, color, lw, label=None, ls="solid"):
    ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, linewidth=lw,
              arrow_length_ratio=0.12, ls=ls)
    if label:
        p = vec * 1.12
        ax.text(p[0], p[1], p[2], label, color=color, fontsize=15)


def render(K, V, coeff, out):
    b = coeff @ V                       # target vector
    bK = coeff[:K] @ V[:K]              # K-term reconstruction
    err = np.linalg.norm(b - bK) / np.linalg.norm(b)

    fig = plt.figure(figsize=(5.6, 5.6))
    ax = fig.add_subplot(111, projection="3d")
    L = 1.25
    # faint coordinate axes
    for d in np.eye(3):
        ax.plot([-L * d[0], L * d[0]], [-L * d[1], L * d[1]],
                [-L * d[2], L * d[2]], color="#e2e8f0", lw=1, zorder=0)

    # eigenvector frame
    for i, v in enumerate(V):
        arrow(ax, v, GRAY, 1.8, rf"$v_{i+1}$")
    # the components kept so far (faint, along their eigenvectors)
    for i in range(K):
        c = coeff[i] * V[i]
        ax.plot([0, c[0]], [0, c[1]], [0, c[2]], color=TEAL, lw=3, alpha=0.35, zorder=1)

    arrow(ax, b, CRIMSON, 3.0, r"$b$")
    arrow(ax, bK, TEAL, 3.0, None)
    # residual
    ax.plot([bK[0], b[0]], [bK[1], b[1]], [bK[2], b[2]], color=CRIMSON, lw=1.8,
            ls=(0, (4, 3)), zorder=4)
    ax.text(bK[0] - 0.05, bK[1], bK[2] - 0.12, r"$b_K$", color=TEAL, fontsize=15)

    ax.text2D(0.03, 0.95, rf"$K={K}$   ·   rel. error ${err*100:.0f}\%$",
              transform=ax.transAxes, fontsize=14, color=FG)

    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=18, azim=35)
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / out), dpi=160, transparent=True,
                bbox_inches="tight", pad_inches=0.0)
    plt.close()
    print(f"[ok] {out}  (rel err {err:.2f})")


def build():
    V = orthonormal_frame()
    coeff = np.array([1.0, 0.62, 0.34])     # decreasing → progressive improvement
    for K in (1, 2, 3):
        render(K, V, coeff, f"eig_r3_k{K}.png")


if __name__ == "__main__":
    build()
