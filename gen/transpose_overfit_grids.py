"""Transpose the supplied qualitative-comparison PNGs.

Each input PNG (`supp_overfit1@0.5x.png`, `supp_overfit2@0.5x.png`,
`overfit_eigenvector@0.5x.png`) is a grid where

  - rows go top→bottom over eigenvector indices (v_2 ... v_41) and the
    bottom reconstruction rows (k = 5, 25, 45),
  - columns go left→right over shapes; each shape occupies two adjacent
    sub-columns (Cot. Lap. | Ours).

We want them transposed:

  - rows go top→bottom over shapes,
  - columns go left→right over eigenvector indices + reconstruction k's.

Each macro cell keeps its internal (Cot. Lap. | Ours) horizontal pair
intact. Row/column text labels are dropped — they can be re-added in
the slide layout.

Approach: alpha-mask-based gap detection finds 8 macro shape-columns and
N macro content-rows (N = 12 for overfit1/2, 12 for the smaller file).
Each macro cell is cropped and pasted into a new canvas in the swapped
position. Cells are resized to a shared (W, H) so the result is regular.
"""
from pathlib import Path
import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ROWS_DIR = ROOT / "public" / "applications" / "overfit"

# Shape order in each input (top→bottom in the source, which becomes
# left→right in the transposed canvas and per-row slicing).
INPUTS = [
    ("supp_overfit1@0.5x.png",
     "supp_overfit1_transposed.png",
     ["dragon", "bimba", "dente", "knot", "teddy", "eros", "beetle", "kitten"]),
    ("supp_overfit2@0.5x.png",
     "supp_overfit2_transposed.png",
     ["cylinder", "armadillo", "elephant", "heptotoroid",
      "wrench", "david", "horse", "hand"]),
    ("overfit_eigenvector@0.5x.png",
     "overfit_eigenvector_transposed.png",
     ["lion", "botijo", "fertility", "pegaso"]),
]


def find_runs(boolean_1d):
    """Indices (start, end_inclusive) of every True-run in a 1D bool array."""
    out = []
    i, n = 0, len(boolean_1d)
    while i < n:
        if not boolean_1d[i]:
            i += 1; continue
        j = i
        while j < n and boolean_1d[j]:
            j += 1
        out.append((i, j - 1))
        i = j
    return out


def detect_cells(arr, *, n_shapes, smooth_k=20, thresh_frac=0.01):
    """Return list of (row_y0, row_y1) and (col_x0, col_x1) tuples
    representing every cell-row and every shape-column in the body of
    `arr`. Text labels on the top + left margins are skipped by
    discarding the smallest-area runs at each end."""
    mask = arr[..., 3] > 5  # alpha-aware content mask
    H, W = mask.shape

    # Column runs (use full mask; later we crop horizontally to the body).
    kernel = np.ones(smooth_k) / smooth_k
    col_count = mask.sum(axis=0).astype(float)
    col_smooth = np.convolve(col_count, kernel, mode="same")
    col_thresh = col_smooth.max() * thresh_frac
    col_runs = find_runs(col_smooth >= col_thresh)
    # The last `n_shapes` wide runs are the macro shape-columns. Tiny
    # runs at the start of the file are text labels.
    col_runs_by_w = sorted(col_runs, key=lambda r: r[1] - r[0], reverse=True)
    shape_cols = sorted(col_runs_by_w[:n_shapes], key=lambda r: r[0])

    # Crop horizontally to body and recompute row runs there.
    body_x0 = shape_cols[0][0]
    body_x1 = shape_cols[-1][1]
    body_mask = mask[:, body_x0:body_x1 + 1]
    row_count = body_mask.sum(axis=1).astype(float)
    row_smooth = np.convolve(row_count, kernel, mode="same")
    row_thresh = row_smooth.max() * thresh_frac
    row_runs = find_runs(row_smooth >= row_thresh)
    # The body rows are everything below the header. We keep the runs
    # that are at least, say, 30% of the median run height — this drops
    # the thin header rows.
    heights = np.array([r[1] - r[0] + 1 for r in row_runs])
    median_h = float(np.median(heights))
    body_rows = [r for r in row_runs if (r[1] - r[0] + 1) >= 0.5 * median_h]
    return body_rows, shape_cols


def transpose_grid(in_path: Path, out_path: Path, *, n_shapes=8,
                   cell_w=300, cell_h=260, pad=24,
                   intra_pair_gap=4, shape_names=None):
    """Slice `in_path` into shape × index macro cells and re-emit as a
    transposed grid (`n_shapes` rows × N indices columns) saved at
    `out_path`."""
    im = Image.open(in_path).convert("RGBA")
    arr = np.array(im)

    rows, cols = detect_cells(arr, n_shapes=n_shapes)
    n_indices = len(rows)
    print(f"  {in_path.name}: {n_shapes} shapes × {n_indices} indices "
          f"(grid {len(cols)} cols x {len(rows)} rows in body)")

    # Crop each macro cell (one shape × one index), split into left half
    # (Cot. Lap. = GT) and right half (Ours = Pred), and TRIM each half
    # to the bbox of every connected alpha component above MIN_AREA.
    # Keeping any large component means the rendered shape AND its soft
    # shadow disc both survive; the only thing dropped is the per-cell
    # similarity-score text (digits are ≪ MIN_AREA pixels).
    from scipy.ndimage import label as _cc_label

    MIN_AREA = 600  # px²

    def _alpha_trim(img):
        a = np.array(img)
        if a.shape[2] < 4:
            return img
        mask = a[..., 3] > 10
        if not mask.any():
            return img
        labels, n_cc = _cc_label(mask)
        sizes = np.bincount(labels.ravel())
        sizes[0] = 0
        keep_ids = [cid for cid in range(1, n_cc + 1) if sizes[cid] >= MIN_AREA]
        if not keep_ids:
            keep_ids = [int(sizes.argmax())]
        keep_mask = np.isin(labels, keep_ids)
        ys, xs = np.where(keep_mask)
        bbox = (int(xs.min()), int(ys.min()),
                int(xs.max()) + 1, int(ys.max()) + 1)
        return img.crop(bbox)

    half_w = cell_w
    crops_gt   = []
    crops_pred = []
    for r0, r1 in rows:
        row_gt, row_pred = [], []
        for c0, c1 in cols:
            full = im.crop((c0, r0, c1 + 1, r1 + 1))
            mid = full.width // 2
            row_gt.append(_alpha_trim(full.crop((0, 0, mid, full.height))))
            row_pred.append(_alpha_trim(full.crop((mid, 0, full.width, full.height))))
        crops_gt.append(row_gt)
        crops_pred.append(row_pred)

    n_rows = len(rows)
    n_cols = len(cols)
    # Per-shape scale factor — preserve aspect ratio across all index
    # columns of the SAME shape. Use the union (GT ∪ Pred) maxes.
    scale_per_shape = []
    for c in range(n_cols):
        max_w = max(
            max(crops_gt[r][c].width,   crops_pred[r][c].width)
            for r in range(n_rows)
        )
        max_h = max(
            max(crops_gt[r][c].height,  crops_pred[r][c].height)
            for r in range(n_rows)
        )
        s = min(half_w / max_w, cell_h / max_h)
        scale_per_shape.append(s)

    # Transposed canvas — 2 sub-rows per shape.
    # `pair_h` = GT + small intra-pair gap + Pred; shapes are separated
    # by the wider `pad` so the GT/Pred pairing reads clearly.
    pair_h = 2 * cell_h + intra_pair_gap
    out_w = n_indices * half_w + (n_indices + 1) * pad
    out_h = n_shapes * pair_h + (n_shapes + 1) * pad
    canvas = Image.new("RGBA", (out_w, out_h), (255, 255, 255, 0))

    def _paste(crop, scale, slot_x, slot_y):
        new_w = max(1, int(round(crop.width  * scale)))
        new_h = max(1, int(round(crop.height * scale)))
        scaled = crop.resize((new_w, new_h), Image.LANCZOS)
        x = slot_x + (half_w - new_w) // 2
        y = slot_y + (cell_h  - new_h) // 2
        canvas.paste(scaled, (x, y), scaled)

    for shape_i in range(n_shapes):           # shape row group
        s = scale_per_shape[shape_i]
        pair_y0 = pad + shape_i * (pair_h + pad)
        gt_y    = pair_y0
        pred_y  = pair_y0 + cell_h + intra_pair_gap
        for index_i in range(n_indices):      # eigenvector / k column
            slot_x = pad + index_i * (half_w + pad)
            _paste(crops_gt  [index_i][shape_i], s, slot_x, gt_y)
            _paste(crops_pred[index_i][shape_i], s, slot_x, pred_y)

    canvas.save(out_path)
    print(f"  -> {out_path.name}  ({out_w}x{out_h})")

    # Per-row exports: one PNG per (shape, GT|Pred). Each row is a wide
    # strip showing all n_indices cells for that shape & flavour. We do
    # NOT alpha-trim these strips — every row PNG must keep the same
    # (out_w, cell_h) dimensions so the column slots stay at the same
    # x-positions across rows. That way, stacking the strips as
    # separate <img>s in the slide preserves vertical column alignment.
    if shape_names is None:
        return
    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    for shape_i, shape_name in enumerate(shape_names):
        pair_y0 = pad + shape_i * (pair_h + pad)
        gt_box   = (0, pair_y0,                            out_w,
                    pair_y0 + cell_h)
        pred_box = (0, pair_y0 + cell_h + intra_pair_gap,  out_w,
                    pair_y0 + cell_h + intra_pair_gap + cell_h)
        for tag, box in (("gt", gt_box), ("pred", pred_box)):
            strip = canvas.crop(box)
            # The source-PNG shadow under each shape is very low-alpha
            # (~5/255) AND light-grey (RGB ~ 200), so on a light slide
            # background it's nearly invisible. Repaint the shadow
            # region (alpha 1..59) with a soft mid-grey and gently
            # boost its alpha so it reads as an actual shadow.
            sa = np.array(strip)
            if sa.shape[-1] == 4:
                a_orig = sa[..., 3]
                shadow_mask = (a_orig >= 1) & (a_orig < 60)
                sa[shadow_mask, 0] = 180
                sa[shadow_mask, 1] = 180
                sa[shadow_mask, 2] = 180
                a_f = a_orig.astype(np.float32)
                sa[..., 3] = np.clip(a_f * 4.0, 0, 255).astype(np.uint8)
                strip = Image.fromarray(sa)
            row_path = ROWS_DIR / f"overfit_{shape_name}_{tag}.png"
            strip.save(row_path)
            print(f"     row -> {row_path.relative_to(ROOT)}")


for src, dst, names in INPUTS:
    in_p = ROOT / src
    out_p = ROOT / dst
    if not in_p.exists():
        print(f"[skip] {src} (not found)")
        continue
    transpose_grid(in_p, out_p, n_shapes=len(names), shape_names=names)
