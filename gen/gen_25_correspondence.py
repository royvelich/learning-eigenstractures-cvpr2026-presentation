"""Shape correspondence via functional maps — intuition arc.

Two near-isometric horse poses (shared topology → ground-truth identity map).
We show that instead of searching over N! point matchings, a correspondence is
a small matrix C in the LBO eigenbasis:

    a = Phi_A^T M_A f          (coeffs of a function on A)
    C = Phi_B^T M_B Phi_A      (functional map, identity correspondence)
    b = C a                    (transported coeffs on B)
    g = Phi_B b                (the function, now on B)

Outputs (public/applications/):
  corr_horse_a.png / _b.png        plain grey poses (the "hard" slide)
  corr_func_a.png  / _b.png        a banded function transported A -> B
  corr_cmat.png                    the functional map C (near-diagonal)
  corr_delta_a_{0..2}.png          band-limited delta at a point on A
  corr_delta_b_{0..2}.png          its transport on B (peak = match)
"""
from _common import OUT_DIR, load_mesh, cotangent_laplacian
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import gen_24_shape_descriptors as d   # reuse eigs / render helpers

plt.rcParams["mathtext.fontset"] = "cm"

POSE_A = d.POSE_A                                   # horse-gallop-03
POSE_B = d.POSE_B                                   # horse-gallop-20
KMAP = 80                                            # eigenfunctions for the map
GREEN = "#39ff14"
FG = "#0f172a"
TEAL = "#2B5876"
BAND = "coolwarm"


def build():
    Va, Fa = load_mesh(POSE_A)
    Vb, Fb = load_mesh(POSE_B)
    La, Ma = cotangent_laplacian(Va, Fa)
    Lb, Mb = cotangent_laplacian(Vb, Fb)
    _, Pa, mda = d.lbo_eigs_sparse(La, Ma, k=KMAP)
    _, Pb, mdb = d.lbo_eigs_sparse(Lb, Mb, k=KMAP)

    # functional map for the identity (shared-topology) correspondence
    C = Pb.T @ (mdb[:, None] * Pa)                   # (K, K) = Phi_B^T M_B Phi_A

    # ---- plain grey poses (slide 1) -------------------------------------
    d.render_field(Va, Fa, np.zeros(len(Va)), "Greys", (-1, 1),
                   str(OUT_DIR / "corr_horse_a.png"))
    d.render_field(Vb, Fb, np.zeros(len(Vb)), "Greys", (-1, 1),
                   str(OUT_DIR / "corr_horse_b.png"))
    print("[ok] corr_horse_a/b.png")

    # ---- function transfer (slide 2): banded function along the body ----
    z = Va[:, 2]
    f = np.sin(2.4 * np.pi * (z - z.min()) / (z.max() - z.min()))
    a = Pa.T @ (mda * f)
    g = Pb @ (C @ a)
    clim = (-1.0, 1.0)
    d.render_field(Va, Fa, f, BAND, clim, str(OUT_DIR / "corr_func_a.png"))
    d.render_field(Vb, Fb, g, BAND, clim, str(OUT_DIR / "corr_func_b.png"))
    print("[ok] corr_func_a/b.png")

    # ---- coefficient bars + compact C (the b = C a slide) --------------
    n = 30
    av, bv = a[:n], (C @ a)[:n]
    ym = max(np.abs(av).max(), np.abs(bv).max()) * 1.12

    def coeff_bars(vec, color, out):
        fig, ax = plt.subplots(figsize=(4.4, 1.7))
        ax.bar(np.arange(1, len(vec) + 1), vec, color=color, width=0.8)
        ax.axhline(0, color="#cbd5e1", lw=0.8)
        ax.set_ylim(-ym, ym)
        ax.set_xlim(0.3, len(vec) + 0.7)
        ax.set_xticks([1, 10, 20, 30])
        ax.tick_params(labelsize=9)
        ax.set_yticks([])
        ax.spines[["top", "right", "left"]].set_visible(False)
        plt.tight_layout()
        plt.savefig(out, dpi=150, transparent=True, bbox_inches="tight", pad_inches=0.04)
        plt.close()

    coeff_bars(av, TEAL, str(OUT_DIR / "corr_coeff_a.png"))
    coeff_bars(bv, "#b45309", str(OUT_DIR / "corr_coeff_b.png"))
    print("[ok] corr_coeff_a/b.png")

    Cn = C[:n, :n]
    m = np.abs(Cn).max()
    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    ax.imshow(Cn, cmap="RdBu_r", norm=colors.Normalize(-m, m))
    ax.set_xticks([]); ax.set_yticks([])
    plt.tight_layout(pad=0.2)
    plt.savefig(str(OUT_DIR / "corr_cmat_small.png"), dpi=150, transparent=True,
                bbox_inches="tight", pad_inches=0.04)
    plt.close()
    print("[ok] corr_cmat_small.png")

    # ---- the functional map C (slide 3) --------------------------------
    n = 30
    Cn = C[:n, :n]
    m = np.abs(Cn).max()
    fig, ax = plt.subplots(figsize=(5.4, 5.0))
    im = ax.imshow(Cn, cmap="RdBu_r", norm=colors.Normalize(-m, m))
    ax.set_title("Functional map  $C$  (near-diagonal)", fontsize=14, color=FG)
    ax.set_xlabel("eigenfunction on  $A$", fontsize=12)
    ax.set_ylabel("eigenfunction on  $B$", fontsize=12)
    ax.set_xticks([0, 9, 19, 29]); ax.set_yticks([0, 9, 19, 29])
    ax.set_xticklabels([1, 10, 20, 30]); ax.set_yticklabels([1, 10, 20, 30])
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    plt.tight_layout()
    plt.savefig(str(OUT_DIR / "corr_cmat.png"), dpi=150, transparent=True,
                bbox_inches="tight", pad_inches=0.06)
    plt.close()
    print("[ok] corr_cmat.png")

    # ---- delta transport (slide 4) -------------------------------------
    lm = d.landmarks(Va)
    pts = [lm["nose"], lm["hoof"], lm["tail"]]
    for j, p in enumerate(pts):
        aD = Pa[p]                                    # coeffs of delta at p
        dA = Pa @ aD                                  # band-limited delta on A
        dB = Pb @ (C @ aD)                            # transported onto B
        q = int(np.argmax(dB))                        # recovered match on B
        ca = (float(np.percentile(dA, 1)), float(np.percentile(dA, 99.7)))
        cb = (float(np.percentile(dB, 1)), float(np.percentile(dB, 99.7)))
        d.render_field(Va, Fa, dA, "inferno", ca,
                       str(OUT_DIR / f"corr_delta_a_{j}.png"),
                       pts=[p], pcols=[GREEN])
        d.render_field(Vb, Fb, dB, "inferno", cb,
                       str(OUT_DIR / f"corr_delta_b_{j}.png"),
                       pts=[q], pcols=[GREEN])
        print(f"[ok] corr_delta_a/b_{j}.png  (p={p} -> q={q})")


if __name__ == "__main__":
    build()
