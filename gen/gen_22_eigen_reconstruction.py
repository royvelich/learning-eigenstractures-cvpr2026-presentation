"""Eigen-reconstruction animation frames — one idea, three domains.

For each domain we approximate a fixed target signal f by its truncated
eigen-expansion  f_K = sum_{k<K} <f, phi_k> phi_k  and watch the residual
shrink as K grows along a shared ladder [1, 2, 4, 8, 16, 32].

Each frame is a 3-panel composite  TARGET | RECONSTRUCTION | RESIDUAL  with
the term count K and the relative error baked in, so the slide just swaps the
PNG by click index.

Outputs (public/applications/):
  eigrec_1d_{i}.png   i = 0..5   (1-D interval, cosine basis)
  eigrec_2d_{i}.png   i = 0..5   (2-D square, cosine-product basis)
  eigrec_3d_{i}.png   i = 0..5   (armadillo surface, LBO eigenbasis)
"""
from _common import OUT_DIR, MPZ14, load_mesh, cotangent_laplacian, lbo_eigs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors

plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern — the LaTeX look

trapz = getattr(np, "trapezoid", None) or np.trapz  # numpy>=2 renamed trapz

LADDER = [1, 2, 4, 8, 16, 32]

INDIGO = "#4E4376"
TEAL = "#2B5876"
RED = "#b91c1c"
BLUE = "#1d4ed8"
GRAY = "#94a3b8"
FG = "#0f172a"

VIRIDIS = "viridis"
DIVERGE = "coolwarm"


def panel_title(ax, txt, color=FG):
    ax.set_title(txt, fontsize=13, color=color, pad=8)


# ===========================================================================
# 1-D : interval [0, pi], Neumann cosine eigenbasis  phi_k ∝ cos(k x)
# ===========================================================================
def gen_1d():
    n = 800
    x = np.linspace(0.0, np.pi, n)

    # target: a localized bump and a softer dip — smooth but multi-scale
    f = (np.exp(-((x - 0.95) / 0.30) ** 2)
         - 0.65 * np.exp(-((x - 2.25) / 0.55) ** 2)
         + 0.18 * np.cos(3 * x))
    f = f - 0.0

    # orthonormal cosine eigenbasis on [0, pi]
    KMAX = max(LADDER)
    phi = np.zeros((KMAX, n))
    phi[0] = 1.0 / np.sqrt(np.pi)
    for k in range(1, KMAX):
        phi[k] = np.sqrt(2.0 / np.pi) * np.cos(k * x)
    coeff = np.array([trapz(f * phi[k], x) for k in range(KMAX)])

    ymin, ymax = f.min() - 0.25, f.max() + 0.25

    for i, K in enumerate(LADDER):
        rec = coeff[:K] @ phi[:K]
        res = f - rec
        rel = np.sqrt(trapz(res ** 2, x) / trapz(f ** 2, x))

        fig, axes = plt.subplots(1, 3, figsize=(13.0, 3.5))

        ax = axes[0]
        ax.plot(x, f, color=INDIGO, lw=3.0)
        panel_title(ax, r"Target  $f$", INDIGO)

        ax = axes[1]
        ax.plot(x, f, color=GRAY, lw=1.6, ls="--", alpha=0.8)
        ax.plot(x, rec, color=TEAL, lw=3.0)
        panel_title(ax, rf"Reconstruction  $f_K,\ K={K}$", TEAL)

        ax = axes[2]
        ax.axhline(0, color=GRAY, lw=1.0)
        ax.fill_between(x, res, 0, where=res >= 0, color=BLUE, alpha=0.30)
        ax.fill_between(x, res, 0, where=res < 0, color=RED, alpha=0.30)
        ax.plot(x, res, color=FG, lw=2.0)
        panel_title(ax, rf"Residual  ·  rel. error ${rel*100:.0f}\%$", RED)

        for ax in axes:
            ax.set_xlim(0, np.pi)
            ax.set_ylim(ymin, ymax)
            ax.axis("off")

        plt.tight_layout()
        out = OUT_DIR / f"eigrec_1d_{i}.png"
        plt.savefig(str(out), dpi=150, transparent=True,
                    bbox_inches="tight", pad_inches=0.06)
        plt.close()
        print(f"[ok] {out.name}  (K={K}, rel={rel:.3f})")


# ===========================================================================
# 2-D : unit square, cosine-product eigenbasis  cos(i pi x) cos(j pi y)
# ===========================================================================
def gen_2d():
    n = 140
    g = np.linspace(0.0, 1.0, n)
    X, Y = np.meshgrid(g, g)

    def gauss(cx, cy, s):
        return np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * s ** 2))

    f = (1.0 * gauss(0.30, 0.34, 0.13)
         - 0.75 * gauss(0.70, 0.66, 0.16)
         + 0.45 * gauss(0.72, 0.28, 0.10))

    # build cosine-product modes ordered by eigenvalue i^2 + j^2
    KMAX = max(LADDER)
    modes = []
    for i in range(0, 16):
        for j in range(0, 16):
            modes.append((i * i + j * j, i, j))
    modes.sort()
    modes = modes[:KMAX]

    cx = np.cos(np.outer(g, np.pi * np.arange(16)))   # n x 16, cos(i pi x)
    coeff, basis = [], []
    for _, i, j in modes:
        ni = 1.0 if i == 0 else np.sqrt(2.0)
        nj = 1.0 if j == 0 else np.sqrt(2.0)
        b = (ni * cx[:, i])[None, :] * (nj * cx[:, j])[:, None]  # cos(i pi x) cos(j pi y)
        c = trapz(trapz(f * b, g, axis=1), g)
        coeff.append(c)
        basis.append(b)
    coeff = np.array(coeff)
    basis = np.array(basis)

    vmax = np.abs(f).max()
    norm = colors.Normalize(vmin=-vmax, vmax=vmax)
    fro = np.sqrt((f ** 2).mean())

    for idx, K in enumerate(LADDER):
        rec = np.tensordot(coeff[:K], basis[:K], axes=(0, 0))
        res = f - rec
        rel = np.sqrt((res ** 2).mean()) / fro

        fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.4))

        axes[0].imshow(f, cmap=VIRIDIS, norm=norm, origin="lower", extent=[0, 1, 0, 1])
        panel_title(axes[0], r"Target  $f$", INDIGO)

        axes[1].imshow(rec, cmap=VIRIDIS, norm=norm, origin="lower", extent=[0, 1, 0, 1])
        panel_title(axes[1], rf"Reconstruction  $f_K,\ K={K}$", TEAL)

        rmax = max(np.abs(res).max(), 1e-9)
        axes[2].imshow(res, cmap=DIVERGE, norm=colors.Normalize(-rmax, rmax),
                       origin="lower", extent=[0, 1, 0, 1])
        panel_title(axes[2], rf"Residual  ·  rel. error ${rel*100:.0f}\%$", RED)

        for ax in axes:
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor("#cbd5e1")

        plt.tight_layout()
        out = OUT_DIR / f"eigrec_2d_{idx}.png"
        plt.savefig(str(out), dpi=150, transparent=True,
                    bbox_inches="tight", pad_inches=0.06)
        plt.close()
        print(f"[ok] {out.name}  (K={K}, rel={rel:.3f})")


# ===========================================================================
# 3-D : armadillo surface, true Laplace-Beltrami eigenbasis
# ===========================================================================
def gen_3d():
    import pyvista as pv

    V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=9000)
    V[:, 0] = -V[:, 0]; V[:, 2] = -V[:, 2]   # 180° about vertical axis → face the camera
    L, M = cotangent_laplacian(V, F)
    KMAX = max(LADDER)
    _, Phi = lbo_eigs(L, M, k=KMAX + 1)   # Phi: M-orthonormal, columns ascending

    # target signal: a few smooth Gaussian bumps in ambient space
    centres = [(np.array([0.18, 0.30, 0.10]), 1.0, 0.22),
               (np.array([-0.22, -0.05, 0.12]), -0.85, 0.20),
               (np.array([0.05, -0.28, -0.10]), 0.7, 0.20)]
    f = np.zeros(V.shape[0])
    for c, amp, sig in centres:
        d2 = np.sum((V - c) ** 2, axis=1)
        f += amp * np.exp(-d2 / (2 * sig ** 2))

    md = np.asarray(M.diagonal())
    Mf = md * f
    coeff = Phi.T @ Mf                      # c_k = phi_k^T M f
    fMf = float(f @ Mf)

    faces_pv = np.hstack(
        [np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
    clim = (float(np.percentile(f, 2)), float(np.percentile(f, 98)))

    from PIL import Image

    def render_tile(scal, cmap, cl, path):
        """Render one mesh panel to a tight-cropped transparent PNG (no text)."""
        pv.global_theme.transparent_background = True
        p = pv.Plotter(off_screen=True, window_size=(640, 620))
        p.set_background([1, 1, 1, 0])
        m = pv.PolyData(V, faces_pv)
        m["s"] = scal
        p.add_mesh(m, scalars="s", cmap=cmap, clim=cl, smooth_shading=True,
                   show_scalar_bar=False, ambient=0.32, diffuse=0.70,
                   specular=0.18, specular_power=15)
        p.camera_position = "xy"
        p.reset_camera()
        p.camera.zoom(1.25)   # keep ears/feet in frame
        p.enable_anti_aliasing("msaa")
        p.screenshot(str(path), transparent_background=True, return_img=False)
        p.close()
        im = Image.open(path)
        bbox = im.getchannel("A").getbbox()
        if bbox:
            im.crop(bbox).save(path)

    for idx, K in enumerate(LADDER):
        rec = Phi[:, :K] @ coeff[:K]
        res = f - rec
        rel = np.sqrt(float(res @ (md * res)) / fMf)
        rmax = max(np.abs(res).max(), 1e-9)

        tiles = [OUT_DIR / f"_eigrec_3d_tile_{j}.png" for j in range(3)]
        render_tile(f, VIRIDIS, clim, tiles[0])
        render_tile(rec, VIRIDIS, clim, tiles[1])
        render_tile(res, DIVERGE, (-rmax, rmax), tiles[2])

        # compose into a 1x3 row with crisp mathtext titles
        titles = [(r"Target  $f$", INDIGO),
                  (rf"Reconstruction  $f_K,\ K={K}$", TEAL),
                  (rf"Residual  ·  rel. error ${rel*100:.0f}\%$", RED)]
        fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.6))
        for ax, tile, (title, tcol) in zip(axes, tiles, titles):
            im = Image.open(tile)
            W, H = im.size
            ax.imshow(im)
            ax.set_xlim(-0.5 - 0.03 * W, W - 0.5 + 0.03 * W)
            ax.set_ylim(H - 0.5 + 0.02 * H, -0.5 - 0.10 * H)
            ax.set_title(title, fontsize=15, color=tcol, pad=8)
            ax.axis("off")
        plt.tight_layout()
        out = OUT_DIR / f"eigrec_3d_{idx}.png"
        plt.savefig(str(out), dpi=150, transparent=True, bbox_inches="tight", pad_inches=0.06)
        plt.close()
        for t in tiles:
            t.unlink(missing_ok=True)
        print(f"[ok] {out.name}  (K={K}, rel={rel:.3f})")


if __name__ == "__main__":
    gen_1d()
    gen_2d()
    gen_3d()
