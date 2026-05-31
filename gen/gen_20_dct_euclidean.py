"""DCT basis on Euclidean domains with boundary.

Each panel of the slide has a sample (a 1D smooth signal / a 2D natural
image from imagenette) above its corresponding DCT-II basis. Sample and
basis are emitted as SEPARATE PNGs so the slide layout can align the
two samples at the same display height.

  dct_1d_sample.png   smooth 1D probe signal on [0, L]
  dct_1d_basis.png    2x4 grid of cosine modes phi_n(x) = cos(n pi x / L)
  dct_2d_sample.png   centre-cropped imagenette photo (RGB, square)
  dct_2d_basis.png    4x4 grid of product modes
                      phi_{n,m}(x, y) = cos(n pi x / Lx) cos(m pi y / Ly)
"""
from _common import OUT_DIR
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.ndimage import gaussian_filter1d

plt.rcParams["mathtext.fontset"] = "cm"

INDIGO = "#4E4376"
TEAL = "#2B5876"
GREY = "#94a3b8"
EDGE_GREY = "#cbd5e1"
SIG_COLOR = "#1f2937"


def _frame_panel(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_color(EDGE_GREY)
        s.set_linewidth(0.8)


def _save_tight(fig, name):
    """Save with zero padding, then PIL-crop the alpha bbox so the PNG's
    pixel bounds equal the drawn content's tight bbox."""
    out = OUT_DIR / name
    fig.savefig(out, dpi=220, transparent=True,
                bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    im = Image.open(out)
    bbox = im.getchannel("A").getbbox()
    if bbox:
        im.crop(bbox).save(out)
    print(f"[ok] {name}")


# 1D sample ---------------------------------------------------------------
rng = np.random.default_rng(7)
N_X = 480
x = np.linspace(0.0, 1.0, N_X)
sig1d = gaussian_filter1d(rng.standard_normal(N_X), sigma=28.0)
sig1d -= sig1d.mean()
sig1d /= np.max(np.abs(sig1d)) * 1.05

fig = plt.figure(figsize=(11.0, 6.0))
ax = fig.add_subplot(111)
ax.plot(x, sig1d, color=SIG_COLOR, lw=2.6)
ax.fill_between(x, 0.0, sig1d, color=SIG_COLOR, alpha=0.08)
ax.axhline(0.0, color=GREY, lw=0.6)
ax.set_xlim(0.0, 1.0)
ax.set_ylim(-1.03, 1.03)
_frame_panel(ax)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
_save_tight(fig, "dct_1d_sample.png")


# 1D basis ---------------------------------------------------------------
N1D = 12
fig, axes = plt.subplots(3, 4, figsize=(11.0, 6.0))
for k in range(N1D):
    ax = axes[k // 4, k % 4]
    y = np.cos(k * np.pi * x)
    ax.plot(x, y, color=TEAL, lw=2.2)
    ax.fill_between(x, 0.0, y, color=TEAL, alpha=0.10)
    ax.axhline(0.0, color=GREY, lw=0.6)
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(-1.03, 1.03)
    _frame_panel(ax)
# Zero OUTER margins (so the PNG's pixel bounds touch the first/last
# row's frame), but keep the original inter-subplot spacing.
plt.subplots_adjust(left=0, right=1, top=1, bottom=0,
                    wspace=0.35, hspace=0.35)
_save_tight(fig, "dct_1d_basis.png")


# 2D sample (imagenette) -------------------------------------------------
src = Path(__file__).resolve().parents[1] / "public" / "datasets" / "imagenette_2.jpg"
src_im = Image.open(src).convert("RGB")
W, H = src_im.size
s = min(W, H)
left = (W - s) // 2
top = (H - s) // 2
square = src_im.crop((left, top, left + s, top + s)).resize((480, 480), Image.LANCZOS)

fig = plt.figure(figsize=(4.4, 4.4))
ax = fig.add_subplot(111)
ax.imshow(np.asarray(square), extent=[0.0, 1.0, 0.0, 1.0], origin="upper")
_frame_panel(ax)
_save_tight(fig, "dct_2d_sample.png")


# 2D basis ---------------------------------------------------------------
N2D = 4
N_PX = 240
xx, yy = np.meshgrid(np.linspace(0.0, 1.0, N_PX),
                     np.linspace(0.0, 1.0, N_PX))

fig, axes = plt.subplots(N2D, N2D, figsize=(6.8, 6.8))
for n in range(N2D):
    for m in range(N2D):
        ax = axes[n, m]
        f = np.cos(n * np.pi * xx) * np.cos(m * np.pi * yy)
        ax.imshow(f, cmap="RdBu_r", vmin=-1.0, vmax=1.0,
                  extent=[0.0, 1.0, 0.0, 1.0], origin="lower")
        _frame_panel(ax)
plt.subplots_adjust(wspace=0.18, hspace=0.18)
_save_tight(fig, "dct_2d_basis.png")
