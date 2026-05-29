"""Card 02 — Correspondence via functional maps (geomfum).

For each (pose A, pose B) pair we:
  1. Decimate the two poses jointly so they share topology.
  2. Compute the LBO eigenbasis on EACH mesh independently with geomfum.
  3. Build the functional map A → B from the (identity) point-to-point map.
  4. Take a low-frequency function on A, transfer it through the functional
     map onto B, and colour the two meshes accordingly. Matching anatomical
     regions get matching colours — even though the LBO eigenvectors are
     independently computed (and may differ in sign / order).

One image per pair → app_02_corr_<name>.png
"""
from _common import decimate_pair, setup_plotter, save_screenshot, DEFTRANSFER
import numpy as np
import pyvista as pv
import trimesh
from geomfum.shape import TriangleMesh
from geomfum.laplacian import LaplacianFinder, LaplacianSpectrumFinder
from geomfum.refine import FmFromP2pConverter

PAIRS = [
    ("horse", "horse-poses/horse-01.obj", "horse-poses/horse-08.obj"),
    ("camel", "camel-poses/camel-01.obj", "camel-poses/camel-08.obj"),
    ("cat", "cat-poses/cat-01.obj", "cat-poses/cat-06.obj"),
    ("elephant", "elephant-poses/elephant-01.obj", "elephant-poses/elephant-07.obj"),
    ("lion", "lion-poses/lion-01.obj", "lion-poses/lion-06.obj"),
    ("flamingo", "flamingo-poses/flam-01.obj", "flamingo-poses/flam-06.obj"),
]
TARGET_FACES = 8000
SPECTRUM_SIZE = 30


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


# geomfum LBO machinery — robust mesh Laplacian + Lanczos eigensolver.
laplacian_finder = LaplacianFinder.from_registry(which="robust")
spectrum_finder = LaplacianSpectrumFinder(
    spectrum_size=SPECTRUM_SIZE,
    nonzero=True,
    laplacian_finder=laplacian_finder,
)
fm_converter = FmFromP2pConverter()


for name, fa, fb in PAIRS:
    Va, Fa = load_raw(DEFTRANSFER / fa)
    Vb, Fb = load_raw(DEFTRANSFER / fb)
    if Va.shape != Vb.shape or Fa.shape != Fb.shape:
        print(f"[skip] {name}: poses have different topology")
        continue

    Va, Vb, F = decimate_pair(Va, Vb, Fa, TARGET_FACES)
    Va, Vb = normalize(Va), normalize(Vb)

    # Independent LBO bases on each pose (geomfum).
    mesh_a_gm = TriangleMesh(Va, F)
    mesh_b_gm = TriangleMesh(Vb, F)
    basis_a = spectrum_finder(mesh_a_gm)
    basis_b = spectrum_finder(mesh_b_gm)

    # Ground-truth p2p map: identity (joint decimation preserves topology).
    p2p = np.arange(mesh_b_gm.n_vertices)

    # Functional map A → B (built from p2p via least squares).
    fmap = fm_converter(p2p, basis_a, basis_b)

    # Low-frequency signal on A: combination of the first two non-trivial
    # eigenvectors of basis A.
    signal_a = basis_a.vecs[:, 1] + 0.6 * basis_a.vecs[:, 2]

    # Project onto basis_a, push through fmap, reconstruct on B.
    signal_a_coeffs = basis_a.pinv @ signal_a
    signal_b_coeffs = fmap @ signal_a_coeffs
    signal_b = basis_b.vecs @ signal_b_coeffs

    # Render.
    faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
    Va_r = rot_y(Va, 35)
    Vb_r = rot_y(Vb, 35)
    Va_r[:, 0] -= 0.38
    Vb_r[:, 0] += 0.38

    mesh_a = pv.PolyData(Va_r, faces_pv)
    mesh_b = pv.PolyData(Vb_r, faces_pv)
    mesh_a["sig"] = signal_a
    mesh_b["sig"] = signal_b

    # Shared color range across both meshes so equal anatomical regions
    # actually map to equal colours visually.
    clim_lo = float(min(signal_a.min(), signal_b.min()))
    clim_hi = float(max(signal_a.max(), signal_b.max()))

    p = setup_plotter((1000, 500))
    common = dict(
        scalars="sig", cmap="Spectral", smooth_shading=True, show_scalar_bar=False,
        clim=(clim_lo, clim_hi),
        ambient=0.25, diffuse=0.75, specular=0.2, specular_power=15,
    )
    p.add_mesh(mesh_a, **common)
    p.add_mesh(mesh_b, **common)
    p.camera_position = [(0.0, 0.0, 2.4), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.camera.zoom(1.7)
    p.enable_anti_aliasing("msaa")
    save_screenshot(p, f"app_02_corr_{name}")
