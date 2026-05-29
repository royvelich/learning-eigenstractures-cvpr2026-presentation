"""Card 05 — Geometry Processing. Geodesic distance from a source vertex
via the heat method (potpourri3d's `MeshHeatMethodDistanceSolver`)."""
from _common import load_mesh, setup_plotter, save_screenshot, MPZ14
import numpy as np
import pyvista as pv
import potpourri3d as pp3d

V, F = load_mesh(MPZ14 / "bimba100K.obj")

# Pick a source point (apex / top of the head) so the distance bands are visually clean.
source = int(np.argmax(V[:, 1]))

# Heat-method geodesics (Crane et al.) via potpourri3d.
solver = pp3d.MeshHeatMethodDistanceSolver(V.astype(np.float64), F.astype(np.int64))
dist = solver.compute_distance(source)

# Banded colormap by modulating
period = 0.06
banded = np.cos(2 * np.pi * dist / period) * 0.25 + dist

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
mesh = pv.PolyData(V, faces_pv)
mesh["d"] = banded

p = setup_plotter((700, 700))
p.add_mesh(
    mesh,
    scalars="d",
    cmap="magma",
    smooth_shading=True,
    show_scalar_bar=False,
    ambient=0.2,
    diffuse=0.8,
    specular=0.15,
    specular_power=12,
)
# Small sphere at the source
p.add_mesh(pv.Sphere(radius=0.015, center=V[source]), color="white", smooth_shading=True)
p.camera_position = [(0.0, 0.05, 1.6), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
p.enable_anti_aliasing("msaa")
save_screenshot(p, "app_05_geometry_processing")
