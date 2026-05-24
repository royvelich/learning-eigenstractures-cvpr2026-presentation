"""Intro primer — the Laplace-Beltrami operator on a curved surface.

Same idea as the 2D Laplacian, but the domain is a curved manifold.
Two spheres: left coloured by a scalar function f, right by its LBO Δf.
lap_lbo.png
"""
from _common import cotangent_laplacian, save_screenshot
import numpy as np
import pyvista as pv

# Icosphere — uniform triangulation, no pole artifacts.
sphere = pv.Icosphere(radius=1.0, nsub=6).triangulate()
V = np.asarray(sphere.points, dtype=np.float64)
F = sphere.regular_faces.astype(np.int32)

# Scalar function on the surface: a few smooth Gaussian bumps/dips.
centres = [(np.array([0.3, 0.9, 0.3]), 1.0, 0.55),
           (np.array([-0.9, 0.1, 0.4]), -0.9, 0.5),
           (np.array([0.4, -0.5, 0.8]), 0.85, 0.55)]
fval = np.zeros(V.shape[0])
for c, amp, sig in centres:
    c = c / np.linalg.norm(c)
    d2 = np.sum((V - c) ** 2, axis=1)
    fval += amp * np.exp(-d2 / (2 * sig ** 2))

# LBO of f:  Δf = -M^{-1} L f   (our L is the +PSD cotangent matrix, so Δ = -M⁻¹L)
L, M = cotangent_laplacian(V, F)
lap = -(L @ fval) / np.asarray(M.diagonal()).clip(min=1e-12)
lap = np.clip(lap, *np.percentile(lap, [2, 98]))

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()

pv.global_theme.transparent_background = True
p = pv.Plotter(off_screen=True, window_size=(1150, 600), shape=(1, 2))
p.set_background([1, 1, 1, 0])

p.subplot(0, 0)
m0 = pv.PolyData(V, faces_pv)
m0["f"] = fval
p.add_mesh(m0, scalars="f", cmap="viridis", smooth_shading=True, show_scalar_bar=False,
           ambient=0.3, diffuse=0.72, specular=0.2, specular_power=15)
p.camera_position = "iso"
p.reset_camera()
p.camera.zoom(1.25)
p.enable_anti_aliasing("msaa")

p.subplot(0, 1)
m1 = pv.PolyData(V, faces_pv)
m1["lap"] = lap
p.add_mesh(m1, scalars="lap", cmap="coolwarm", smooth_shading=True, show_scalar_bar=False,
           ambient=0.3, diffuse=0.72, specular=0.2, specular_power=15)
p.camera_position = "iso"
p.reset_camera()
p.camera.zoom(1.25)
p.enable_anti_aliasing("msaa")

save_screenshot(p, "lap_lbo")
