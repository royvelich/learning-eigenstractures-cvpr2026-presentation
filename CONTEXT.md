# Presentation Context

CVPR 2026 oral presentation for *Learning Eigenstructures of Unstructured Data Manifolds*.

**Authors:** Roy Velich, Arkadi Piven, David Bensaïd, Daniel Cremers, Thomas Dagès, Ron Kimmel
**Dedication:** In memory of Haïm Brezis (1944–2024)

---

## How to run

```powershell
npm run dev          # starts Slidev on http://localhost:3030/
```

Useful URLs:
| URL | Purpose |
|---|---|
| `/` | slideshow |
| `/presenter/` | notes + timer + next-slide preview |
| `/overview/` | grid of all slides |
| `/export/` | PDF export |

Hot-reload is on — edits to `slides.md` / `style.css` reflect instantly.

---

## Setup on a new machine

**To present / edit the deck (Node only — this is all that's needed):**

```bash
npm ci          # exact install from package-lock.json — use `ci`, NOT `install`
npm run dev     # → http://localhost:3030/
```

- Use **`npm ci`, not `npm install`**: several deps are pinned to `"latest"` in `package.json`, so only the committed `package-lock.json` guarantees a reproducible tree.
- All figures are committed PNGs under `public/`, so **no Python is required just to run or present.**

**To regenerate figures (optional — only when changing the `gen/` image generators):**

```bash
cd gen
python -m venv .venv && source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
```

- `gen/requirements.txt`: numpy, scipy, pyvista, libigl, trimesh, scikit-learn, matplotlib, pillow.
- Heads-up: `libigl` + `pyvista` / VTK can be fiddly on Apple Silicon — expect possible install friction.

**Known-good versions** (Roy's dev machine, 2026-06): Node **v24** (Slidev v52 needs ≥ 20), npm **11**, Python **3.12**, `@slidev/cli` **52.15.2**. These are **not pinned** in the repo (no `.nvmrc` / `engines` / `==` versions).

**Pinning is intentionally left optional.** When setting up on a new machine, **ASK Roy first** whether he wants a pinned/reproducible environment or just the latest:
- **Pinned** → add `.nvmrc` (or an `engines` field) for Node, and freeze Python (`pip freeze > gen/requirements.txt`, add a `.python-version`).
- **Unpinned** → just `npm ci` + an unpinned `pip install -r gen/requirements.txt`; accept whatever's latest.

Don't pin unprompted — Roy wants to decide per-setup.

---

## File layout

- `slides.md` — the deck (single markdown file, `---` separators between slides; also holds many `hide: true` slides)
- `transcripts/` — spoken-narration drafts for the ~5-min video (see "Video transcript" below)
- `style.css` — global CSS (color palette, utility classes)
- `package.json` — Slidev + theme deps
- `public/` — static assets served at `/`
  - `cvpr2026_logo.png` — CVPR 2026 Denver logo
  - `laplace_beltrami_swiss_knife_transparent.png` — used on slide 2
  - `swiss_knife_transparent.png` — older variant, unused
- `_CVPR_2026__Learning_Eigenstructures_of_Unstructured_Data_Manifolds (1).pdf` — the accepted paper
- `_CVPR_2026__Learning_Eigenstructures_of_Unstructured_Data_Manifolds.pdf` — the rebuttal letter
- `paper_full.pdf` — full paper incl. supplementary (41 pages; gitignored, local only)
- `old_presentation.pdf` — earlier version of the talk (38 slides)
- `AflaoBrezisBrucksteinKimmelSochen_CRMA2016.pdf` — **Brezis et al. 2016**, "Best bases for signal spaces" (CRAS, 13 pp). Source of Theorem 2.1 (min-max optimality of eigenvectors, α_k = 1/λ_{k+1}) and §5 (relation to PCA over C_L). Cited on slides 9/10.

---

## Tech stack

- **Slidev v52** with theme `@slidev/theme-seriph`
- `colorSchema: light` (white background)
- **KaTeX** for math via `$...$` (inline) and `$$...$$` (display)
- **UnoCSS** for utility classes (Tailwind-like)

---

## Design system

### Palette (CSS variables in `style.css`)

| Token | Hex | Use |
|---|---|---|
| `--c-bg` | `#ffffff` | slide background |
| `--c-bg-soft` | `#f8fafc` | card backgrounds |
| `--c-border` | `#e2e8f0` | card borders |
| `--c-fg` | `#0f172a` | headings |
| `--c-fg-body` | `#1f2937` | body |
| `--c-fg-muted` | `#475569` | secondary |
| `--c-fg-subtle` | `#94a3b8` | eyebrow labels |
| `--c-brand-from` → `--c-brand-to` | `#4E4376` → `#2B5876` | indigo → teal gradient (titles + key terms) |
| `--c-accent` | `#b45309` | amber-700 — warnings, `<em>`, bypassed |
| `--c-success` | `#047857` | emerald-700 — gains, implications |
| `--c-link` | `#1d4ed8` | links |

### Utility classes

- `.grad` / `.lbo` — applies brand gradient on text
- `.eyebrow` — small uppercase tracked label above slide titles
- `.muted` — slate-600 secondary text

---

## Gotchas (hard-won)

1. **Math inside HTML blocks does NOT render** unless there are **blank lines** around the content. Markdown-it treats `<div>…content…</div>` as a single passthrough block and skips inline parsing. Fix: split content with blank lines so markdown re-enters parsing mode.

   ```html
   <div class="card">

   Body with $math$ and **bold**.

   </div>
   ```

2. **`vh` / `vw` measure the browser viewport, not the slide canvas.** Slidev canvas is fixed at 980×552. Use `flex-1 min-h-0` + `max-h-full` for images that should fit the remaining space, not `max-h-[60vh]`.

3. **`<br/>` inside an `<h1>` with blank lines breaks line-height** because each line gets wrapped in its own `<p>`. Keep multiline headings as one continuous HTML block (no internal blank lines); use `!leading-[1.6]` for spacing.

4. **Image `<img src="/...">` in markdown breaks Vite on Windows** — the path resolves to `C:\...` and gets blocked by `fs.allow`. Use dynamic binding instead:

   ```html
   <img :src="`${$slidev.configs.base ?? '/'}image.png`" />
   ```

5. **Titles in a multi-card row need a `min-height`** to align if some titles wrap and others don't. Reserve room for the worst-case wrap count.

6. **Staggered "all on one click" reveals** use CSS `transition-delay`, not multiple `v-click` stops. Bind each element's `opacity` (and `transform`) to `$clicks >= N` via `:style`, and put a `transition` + a per-element `transition-delay` staircase in the static `style`. Vue merges static `style` and `:style`, so positioning/transition live in one and the animated props in the other. Set an explicit `clicks: N` in frontmatter so Slidev registers the intermediate stop even when no element literally carries `v-click="N"`. (See slide 3's `Δ(f)=Δf` assembly, and the `$clicks >= 2 ? 9 : 0` stage-image swap on slides 4/5.)

7. **Numbered-badge + pastel-box pattern** (slide 12): make the box `position: relative`, drop an absolutely-positioned `.thm-num` circle at `top:-11px; left:-11px`, and give each box a light pastel via a per-box class. The happy palette in use: sky `#e0f2fe`/`#38bdf8`, violet `#ede9fe`/`#a78bfa`, green `#dcfce7`/`#4ade80`, peach `#ffedd5`/`#fb923c`. The same pastels color-code the slide-10 pipeline chips by role (input/output/network/skipped).

---

## Video transcript (in progress)

Roy is writing the spoken narration for a **~5-minute presentation video** (the full skeleton currently runs ~6:00, so there's trimming to do). Drafts live in `transcripts/`:

- `full_draft_6min.txt` — end-to-end skeleton with `[SLIDE N · click X — Ys]` cues.
- `slide01_title.txt`, `slide02_laplacian.txt`, `slide02_laplacian_short.txt` — early per-slide drafts (full + short variants).
- `slide02_laplacian_short.txt` is being **repurposed as the running consolidated transcript** — Roy pastes the agreed short narration for each slide (currently slides 2–12) into it, keyed by `slide N:` / `[click K]`.

How Roy likes transcript work (see memory `feedback-transcript-style`): **short, simple, viewer-friendly**, mapped to the slide's exact click structure, with a tighter length variant offered so he can pick. Causal claims must be technically precise (e.g. on slide 9 he wanted neighborhood-extraction→discrete, operator-assembly→explicit, eigensolve→non-differentiable — each cause matched to the right pipeline step).

## Slide numbering convention

When the user says "slide N," they mean the **N-th visible slide counting the title as slide 1 and skipping `hide: true` slides** — i.e. presentation order, not the position in `slides.md`. Always map a requested number through the live visible order (a quick parse of `slides.md` for `---` blocks + `hide:` flags), because the file also holds a large bank of hidden slides interleaved among the visible ones.

## Branch: `elongated-version` — the long talk (54 visible slides)

Work since 2026-06 happens on the **`elongated-version`** branch (forked from `main`), an expanded version of the talk that inserts intuition-building "warm-up" and "application elaboration" sections with heavily-animated, generated figures (many as autoplay/looping **GIFs**). `main` keeps the tighter ~27-slide version below.

What was added on this branch (all figures generated by `gen/gen_22 … gen_30`):

- **Eigenbasis warm-ups & reconstruction** (after the curved-domains slide): an R³ eigenbasis warm-up (3×3 PSD matrix, rotating turntable GIF, reconstruct a vector with K=1→2→3) → per-domain **eigenfunction galleries** (1D / 2D / curved) → **eigen-reconstruction** animations (target | reconstruction | residual, K-ladder) on interval, square, and the armadillo (`gen_22`, `gen_23`, `gen_30`).
- **Shape descriptors (HKS)** — heat-diffusion intuition, few-points→all (field at scale $t^\star$), and a 3-scale RGB pose-invariance payoff across horse-gallop poses (`gen_24`).
- **Shape correspondence (functional maps)** — across-shapes line reveal, "one map many transfers" (texture / part-segmentation / horse→camel animation GIFs), N! is hard, $b=C\mathbf a$ as a change of coordinates, near-diagonal $C$, delta transport (`gen_25`, `gen_26`).
- **Mesh smoothing / curvature flow** — $\Delta X = 2HN$ built from the coordinate functions (rotating curvature-vector sphere GIF) + a bumpy-sphere mean-curvature-flow smoothing GIF (`gen_27`).
- **Discretizing Δ** — "a surface is a discrete mesh" (smooth → vertices+edges → function-on-vertices → highlighted 1-ring), assembling a row of the **stiffness matrix $S$** (cotangent weights as an example), the **mass matrix $M$** & why we normalize (Voronoi cell vs. 1-to-4 refined cell → $A_i'\approx\tfrac14A_i$), and the summary $L = M^{-1}S$ (`gen_28`, `gen_29`).
- **Convention:** stiffness = $S$, mass = $M$, Laplacian operator $L = M^{-1}S$.
- **Unhidden from the bank:** the 1D-DCT best-$k$-term slide (before the 2D one), the pegaso "train low-res (3K) → infer high-res (12K)" rebuttal slide, and "Predicted vertex areas / sampling density". ("Predicted metric" was unhidden then re-hidden.)

**GIF rendering pattern (reused across `gen_22+`):** render frames to PNG/array, crop all to a *common* bounding box (so the shape doesn't jump), `PIL` `save_all` as a looping GIF; for turntables rotate the **geometry** per frame (pyvista's `camera.Azimuth` doesn't re-render) about the area-weighted centroid with a single fixed camera.

---

## Core arc (the ~27-slide `main` version)

The deck is a full talk, not the old 8-slide draft. Many older / alternate / detailed-results / closing slides remain in `slides.md` as `hide: true` and do **not** appear in the deck.

| # | Title | Notes |
|---|---|---|
| 1 | **Title** | CVPR 2026 logo backdrop, authors, Brezis dedication. |
| 2 | **The Laplacian** (intuition) | Point cloud → scalar signal → focal point → "deviation from local average" → Δf heatmap. |
| 3 | **The Laplacian** (operator) `c3` | Linear PSD operator; `Δ(f)=Δf` self-assembles on click 2 (staggered); spectral-decomposition line on click 3. |
| 4 | **Laplacian on Euclidean domains** `c4` | graphs → points/balls/Δf-labels → per-dim formulas → `Δf=-div(grad f)`. Stage-9 image revealed on click 2. |
| 5 | **Laplacian on curved domains** `c3` | graph → geodesic balls/labels → Laplace–Beltrami formula. |
| 6 | **The LBO is the swiss knife** | Swiss-knife hero image. |
| 7 | **A single spectral basis — many families of tools** | 3×2 application grid (descriptors, correspondence, manifold learning, geodesics, mesh smoothing, deformation) + "…and more". |
| 8 | **Computing the eigenstructure, the traditional way** | Two-track pipeline (mesh/cotangent + kNN/Belkin–Niyogi): neighborhood → operator → eigensolve → basis. |
| 9 | **Three properties of the traditional pipeline** `c6` | discrete / explicit / not-differentiable, each struck through → continuous / implicit / differentiable. |
| 10 | **Our approach** (pipeline) | Traditional row → middle struck → Ours: Point cloud › Neural network › Eigenbasis. **Light pastel chips, color-coded by role.** |
| 11 | **Our approach** (principle) | *Operator construction → Probe-function design* (click 1); objective (click 2) + "LBO eigenbasis falls out on its own" (click 3). |
| 12 | **The optimal *k*-term basis is the eigenbasis of *L*** `c4` | Aflalo–Brezis–Bruckstein–Kimmel–Sochen 2016. **2×2 four-box** layout, numbered badges + happy pastels: (1) class $\mathcal{C}_L$, (2) $p_L=\text{Uniform}$, (3) optimal basis $=\{\mathbf{v}_1,\dots,\mathbf{v}_k\}$, (4) worst-case error $1/\lambda_{k+1}$. |
| 13 | **Best *k*-truncated basis on curved domains** `c7` | Laplace–Beltrami eigenbasis. |
| 14 | **Our pipeline** `c23` | The full method, heavily animated. |
| 15–16 | **Train on different samplings of a single shape** | Overfit / single-shape results. |
| 17 | **Train on many shapes, test on unseen shapes** `c3` | Generalization. |
| 18 | **Experiments on volumetric shapes** | No mesh, volumetric LBO. |
| 19 | **Hadamard probe distributions** | Probe family swap. |
| 20 | **Schrödinger operator** `c5` | Swap −Δ → −Δ+V. |
| 21 | **Train low-res, infer high-res** `c2` | Sampling-agnostic. |
| 22 | **Predicted vertex areas / sampling density** `c1` | Density encoded by first eigenvector ($\sqrt{M}$). |
| 23 | **Setup** (image manifold) | CLIP / DINOv2 embeddings as a data manifold. |
| 24–25 | **STL10 clusters — CLIP / DINOv2** | Image-manifold qualitative. |
| 26 | **Quantitative comparison — NMI & ARI** | vs UMAP / t-SNE / PCA / LE. |
| 27 | **Summary** | Recap. |

Hidden bank (in-file, `hide: true`): "Maximizing variance ⇔ minimizing reconstruction error"; the two "Best *k*-truncated basis" theory slides (3D toy, 1D/2D images); an alternate "Train on many shapes…"; a full block of how-we-learn / training-algorithm / "Plug in Δ" / full-pipeline / single-3D-shape result detail (cosine similarity, oracle eigenfunctions I/II, predicted metric, generalize, image-manifold detail, Imagenette/STL10, trade-offs); the **Thank you!** closing; and an **"Animation test — armadillo clones"** v-motion prototype.

---

## Resuming next session

1. `cd` into this directory.
2. `npm run dev` → open `http://localhost:3030/`.
3. Read this file + skim current `slides.md` to recall design language.
4. Ask Claude: *"what should be the next slide?"* — or pick from the arc table above and say *"build slide N: …"*.
5. Reminder of the math-rendering gotcha (#1 in **Gotchas**) — surround any `$math$` inside a `<div>` with blank lines.
