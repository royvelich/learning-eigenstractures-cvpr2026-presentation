"""Inject per-(shape, eigenvector) cosine-similarity labels into the four
overfit / generalization slides (16, 17, 18, 19).

For each `gt_eigenXXX.png` image tag in those slides' grids, we read the
matching `..._cosine_similarities.txt` (in either `overfit_screenshots/`
or `generalization_screenshots/`) and wrap the image in a relative
container with a small absolutely-positioned label that floats just
below the Cot. Lap. cell.

Reconstruction columns (recon_k005/025/050) are left alone — the score
file only carries per-eigenvector cosine sim.

Idempotent: lines already wrapped (starting with `<div class="cos-cell">`)
are skipped by the regex match.

Run:
    gen/.venv/Scripts/python.exe gen/add_cosine_labels.py
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SLIDES = ROOT / "slides.md"
PUBLIC = ROOT / "public"

# Two-phase line match: detect an <img ... /> line that references a
# gt_eigen<XX> screenshot under either screenshot folder, then pull the
# folder / shape / item / eigen index out of the URL substring.
# Use `.*?` (not `[^>]*`) because attrs include `>` inside `$clicks >= 1`.
IMG_LINE = re.compile(
    r'^(?P<indent>\s*)<img\b.*?(?:overfit|generalization|rebuttal)_screenshots/'
    r'.*?gt_eigen\d+\.png.*?/>\s*$'
)
URL_PARTS = re.compile(
    r'(?P<folder>(?:overfit|generalization|rebuttal)_screenshots)/'
    r'(?P<shape>[^/]+)/item_(?P<item>\d+)_gt_eigen(?P<idx>\d+)\.png'
)

# Title fragments that identify the slides we want to process.
SLIDE_TITLE_FRAGMENTS = (
    'Train on different <span class="grad">samplings</span> of a single shape.',
    'Train on many shapes, test on <span class="grad">unseen</span> shapes.',
    'Experiments on the <span class="grad">Schrödinger</span> operator.',
)

# Cache of (folder, shape, item) -> {eigen_idx: score}
_score_cache: dict[tuple[str, str, str], dict[int, float]] = {}


def _load_scores(folder: str, shape: str, item: str) -> dict[int, float]:
    key = (folder, shape, item)
    if key in _score_cache:
        return _score_cache[key]
    path = PUBLIC / folder / shape / f"item_{item}_cosine_similarities.txt"
    scores: dict[int, float] = {}
    if path.exists():
        for line in path.read_text().splitlines():
            m = re.match(r"\s*Eigenvector\s+(\d+):\s+([0-9.]+)", line)
            if m:
                scores[int(m.group(1))] = float(m.group(2))
    _score_cache[key] = scores
    return scores


def _wrap(line: str) -> str | None:
    stripped = line.rstrip("\n")
    m_line = IMG_LINE.match(stripped)
    if not m_line:
        return None
    m_url = URL_PARTS.search(stripped)
    if not m_url:
        return None
    indent = m_line.group("indent")
    folder = m_url.group("folder")
    shape = m_url.group("shape")
    item = m_url.group("item")
    idx = int(m_url.group("idx"))
    scores = _load_scores(folder, shape, item)
    if idx not in scores:
        return None
    score = scores[idx]
    img_html = line.strip()
    # Color-code: green if >= 0.75, amber if 0.5-0.75, red below.
    if score >= 0.75:
        color = "#047857"
    elif score >= 0.5:
        color = "#b45309"
    else:
        color = "#b91c1c"
    label = (
        f'<div class="cosine-label" style="color: {color}">'
        f"{score:.2f}</div>"
    )
    return f'{indent}<div class="cos-cell">{img_html}{label}</div>\n'


# Match a previously wrapped line so we can strip it and re-wrap fresh
# (so threshold / color changes propagate on re-run).
UNWRAP_PATTERN = re.compile(
    r'^(?P<indent>\s*)<div class="cos-cell">(?P<img><img\b.*?/>)'
    r'<div class="cosine-label".*?>[^<]+</div></div>\s*$'
)


def _maybe_unwrap(line: str) -> str:
    """If `line` is a cos-cell wrapper, return the bare <img> line so the
    main `_wrap` can re-process it with the current thresholds."""
    m = UNWRAP_PATTERN.match(line.rstrip("\n"))
    if not m:
        return line
    return f"{m.group('indent')}{m.group('img')}\n"


def main() -> None:
    text = SLIDES.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Unwrap any existing labels so re-running with updated colors /
    # thresholds rewrites them from scratch.
    unwrapped = 0
    for i, line in enumerate(lines):
        new_line = _maybe_unwrap(line)
        if new_line is not line:
            lines[i] = new_line
            unwrapped += 1
    if unwrapped:
        print(f"[..] unwrapped {unwrapped} previously labelled cells")

    # Find every slide whose H2 starts with our title prefix.  For each
    # such slide, wrap gt_eigen images between the title line and the
    # next top-level `---` separator.
    slide_starts = [
        i for i, line in enumerate(lines)
        if any(frag in line for frag in SLIDE_TITLE_FRAGMENTS)
    ]
    print(f"[..] found {len(slide_starts)} target slides")

    total_edited = 0
    for s_idx, start in enumerate(slide_starts):
        # End of this slide = next `---` line on its own.
        end = len(lines)
        for i in range(start + 1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        edited = 0
        for i in range(start, end):
            wrapped = _wrap(lines[i])
            if wrapped is not None:
                lines[i] = wrapped
                edited += 1
        print(f"     slide #{s_idx + 1}: lines {start + 1}..{end} — wrapped {edited} cells")
        total_edited += edited

    print(f"[ok] wrapped {total_edited} Cot. Lap. images total")
    SLIDES.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
