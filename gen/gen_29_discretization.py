"""What it means to work on a discretized surface.

Same mesh, one camera, three reveals:
  disc_smooth.png   smooth-shaded surface
  disc_mesh.png     surface with vertices + edges overlaid (a discrete sample)
  disc_func.png     a scalar function as values at the vertices (coloured points)
"""
from _common import MPZ14, OUT_DIR, load_mesh
import numpy as np


def faces_pv(F):
    return np.hstack([np.full((len(F), 1), 3, np.int64), F.astype(np.int64)]).ravel()


def build():
    import pyvista as pv
    from PIL import Image

    V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=1700)
    V[:, 0] = -V[:, 0]; V[:, 2] = -V[:, 2]          # face the camera
    faces = faces_pv(F)
    CAM = "xy"

    # a smooth scalar function sampled at the vertices (a height-based gradient,
    # so every vertex is clearly coloured)
    f = V[:, 1] + 0.25 * np.sin(6.0 * V[:, 0])
    f = f - f.mean()
    cap = float(np.percentile(np.abs(f), 98))

    def setup(p):
        p.camera_position = CAM
        p.reset_camera()
        p.camera.zoom(1.35)
        p.enable_anti_aliasing("ssaa")

    def render(name):
        arr = p.screenshot(transparent_background=True, return_img=True)
        p.close()
        return (name, arr)

    pv.global_theme.transparent_background = True
    shots = []

    # 1) smooth surface
    p = pv.Plotter(off_screen=True, window_size=(1000, 1000))
    p.set_background([1, 1, 1, 0])
    p.add_mesh(pv.PolyData(V, faces), color="#c9ccd1", smooth_shading=True,
               ambient=0.32, diffuse=0.72, specular=0.18, specular_power=16)
    setup(p); shots.append(render("disc_smooth.png"))

    # 2) surface + edges + vertices
    p = pv.Plotter(off_screen=True, window_size=(1000, 1000))
    p.set_background([1, 1, 1, 0])
    p.add_mesh(pv.PolyData(V, faces), color="#dfe3e8", smooth_shading=False,
               show_edges=True, edge_color="#475569", line_width=1,
               ambient=0.4, diffuse=0.66)
    p.add_mesh(pv.PolyData(V), color="#0f172a", point_size=5.5,
               render_points_as_spheres=True)
    setup(p); shots.append(render("disc_mesh.png"))

    # 3) a scalar function = values at the vertices: keep the triangulation +
    # edges, add the colour only on the vertex balls on top
    p = pv.Plotter(off_screen=True, window_size=(1000, 1000))
    p.set_background([1, 1, 1, 0])
    p.add_mesh(pv.PolyData(V, faces), color="#dfe3e8", smooth_shading=False,
               show_edges=True, edge_color="#475569", line_width=1,
               ambient=0.4, diffuse=0.66)
    pts = pv.PolyData(V); pts["f"] = f
    p.add_mesh(pts, scalars="f", cmap="coolwarm", clim=(-cap, cap),
               point_size=22, render_points_as_spheres=True, show_scalar_bar=False)
    setup(p); shots.append(render("disc_func.png"))

    # crop all three to a common box so the framing never jumps between clicks
    boxes = [Image.fromarray(a).getchannel("A").getbbox() for _, a in shots]
    pad = 6
    x0 = max(min(b[0] for b in boxes) - pad, 0)
    y0 = max(min(b[1] for b in boxes) - pad, 0)
    x1 = min(max(b[2] for b in boxes) + pad, shots[0][1].shape[1])
    y1 = min(max(b[3] for b in boxes) + pad, shots[0][1].shape[0])
    for name, a in shots:
        Image.fromarray(a[y0:y1, x0:x1]).save(str(OUT_DIR / name))
        print(f"[ok] {name}")


if __name__ == "__main__":
    build()
