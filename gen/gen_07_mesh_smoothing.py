"""Card 07 — Mesh Smoothing. Project vertex coordinates onto the first k LBO eigenvectors."""
from _common import load_mesh, cotangent_laplacian, lbo_eigs, setup_plotter, save_screenshot, MPZ14
import numpy as np
import pyvista as pv

V, F = load_mesh(MPZ14 / "bumpy_sphere.obj", target_faces=6000)
L, M = cotangent_laplacian(V, F)
vals, vecs = lbo_eigs(L, M, k=40)

# Project each coordinate column onto the LBO basis and reconstruct → smooth shape
M_csr = M.tocsr()
coords_lp = vecs @ (vecs.T @ (M_csr @ V))

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
mesh_n = pv.PolyData(V, faces_pv)
mesh_s = pv.PolyData(coords_lp, faces_pv)

mesh_n.translate([-0.35, 0.0, 0.0], inplace=True)
mesh_s.translate([0.35, 0.0, 0.0], inplace=True)

p = setup_plotter((1000, 500))
common = dict(
    color="#b6c3d4",
    smooth_shading=True,
    show_scalar_bar=False,
    ambient=0.25,
    diffuse=0.75,
    specular=0.35,
    specular_power=20,
)
p.add_mesh(mesh_n, **common)
p.add_mesh(mesh_s, **common)
p.camera_position = [(0.0, 0.0, 2.3), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
p.enable_anti_aliasing("msaa")
save_screenshot(p, "app_07_mesh_smoothing")
