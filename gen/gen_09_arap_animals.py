"""Card 09 — ARAP deformation on animal shapes.

For each animal: align the long axis to X, pin the rear, rotate the head
region up. libigl's ARAP fills the smooth, locally-rigid pose change.
One image per animal → app_09_arap_<name>.png  (rest | deformed)
"""
from _common import load_mesh, setup_plotter, save_screenshot, DEFTRANSFER
import numpy as np
import pyvista as pv
import igl

ANIMALS = [
    ("horse", "horse-poses/horse-01.obj"),
    ("camel", "camel-poses/camel-01.obj"),
    ("cat", "cat-poses/cat-01.obj"),
    ("lion", "lion-poses/lion-01.obj"),
]
HEAD_DEG = 40.0  # how far to swing the head up


def align_long_axis_to_x(V):
    """Rotate about Y so the dominant horizontal axis lies along X."""
    xz = V[:, [0, 2]] - V[:, [0, 2]].mean(0)
    _, evecs = np.linalg.eigh(xz.T @ xz)
    d = evecs[:, -1]
    ang = np.arctan2(d[1], d[0])
    c, s = np.cos(-ang), np.sin(-ang)
    Ry = np.array([[c, 0, -s], [0, 1, 0], [s, 0, c]])
    return V @ Ry.T


for name, rel in ANIMALS:
    V, F = load_mesh(DEFTRANSFER / rel, target_faces=9000)
    V = align_long_axis_to_x(V)
    # head should sit at +x: flip if the tallest vertex is on the −x side
    if V[np.argmax(V[:, 1]), 0] < 0:
        V[:, 0] *= -1.0

    x, y = V[:, 0], V[:, 1]
    x_lo, x_hi = np.percentile(x, [2, 98])
    y_mid = np.median(y)
    # pinned: the rear body block
    rear = np.where(x < x_lo + 0.32 * (x_hi - x_lo))[0]
    # moved: only the elevated head region (exclude forward-reaching legs)
    head = np.where((x > x_lo + 0.80 * (x_hi - x_lo)) & (y > y_mid))[0]
    b = np.concatenate([rear, head]).astype(np.int32)

    th = np.radians(HEAD_DEG)
    c, s = np.cos(th), np.sin(th)
    Rz = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
    bc = np.vstack([V[rear], V[head] @ Rz.T]).astype(np.float64)

    data = igl.ARAPData()
    data.max_iter = 120
    igl.arap_precomputation(V.astype(np.float64), F.astype(np.int64), 3, b, data)
    U = igl.arap_solve(bc, data, V.astype(np.float64).copy())

    faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()

    MESH_COLOR = "#c2cad6"
    PIN_COLOR = "#2563eb"
    HANDLE_COLOR = "#dc2626"
    # subsample dense constraint regions so the markers read as a region, not a blob
    rng = np.random.default_rng(0)
    rear_s = rear if len(rear) <= 220 else rng.choice(rear, 220, replace=False)
    head_s = head if len(head) <= 220 else rng.choice(head, 220, replace=False)

    p = setup_plotter((1100, 540))

    def draw(P, dx):
        Q = P.copy()
        Q[:, 0] += dx
        p.add_mesh(pv.PolyData(Q, faces_pv), color=MESH_COLOR, smooth_shading=True,
                   show_scalar_bar=False, ambient=0.3, diffuse=0.7, specular=0.25, specular_power=18)
        p.add_mesh(pv.PolyData(Q[rear_s]), color=PIN_COLOR,
                   render_points_as_spheres=True, point_size=7)
        p.add_mesh(pv.PolyData(Q[head_s]), color=HANDLE_COLOR,
                   render_points_as_spheres=True, point_size=7)

    draw(V, -0.62)   # rest pose
    draw(U, +0.62)   # deformed pose
    p.camera_position = [(0.0, 0.0, 3.2), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.camera.zoom(1.35)
    p.enable_anti_aliasing("msaa")
    save_screenshot(p, f"app_09_arap_{name}")
