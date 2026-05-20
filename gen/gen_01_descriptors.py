"""Card 01 — Shape Descriptors. Armadillo (front view) coloured by the Heat
Kernel Signature at four diffusion times.

Produces two strips:
  app_01_descriptors.png      — each panel independently normalized
  app_01_descriptors_abs.png  — one shared colour scale across all panels
"""
from _common import load_mesh, cotangent_laplacian, lbo_eigs, OUT_DIR, MPZ14
import numpy as np
import pyvista as pv

V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=6000)
L, M = cotangent_laplacian(V, F)
vals, vecs = lbo_eigs(L, M, k=200)

# Drop spurious near-zero eigenvalues (numerical noise around the constant mode)
keep = vals > 1e-6
vals, vecs = vals[keep], vecs[:, keep]

# Four diffusion times, log-spaced from local (small t) to global (large t).
t_min = 4.0 / vals[80]
t_max = 4.0 / vals[3]
t_values = np.logspace(np.log10(t_min), np.log10(t_max), 4)

# HKS at each scale: h(x,t) = Σ_i exp(-λ_i t) φ_i(x)^2  (log-transformed for display)
hks_logs = []
for t in t_values:
    h = (np.exp(-vals[None, :] * t) * vecs ** 2).sum(axis=1)
    hks_logs.append(np.log(h + 1e-12))

faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
front_cam = [(0.0, 0.05, -1.7), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]

pv.global_theme.transparent_background = True


def render(name, clims):
    """clims: list of (lo, hi) per panel."""
    p = pv.Plotter(off_screen=True, window_size=(2400, 640), shape=(1, 4))
    p.set_background([1, 1, 1, 0])
    for i, (h, clim) in enumerate(zip(hks_logs, clims)):
        mesh = pv.PolyData(V, faces_pv)
        mesh["hks"] = np.clip(h, *clim)
        p.subplot(0, i)
        p.add_mesh(
            mesh, scalars="hks", cmap="coolwarm", clim=clim,
            smooth_shading=True, show_scalar_bar=False,
            ambient=0.25, diffuse=0.75, specular=0.2, specular_power=15,
        )
        p.camera_position = front_cam
        p.enable_anti_aliasing("msaa")
    out = OUT_DIR / name
    p.screenshot(str(out), transparent_background=True)
    p.close()
    print(f"[ok] {name}")


# A — per-panel normalization (each panel uses its own 3–97 percentile)
per_panel = [tuple(np.percentile(h, [3, 97])) for h in hks_logs]
render("app_01_descriptors.png", per_panel)

# B — shared scale: one global range applied to every panel
allv = np.concatenate(hks_logs)
g_lo, g_hi = np.percentile(allv, [2, 98])
render("app_01_descriptors_abs.png", [(g_lo, g_hi)] * 4)

print(f"t = {', '.join(f'{t:.3g}' for t in t_values)}")
