"""Composite  Δ ( f )  =  Δf  image — the Laplacian's action in operator form.

Lays out, left → right, on a single row:

    Δ   (   f-strip   )   =   Δf-strip

mirroring slide 3 of the deck.  Output → public/applications/data_manifold_action.png.
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

plt.rcParams["mathtext.fontset"] = "cm"

# ── Source strips ────────────────────────────────────────────────────────
f_img  = np.asarray(Image.open(str(OUT_DIR / "data_manifold_coloured.png")).convert("RGBA"))
df_img = np.asarray(Image.open(str(OUT_DIR / "data_manifold_laplacian_full.png")).convert("RGBA"))
H, W = f_img.shape[:2]

# ── Element widths (in image pixels) ─────────────────────────────────────
GAP          = 30
EQ_GAP       = 80     # extra breathing room on each side of the = sign
DELTA_GAP    = 60     # extra breathing room between Δ and the opening paren
DELTA_W      = 160    # Δ glyph slot
PAREN_W      = 80     # one paren glyph slot
EQUALS_W     = 170    # = glyph slot

# X-positions of each element's left edge.
x_delta  = GAP
x_lparen = x_delta  + DELTA_W  + DELTA_GAP
x_f      = x_lparen + PAREN_W  + int(0.5 * GAP)
x_rparen = x_f      + W        + int(0.5 * GAP)
x_equals = x_rparen + PAREN_W  + EQ_GAP
x_df     = x_equals + EQUALS_W + EQ_GAP

canvas_w = x_df + W + GAP
canvas_h = H

fig, ax = plt.subplots(figsize=(canvas_w / 200, canvas_h / 200), dpi=200)

# ── Strips ───────────────────────────────────────────────────────────────
ax.imshow(f_img,  extent=(x_f,  x_f  + W, H, 0))
ax.imshow(df_img, extent=(x_df, x_df + W, H, 0))

DARK   = "#0f172a"
INDIGO = "#4E4376"

# ── Δ on the left ────────────────────────────────────────────────────────
ax.text(x_delta + DELTA_W / 2, H / 2, r"$\Delta$",
        color=INDIGO, fontsize=75, fontweight="bold",
        ha="center", va="center")

# ── ( around f ──────────────────────────────────────────────────────────
ax.text(x_lparen + PAREN_W / 2, H / 2, "(",
        color=DARK, fontsize=140, family="serif",
        ha="center", va="center")
ax.text(x_rparen + PAREN_W / 2, H / 2, ")",
        color=DARK, fontsize=140, family="serif",
        ha="center", va="center")

# ── = between Δ(f) and Δf ───────────────────────────────────────────────
ax.text(x_equals + EQUALS_W / 2, H / 2, "=",
        color=DARK, fontsize=95,
        ha="center", va="center")

ax.set_xlim(0, canvas_w)
ax.set_ylim(canvas_h, 0)         # image-coord convention: y grows downward
ax.set_aspect("equal")
ax.axis("off")

plt.savefig(str(OUT_DIR / "data_manifold_action.png"),
            dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.0)
plt.close()
print("[ok] data_manifold_action.png")
