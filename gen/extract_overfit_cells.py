"""Per-cell PNGs for the overfit results slides.

Slices each of the three qualitative-comparison source PNGs into one
PNG per (shape, flavor, index) cell, named so the slide layout can pull
them by file name. The slide-side grid then handles alignment, so we
never have to worry about any row strip getting clipped — each cell is
its own image.

Output layout:

  public/applications/overfit_cells/overfit_{shape}_{flavor}_{idx}.png

  shape  ∈ {dragon, bimba, …, lion, botijo, …}
  flavor ∈ {cot_lap, ours}
  idx    ∈ {v_2, v_3, v_4, v_5, v_6, v_7,
            v_10/v_11, v_25/v_26, v_40/v_41,
            k_5, k_25, k_45}                       (per source)
"""
from pathlib import Path
import numpy as np
from PIL import Image
from scipy.ndimage import label as _cc_label

ROOT = Path(__file__).resolve().parents[1]

# Each entry: (source PNG, output dir, shape names, index labels).
INPUTS = [
    ("supp_overfit1@0.5x.png",
     ROOT / "public" / "applications" / "overfit_cells",
     "overfit",
     ["dragon", "bimba", "dente", "knot", "teddy", "eros", "beetle", "kitten"],
     ["v_2", "v_3", "v_4", "v_5", "v_6", "v_7", "v_11", "v_26", "v_41",
      "k_5", "k_25", "k_45"]),
    ("supp_overfit2@0.5x.png",
     ROOT / "public" / "applications" / "overfit_cells",
     "overfit",
     ["cylinder", "armadillo", "elephant", "heptotoroid",
      "wrench", "david", "horse", "hand"],
     ["v_2", "v_3", "v_4", "v_5", "v_6", "v_7", "v_11", "v_26", "v_41",
      "k_5", "k_25", "k_45"]),
    ("overfit_eigenvector@0.5x.png",
     ROOT / "public" / "applications" / "overfit_cells",
     "overfit",
     ["lion", "botijo", "fertility", "pegaso"],
     ["v_2", "v_3", "v_4", "v_5", "v_6", "v_7", "v_10", "v_25", "v_40",
      "k_5", "k_25", "k_45"]),
    ("generalization_qualitative1.png",
     ROOT / "public" / "applications" / "generalization_cells",
     "gen",
     ["g1_s1", "g1_s2", "g1_s3", "g1_s4", "g1_s5"],
     ["v_2", "v_3", "v_11", "v_31", "k_10", "k_50"]),
    ("generalization_qualitative2.png",
     ROOT / "public" / "applications" / "generalization_cells",
     "gen",
     ["g2_s1", "g2_s2", "g2_s3", "g2_s4", "g2_s5"],
     ["v_2", "v_3", "v_11", "v_31", "k_10", "k_50"]),
]

# Alpha trim — keep every connected alpha component above MIN_AREA so
# the shape AND its faint shadow disc are preserved; components smaller
# than that (the similarity-score digits) are dropped. BBOX_PAD adds a
# few transparent pixels around the trimmed bbox so the rendered shape
# doesn't look "cropped" tight against the image edge in the slide.
MIN_AREA = 600
BBOX_PAD = 12
SHADOW_RGB = 180
SHADOW_ALPHA_BOOST = 4.0


def find_runs(b):
    """Return [(start, end_inclusive), …] for every True-run in b."""
    out = []
    i, n = 0, len(b)
    while i < n:
        if not b[i]:
            i += 1
            continue
        j = i
        while j < n and b[j]:
            j += 1
        out.append((i, j - 1))
        i = j
    return out


def detect_cells(arr, *, n_shapes, smooth_k=20, thresh_frac=0.01):
    """Detect (cell_rows, shape_cols, mids) in the body of `arr`.

    `shape_cols` is a list of (c0, c1) macro-column bounds (one per
    shape) and `mids` is a list of GT/Ours split points (one per shape).
    Two layouts are supported:
      • Cot.Lap. and Ours touch each other inside the macro column
        (overfit files) — detection finds `n_shapes` wide runs and the
        split point is the run's centre.
      • Cot.Lap. and Ours are visibly separated (generalization files)
        — detection finds `2 * n_shapes` wide runs which are paired up;
        the split point is the centre of the gap between the two runs
        of each pair.
    """
    mask = arr[..., 3] > 5
    kernel = np.ones(smooth_k) / smooth_k

    col_count = mask.sum(axis=0).astype(float)
    col_smooth = np.convolve(col_count, kernel, mode="same")
    col_thresh = col_smooth.max() * thresh_frac
    col_runs = find_runs(col_smooth >= col_thresh)

    # Wide runs only — drops the thin annotation/text runs.
    MIN_WIDE_RUN_W = 100
    wide = [r for r in col_runs if (r[1] - r[0] + 1) >= MIN_WIDE_RUN_W]

    if len(wide) >= 2 * n_shapes:
        # Paired layout — each shape spans two adjacent wide runs.
        wide_top = sorted(wide, key=lambda r: r[1] - r[0], reverse=True)[: 2 * n_shapes]
        wide_top = sorted(wide_top, key=lambda r: r[0])
        shape_cols, mids = [], []
        for i in range(0, len(wide_top), 2):
            a, b = wide_top[i], wide_top[i + 1]
            shape_cols.append((a[0], b[1]))
            mids.append((a[1] + b[0]) // 2)
    else:
        # Unified layout — each shape is one wide run, split at centre.
        top = sorted(wide, key=lambda r: r[1] - r[0], reverse=True)[:n_shapes]
        shape_cols = sorted(top, key=lambda r: r[0])
        mids = [(c0 + c1) // 2 for (c0, c1) in shape_cols]

    body_x0 = shape_cols[0][0]
    body_x1 = shape_cols[-1][1]
    row_count = mask[:, body_x0:body_x1 + 1].sum(axis=1).astype(float)
    row_smooth = np.convolve(row_count, kernel, mode="same")
    row_thresh = row_smooth.max() * thresh_frac
    row_runs = find_runs(row_smooth >= row_thresh)
    heights = np.array([r[1] - r[0] + 1 for r in row_runs])
    median_h = float(np.median(heights))
    body_rows = [r for r in row_runs if (r[1] - r[0] + 1) >= 0.5 * median_h]
    return body_rows, shape_cols, mids


PROXIMITY_MARGIN = 40  # px — distance from main shape's bbox within which
                       # secondary components (the shadow blob) are kept;
                       # anything farther away is treated as a stray
                       # fragment from an adjacent cell and discarded.


def trim_and_boost(img, core_x_bounds=None):
    """Trim the image to the largest connected component (the rendered
    shape) plus any nearby connected components (e.g. the shadow blob),
    dropping everything that's too far away — those are spill-over
    fragments from adjacent cells.
    """
    a = np.array(img)
    if a.shape[2] < 4:
        return img
    mask = a[..., 3] > 10
    if not mask.any():
        return img

    labels, n_cc = _cc_label(mask)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0

    # Main shape = largest connected component.
    biggest_id = int(sizes.argmax())
    big_ys, big_xs = np.where(labels == biggest_id)
    big_box = (int(big_xs.min()) - PROXIMITY_MARGIN,
               int(big_ys.min()) - PROXIMITY_MARGIN,
               int(big_xs.max()) + PROXIMITY_MARGIN,
               int(big_ys.max()) + PROXIMITY_MARGIN)

    # Adaptive minimum: secondary components must be both above the
    # fixed MIN_AREA floor AND at least 1% of the main shape's pixel
    # count. The latter scales with image resolution so that annotation
    # text (which is comparable across image sizes when measured as a
    # FRACTION of the shape) is filtered out consistently.
    adaptive_min = max(MIN_AREA, int(sizes[biggest_id] * 0.01))

    keep_ids = [biggest_id]
    for cid in range(1, n_cc + 1):
        if cid == biggest_id or sizes[cid] < adaptive_min:
            continue
        ys_c, xs_c = np.where(labels == cid)
        # Keep iff this component's bbox overlaps the main shape's
        # expanded bbox.
        if (int(xs_c.max()) >= big_box[0] and int(xs_c.min()) <= big_box[2] and
                int(ys_c.max()) >= big_box[1] and int(ys_c.min()) <= big_box[3]):
            keep_ids.append(cid)
    keep_mask = np.isin(labels, keep_ids)

    # Zero out alpha for every pixel that isn't in a kept component.
    # bbox crop is rectangular, so stray fragments (e.g. tiny 30-px
    # spill-over from an adjacent cell) would otherwise still appear
    # inside the bbox rectangle even though they failed MIN_AREA /
    # proximity filtering. Blanking them removes those artifacts.
    arr_clean = np.array(img).copy()
    arr_clean[~keep_mask, 3] = 0
    img_clean = Image.fromarray(arr_clean)

    ys, xs = np.where(keep_mask)
    bbox = (
        max(0, int(xs.min()) - BBOX_PAD),
        max(0, int(ys.min()) - BBOX_PAD),
        min(img.width,  int(xs.max()) + 1 + BBOX_PAD),
        min(img.height, int(ys.max()) + 1 + BBOX_PAD),
    )
    cropped = img_clean.crop(bbox)

    # Shadow is left untouched — the source PNG's natural shadow shows
    # through whatever the slide background is.
    return cropped


def extract_source(src_name, out_dir, prefix, shape_names, index_names):
    in_p = ROOT / src_name
    if not in_p.exists():
        print(f"[skip] {src_name}")
        return
    im = Image.open(in_p).convert("RGBA")
    arr = np.array(im)
    rows, cols, mids = detect_cells(arr, n_shapes=len(shape_names))
    print(f"{src_name}: {len(rows)} rows x {len(cols)} shape-cols detected")

    if len(rows) != len(index_names):
        print(f"  ! row mismatch: detected {len(rows)}, expected {len(index_names)}")
    if len(cols) != len(shape_names):
        print(f"  ! col mismatch: detected {len(cols)}, expected {len(shape_names)}")

    # For each shape column, compute an EXPANDED bounding range that
    # includes half the gap to the neighbouring shape. Some renders
    # (e.g. the botijo k=5) spill past the alpha-density-detected
    # column edge, and the expansion lets the alpha-trim recover them.
    # GT/Ours still split at the ORIGINAL column midpoint so pairing
    # stays correct.
    # For the FIRST/LAST shape, the "neighbour" is the image edge —
    # cap that outer padding at MAX_EDGE_PAD so the first shape doesn't
    # reach the row labels (e.g. "v_2") that sit in the source margin.
    MAX_EDGE_PAD = 25
    expanded = []
    for i, (c0, c1) in enumerate(cols):
        if i > 0:
            left_pad = (c0 - cols[i-1][1] - 1) // 2
        else:
            left_pad = min(MAX_EDGE_PAD, c0)
        if i + 1 < len(cols):
            right_pad = (cols[i+1][0] - c1 - 1) // 2
        else:
            right_pad = min(MAX_EDGE_PAD, im.width - 1 - c1)
        expanded.append((c0 - left_pad, c1 + right_pad))

    for r_i, (r0, r1) in enumerate(rows[:len(index_names)]):
        idx = index_names[r_i]
        for c_i in range(len(shape_names)):
            shape = shape_names[c_i]
            orig_c0, orig_c1 = cols[c_i]
            exp_c0, exp_c1 = expanded[c_i]
            mid = mids[c_i]

            # Core x-range (in crop-local coords) covers ONLY the original
            # cell column — components mostly inside this range belong to
            # this cell, components mostly outside are adjacent-cell spill.
            gt_crop = im.crop((exp_c0, r0, mid, r1 + 1))
            gt_core = (orig_c0 - exp_c0, mid - exp_c0)
            gt = trim_and_boost(gt_crop, core_x_bounds=gt_core)

            pred_crop = im.crop((mid, r0, exp_c1 + 1, r1 + 1))
            pred_core = (0, orig_c1 - mid + 1)
            pred = trim_and_boost(pred_crop, core_x_bounds=pred_core)

            out_dir.mkdir(parents=True, exist_ok=True)
            gt_path   = out_dir / f"{prefix}_{shape}_cot_lap_{idx}.png"
            pred_path = out_dir / f"{prefix}_{shape}_ours_{idx}.png"
            gt.save(gt_path)
            pred.save(pred_path)
    print(f"  -> {2 * len(shape_names) * len(index_names)} cells written")


for src, out_dir, prefix, shapes, indices in INPUTS:
    extract_source(src, out_dir, prefix, shapes, indices)
