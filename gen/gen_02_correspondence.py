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
import matplotlib.colors as mcolors
import matplotlib.cm as mcm
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
SPECTRUM_SIZE = 120


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

    # Paint mesh A by its (normalized) XYZ position, used as an RGB
    # triple per vertex. Each channel is then independently projected
    # onto basis_a, pushed by fmap into basis_b, and reconstructed on B,
    # so matching anatomy on B inherits the colour of the corresponding
    # region of A.
    xyz_a = Va - Va.min(axis=0, keepdims=True)
    xyz_a = xyz_a / np.maximum(xyz_a.max(axis=0, keepdims=True), 1e-12)
    rgb_a = xyz_a

    # The LBO basis is built with nonzero=True, which excludes the
    # constant eigenvector. The projection therefore drops the DC mean
    # of each channel — without restoring it, the reconstruction on B
    # would be zero-mean and most of the surface would clip to black.
    # We subtract the mean before projecting and add it back after, since
    # the constant component is preserved by any correspondence.
    mean_a = rgb_a.mean(axis=0, keepdims=True)        # (1, 3)
    rgb_a_ac = rgb_a - mean_a                         # zero-mean per channel

    coeffs_a = basis_a.pinv @ rgb_a_ac                # (k, 3)
    coeffs_b = fmap @ coeffs_a                        # (k, 3)
    rgb_b = basis_b.vecs @ coeffs_b + mean_a          # (n, 3) on mesh B

    # Reconstruction on a finite basis can overshoot [0, 1]; clip so
    # PyVista accepts the values as colours.
    rgb_b = np.clip(rgb_b, 0.0, 1.0)

    # PyVista expects uint8 RGB arrays when scalars are colours.
    rgb_a_u8 = (rgb_a * 255.0 + 0.5).astype(np.uint8)
    rgb_b_u8 = (rgb_b * 255.0 + 0.5).astype(np.uint8)

    # Render.
    faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
    Va_r = rot_y(Va, 35)
    Vb_r = rot_y(Vb, 35)
    Va_r[:, 0] -= 0.38
    Vb_r[:, 0] += 0.38

    mesh_a = pv.PolyData(Va_r, faces_pv)
    mesh_b = pv.PolyData(Vb_r, faces_pv)
    mesh_a["rgb"] = rgb_a_u8
    mesh_b["rgb"] = rgb_b_u8

    p = setup_plotter((1000, 500))
    # Original Phong-style mix (low ambient, strong diffuse + crisp
    # specular) — gives clear 3-D shading and sharp highlights.
    common = dict(
        scalars="rgb", rgb=True, smooth_shading=True, show_scalar_bar=False,
        ambient=0.25, diffuse=0.75, specular=0.2, specular_power=15,
    )
    p.add_mesh(mesh_a, **common)
    p.add_mesh(mesh_b, **common)
    p.camera_position = [(0.0, 0.0, 2.4), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.camera.zoom(1.7)
    p.enable_anti_aliasing("msaa")
    save_screenshot(p, f"app_02_corr_{name}")
