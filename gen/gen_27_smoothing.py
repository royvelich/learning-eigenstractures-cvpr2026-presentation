"""Mesh smoothing / curvature flow — Laplacian of the coordinates.

Delta X = 2 H N : applying the Laplace-Beltrami operator to the coordinate
functions yields the mean-curvature vector. Smoothing diffuses the coordinates,
  dX/dt = -Delta X = -2 H N   (mean-curvature flow).

Outputs (public/applications/):
  smooth_intuition.png   1-D cross-section: position minus neighbour-average
  smooth_curv.png        bumpy sphere coloured by mean curvature (= |Delta X|)
  smooth_flow.gif        implicit mean-curvature flow smoothing the bumpy sphere
"""
from _common import MPZ14, load_mesh
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
import igl
import trimesh

plt.rcParams["mathtext.fontset"] = "cm"

OUT = __import__("_common").OUT_DIR
SPHERE = MPZ14 / "bumpy_sphere.obj"
INDIGO, TEAL, RED, GRAY, FG = "#4E4376", "#2B5876", "#b91c1c", "#94a3b8", "#0f172a"


def mean_curv_signed(V, F):
    """Signed mean curvature per vertex (H>0 convex), via cotan/mass + normals."""
    L = igl.cotmatrix(V, F)                                  # div grad (neg. s.d.)
    M = igl.massmatrix(V, F, igl.MASSMATRIX_TYPE_VORONOI)
    HN = sp.diags(1.0 / np.asarray(M.diagonal())) @ (L @ V)  # = -2 H N
    n = trimesh.Trimesh(V, F, process=False).vertex_normals
    return -0.5 * np.sum(HN * n, axis=1)


def faces_pv(F):
    return np.hstack([np.full((len(F), 1), 3, np.int64), F.astype(np.int64)]).ravel()


# ===========================================================================
def build_intuition():
    """1-D schematic: Delta X = position - average of neighbours."""
    x = np.linspace(-3.4, 3.4, 700)
    f = 0.6 * np.exp(-((x - 1.4) / 0.5) ** 2) + 0.05 * x      # a bump + gentle slope
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.plot(x, f, color=INDIGO, lw=3, zorder=2)

    def fval(xx):
        return np.interp(xx, x, f)

    for x0, h, col, lbl, on_bump in [(1.4, 0.7, RED, r"$\Delta x \propto 2H\,N$", True),
                                     (-2.2, 0.7, TEAL, r"$\Delta x \approx 0$", False)]:
        xn = np.array([x0 - h, x0 + h])
        yn = fval(xn)
        avg = yn.mean()
        p = fval(x0)
        ax.plot(xn, yn, "--", color=GRAY, lw=1.6, zorder=3)
        ax.scatter(xn, yn, color=GRAY, s=40, zorder=4)
        ax.scatter([x0], [avg], color=GRAY, s=46, zorder=4)              # neighbour avg
        ax.scatter([x0], [p], color=col, s=110, zorder=5)               # the point p
        if on_bump:
            ax.annotate("", xy=(x0, p), xytext=(x0, avg),
                        arrowprops=dict(arrowstyle="-|>", color=col, lw=2.6), zorder=4)
            ax.text(x0 + 0.18, (p + avg) / 2, lbl, color=col, fontsize=14, va="center")
            ax.text(x0, p + 0.12, "point $p$", color=col, fontsize=11, ha="center")
            ax.text(x0 + 0.05, avg - 0.13, "avg. of neighbours", color=GRAY,
                    fontsize=10, ha="center", va="top")
        else:
            ax.text(x0, p - 0.16, lbl, color=col, fontsize=14, ha="center", va="top")

    ax.set_title(r"$\Delta x \;=\;$ point $-$ average of its neighbours",
                 fontsize=14, color=FG)
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(f.min() - 0.5, f.max() + 0.5)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(str(OUT / "smooth_intuition.png"), dpi=150, transparent=True,
                bbox_inches="tight", pad_inches=0.05)
    plt.close()
    print("[ok] smooth_intuition.png")


# ===========================================================================
def _render_sphere(V, F, scal, clim, out, crop_box=None, window=(820, 820)):
    import pyvista as pv
    from PIL import Image
    pv.global_theme.transparent_background = True
    p = pv.Plotter(off_screen=True, window_size=window)
    p.set_background("white")
    m = pv.PolyData(V, faces_pv(F))
    m["s"] = scal
    p.add_mesh(m, scalars="s", cmap="coolwarm", clim=clim, smooth_shading=True,
               show_scalar_bar=False, ambient=0.3, diffuse=0.72,
               specular=0.2, specular_power=18)
    p.camera_position = [(1.0, 0.3, 0.0), (0, 0, 0), (0, 1, 0)]
    p.reset_camera()
    p.camera.zoom(1.4)
    p.enable_anti_aliasing("ssaa")
    arr = p.screenshot(transparent_background=False, return_img=True)
    p.close()
    return arr


def build_curvature():
    from PIL import Image
    V, F = load_mesh(SPHERE)
    H = mean_curv_signed(V, F)
    cap = float(np.percentile(np.abs(H - np.median(H)), 96))
    med = float(np.median(H))
    arr = _render_sphere(V, F, H, (med - cap, med + cap), None)
    # tight crop to non-white
    mask = (arr[:, :, :3] < 245).any(2)
    ys, xs = np.where(mask)
    Image.fromarray(arr[ys.min():ys.max()+1, xs.min():xs.max()+1]).save(
        str(OUT / "smooth_curv.png"))
    print("[ok] smooth_curv.png")


# ===========================================================================
def build_flow_gif(n_steps=20, tau=6e-4, every=1, out_name="smooth_flow.gif"):
    from PIL import Image
    V0, F = load_mesh(SPHERE)
    # implicit mean-curvature flow, recomputing L,M each step (true MCF)
    Vc = V0.copy()
    seq = [Vc.copy()]
    for _ in range(n_steps):
        L = igl.cotmatrix(Vc, F)
        M = igl.massmatrix(Vc, F, igl.MASSMATRIX_TYPE_VORONOI)
        A = (M - tau * L).tocsc()
        Vc = spla.spsolve(A, M @ Vc)
        seq.append(Vc.copy())
    sel = seq[::every]

    # fixed colour scale from the initial curvature
    H0 = mean_curv_signed(V0, F)
    cap = float(np.percentile(np.abs(H0 - np.median(H0)), 96))
    med = float(np.median(H0))

    def normalize(V):
        Vc = V - V.mean(0)
        return Vc / np.sqrt((Vc ** 2).sum(1).mean())          # unit RMS radius

    raw = []
    for V in sel:
        Vn = normalize(V)
        H = mean_curv_signed(Vn, F)
        raw.append(_render_sphere(Vn, F, H, (med - cap, med + cap), None, window=(680, 680)))

    # common content-box crop so the sphere stays put
    def box(a):
        mk = (a[:, :, :3] < 245).any(2)
        ys, xs = np.where(mk)
        return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    bs = [box(a) for a in raw]
    pad = 6
    x0 = max(min(b[0] for b in bs) - pad, 0); y0 = max(min(b[1] for b in bs) - pad, 0)
    x1 = min(max(b[2] for b in bs) + pad, raw[0].shape[1])
    y1 = min(max(b[3] for b in bs) + pad, raw[0].shape[0])
    imgs = [Image.fromarray(a[y0:y1, x0:x1]).convert("P", palette=Image.ADAPTIVE, colors=128)
            for a in raw]
    # hold the last (smooth) frame a bit before looping
    imgs[0].save(str(OUT / out_name), save_all=True, append_images=imgs[1:],
                 loop=0, duration=[90] * (len(imgs) - 1) + [1200], disposal=2, optimize=True)
    print(f"[ok] {out_name}  ({len(imgs)} frames)")


if __name__ == "__main__":
    build_intuition()
    build_curvature()
    build_flow_gif()
