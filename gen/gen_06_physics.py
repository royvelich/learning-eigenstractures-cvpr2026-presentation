"""Card 06 — Physics & Simulation. Heat diffusion from a point source via the LBO."""
from _common import load_mesh, cotangent_laplacian, lbo_eigs, setup_plotter, save_screenshot, MPZ14
import numpy as np
import pyvista as pv

V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=6000)
L, M = cotangent_laplacian(V, F)
vals, vecs = lbo_eigs(L, M, k=200)
# Filter out spurious near-zero eigvalues (numerical noise around the zero mode)
keep = vals > 1e-6
vals = vals[keep]
vecs = vecs[:, keep]

# Pick a heat source — tip of the right hand (max along +x direction)
source = int(np.argmax(V[:, 0]))
u0 = np.zeros(V.shape[0])
u0[source] = 1.0 / max(M.diagonal()[source], 1e-9)  # delta in the M-norm

# u(t) = sum_i exp(-λ_i t) <u0, phi_i>_M phi_i
M_csr = M.tocsr()
a = vecs.T @ (M_csr @ u0)
# pick t so that mid-frequency modes are damped to ~e^{-2} ≈ 0.13
t_diff = 2.0 / vals[20]
u_t = vecs @ (np.exp(-vals * t_diff) * a)

# Color in log scale so the diffusion gradient is visible
u_log = np.log(np.maximum(u_t, 1e-9))
lo, hi = np.percentile(u_log, [5, 99])
u_log = np.clip(u_log, lo, hi)

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
mesh = pv.PolyData(V, faces_pv)
mesh["u"] = u_log

p = setup_plotter((700, 700))
p.add_mesh(
    mesh,
    scalars="u",
    cmap="inferno",
    smooth_shading=True,
    show_scalar_bar=False,
    ambient=0.25,
    diffuse=0.75,
    specular=0.2,
    specular_power=15,
)
p.add_mesh(pv.Sphere(radius=0.015, center=V[source]), color="white", smooth_shading=True)
p.camera_position = [(0.4, 0.1, 1.6), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
p.enable_anti_aliasing("msaa")
save_screenshot(p, "app_06_physics")
