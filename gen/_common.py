"""Shared utilities for the application image generators."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import trimesh

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "public" / "applications"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MPZ14 = Path("F:/input/mpz14")
DEFTRANSFER = Path("F:/input/deftransfer")


def load_mesh(path, target_faces=None):
    m = trimesh.load(str(path), process=False, force="mesh")
    if isinstance(m, trimesh.Scene):
        m = m.dump().sum()
    if target_faces is not None and len(m.faces) > target_faces:
        m = m.simplify_quadric_decimation(face_count=target_faces)
        # remove orphan / unreferenced vertices left over by the decimator
        m.remove_unreferenced_vertices()
        m.merge_vertices()
    V = np.asarray(m.vertices, dtype=np.float64)
    F = np.asarray(m.faces, dtype=np.int32)
    V = V - V.mean(axis=0, keepdims=True)
    scale = np.linalg.norm(V.max(axis=0) - V.min(axis=0))
    if scale > 0:
        V /= scale
    return V, F


def decimate_pair(Va, Vb, F, target_faces):
    """Decimate two meshes that share topology (same F) *consistently*, so the
    decimated pair still shares vertex indexing. Returns (Va2, Vb2, F2)."""
    import fast_simplification as fs
    if len(F) <= target_faces:
        return Va, Vb, F
    reduction = 1.0 - target_faces / len(F)
    pa, F2, collapses = fs.simplify(
        Va.astype(np.float32), F.astype(np.int64), reduction, return_collapses=True
    )
    pb = fs.replay_simplification(Vb.astype(np.float32), F.astype(np.int64), collapses)[0]
    return np.asarray(pa, np.float64), np.asarray(pb, np.float64), np.asarray(F2, dtype=np.int32)


def cotangent_laplacian(V, F):
    """Returns (L, M) — positive-semi-definite cotangent Laplacian and lumped mass.

    Prefers `robust_laplacian` (Sharp & Crane 2020) which handles degenerate
    triangles cleanly; falls back to libigl, then to a from-scratch builder."""
    try:
        import robust_laplacian
        L, M = robust_laplacian.mesh_laplacian(V, F)
        L = sp.csc_matrix(L)
        M = sp.csc_matrix(M)
        total = float(M.diagonal().sum())
        if total > 0:
            M = M * (V.shape[0] / total)
        return L, M
    except Exception:
        pass
    try:
        import igl
        L = igl.cotmatrix(V, F)
        if L.diagonal().mean() < 0:
            L = -L
        M = igl.massmatrix(V, F, igl.MASSMATRIX_TYPE_VORONOI)
        return sp.csc_matrix(L), sp.csc_matrix(M)
    except Exception:
        pass
    # Fallback: build cotangent Laplacian manually
    nv = V.shape[0]
    I, J, S = [], [], []
    Ma = np.zeros(nv)
    for face in F:
        i, j, k = face
        vi, vj, vk = V[i], V[j], V[k]
        e0 = vk - vj
        e1 = vi - vk
        e2 = vj - vi
        area = 0.5 * np.linalg.norm(np.cross(e1, -e2))
        Ma[i] += area / 3.0
        Ma[j] += area / 3.0
        Ma[k] += area / 3.0
        cot0 = np.dot(e1, -e2) / (2.0 * area)  # angle at i
        cot1 = np.dot(-e0, e2) / (2.0 * area)  # angle at j
        cot2 = np.dot(e0, -e1) / (2.0 * area)  # angle at k
        for a, b, w in ((j, k, cot0), (k, i, cot1), (i, j, cot2)):
            I += [a, b, a, b]
            J += [b, a, a, b]
            S += [-0.5 * w, -0.5 * w, 0.5 * w, 0.5 * w]
    L = sp.coo_matrix((S, (I, J)), shape=(nv, nv)).tocsc()
    M = sp.diags(Ma).tocsc()
    return L, M


def lbo_eigs(L, M, k=200):
    """Generalised eigenproblem L φ = λ M φ. Returns (λ[k], Φ[n_v, k]) ascending.

    For small meshes (n < ~8k) we use a dense eigh on M^{-1/2} L M^{-1/2}
    which is rock-solid. For larger meshes we fall back to sparse Lanczos."""
    import scipy.linalg as sla
    M_csc = M.tocsc()
    L_csc = L.tocsc()
    if L_csc.diagonal().mean() < 0:
        L_csc = -L_csc
    n = L_csc.shape[0]
    m_diag = np.asarray(M_csc.diagonal()).clip(min=1e-14)
    Mi_sqrt = sp.diags(1.0 / np.sqrt(m_diag), format="csc")
    S = (Mi_sqrt @ L_csc @ Mi_sqrt).tocsc()
    S = 0.5 * (S + S.T)
    if n <= 12000:
        S_dense = S.toarray()
        vals_all, vecs_all = sla.eigh(S_dense)
        vals = vals_all[:k]
        vs = vecs_all[:, :k]
    else:
        vals, vs = spla.eigsh(S, k=k, which="SM")
    vecs = Mi_sqrt @ vs
    order = np.argsort(vals)
    return vals[order], vecs[:, order]


def setup_plotter(window_size=(800, 800)):
    """Headless pyvista plotter with transparent background."""
    import pyvista as pv
    pv.global_theme.transparent_background = True
    pv.global_theme.anti_aliasing = "msaa"
    p = pv.Plotter(off_screen=True, window_size=window_size)
    p.set_background([1, 1, 1, 0])  # transparent
    return p


def save_screenshot(plotter, name):
    """Save plotter screenshot to public/applications/<name>.png (transparent)."""
    out = OUT_DIR / f"{name}.png"
    plotter.screenshot(str(out), transparent_background=True, return_img=False)
    plotter.close()
    print(f"[ok] {out.relative_to(REPO_ROOT)}")
    return out
