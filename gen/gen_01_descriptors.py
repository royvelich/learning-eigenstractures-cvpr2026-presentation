"""Card 01 — Shape Descriptors via geomfum's Heat Kernel Signature.

Three armadillos coloured by HKS at three diffusion times (geomfum picks
the time domain from the LBO spectrum). They sit in a single subplot so we
can place them close together — no inter-subplot borders or padding.

Produces:
  app_01_descriptors.png      — each panel independently normalised
  app_01_descriptors_abs.png  — one shared colour scale across all panels
"""
from _common import load_mesh, OUT_DIR, MPZ14
import numpy as np
import pyvista as pv
from geomfum.shape import TriangleMesh
from geomfum.laplacian import LaplacianFinder, LaplacianSpectrumFinder
from geomfum.descriptor.spectral import HeatKernelSignature

V, F = load_mesh(MPZ14 / "armadillo.obj", target_faces=6000)

# --- LBO basis via geomfum ---------------------------------------------------
mesh_gm = TriangleMesh(V, F)
laplacian_finder = LaplacianFinder.from_registry(which="robust")
spectrum_finder = LaplacianSpectrumFinder(
    spectrum_size=200,
    nonzero=True,
    laplacian_finder=laplacian_finder,
)
basis = spectrum_finder(mesh_gm)
mesh_gm.set_basis(basis)

# --- Heat Kernel Signature (3 time points) -----------------------------------
hks = HeatKernelSignature(scale=True, n_domain=3)
hks_values = np.asarray(hks(mesh_gm))           # (3, n_vertices)
hks_logs = [np.log(h + 1e-12) for h in hks_values]

# --- Render ------------------------------------------------------------------
faces_pv = np.hstack([np.full((F.shape[0], 1), 3, dtype=np.int64), F.astype(np.int64)]).ravel()
DX = 0.50  # horizontal spacing between the three armadillos
pv.global_theme.transparent_background = True


def render(name, clims):
    """clims: list of (lo, hi) per armadillo."""
    p = pv.Plotter(off_screen=True, window_size=(2100, 640))
    p.set_background([1, 1, 1, 0])
    for i, (h, clim) in enumerate(zip(hks_logs, clims)):
        V_t = V.copy()
        V_t[:, 0] += (i - 1) * DX  # i = 0,1,2 → -DX, 0, +DX
        mesh = pv.PolyData(V_t, faces_pv)
        mesh["hks"] = np.clip(h, *clim)
        p.add_mesh(
            mesh, scalars="hks", cmap="coolwarm", clim=clim,
            smooth_shading=True, show_scalar_bar=False,
            ambient=0.25, diffuse=0.75, specular=0.2, specular_power=15,
        )
    # Front-facing camera that frames the 3 armadillos as a horizontal band.
    p.camera_position = [(0.0, 0.05, -2.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]
    p.enable_anti_aliasing("msaa")
    out = OUT_DIR / name
    p.screenshot(str(out), transparent_background=True)
    p.close()
    # Tight-crop the alpha bbox.
    from PIL import Image
    im = Image.open(out)
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im.crop(bbox).save(out)
    print(f"[ok] {name}")


# A — per-panel normalisation
per_panel = [tuple(np.percentile(h, [3, 97])) for h in hks_logs]
render("app_01_descriptors.png", per_panel)

# B — shared scale
allv = np.concatenate(hks_logs)
g_lo, g_hi = np.percentile(allv, [2, 98])
render("app_01_descriptors_abs.png", [(g_lo, g_hi)] * 3)
