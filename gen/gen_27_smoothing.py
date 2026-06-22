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


CAM = [(1.0, 0.3, 0.0), (0, 0, 0), (0, 1, 0)]


def _fps(V, n, seed=0):
    idx = [seed]
    d2 = np.sum((V - V[seed]) ** 2, axis=1)
    for _ in range(n - 1):
        j = int(np.argmax(d2)); idx.append(j)
        d2 = np.minimum(d2, np.sum((V - V[j]) ** 2, axis=1))
    return np.array(idx)


def _sphere_arr(V, F, scal=None, clim=None, arrows=None, window=(760, 760)):
    import pyvista as pv
    pv.global_theme.transparent_background = True
    p = pv.Plotter(off_screen=True, window_size=window)
    p.set_background("white")
    m = pv.PolyData(V, faces_pv(F))
    if scal is None:
        p.add_mesh(m, color="#cbd0d6", smooth_shading=True,
                   ambient=0.3, diffuse=0.72, specular=0.2, specular_power=18)
    else:
        m["s"] = scal
        p.add_mesh(m, scalars="s", cmap="coolwarm", clim=clim, smooth_shading=True,
                   show_scalar_bar=False, ambient=0.3, diffuse=0.72,
                   specular=0.2, specular_power=18)
    if arrows is not None:
        pts, vec = arrows
        p.add_arrows(pts, vec, mag=1.0, color="#0f172a")
    p.camera_position = CAM
    p.reset_camera()
    p.camera.zoom(1.35)
    p.enable_anti_aliasing("ssaa")
    arr = p.screenshot(transparent_background=False, return_img=True)
    p.close()
    return arr


def _save_crop(arr, out, box=None):
    from PIL import Image
    if box is None:
        mask = (arr[:, :, :3] < 245).any(2)
        ys, xs = np.where(mask)
        box = (xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)
    Image.fromarray(arr[box[1]:box[3], box[0]:box[2]]).save(str(out))
    return box


def build_coord_decomposition():
    V, F = load_mesh(SPHERE)
    L = igl.cotmatrix(V, F)
    M = igl.massmatrix(V, F, igl.MASSMATRIX_TYPE_VORONOI)
    minv = 1.0 / np.asarray(M.diagonal())
    LX = minv[:, None] * (L @ V)              # = ΔX (igl sign: -2 H N)
    vec = -LX                                  # = 2 H N  (deck PSD convention)
    n = trimesh.Trimesh(V, F, process=False).vertex_normals
    H = 0.5 * np.sum(vec * n, axis=1)          # signed mean curvature

    # plain + coordinate fields + laplacian fields (identical geometry → same box)
    _save_crop(_sphere_arr(V, F), OUT / "smooth_sph_plain.png")
    names = ["x", "y", "z"]
    for i, nm in enumerate(names):
        cap = float(np.abs(V[:, i]).max())
        _save_crop(_sphere_arr(V, F, V[:, i], (-cap, cap)),
                   OUT / f"smooth_sph_{nm}.png")
        capL = float(np.percentile(np.abs(LX[:, i]), 96))
        _save_crop(_sphere_arr(V, F, LX[:, i], (-capL, capL)),
                   OUT / f"smooth_sph_l{nm}.png")
    print("[ok] smooth_sph_plain / _x/_y/_z / _lx/_ly/_lz.png")

    # merged: H-coloured sphere with mean-curvature vectors at sampled points
    sample = _fps(V, 90)
    vmag = np.linalg.norm(vec, axis=1)
    # clamp arrow length so a few high-curvature bumps don't dominate
    clamp = np.percentile(vmag[sample], 80)
    vclamp = vec * np.minimum(1.0, clamp / np.maximum(vmag, 1e-9))[:, None]
    factor = 0.07 / np.median(vmag[sample])
    cap = float(np.percentile(np.abs(H - np.median(H)), 96))
    med = float(np.median(H))
    arr = _sphere_arr(V, F, H, (med - cap, med + cap),
                      arrows=(V[sample] + n[sample] * 0.004, vclamp[sample] * factor))
    _save_crop(arr, OUT / "smooth_sph_Hvec.png")
    print("[ok] smooth_sph_Hvec.png")


def build_Hvec_gif(n_frames=90, out_name="smooth_sph_Hvec.gif"):
    """Rotating turntable of the H-coloured sphere with mean-curvature arrows."""
    import pyvista as pv
    from PIL import Image

    V, F = load_mesh(SPHERE)
    L = igl.cotmatrix(V, F)
    M = igl.massmatrix(V, F, igl.MASSMATRIX_TYPE_VORONOI)
    md = np.asarray(M.diagonal())
    V = V - (md[:, None] * V).sum(0) / md.sum()      # area-weighted centre of mass
    minv = 1.0 / md
    vec = -(minv[:, None] * (L @ V))                 # 2 H N  (L kills the shift)
    n = trimesh.Trimesh(V, F, process=False).vertex_normals
    H = 0.5 * np.sum(vec * n, axis=1)
    sample = _fps(V, 90)
    vmag = np.linalg.norm(vec, axis=1)
    clamp = np.percentile(vmag[sample], 80)
    vclamp = vec * np.minimum(1.0, clamp / np.maximum(vmag, 1e-9))[:, None]
    factor = 0.07 / np.median(vmag[sample])
    cap = float(np.percentile(np.abs(H - np.median(H)), 96))
    med = float(np.median(H))

    faces = faces_pv(F)
    psample = V[sample] + n[sample] * 0.004        # arrow bases (lifted off surface)
    vsample = vclamp[sample] * factor              # arrow vectors

    def Ry(t):
        c, s = np.cos(t), np.sin(t)
        return np.array([[c, 0, s], [0, 1.0, 0], [-s, 0, c]])

    pv.global_theme.transparent_background = True

    # one fixed camera for every frame (rotation is about the centre of mass and
    # the bounding sphere is rotation-invariant, so no per-frame reset is needed)
    p0 = pv.Plotter(off_screen=True, window_size=(600, 600))
    p0.add_mesh(pv.PolyData(V, faces))
    p0.camera_position = CAM
    p0.reset_camera()
    cam_fixed = p0.camera_position
    p0.close()

    raw = []
    for k in range(n_frames):
        R = Ry(2 * np.pi * k / n_frames).T          # rotate geometry about vertical axis
        p = pv.Plotter(off_screen=True, window_size=(600, 600))
        p.set_background("white")
        m = pv.PolyData(V @ R, faces); m["s"] = H
        p.add_mesh(m, scalars="s", cmap="coolwarm", clim=(med - cap, med + cap),
                   smooth_shading=True, show_scalar_bar=False, ambient=0.3,
                   diffuse=0.72, specular=0.2, specular_power=18)
        p.add_arrows(psample @ R, vsample @ R, mag=1.0, color="#0f172a")
        p.camera_position = cam_fixed
        p.camera.zoom(1.0)
        p.enable_anti_aliasing("ssaa")
        raw.append(p.screenshot(transparent_background=False, return_img=True))
        p.close()

    def box(a):
        mk = (a[:, :, :3] < 245).any(2)
        ys, xs = np.where(mk)
        return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1
    bs = [box(a) for a in raw]
    pad = 6
    x0 = max(min(b[0] for b in bs) - pad, 0); y0 = max(min(b[1] for b in bs) - pad, 0)
    x1 = min(max(b[2] for b in bs) + pad, raw[0].shape[1])
    y1 = min(max(b[3] for b in bs) + pad, raw[0].shape[0])
    imgs = [Image.fromarray(a[y0:y1, x0:x1]).convert("P", palette=Image.ADAPTIVE, colors=96)
            for a in raw]
    imgs[0].save(str(OUT / out_name), save_all=True, append_images=imgs[1:],
                 loop=0, duration=70, disposal=2, optimize=True)
    print(f"[ok] {out_name}  ({len(imgs)} frames)")


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
def build_flow_gif(n_steps=75, tau=2e-5, every=1, out_name="smooth_flow.gif"):
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
        raw.append(_render_sphere(Vn, F, H, (med - cap, med + cap), None, window=(600, 600)))

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
    imgs = [Image.fromarray(a[y0:y1, x0:x1]).convert("P", palette=Image.ADAPTIVE, colors=96)
            for a in raw]
    # hold the last (smooth) frame a bit before looping
    imgs[0].save(str(OUT / out_name), save_all=True, append_images=imgs[1:],
                 loop=0, duration=[70] * (len(imgs) - 1) + [1200], disposal=2, optimize=True)
    print(f"[ok] {out_name}  ({len(imgs)} frames)")


if __name__ == "__main__":
    build_intuition()
    build_curvature()
    build_flow_gif()
