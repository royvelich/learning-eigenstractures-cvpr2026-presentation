"""Eigenfunction galleries — the first few Laplacian eigenfunctions per domain.

One composite image per domain, showing phi_0 .. phi_5 with their eigenvalues,
to introduce each reconstruction slide.

Outputs (public/applications/):
  eigfun_1d.png   1x6 row of cos(k x) on the interval [0, pi]
  eigfun_2d.png   2x3 grid of cos(i pi x) cos(j pi y) on the unit square
  eigfun_3d.png   2x3 grid of LBO eigenfunctions on the armadillo
"""
from _common import OUT_DIR, MPZ14, load_mesh, cotangent_laplacian, lbo_eigs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern — the LaTeX look

INDIGO = "#4E4376"
TEAL = "#2B5876"
FG = "#0f172a"
DIVERGE = "RdBu_r"   # signed eigenfunctions: diverging, centred at 0


# ===========================================================================
# 1-D : phi_k(x) = cos(k x) on [0, pi],  lambda_k = k^2
# ===========================================================================
def gen_1d():
    n = 600
    x = np.linspace(0.0, np.pi, n)
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 5.2))
    for k, ax in enumerate(axes.ravel()):
        y = np.cos(k * x)
        ax.axhline(0, color="#cbd5e1", lw=1.0)
        ax.plot(x, y, color=TEAL, lw=2.8)
        ax.set_title(rf"$\varphi_{k}$,  $\lambda={k*k}$", fontsize=15, color=FG, pad=6)
        ax.set_xlim(0, np.pi)
        ax.set_ylim(-1.25, 1.25)
        ax.axis("off")
    plt.tight_layout(w_pad=3.0, h_pad=2.5)
    out = OUT_DIR / "eigfun_1d.png"
    plt.savefig(str(out), dpi=150, transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close()
    print(f"[ok] {out.name}")


# ===========================================================================
# 2-D : phi_ij = cos(i pi x) cos(j pi y) on [0,1]^2,  lambda = pi^2 (i^2+j^2)
# ===========================================================================
def gen_2d():
    n = 120
    g = np.linspace(0.0, 1.0, n)
    X, Y = np.meshgrid(g, g)
    modes = sorted([(i * i + j * j, i, j) for i in range(4) for j in range(4)])[:6]

    fig, axes = plt.subplots(2, 3, figsize=(10.5, 7.0))
    for (ev, i, j), ax in zip(modes, axes.ravel()):
        phi = np.cos(i * np.pi * X) * np.cos(j * np.pi * Y)
        ax.imshow(phi, cmap=DIVERGE, norm=colors.Normalize(-1, 1),
                  origin="lower", extent=[0, 1, 0, 1])
        ax.set_title(rf"$\varphi_{{{i}{j}}}$,  $\lambda=\pi^2\!\cdot\!{ev}$",
                     fontsize=15, color=FG, pad=6)
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#cbd5e1")
    plt.tight_layout()
    out = OUT_DIR / "eigfun_2d.png"
    plt.savefig(str(out), dpi=150, transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close()
    print(f"[ok] {out.name}")


# ===========================================================================
# 3-D : Laplace-Beltrami eigenfunctions on the armadillo surface
# ===========================================================================
def gen_3d():
    import pyvista as pv
    from PIL import Image

    V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=9000)
    V[:, 0] = -V[:, 0]; V[:, 2] = -V[:, 2]   # 180° about vertical axis → face the camera
    L, M = cotangent_laplacian(V, F)
    lam, Phi = lbo_eigs(L, M, k=6)
    faces_pv = np.hstack(
        [np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()

    # render each eigenfunction as its own tight-cropped transparent PNG
    tiles = []
    for k in range(6):
        phi = Phi[:, k].copy()
        if k == 0:
            phi[:] = 0.0          # constant mode → uniform (diverging centre)
            a = 1.0
        else:
            a = max(np.abs(phi).max(), 1e-9)
        pv.global_theme.transparent_background = True
        p = pv.Plotter(off_screen=True, window_size=(640, 640))
        p.set_background([1, 1, 1, 0])
        m = pv.PolyData(V, faces_pv)
        m["s"] = phi
        p.add_mesh(m, scalars="s", cmap=DIVERGE, clim=(-a, a), smooth_shading=True,
                   show_scalar_bar=False, ambient=0.32, diffuse=0.70,
                   specular=0.18, specular_power=15)
        p.camera_position = "xy"
        p.reset_camera()
        p.camera.zoom(1.25)   # gentle zoom — keep ears/feet inside the frame
        p.enable_anti_aliasing("msaa")
        tile = OUT_DIR / f"_eigfun_3d_tile_{k}.png"
        p.screenshot(str(tile), transparent_background=True, return_img=False)
        p.close()
        im = Image.open(tile)
        bbox = im.getchannel("A").getbbox()
        if bbox:
            im.crop(bbox).save(tile)
        tiles.append(tile)

    # compose into a 2x3 grid with crisp mathtext titles
    scale = lam[1] if lam[1] > 1e-9 else 1.0   # normalize so lambda_1 = 1
    fig, axes = plt.subplots(2, 3, figsize=(10.5, 7.6))
    for k, ax in enumerate(axes.ravel()):
        im = Image.open(tiles[k])
        W, H = im.size
        ax.imshow(im)
        # pad the cell with whitespace so the armadillo sits smaller, clear of the label
        ax.set_xlim(-0.5 - 0.04 * W, W - 0.5 + 0.04 * W)
        ax.set_ylim(H - 0.5 + 0.02 * H, -0.5 - 0.10 * H)   # extra room on top
        lab = r"$\lambda=0$" if k == 0 else rf"$\lambda={lam[k]/scale:.1f}\,\lambda_1$"
        ax.set_title(rf"$\varphi_{k}$,  {lab}", fontsize=18, color=FG, pad=8)
        ax.axis("off")
    plt.tight_layout(h_pad=2.5)
    out = OUT_DIR / "eigfun_3d.png"
    plt.savefig(str(out), dpi=150, transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close()
    for t in tiles:
        t.unlink(missing_ok=True)
    print(f"[ok] {out.name}  (lambda: {np.round(lam, 4)})")


if __name__ == "__main__":
    gen_1d()
    gen_2d()
    gen_3d()
