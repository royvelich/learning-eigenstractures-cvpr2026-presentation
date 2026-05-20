"""Smoke test: load an OBJ, render it once, write a transparent PNG."""
from _common import load_mesh, setup_plotter, save_screenshot, MPZ14
import pyvista as pv
import numpy as np

V, F = load_mesh(MPZ14 / "armadillo.obj")
print(f"loaded armadillo: {V.shape[0]} vertices, {F.shape[0]} faces")

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
mesh = pv.PolyData(V, faces_pv)

p = setup_plotter((600, 600))
p.add_mesh(mesh, color="#9bb4cf", smooth_shading=True, show_edges=False, ambient=0.25, diffuse=0.7, specular=0.3, specular_power=20)
p.camera_position = [(0.5, 0.0, 1.5), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
p.enable_anti_aliasing("msaa")
save_screenshot(p, "_probe")
