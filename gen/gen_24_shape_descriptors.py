"""Shape descriptors via the Heat Kernel Signature (HKS).

The HKS is built straight from the LBO eigenbasis:
    h(x, t) = sum_k exp(-lambda_k t) * phi_k(x)^2          (heat retained at x)
and the heat kernel that drives the intuition is
    k_t(p, x) = sum_k exp(-lambda_k t) * phi_k(p) * phi_k(x).

Three-slide arc:
  (1) intuition  — drop heat at a point, watch it diffuse, read off the curve
  (2) few -> all — signatures at a few points, then the field over every vertex
  (3) payoff     — 3-scale RGB descriptor matches across two poses (near-isometry)

Outputs (public/applications/):
  desc_diffuse_{0..4}.png   heat spreading from a source point
  desc_curve_one.png        HKS curve at the source point (with t-markers)
  desc_points.png           the chosen points marked on the horse
  desc_curves3.png          HKS curves for the chosen points
  desc_field.png            HKS field over all vertices (one scale)
  desc_rgb_a.png / _b.png   3-scale RGB descriptor on two poses
"""
from _common import OUT_DIR, DEFTRANSFER, load_mesh, cotangent_laplacian
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
from matplotlib import colors

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
TEAL = "#2B5876"
RED = "#b91c1c"
GREEN = "#047857"
FG = "#0f172a"
GRAY = "#94a3b8"

HEAT = "inferno"
FIELD = "viridis"

POSE_A = DEFTRANSFER / "horse-gallop" / "horse-gallop-03.obj"
POSE_B = DEFTRANSFER / "horse-gallop" / "horse-gallop-20.obj"


def lbo_eigs_sparse(L, M, k):
    """Smallest-k generalized eigenpairs via shift-invert; M-orthonormal Phi."""
    L = L.tocsc(); M = M.tocsc()
    if L.diagonal().mean() < 0:
        L = -L
    md = np.asarray(M.diagonal()).clip(min=1e-12)
    Misq = sp.diags(1.0 / np.sqrt(md))
    S = (Misq @ L @ Misq).tocsc()
    S = 0.5 * (S + S.T)
    vals, vecs = spla.eigsh(S, k=k, sigma=0.0, which="LM")
    vecs = Misq @ vecs
    order = np.argsort(vals)
    return vals[order], vecs[:, order], md


def faces_pv(F):
    return np.hstack([np.full((len(F), 1), 3, np.int64), F.astype(np.int64)]).ravel()


def set_side(p, V):
    """Clean side view: camera on +x, up = +y."""
    p.camera_position = [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.reset_camera()
    p.camera.zoom(1.4)
    p.enable_anti_aliasing("msaa")


def hks_scales(lam, n):
    lo = lam[1] if lam[1] > 1e-9 else lam[lam > 1e-9][0]
    hi = lam[-1]
    tmin = 4 * np.log(10) / hi
    tmax = 4 * np.log(10) / lo
    return np.geomspace(tmin, tmax, n)


# ---------------------------------------------------------------------------
def landmarks(V):
    """Pick a few salient vertices by geometric extremes (side view friendly)."""
    z, y, x = V[:, 2], V[:, 1], V[:, 0]
    return {
        "nose":  int(np.argmax(z + 0.3 * y)),     # head / muzzle
        "hoof":  int(np.argmin(y)),               # a hoof (lowest)
        "tail":  int(np.argmin(z)),               # tail tip
        "back":  int(np.argmax(y - 0.2 * abs(z))),  # top of the back
    }


def render_field(V, F, scal, cmap, clim, out, rgb=False, pts=None, pcols=None):
    import pyvista as pv
    from PIL import Image
    pv.global_theme.transparent_background = True
    p = pv.Plotter(off_screen=True, window_size=(900, 560))
    p.set_background([1, 1, 1, 0])
    m = pv.PolyData(V, faces_pv(F))
    if rgb:
        m["rgb"] = scal
        p.add_mesh(m, scalars="rgb", rgb=True, smooth_shading=True,
                   ambient=0.35, diffuse=0.7, specular=0.15)
    else:
        m["s"] = scal
        p.add_mesh(m, scalars="s", cmap=cmap, clim=clim, smooth_shading=True,
                   show_scalar_bar=False, ambient=0.3, diffuse=0.72,
                   specular=0.18, specular_power=15)
    if pts is not None:
        for i, c in zip(pts, pcols):
            p.add_mesh(pv.Sphere(radius=0.022, center=V[i]), color=c)
    set_side(p, V)
    p.screenshot(out, transparent_background=True, return_img=False)
    p.close()
    im = Image.open(out)
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im.crop(bbox).save(out)


# ===========================================================================
def build():
    V, F = load_mesh(POSE_A)
    L, M = cotangent_laplacian(V, F)
    lam, Phi, md = lbo_eigs_sparse(L, M, k=150)
    lm = landmarks(V)
    print("landmarks", lm)

    ts = hks_scales(lam, 6)
    src = lm["nose"]

    # ---- (1) heat diffusion frames from a delta at the source ------------
    diff_ts = np.geomspace(ts[0] * 0.6, ts[-1] * 0.5, 5)
    e = np.exp(-np.outer(diff_ts, lam))                    # (5, K)
    U = (e * Phi[src]) @ Phi.T                             # (5, nV)
    for j in range(5):
        u = U[j]
        clim = (0.0, float(np.percentile(u, 99.5)))
        render_field(V, F, u, HEAT, clim, str(OUT_DIR / f"desc_diffuse_{j}.png"),
                     pts=[src], pcols=["#39ff14"])
        print(f"[ok] desc_diffuse_{j}.png")

    # ---- HKS curves ------------------------------------------------------
    # dense curve spanning the marker range so the markers lie exactly on it
    tfine = np.geomspace(diff_ts[0], diff_ts[-1], 200)
    hfine = np.einsum("tk,nk->tn", np.exp(-np.outer(tfine, lam)), Phi ** 2)
    # marker y-values evaluated exactly on the HKS function (not interpolated)
    mark_y = np.exp(-np.outer(diff_ts, lam)) @ (Phi[src] ** 2)

    fig, ax = plt.subplots(figsize=(6.6, 4.2))
    ax.plot(tfine, hfine[:, src], color=TEAL, lw=3)
    ax.scatter(diff_ts, mark_y, color="#39ff14", edgecolor=FG, zorder=5, s=55)
    ax.set_xscale("log")
    ax.set_xlabel("$t$  (log scale)", fontsize=13)
    ax.set_ylabel(r"$h(p,t)=\sum_k e^{-\lambda_k t}\varphi_k(p)^2$", fontsize=13)
    ax.set_title("Heat retained at $p$ — its signature", fontsize=14, color=FG)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / "desc_curve_one.png"), dpi=150, transparent=True,
                bbox_inches="tight", pad_inches=0.06)
    plt.close()
    print("[ok] desc_curve_one.png")

    # ---- (2) few points: marked + their curves + field -------------------
    pts = [lm["nose"], lm["hoof"], lm["tail"]]
    pcols = [RED, GREEN, INDIGO]
    # flat light-grey body with the three points marked
    render_field(V, F, np.zeros(len(V)), "Greys", (-1, 1),
                 str(OUT_DIR / "desc_points.png"), pts=pts, pcols=pcols)
    print("[ok] desc_points.png")

    # the scale at which the shape is painted (slide 15 field)
    tmid = ts[len(ts) // 2]

    def plot_curves3(with_line, out):
        fig, ax = plt.subplots(figsize=(6.6, 4.2))
        for i, c, lbl in zip(pts, pcols, ["nose", "hoof", "tail"]):
            ax.plot(tfine, hfine[:, i], color=c, lw=3, label=lbl)
        if with_line:
            # vertical line at the single scale shown on the shape, with the
            # value each curve takes there (= the colour painted on that point)
            ax.axvline(tmid, color=GRAY, ls="--", lw=1.6, zorder=1)
            for i, c in zip(pts, pcols):
                yv = float(np.exp(-tmid * lam) @ (Phi[i] ** 2))
                ax.scatter([tmid], [yv], color=c, edgecolor=FG, zorder=6, s=55)
            ax.annotate(r"$t^\star$ (shown on shape)", xy=(tmid, ax.get_ylim()[1]),
                        xytext=(0, -2), textcoords="offset points",
                        ha="center", va="top", fontsize=12, color=FG)
        ax.set_xscale("log")
        ax.set_xlabel("$t$  (log scale)", fontsize=13)
        ax.set_ylabel("$h(x,t)$", fontsize=13)
        ax.set_title("Each point → a distinct signature", fontsize=14, color=FG)
        ax.legend(frameon=False, fontsize=12)
        ax.spines[["top", "right"]].set_visible(False)
        plt.tight_layout()
        plt.savefig(str(OUT_DIR / out), dpi=150, transparent=True,
                    bbox_inches="tight", pad_inches=0.06)
        plt.close()
        print(f"[ok] {out}")

    plot_curves3(False, "desc_curves3.png")           # curves only
    plot_curves3(True, "desc_curves3_tstar.png")      # + t* line (with field)

    # field at the same mid scale over every vertex
    field = np.exp(-tmid * lam) @ (Phi ** 2).T
    clim = (float(np.percentile(field, 2)), float(np.percentile(field, 98)))
    render_field(V, F, field, FIELD, clim, str(OUT_DIR / "desc_field.png"))
    print("[ok] desc_field.png")

    # ---- (3) RGB 3-scale descriptor across two poses ---------------------
    t3 = ts[[1, 3, 5]]

    def rgb_descriptor(Vp, Fp, ref_lo=None, ref_hi=None):
        Lp, Mp = cotangent_laplacian(Vp, Fp)
        lp, Php, _ = lbo_eigs_sparse(Lp, Mp, k=150)
        chans = np.stack([np.exp(-t * lp) @ (Php ** 2).T for t in t3], axis=1)  # (nV,3)
        if ref_lo is None:
            ref_lo = np.percentile(chans, 3, axis=0)
            ref_hi = np.percentile(chans, 97, axis=0)
        rgb = (chans - ref_lo) / np.clip(ref_hi - ref_lo, 1e-12, None)
        return np.clip(rgb, 0, 1), ref_lo, ref_hi

    rgbA, lo, hi = rgb_descriptor(V, F)
    render_field(V, F, rgbA, None, None, str(OUT_DIR / "desc_rgb_a.png"), rgb=True)
    print("[ok] desc_rgb_a.png")

    Vb, Fb = load_mesh(POSE_B)
    rgbB, _, _ = rgb_descriptor(Vb, Fb, lo, hi)
    render_field(Vb, Fb, rgbB, None, None, str(OUT_DIR / "desc_rgb_b.png"), rgb=True)
    print("[ok] desc_rgb_b.png")


if __name__ == "__main__":
    build()
