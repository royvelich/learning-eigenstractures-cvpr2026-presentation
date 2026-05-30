"""Images for the 'reconstruction on a 3D point cloud' slide.

  manifold_pc_mesh.png         — armadillo rendered as a full smooth mesh
  manifold_pc_points.png       — same armadillo as a sampled point cloud
                                 (demonstrates 'sampling from a smooth manifold')
  manifold_pc_signal_NN.png    — point cloud coloured by a smooth scalar f
                                 (mix of ambient Gaussians); a handful of
                                 different f's to show variety.
"""
from _common import OUT_DIR, load_mesh
import numpy as np
import pyvista as pv

MESH_PATH = r"F:\input\mpz14\armadillo.obj"
N_SAMPLES = 3500     # points in the sampled cloud
N_SIGNALS = 5         # how many distinct signals to render
RNG_SEED = 7

V, F = load_mesh(MESH_PATH, target_faces=None)


def orient_upright(V):
    """Rotate the mesh so its longest principal axis (head-to-feet) is +Y."""
    centred = V - V.mean(axis=0)
    cov = np.cov(centred.T)
    eigvals, eigvecs = np.linalg.eigh(cov)        # ascending eigenvalues
    longest = eigvecs[:, 2]                        # principal direction
    if longest[1] < 0:                             # prefer +Y orientation
        longest = -longest
    target = np.array([0.0, 1.0, 0.0])
    cross = np.cross(longest, target)
    s = np.linalg.norm(cross)
    c = float(np.dot(longest, target))
    if s < 1e-10:
        return V
    K = np.array([[0, -cross[2], cross[1]],
                  [cross[2], 0, -cross[0]],
                  [-cross[1], cross[0], 0]])
    R = np.eye(3) + K + K @ K * ((1 - c) / (s * s))
    return centred @ R.T


V = orient_upright(V)


def rotate_z(V, deg):
    """Rotate vertices CCW around world +Z by `deg` degrees (CCW = top tilts left)."""
    th = np.radians(deg)
    R = np.array([[np.cos(th), -np.sin(th), 0.0],
                  [np.sin(th),  np.cos(th), 0.0],
                  [0.0,         0.0,         1.0]])
    return V @ R.T


V = rotate_z(V, -2.0)  # slight CW tilt around the screen-axis
faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64),
                      F.astype(np.int64)]).ravel()
mesh = pv.PolyData(V, faces_pv)

# Sub-sample vertices for the point cloud
rng = np.random.default_rng(RNG_SEED)
sample_idx = rng.choice(V.shape[0], size=min(N_SAMPLES, V.shape[0]),
                       replace=False)
P = V[sample_idx]

# ----------------------------- shared camera (front view, standing on feet)
pv.global_theme.transparent_background = True
_pinit = pv.Plotter(off_screen=True, window_size=(900, 900))
_pinit.set_background([1, 1, 1, 0])
_pinit.add_mesh(mesh, color="#94a3b8")
# Y is up; look at origin from +Z. The mesh has been PCA-aligned so the
# head-to-feet direction is +Y.
# Slightly elevated camera, looking at the chest (focal lifted up a bit).
# Removes the "looking-up-the-soles" effect and lets the armadillo stand
# visually straight.
_pinit.camera_position = [(0.0, 0.45, -3.0), (0.0, 0.20, 0.0), (0.0, 1.0, 0.0)]
_pinit.reset_camera()
_pinit.camera.zoom(1.30)
SHARED_CAM = _pinit.camera_position
_pinit.close()


def add_shadow(p):
    """Soft, BLURRED elliptical ground shadow under the armadillo.

    Single horizontal disc with per-vertex opacity following a Gaussian
    falloff — opaque at the centre, smoothly fading to 0 at the edges.
    The whole disc shares one colour (#0f172a) so opacity is the only
    thing that varies.
    """
    from matplotlib.colors import ListedColormap

    y_min = float(V[:, 1].min())
    x_range = float(V[:, 0].max() - V[:, 0].min())
    z_range = float(V[:, 2].max() - V[:, 2].min())
    base_x = 0.70 * x_range
    base_z = 1.05 * z_range

    # Dense disc so the per-vertex Gaussian samples enough points
    disc = pv.Disc(center=(0.0, 0.0, 0.0),
                   inner=0.0, outer=1.0,
                   normal=(0.0, 1.0, 0.0),
                   c_res=128, r_res=24)
    # remember the [-1, 1] normalised radius before we scale the disc
    r2 = disc.points[:, 0] ** 2 + disc.points[:, 2] ** 2
    disc.points[:, 0] *= base_x
    disc.points[:, 2] *= base_z
    disc.points[:, 1] = y_min - 0.005

    # Gaussian falloff. Peak alpha ~0.35, ~0 at the disc edge.
    alpha = 0.40 * np.exp(-2.8 * r2)
    disc.point_data["alpha"] = alpha

    dark_cmap = ListedColormap([(0.059, 0.090, 0.165, 1.0)])  # #0f172a
    p.add_mesh(disc, scalars="alpha", cmap=dark_cmap,
               opacity="alpha", clim=(0.0, 1.0),
               lighting=False, show_scalar_bar=False,
               smooth_shading=False)


def render(name, builder):
    p = pv.Plotter(off_screen=True, window_size=(900, 900))
    p.set_background([1, 1, 1, 0])
    add_shadow(p)
    builder(p)
    p.camera_position = SHARED_CAM
    p.enable_anti_aliasing("msaa")
    out = OUT_DIR / f"{name}.png"
    p.screenshot(str(out), transparent_background=True, return_img=False)
    p.close()
    # Strip the transparent padding around the visible content so the
    # slide doesn't show a small image inside a big empty box. The
    # alpha bbox is the same crop write_tight() applies — we just bake
    # it into the canonical file instead of an extra "_tight" copy.
    from PIL import Image as _PILImage
    _im = _PILImage.open(out)
    _bbox = _im.getchannel("A").getbbox()
    if _bbox is not None:
        _im.crop(_bbox).save(out)
    print(f"[ok] {out.name}")


def write_tight(name):
    """Crop `{name}.png` to its alpha bounding box and save as `{name}_tight.png`."""
    from PIL import Image as _PILImage
    src = OUT_DIR / f"{name}.png"
    im = _PILImage.open(src)
    bbox = im.getchannel("A").getbbox()
    if bbox is None:
        return
    out = OUT_DIR / f"{name}_tight.png"
    im.crop(bbox).save(out)
    print(f"[ok] {out.name}  (cropped to {bbox})")


# ----------------------------- 1. full mesh
def build_mesh(p):
    p.add_mesh(mesh, color="#cbd5e1", smooth_shading=True,
               ambient=0.30, diffuse=0.72, specular=0.18, specular_power=12)


render("manifold_pc_mesh", build_mesh)


# ----------------------------- 2. bare point cloud
def build_points(p):
    cloud = pv.PolyData(P)
    p.add_mesh(cloud, color="#cbd5e1", render_points_as_spheres=True,
               point_size=16, ambient=0.30, diffuse=0.72)


render("manifold_pc_points", build_points)

write_tight("manifold_pc_points")


# ----------------------------- 3. smooth signals on the point cloud
def make_signal(seed, n_bumps_range=(2, 5)):
    sub_rng = np.random.default_rng(seed)
    n_bumps = sub_rng.integers(n_bumps_range[0], n_bumps_range[1] + 1)
    # Sample bump centres directly from the point cloud so they sit on / near the shape
    centre_idx = sub_rng.choice(P.shape[0], size=n_bumps, replace=False)
    centres = P[centre_idx]
    signs = sub_rng.choice([-1.0, 1.0], size=n_bumps)
    amps = signs * sub_rng.uniform(0.6, 1.0, size=n_bumps)
    sigmas = sub_rng.uniform(0.15, 0.32, size=n_bumps)
    f = np.zeros(P.shape[0])
    for c, amp, sig in zip(centres, amps, sigmas):
        d2 = np.sum((P - c) ** 2, axis=1)
        f += amp * np.exp(-d2 / (2 * sig ** 2))
    return f


for i in range(N_SIGNALS):
    f = make_signal(RNG_SEED + 100 + i)
    m = float(np.abs(f).max())
    if m < 1e-6:
        continue

    def build_signal(p, _f=f, _m=m):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="coolwarm", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_{i + 1:02d}"
    render(name, build_signal)
    write_tight(name)


# ----------------------------- 3b. diffusion-smoothed random signals
# A second family of smooth scalar functions on the cloud. Construction:
#   1. assign each vertex an i.i.d. uniform random value in [-1, 1],
#   2. build a kNN graph with Gaussian-weighted edges (bandwidth = median
#      nearest-neighbour distance); the self-edge has weight 1,
#   3. form the row-stochastic smoothing operator S = D^{-1} W and apply
#      f <- S f for N_SMOOTH_ITERS steps. Higher iteration counts produce
#      smoother fields; small counts leave residual noise.
import scipy.sparse as _sp
from scipy.spatial import cKDTree as _cKDTree

N_DSIGNALS = 5
K_NN_SMOOTH = 15
N_SMOOTH_ITERS = 80

_tree = _cKDTree(P)
_dist, _idx = _tree.query(P, k=K_NN_SMOOTH + 1)
_sigma_s = float(np.median(_dist[:, 1:]))
_rows = np.repeat(np.arange(P.shape[0]), K_NN_SMOOTH + 1)
_cols = _idx.ravel()
_w = np.exp(-(_dist.ravel() ** 2) / (2.0 * _sigma_s ** 2))
W_smooth = _sp.csr_matrix((_w, (_rows, _cols)),
                          shape=(P.shape[0], P.shape[0]))
W_smooth = (W_smooth + W_smooth.T) * 0.5
_d_smooth = np.asarray(W_smooth.sum(axis=1)).ravel().clip(min=1e-14)
S_smooth = _sp.diags(1.0 / _d_smooth) @ W_smooth

_diff_signals = {}   # idx (1-based) -> (f array, clim scale m) ; reused for reconstructions below

for i in range(N_DSIGNALS):
    _r = np.random.default_rng(RNG_SEED + 700 + i)
    f = _r.uniform(-1.0, 1.0, size=P.shape[0])
    for _ in range(N_SMOOTH_ITERS):
        f = S_smooth @ f
    m = max(float(np.abs(f).max()), 1e-9)
    _diff_signals[i + 1] = (f.copy(), m)

    def build_dsignal(p, _f=f, _m=m):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="coolwarm", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_diff_{i + 1:02d}"
    render(name, build_dsignal)
    write_tight(name)


# Mass matrix M from the point-cloud Laplacian — needed both for the LBO
# eigenbasis (Set 4) and for M-orthogonalising the random bases (Sets 1..3),
# so they all live in the same Hilbert structure ⟨f, g⟩_M = fᵀ M g.
import robust_laplacian
import scipy.sparse as sp
import scipy.linalg as sla
L_lbo, M_lbo = robust_laplacian.point_cloud_laplacian(P)
L_lbo = sp.csc_matrix(L_lbo)
M_lbo = sp.csc_matrix(M_lbo)
# M is diagonal (lumped Voronoi) — keep the sqrt around for cheap
# M-orthogonalisation via the Cholesky trick.
_m_diag = np.asarray(M_lbo.diagonal()).ravel()
_m_sqrt = np.sqrt(np.clip(_m_diag, 1e-12, None))


def m_orthogonalize(A):
    """Return Q with M-orthonormal columns (Qᵀ M Q = I) spanning span(A).
    Trick: with M = sqrt(M)·sqrt(M)ᵀ (diagonal here), set B = sqrt(M) A,
    take Euclidean QR(B) = Q_b R, then Q = sqrt(M)⁻¹ Q_b is M-orthonormal."""
    B = _m_sqrt[:, None] * A
    Qb, _ = np.linalg.qr(B)
    return Qb / _m_sqrt[:, None]


# ----------------------------- 4. random orthogonal bases
# 3 sets, each of K basis functions on the point cloud. Functions are
# M-orthonormalised so each row in the slide really shows an orthogonal
# basis in the SAME inner product the LBO eigenbasis uses — they look
# smooth (built from Gaussian mixtures) and differ between sets thanks
# to different random seeds.
N_RANDOM_BASIS_SETS = 3
# Match set 4 (the LBO eigenbasis): each random basis is a full 50-dim
# orthonormal basis. The slide only shows the first 3 + last 3 thumbnails
# to make the "truncated basis" story visible without rendering all 50.
N_BASIS_VECS = 50
SHOWN_FRONT = 3       # which basis indices to render: first 3
SHOWN_BACK = 3        # ... and last 3 (so 6 PNGs per random set)


def build_smooth_atoms(seed, n_atoms, n_bumps_range=(3, 7)):
    sub_rng = np.random.default_rng(seed)
    atoms = []
    for _ in range(n_atoms):
        n_bumps = int(sub_rng.integers(n_bumps_range[0], n_bumps_range[1] + 1))
        centre_idx = sub_rng.choice(P.shape[0], size=n_bumps, replace=False)
        centres = P[centre_idx]
        amps = sub_rng.choice([-1.0, 1.0], size=n_bumps) \
            * sub_rng.uniform(0.5, 1.0, size=n_bumps)
        sigmas = sub_rng.uniform(0.12, 0.30, size=n_bumps)
        f = np.zeros(P.shape[0])
        for c, amp, sig in zip(centres, amps, sigmas):
            d2 = np.sum((P - c) ** 2, axis=1)
            f += amp * np.exp(-d2 / (2 * sig ** 2))
        atoms.append(f)
    return np.column_stack(atoms)


def render_basis_set(set_i, basis_vecs):
    """Render only the first SHOWN_FRONT and last SHOWN_BACK columns of
    `basis_vecs` (the basis is conceptually 50-dim, but the slide only
    displays 3 front + 3 back thumbnails). Naming is 0-indexed to match
    set 4 (the LBO eigenbasis)."""
    total = basis_vecs.shape[1]
    shown_idx = list(range(SHOWN_FRONT)) + list(range(total - SHOWN_BACK, total))
    for k in shown_idx:
        f = basis_vecs[:, k]
        m = float(np.abs(f).max())
        if m < 1e-9:
            continue

        def build_basis(p, _f=f, _m=m):
            cloud = pv.PolyData(P)
            cloud["f"] = _f
            p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                       render_points_as_spheres=True, point_size=16,
                       show_scalar_bar=False,
                       ambient=0.30, diffuse=0.72)

        name = f"manifold_pc_basis_{set_i}_{k}"
        render(name, build_basis)
        write_tight(name)


# Sets 1..3 — random M-orthonormal bases of smooth atoms (50-dim each)
for set_i in range(1, N_RANDOM_BASIS_SETS + 1):
    # Clear stale per-set thumbnails (we used to write 1-indexed names).
    for _old in OUT_DIR.glob(f"manifold_pc_basis_{set_i}_*.png"):
        _old.unlink()
    A = build_smooth_atoms(RNG_SEED + 500 + (set_i - 1) * 17, N_BASIS_VECS)
    Q = m_orthogonalize(A)
    render_basis_set(set_i, Q)


# Set 4 — the canonical LBO eigenbasis on the point cloud, solved as
# the GENERALIZED eigenproblem  L phi = lambda M phi.  The eigenvectors
# are M-orthonormal (matching Sets 1..3) and the first one is a constant
# — the genuine smoothest function on the manifold.
N_LSYM_VECS = 50

# Clear stale basis_4_* files from any previous indexing scheme.
for _old in OUT_DIR.glob("manifold_pc_basis_4_*.png"):
    _old.unlink()

# Generalized eigendecomposition L phi = lambda M phi.  scipy.linalg.eigh
# handles the symmetric-definite generalized problem and returns vectors
# that are M-orthonormal (vecs.T @ M @ vecs = I).
vals_all, vecs_all = sla.eigh(L_lbo.toarray(), M_lbo.toarray())

# First N_LSYM_VECS eigenvectors of the generalized eigenproblem,
# ordered by increasing eigenvalue (smoothest first). This IS the LBO
# eigenbasis in its non-normalized form.
psi = vecs_all[:, :N_LSYM_VECS]

for k in range(N_LSYM_VECS):
    f = psi[:, k]
    m = max(float(np.abs(f).max()), 1e-9)

    def build_basis(p, _f=f, _m=m):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_basis_4_{k}"
    render(name, build_basis)
    write_tight(name)


# Slide 15 ("Our pipeline") shows random orthogonal basis #2 as the
# *predicted* eigenbasis (rather than the canonical LBO basis we just
# rendered for slide 14). Every figure on that slide that depends on the
# basis — per-component projections of signal_diff_01 / signal_diff_02
# and the full reconstructions used as "sum" thumbnails — must be
# computed in THAT same basis to stay coherent.
#
# We rebuild basis #2 here (same seed as in the sets 1..3 loop above) and
# rebind `psi` to it; the projection/reconstruction sections below now
# operate in this random orthonormal smooth basis instead of L_sym's.
_Q2_atoms = build_smooth_atoms(RNG_SEED + 500 + (2 - 1) * 17, N_BASIS_VECS)
_Q2 = m_orthogonalize(_Q2_atoms)
psi = _Q2[:, :N_LSYM_VECS]


# ----------------------------- 5. reconstruction of the diffusion signals on
# the first k vectors of the slide-15 predicted eigenbasis (random M-
# orthonormal smooth basis #2). The vectors {psi_i} satisfy Ψᵀ M Ψ = I, so
# the truncated reconstruction uses the M-INNER-PRODUCT coefficients
#     coeffs_i = ψ_iᵀ M f,    f_k = Σ_{i<k} coeffs_i · ψ_i.
# Using the Euclidean dot ψᵀ f would scale the coefficients by ~Σ m_j and
# blow up every component thumbnail.
RECON_KS = (1, 2, 5, 10, 20, 49, 50)

# Dense M reused for projection / reconstruction.
_M_dense = M_lbo.toarray()
_psi_M = psi.T @ _M_dense        # shape (N_LSYM_VECS, N_pts) — Mᵀψ for each row.

for _sig_i, (_f_orig, _m_orig) in _diff_signals.items():
    _coeffs = _psi_M @ _f_orig    # M-weighted projection coefficients.
    for _k in RECON_KS:
        _f_recon = psi[:, :_k] @ _coeffs[:_k]

        def build_recon(p, _f=_f_recon, _m=_m_orig):
            cloud = pv.PolyData(P)
            cloud["f"] = _f
            p.add_mesh(cloud, scalars="f", cmap="coolwarm", clim=[-_m, _m],
                       render_points_as_spheres=True, point_size=16,
                       show_scalar_bar=False,
                       ambient=0.30, diffuse=0.72)

        name = f"manifold_pc_signal_diff_{_sig_i:02d}_recon_k{_k}"
        render(name, build_recon)
        write_tight(name)


# ----------------------------- 6. Per-component projection of signal_diff_01
# onto each eigenvector of L_sym. For each i in [0, N_LSYM_VECS):
#     component_i = (psi_i^T f) * psi_i
# i.e. the i-th term in the Euclidean Fourier expansion of f in the L_sym
# basis. Rendered with the SAME colour limit as the original signal so the
# magnitude (sign + amplitude) of each spectral component is comparable.
_f0, _m0 = _diff_signals[1]
_coeffs0 = _psi_M @ _f0   # M-weighted: ψᵀ M f, matches Ψ being M-orthonormal.

# Shared-clim compression factor — the high-i projection components carry
# tiny amplitudes, so plotting them at the FULL signal range washes them
# to white. Capping at PROJ_CLIM_FACTOR * m_0 keeps cross-i amplitude
# comparison (low-i components saturate together at the high end while
# high-i components stay visible).
PROJ_CLIM_FACTOR = 0.2

for _i in range(N_LSYM_VECS):
    _comp = _coeffs0[_i] * psi[:, _i]

    # Shared (compressed) clim. Same value used for signal_diff_02 below.
    _m_shared = PROJ_CLIM_FACTOR * _m0

    def build_comp_global(p, _f=_comp, _m=_m_shared):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_diff_01_proj_i{_i}"
    render(name, build_comp_global)
    write_tight(name)

    # Per-image clim: each component drawn at its own dynamic range, so
    # high-i modes are still visible (loses cross-i amplitude comparison).
    _m_local = max(float(np.abs(_comp).max()), 1e-9)

    def build_comp_local(p, _f=_comp, _m=_m_local):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_diff_01_proj_local_i{_i}"
    render(name, build_comp_local)
    write_tight(name)


# ----------------------------- 6b. Per-component projection of signal_diff_02
# Only the 4 indices used by the pipeline slide (eigens 0, 1, 48, 49).
# Both variants: shared clim (proj_iN) and per-image clim (proj_local_iN).
_f2, _m2 = _diff_signals[2]
_coeffs2 = _psi_M @ _f2   # M-weighted projection.

for _i in [0, 1, 48, 49]:
    _comp2 = _coeffs2[_i] * psi[:, _i]

    # Shared (compressed) clim — same factor as signal_diff_01 above so
    # cross-i amplitude comparison is still meaningful but small components
    # remain visible.
    _m_shared2 = PROJ_CLIM_FACTOR * _m2

    def build_comp_global2(p, _f=_comp2, _m=_m_shared2):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_diff_02_proj_i{_i}"
    render(name, build_comp_global2)
    write_tight(name)

    # Per-image clim — each component drawn at its own dynamic range so
    # high-i modes stay visible (loses cross-i amplitude comparison).
    _m_local2 = max(float(np.abs(_comp2).max()), 1e-9)

    def build_comp_local2(p, _f=_comp2, _m=_m_local2):
        cloud = pv.PolyData(P)
        cloud["f"] = _f
        p.add_mesh(cloud, scalars="f", cmap="PiYG", clim=[-_m, _m],
                   render_points_as_spheres=True, point_size=16,
                   show_scalar_bar=False,
                   ambient=0.30, diffuse=0.72)

    name = f"manifold_pc_signal_diff_02_proj_local_i{_i}"
    render(name, build_comp_local2)
    write_tight(name)
