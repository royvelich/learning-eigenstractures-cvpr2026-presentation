"""Card 04 — Signal Processing on Manifolds. Noisy scalar field vs. its LBO low-pass reconstruction."""
from _common import load_mesh, cotangent_laplacian, lbo_eigs, setup_plotter, save_screenshot, MPZ14
import numpy as np
import pyvista as pv

V, F = load_mesh(MPZ14 / "camel.obj", target_faces=6000)
L, M = cotangent_laplacian(V, F)
vals, vecs = lbo_eigs(L, M, k=30)

# Random combination of low-freq LBO eigenfunctions — band-limited and richly varying.
# Normalize by std (not max) so the field uses the colormap range evenly.
# Build the smooth signal explicitly from real (non-degenerate) LBO modes.
# The first ~9 modes are spurious numerical copies of the zero eigenvalue, so we
# pick a band 9-20 that gives genuine low-frequency variation on the surface.
rng = np.random.default_rng(0)
coeffs_base = np.zeros(vecs.shape[1])
coeffs_base[9:20] = rng.normal(size=11)
smooth_base = vecs @ coeffs_base
smooth_base = smooth_base / (smooth_base.std() + 1e-9)
noise = rng.normal(scale=1.5, size=V.shape[0])
noise -= noise.mean()
noisy = smooth_base + noise

# Low-pass: project onto first k LBO eigenvectors (M-orthonormal)
M_csr = M.tocsr()
coeffs = vecs.T @ (M_csr @ noisy)
filtered = vecs @ coeffs
# Pre-translate two copies in numpy to avoid relying on PolyData.translate
V_left = V.copy()
V_left[:, 0] -= 0.6
V_right = V.copy()
V_right[:, 0] += 0.6

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
mesh_n = pv.PolyData(V_left, faces_pv)
mesh_n.point_data["sig"] = noisy.astype(np.float32)
mesh_f = pv.PolyData(V_right, faces_pv)
mesh_f.point_data["sig"] = filtered.astype(np.float32)

clim = (-2.0, 2.0)

p = setup_plotter((1000, 500))
for m in (mesh_n, mesh_f):
    p.add_mesh(
        m,
        scalars="sig",
        cmap="viridis",
        smooth_shading=True,
        show_scalar_bar=False,
        clim=clim,
        ambient=0.25,
        diffuse=0.75,
        specular=0.15,
        specular_power=12,
    )
p.camera_position = [(0.0, 0.05, 2.3), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
p.enable_anti_aliasing("msaa")
save_screenshot(p, "app_04_signal_processing")
