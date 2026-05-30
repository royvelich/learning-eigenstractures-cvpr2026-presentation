# CVPR 2026 Poster

`poster.tex` — 213 × 107 cm landscape, 4 columns, Libertinus font (matches the deck).

## Build

Requires **LuaLaTeX** (for `fontspec` + `unicode-math`) and the **Libertinus** font installed system-wide (or via `texlive-fontsutils`).

```bash
cd poster
lualatex poster.tex
lualatex poster.tex   # run twice for refs / page counts
```

Output: `poster.pdf` at exactly 213 × 107 cm.

## Layout

```
┌───────────────────────────────────────────────────────────────────────┐
│  TITLE  ·  authors  ·  affiliation  ·  CVPR 2026 oral                  │
├──────────────┬──────────────┬──────────────┬──────────────────────────┤
│ Motivation   │ Method       │ Results      │ Beyond the LBO            │
│ Background:  │ Pipeline at  │ Generalization│ Image manifold           │
│ the LBO      │ a glance     │ Learned       │ Take-aways               │
│              │              │ metric        │ Acknowledgements & code  │
└──────────────┴──────────────┴──────────────┴──────────────────────────┘
```

## Figures

The `.tex` references `figures/{pipeline,overfit_grid,generalization_grid,areas_pred_grid,schrodinger_grid,nmi_ari_bars}.pdf`. Drop your renders into `poster/figures/`. PDF is preferred (vector); high-res PNG also works.

To export from the Slidev deck:
1. `slidev export --range 8` (or whichever slide) for a single-slide PDF.
2. Or render directly from the `gen/*.py` scripts that produced the deck figures.
