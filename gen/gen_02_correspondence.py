"""Card 02 — Correspondence. Pairs of deformed poses, coloured by a shared LBO
eigenfunction: matching anatomical regions get matching colours.

One image per shape category → app_02_corr_<name>.png
"""
from _common import decimate_pair, cotangent_laplacian, lbo_eigs, setup_plotter, save_screenshot, DEFTRANSFER
import numpy as np
import pyvista as pv
import trimesh

# (name, pose-A file, pose-B file)
PAIRS = [
    ("horse", "horse-poses/horse-01.obj", "horse-poses/horse-08.obj"),
    ("camel", "camel-poses/camel-01.obj", "camel-poses/camel-08.obj"),
    ("cat", "cat-poses/cat-01.obj", "cat-poses/cat-06.obj"),
    ("elephant", "elephant-poses/elephant-01.obj", "elephant-poses/elephant-07.obj"),
    ("lion", "lion-poses/lion-01.obj", "lion-poses/lion-06.obj"),
    ("flamingo", "flamingo-poses/flam-01.obj", "flamingo-poses/flam-06.obj"),
]
TARGET_FACES = 8000


def load_raw(path):
    m = trimesh.load(str(path), process=True, force="mesh")
    return np.asarray(m.vertices, np.float64), np.asarray(m.faces, np.int32)


def normalize(V):
    V = V - V.mean(0, keepdims=True)
    s = np.linalg.norm(V.max(0) - V.min(0))
    return V / s if s > 0 else V


def rot_y(P, deg):
    th = np.radians(deg)
    c, s = np.cos(th), np.sin(th)
    return P @ np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]).T


for name, fa, fb in PAIRS:
    Va, Fa = load_raw(DEFTRANSFER / fa)
    Vb, Fb = load_raw(DEFTRANSFER / fb)
    if Va.shape != Vb.shape or Fa.shape != Fb.shape:
        print(f"[skip] {name}: poses have different topology")
        continue

    Va, Vb, F = decimate_pair(Va, Vb, Fa, TARGET_FACES)
    Va, Vb = normalize(Va), normalize(Vb)

    # Shared low-frequency LBO signal, computed on pose A
    L, M = cotangent_laplacian(Va, F)
    vals, vecs = lbo_eigs(L, M, k=20)
    keep = vals > 1e-6
    vecs = vecs[:, keep]
    signal = vecs[:, 1] + 0.6 * vecs[:, 2]

    faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
    Va_r = rot_y(Va, 35)
    Vb_r = rot_y(Vb, 35)
    Va_r[:, 0] -= 0.38
    Vb_r[:, 0] += 0.38

    mesh_a = pv.PolyData(Va_r, faces_pv)
    mesh_b = pv.PolyData(Vb_r, faces_pv)
    mesh_a["sig"] = signal
    mesh_b["sig"] = signal

    p = setup_plotter((1000, 500))
    common = dict(
        scalars="sig", cmap="Spectral", smooth_shading=True, show_scalar_bar=False,
        clim=(signal.min(), signal.max()),
        ambient=0.25, diffuse=0.75, specular=0.2, specular_power=15,
    )
    p.add_mesh(mesh_a, **common)
    p.add_mesh(mesh_b, **common)
    p.camera_position = [(0.0, 0.0, 2.4), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.camera.zoom(1.7)
    p.enable_anti_aliasing("msaa")
    save_screenshot(p, f"app_02_corr_{name}")
