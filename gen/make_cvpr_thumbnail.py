"""Compose the 320 x 256 PNG thumbnail required by the CVPR submission.

Layout:
    +---------------------------------------------------+   30 px header
    |  Learning Eigenstructures of Unstructured Data .. |
    +---------------+---------------+-------------------+
    |   v2 v5 v10 v20 (4 cells, 80 x 80)                |   80 px row 1
    |                                                   |
    +---------------------------------------------------+   ~20 px labels
    |   v2  v5  v10  v20                                |
    +---------------------------------------------------+
    |   row of "Ours" predictions (4 cells, 80 x 80)    |   80 px row 2
    +---------------------------------------------------+
    |  Top: cot. Laplacian   |   Bottom: Ours           |   46 px footer
    +---------------------------------------------------+

Eigenfunctions taken from `poster/figures/overfit/lion/`:
  - gt_eigen001.png  (v_2),  gt_eigen004.png  (v_5),
    gt_eigen009.png  (v_10), gt_eigen019.png (v_20)
  - pred_eigen001/004/009/019.png (the matching "Ours" predictions)

Output: poster/poster_cvpr_thumbnail.png  (320 x 256 RGB, target <5 MB).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "poster" / "figures" / "overfit" / "lion"
OUT = ROOT / "poster" / "poster_cvpr_thumbnail.png"

W, H = 320, 256
HEADER_H = 30
ROW_H = 80
LABEL_H = 16
FOOTER_H = H - HEADER_H - 2 * ROW_H - LABEL_H  # = 50 px

assert HEADER_H + ROW_H + LABEL_H + ROW_H + FOOTER_H == H, "vertical layout mismatch"

EIGEN_IDXS = ["001", "004", "009", "019"]     # v_2, v_5, v_10, v_20
EIGEN_LABELS = ["v₂", "v₅", "v₁₀", "v₂₀"]
NUM_COLS = len(EIGEN_IDXS)
CELL_W = W // NUM_COLS                          # = 80
assert CELL_W == 80

# ─── canvas ─────────────────────────────────────────────────────────────
canvas = Image.new("RGB", (W, H), (255, 255, 255))
draw = ImageDraw.Draw(canvas)

# Try to find a font we can use for the title and labels. Fall back to PIL's
# default bitmap font if nothing nicer is on this machine.
def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates += ["seguisb.ttf", "arialbd.ttf", "DejaVuSans-Bold.ttf"]
    candidates += ["segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()

font_title = _font(13, bold=True)
font_label = _font(11)
font_footer = _font(11)

# ─── header ─────────────────────────────────────────────────────────────
header_text = "Learned LBO eigenbasis  —  Cot. Laplacian vs Ours"
tw, th = draw.textbbox((0, 0), header_text, font=font_title)[2:]
draw.text(((W - tw) / 2, (HEADER_H - th) / 2 - 1), header_text,
          font=font_title, fill=(15, 23, 42))

# ─── eigenfunction grid (top: GT, bottom: Ours) ──────────────────────────
def _paste(src: Path, x: int, y: int) -> None:
    im = Image.open(src).convert("RGBA")
    # Resize keeping aspect, fit inside CELL_W x ROW_H.
    im.thumbnail((CELL_W, ROW_H), Image.LANCZOS)
    ox = x + (CELL_W - im.width) // 2
    oy = y + (ROW_H - im.height) // 2
    canvas.paste(im, (ox, oy), im)

ROW1_Y = HEADER_H
ROW2_Y = HEADER_H + ROW_H + LABEL_H
LABEL_Y = HEADER_H + ROW_H

for col, idx in enumerate(EIGEN_IDXS):
    x = col * CELL_W
    _paste(SRC_DIR / f"gt_eigen{idx}.png", x, ROW1_Y)
    _paste(SRC_DIR / f"pred_eigen{idx}.png", x, ROW2_Y)

# ─── column labels between the two rows ─────────────────────────────────
for col, label in enumerate(EIGEN_LABELS):
    tw, th = draw.textbbox((0, 0), label, font=font_label)[2:]
    cx = col * CELL_W + CELL_W // 2
    draw.text((cx - tw / 2, LABEL_Y + (LABEL_H - th) / 2 - 1),
              label, font=font_label, fill=(30, 41, 59))

# ─── footer caption ──────────────────────────────────────────────────────
footer_y_top = HEADER_H + 2 * ROW_H + LABEL_H
footer_caption = "Top: cotangent Laplacian   •   Bottom: Ours (predicted)"
tw, th = draw.textbbox((0, 0), footer_caption, font=font_footer)[2:]
draw.text(((W - tw) / 2, footer_y_top + (FOOTER_H - th) / 2 - 1),
          footer_caption, font=font_footer, fill=(71, 85, 105))

# ─── save (PNG, RGB) ─────────────────────────────────────────────────────
canvas.save(OUT, "PNG", optimize=True)
size_kb = OUT.stat().st_size / 1024
print(f"[ok] {OUT.relative_to(ROOT)}  {canvas.width}x{canvas.height} px  {size_kb:.1f} KB")
