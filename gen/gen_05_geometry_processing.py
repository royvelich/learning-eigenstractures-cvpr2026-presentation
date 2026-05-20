"""Card 05 — Geometry Processing. Geodesic distance from a source vertex via the heat method."""
from _common import load_mesh, setup_plotter, save_screenshot, MPZ14
import numpy as np
import pyvista as pv
import igl

V, F = load_mesh(MPZ14 / "bimba100K.obj")

# Pick a source point (apex / top of the head) so the distance bands are visually clean.
source = int(np.argmax(V[:, 1]))
gamma = np.array([source], dtype=np.int32)

# libigl heat geodesics (Crane et al.)
t = (igl.avg_edge_length(V, F) ** 2)
data = igl.HeatGeodesicsData()
igl.heat_geodesics_precompute(V.astype(np.float64), F.astype(np.int64), float(t), data)
dist = igl.heat_geodesics_solve(data, gamma.astype(np.int64))

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
