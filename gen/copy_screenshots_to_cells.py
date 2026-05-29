"""Copy original per-shape screenshots into the cells folders used by
the results slides, re-named with the slide's `{prefix}_{shape}_{flavor}_
{index}.png` convention.

Original screenshot layout:
  overfit_screenshots/<shape>/item_0000_{gt|pred}_eigen{NNN}.png
  overfit_screenshots/<shape>/item_0000_{gt|pred}_recon_k{NNN}.png
  generalization_screenshots/<shape>/<same>

Slide-side cell naming:
  public/applications/overfit_cells/overfit_{shape}_{cot_lap|ours}_{v_N|k_N}.png
  public/applications/generalization_cells/gen_{shape}_{cot_lap|ours}_{v_N|k_N}.png

Mapping conventions:
  • v_N corresponds to file index N-1 (eigen000 = constant, eigen001 = v_2,
    eigen002 = v_3, …).
  • k_N corresponds to recon_k{NNN} with three-digit padding.
  • gt → cot_lap, pred → ours.

Each PNG is alpha-trimmed (largest CC + nearby small CCs for the shadow)
with a small padding so the shape isn't flush against the image edge.
"""
from pathlib import Path
import shutil
import numpy as np
from PIL import Image
from scipy.ndimage import label as _cc_label

ROOT = Path(__file__).resolve().parents[1]

# Source folder name → list of files needed for the cells.
# Each list is the (shape-folder-name, prefix, output-dir, indices) tuple.
OVERFIT_CELLS_DIR = ROOT / "public" / "applications" / "overfit_cells"
GEN_CELLS_DIR = ROOT / "public" / "applications" / "generalization_cells"

# (shape_dir_name, slide_shape_name) — handles spelling differences
# between the screenshot folders and the slide cell naming.
OVERFIT_SHAPES = [
    ("dragon", "dragon"), ("bimba", "bimba"), ("dente", "dente"),
    ("knot", "knot"), ("teddy", "teddy"), ("eros", "eros"),
    ("beetle", "beetle"), ("kitten", "kitten"),
    ("master_cylinder", "cylinder"),
    ("armadillo", "armadillo"), ("elephant", "elephant"),
    ("heptoroid", "heptotoroid"),     # slide uses "heptotoroid"
    ("wrench", "wrench"), ("david", "david"), ("horse", "horse"),
    ("laurent_hand", "hand"),         # slide uses "hand"
    ("lion", "lion"), ("botijo", "botijo"),
    ("fertility", "fertility"), ("pegaso", "pegaso"),
]
OVERFIT_INDICES = ["v_2", "v_3", "v_4", "v_5", "v_6", "v_7",
                   "v_10", "v_11", "v_25", "v_26", "v_40", "v_41",
                   "k_5", "k_25", "k_45"]


def v_to_eigen_idx(v):
    """v_N (1-indexed display, file index N-1)."""
    return int(v.split("_")[1]) - 1


def k_to_recon_str(k):
    """k_N → 'k005', 'k025', …  (zero-padded to 3 digits)."""
    n = int(k.split("_")[1])
    return f"k{n:03d}"


def alpha_trim(img, *, pad=12, min_area=600, proximity=40):
    """Trim to the bbox of the largest CC plus nearby >=min_area CCs (the
    shadow), then pad by `pad` pixels."""
    a = np.array(img)
    if a.shape[2] < 4:
        return img
    mask = a[..., 3] > 10
    if not mask.any():
        return img
    labels, n_cc = _cc_label(mask)
    sizes = np.bincount(labels.ravel())
    sizes[0] = 0
    biggest = int(sizes.argmax())
    big_ys, big_xs = np.where(labels == biggest)
    box = (int(big_xs.min()) - proximity, int(big_ys.min()) - proximity,
           int(big_xs.max()) + proximity, int(big_ys.max()) + proximity)
    adaptive_min = max(min_area, int(sizes[biggest] * 0.01))
    keep = [biggest]
    for cid in range(1, n_cc + 1):
        if cid == biggest or sizes[cid] < adaptive_min:
            continue
        ys_c, xs_c = np.where(labels == cid)
        if (int(xs_c.max()) >= box[0] and int(xs_c.min()) <= box[2] and
                int(ys_c.max()) >= box[1] and int(ys_c.min()) <= box[3]):
            keep.append(cid)
    keep_mask = np.isin(labels, keep)
    arr_clean = a.copy()
    arr_clean[~keep_mask, 3] = 0
    img_clean = Image.fromarray(arr_clean)
    ys, xs = np.where(keep_mask)
    bbox = (
        max(0, int(xs.min()) - pad),
        max(0, int(ys.min()) - pad),
        min(img.width,  int(xs.max()) + 1 + pad),
        min(img.height, int(ys.max()) + 1 + pad),
    )
    return img_clean.crop(bbox)


def process(src_path: Path, dst_path: Path):
    img = Image.open(src_path).convert("RGBA")
    img = alpha_trim(img)
    img.save(dst_path)


import re
_ITEM_RE = re.compile(r"^(item_\d+)_")


def detect_item_stem(shape_dir: Path):
    """Find the `item_NNNN` stem actually used inside `shape_dir`."""
    for f in shape_dir.iterdir():
        m = _ITEM_RE.match(f.name)
        if m:
            return m.group(1)
    return None


def export_set(screenshot_root: Path, shapes, indices, out_dir: Path, prefix: str):
    out_dir.mkdir(parents=True, exist_ok=True)
    missing, written, skipped_dirs = [], 0, []
    for src_shape, slide_shape in shapes:
        shape_dir = screenshot_root / src_shape
        if not shape_dir.exists() or not any(shape_dir.iterdir()):
            skipped_dirs.append(src_shape)
            continue
        stem = detect_item_stem(shape_dir)
        if stem is None:
            skipped_dirs.append(src_shape)
            continue
        for idx in indices:
            if idx.startswith("v_"):
                file_idx = v_to_eigen_idx(idx)
                gt_src   = shape_dir / f"{stem}_gt_eigen{file_idx:03d}.png"
                pred_src = shape_dir / f"{stem}_pred_eigen{file_idx:03d}.png"
            else:
                rk = k_to_recon_str(idx)
                gt_src   = shape_dir / f"{stem}_gt_recon_{rk}.png"
                pred_src = shape_dir / f"{stem}_pred_recon_{rk}.png"
            for src, flavor in ((gt_src, "cot_lap"), (pred_src, "ours")):
                if not src.exists():
                    missing.append(str(src))
                    continue
                dst = out_dir / f"{prefix}_{slide_shape}_{flavor}_{idx}.png"
                process(src, dst)
                written += 1
    print(f"  -> {written} cells written to {out_dir.name}")
    if skipped_dirs:
        print(f"  ! skipped {len(skipped_dirs)} empty/missing dirs: {skipped_dirs}")
    if missing:
        print(f"  ! missing {len(missing)} files (first 3: {missing[:3]})")


print("Processing overfit screenshots…")
export_set(ROOT / "overfit_screenshots", OVERFIT_SHAPES, OVERFIT_INDICES,
           OVERFIT_CELLS_DIR, "overfit")

# Generalization — list the shape sub-folders that exist.
gen_root = ROOT / "generalization_screenshots"
if gen_root.exists():
    print("Processing generalization screenshots…")
    GEN_INDICES = ["v_2", "v_3", "v_11", "v_31", "k_10", "k_50"]
    gen_shapes = [(d.name, d.name) for d in sorted(gen_root.iterdir()) if d.is_dir()]
    export_set(gen_root, gen_shapes, GEN_INDICES, GEN_CELLS_DIR, "gen")
