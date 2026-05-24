"""Intro primer — the Laplacian on a curved surface (manifold).

Three figures of the same mesh in the same view:
  manifold_shape_grey.png         — bare shape, single colour
  manifold_shape_coloured.png     — same shape coloured by a smooth scalar f
  manifold_shape_neighbourhood.png — same scalar, with a focal point on the
                                     surface and a unit-ball neighbourhood
                                     (transparent yellow sphere) around it.
"""
from _common import load_mesh, save_screenshot
import numpy as np
import pyvista as pv

MESH_PATH = r"F:\input\mpz14\armadillo.obj"

V, F = load_mesh(MESH_PATH, target_faces=15000)
faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64),
                      F.astype(np.int64)]).ravel()
mesh = pv.PolyData(V, faces_pv)

# Smooth scalar function: red hill + blue valley, anchored in 3D ambient space.
centre_red = np.array([0.45, 0.10, -0.20])
centre_blue = np.array([-0.40, -0.10, 0.35])
sigma = 0.55
d_red = np.linalg.norm(V - centre_red, axis=1)
d_blue = np.linalg.norm(V - centre_blue, axis=1)
vals = 1.0 * np.exp(-d_red ** 2 / (2 * sigma ** 2)) \
    - 0.95 * np.exp(-d_blue ** 2 / (2 * sigma ** 2))
m = float(np.abs(vals).max())

# Focal point on the mesh near the centre.
focal_target = np.array([0.05, 0.20, 0.10])
focal_idx = int(np.argmin(np.linalg.norm(V - focal_target, axis=1)))
focal_pt = V[focal_idx]

R_BALL = 0.14
GREY = "#94a3b8"
DARK = "#0f172a"
BALL_FILL = "#fbbf24"

# Compute the camera framing once from the bare mesh so all three figures
# share the exact same view (otherwise pyvista refits when the ball is added).
pv.global_theme.transparent_background = True
_pinit = pv.Plotter(off_screen=True, window_size=(800, 800))
_pinit.set_background([1, 1, 1, 0])
_pinit.add_mesh(mesh, color=GREY)
_pinit.camera_position = "iso"
_pinit.reset_camera()
_pinit.camera.zoom(1.30)
SHARED_CAM = _pinit.camera_position
_pinit.close()


def render(name, builder):
    p = pv.Plotter(off_screen=True, window_size=(800, 800))
    p.set_background([1, 1, 1, 0])
    builder(p)
    p.camera_position = SHARED_CAM
    p.enable_anti_aliasing("msaa")
    save_screenshot(p, name)


def build_grey(p):
    p.add_mesh(mesh, color=GREY, smooth_shading=True,
               ambient=0.30, diffuse=0.72, specular=0.18, specular_power=12)


def build_coloured(p):
    m_copy = mesh.copy()
    m_copy["f"] = vals
    p.add_mesh(m_copy, scalars="f", cmap="coolwarm", clim=[-m, m],
               show_scalar_bar=False, smooth_shading=True,
               ambient=0.30, diffuse=0.72, specular=0.18, specular_power=12)


def build_neighbourhood(p):
    build_coloured(p)
    ball = pv.Sphere(radius=R_BALL, center=focal_pt, theta_resolution=48,
                     phi_resolution=48)
    p.add_mesh(ball, color=BALL_FILL, opacity=0.30, smooth_shading=True,
               ambient=0.50, diffuse=0.50, specular=0.0)
    focal_sphere = pv.Sphere(radius=0.022, center=focal_pt, theta_resolution=32,
                             phi_resolution=32)
    p.add_mesh(focal_sphere, color=DARK, smooth_shading=True,
               ambient=0.40, diffuse=0.60, specular=0.20)


render("manifold_shape_grey", build_grey)
render("manifold_shape_coloured", build_coloured)
render("manifold_shape_neighbourhood", build_neighbourhood)
