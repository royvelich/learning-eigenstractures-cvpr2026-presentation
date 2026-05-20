"""Card 08 — Mesh Deformation (As-Rigid-As-Possible).

A tube is pinned at the left end; the right end is rotated up. libigl's ARAP
solver fills in the smooth, locally-rigid bend.
Left panel: rest pose.  Right panel: deformed, coloured by per-vertex displacement.
"""
from _common import OUT_DIR
import numpy as np
import pyvista as pv
import igl

# --- build a clean open tube along x -------------------------------------
nx, nth = 90, 36
r = 0.16
xs = np.linspace(-1.0, 1.0, nx)
ths = np.linspace(0.0, 2 * np.pi, nth, endpoint=False)
V = np.array([[x, r * np.cos(t), r * np.sin(t)] for x in xs for t in ths], dtype=np.float64)

F = []
for i in range(nx - 1):
    for j in range(nth):
        j2 = (j + 1) % nth
        a, b = i * nth + j, i * nth + j2
        c, d = (i + 1) * nth + j, (i + 1) * nth + j2
        F.append([a, b, d])
        F.append([a, d, c])
F = np.array(F, dtype=np.int64)

# --- handles: pin the left end, rotate the right end up ------------------
left = np.where(V[:, 0] < -0.90)[0]
right = np.where(V[:, 0] > 0.90)[0]
b = np.concatenate([left, right]).astype(np.int32)

angle = np.radians(60.0)
c, s = np.cos(angle), np.sin(angle)
Rz = np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])
# rotate the right handle rigidly about the pinned (left) end so it swings up
pivot = np.array([-1.0, 0.0, 0.0])
bc = np.vstack([V[left], (V[right] - pivot) @ Rz.T + pivot]).astype(np.float64)

# --- ARAP solve ----------------------------------------------------------
data = igl.ARAPData()
data.max_iter = 150
igl.arap_precomputation(V, F, 3, b, data)
U = igl.arap_solve(bc, data, V.copy())

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F]).ravel()

MESH_COLOR = "#c2cad6"
PIN_COLOR = "#2563eb"   # fixed constraint points
HANDLE_COLOR = "#dc2626"  # moved handle points


def draw(panel, P):
    """Render the tube at vertex positions P plus the constraint markers."""
    p.subplot(0, panel)
    p.add_mesh(pv.PolyData(P, faces_pv), color=MESH_COLOR, smooth_shading=True,
               show_scalar_bar=False, ambient=0.3, diffuse=0.7, specular=0.3, specular_power=20)
    p.add_mesh(pv.PolyData(P[left]), color=PIN_COLOR, render_points_as_spheres=True,
               point_size=11)
    p.add_mesh(pv.PolyData(P[right]), color=HANDLE_COLOR, render_points_as_spheres=True,
               point_size=11)
    p.camera_position = "xy"
    p.reset_camera()
    p.camera.zoom(0.85)
    p.enable_anti_aliasing("msaa")


pv.global_theme.transparent_background = True
p = pv.Plotter(off_screen=True, window_size=(1100, 520), shape=(1, 2))
p.set_background([1, 1, 1, 0])

draw(0, V)   # rest pose — constraints at original positions
draw(1, U)   # deformed — pinned points fixed, handle points moved

out = OUT_DIR / "app_08_arap.png"
p.screenshot(str(out), transparent_background=True)
p.close()
print(f"[ok] {out.name}")
