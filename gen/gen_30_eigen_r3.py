"""Warm-up: reconstruction in the eigenbasis of a 3x3 symmetric PSD operator.

A = A^T >= 0 has an orthonormal eigenbasis {v1,v2,v3}. A vector b is the sum of
its projections; keeping K terms gives a better and better approximation.
Rendered as slowly rotating turntable GIFs (azimuth sweep about the z-axis).

Outputs (public/applications/):
  eig_r3_k1.gif, eig_r3_k2.gif, eig_r3_k3.gif
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from PIL import Image

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


def _arrow(ax, vec, color, lw, label=None):
    ax.quiver(0, 0, 0, vec[0], vec[1], vec[2], color=color, linewidth=lw,
              arrow_length_ratio=0.12)
    if label:
        p = vec * 1.12
        ax.text(p[0], p[1], p[2], label, color=color, fontsize=15)


def draw_scene(ax, K, V, coeff, err, azim):
    L = 1.25
    for d in np.eye(3):
        ax.plot([-L * d[0], L * d[0]], [-L * d[1], L * d[1]],
                [-L * d[2], L * d[2]], color="#e2e8f0", lw=1, zorder=0)
    b = coeff @ V
    bK = coeff[:K] @ V[:K]
    for i, v in enumerate(V):
        _arrow(ax, v, GRAY, 1.8, rf"$v_{i+1}$")
    for i in range(K):
        c = coeff[i] * V[i]
        ax.plot([0, c[0]], [0, c[1]], [0, c[2]], color=TEAL, lw=3, alpha=0.35, zorder=1)
    _arrow(ax, b, CRIMSON, 3.0, r"$b$")
    _arrow(ax, bK, TEAL, 3.0, None)
    ax.plot([bK[0], b[0]], [bK[1], b[1]], [bK[2], b[2]], color=CRIMSON, lw=1.8,
            ls=(0, (4, 3)), zorder=4)
    ax.text(bK[0] - 0.05, bK[1], bK[2] - 0.12, r"$b_K$", color=TEAL, fontsize=15)
    ax.text2D(0.03, 0.97, rf"$K={K}$   ·   rel. error ${err*100:.0f}\%$",
              transform=ax.transAxes, fontsize=14, color=FG)
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
    ax.set_box_aspect([1, 1, 1])
    ax.view_init(elev=18, azim=azim)
    ax.set_axis_off()


def render_gif(K, V, coeff, out, n_frames=50, duration=110):
    b = coeff @ V
    err = np.linalg.norm(b - coeff[:K] @ V[:K]) / np.linalg.norm(b)
    raw = []
    for f in range(n_frames):
        azim = 35 + 360.0 * f / n_frames
        fig = plt.figure(figsize=(5.6, 5.6), dpi=110)
        fig.patch.set_facecolor("white")
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor("white")
        draw_scene(ax, K, V, coeff, err, azim)
        fig.canvas.draw()
        arr = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
        plt.close(fig)
        raw.append(arr)

    # common content-box crop so the plot doesn't jump as it spins
    def box(a):
        m = (a < 245).any(2)
        ys, xs = np.where(m)
        return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    bs = [box(a) for a in raw]
    pad = 8
    x0 = max(min(b_[0] for b_ in bs) - pad, 0); y0 = max(min(b_[1] for b_ in bs) - pad, 0)
    x1 = min(max(b_[2] for b_ in bs) + pad, raw[0].shape[1])
    y1 = min(max(b_[3] for b_ in bs) + pad, raw[0].shape[0])
    imgs = [Image.fromarray(a[y0:y1, x0:x1]).convert("P", palette=Image.ADAPTIVE, colors=96)
            for a in raw]
    imgs[0].save(str(OUT_DIR / out), save_all=True, append_images=imgs[1:],
                 loop=0, duration=duration, disposal=2, optimize=True)
    print(f"[ok] {out}  ({n_frames} frames, rel err {err:.2f})")


def build():
    V = orthonormal_frame()
    coeff = np.array([1.0, 0.62, 0.34])     # decreasing → progressive improvement
    for K in (1, 2, 3):
        render_gif(K, V, coeff, f"eig_r3_k{K}.gif")


if __name__ == "__main__":
    build()
