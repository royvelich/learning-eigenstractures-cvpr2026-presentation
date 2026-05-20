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

## File layout

- `slides.md` — the deck (single markdown file, `---` separators between slides)
- `style.css` — global CSS (color palette, utility classes)
- `package.json` — Slidev + theme deps
- `public/` — static assets served at `/`
  - `cvpr2026_logo.png` — CVPR 2026 Denver logo
  - `laplace_beltrami_swiss_knife_transparent.png` — used on slide 2
  - `swiss_knife_transparent.png` — older variant, unused
- `paper_full.pdf` — accepted paper (41 pages)
- `_CVPR_2026__Learning_Eigenstructures...pdf` — rebuttal letter
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

---

## Current deck (8 slides)

| # | Title / theme | Notes |
|---|---|---|
| 1 | **Title** | CVPR 2026 logo as 18% opacity backdrop (top-anchored). Author list, affiliations, Brezis dedication. |
| 2 | **LBO is the workhorse** | Swiss-knife hero image labeled `Laplace–Beltrami Operator`. Eyebrow: "Motivation". |
| 3 | **What its eigendecomposition unlocks** | 3×2 grid of 6 application cards (Shape Descriptors, Correspondence, Manifold Learning, Signal Processing, Geometry Processing, Physics). |
| 4 | **Traditional pipeline** | 4 horizontal cards: Mesh › Stiffness & Mass › Eigensolve ($S\phi = \lambda M\phi$) › Eigenbasis. Titles have `min-height: 2.4rem` for vertical alignment. |
| 5 | **Where the pipeline breaks down** | 3 cards: hard-coded intrinsic dim · no high-d extension · not differentiable (`torch.linalg.eigh` unstable, `torch.lobpcg` no grad). |
| 6 | **The question** | Single big centered H1: "Can we bypass the bottlenecks and learn the eigenbasis…". Tagline: No mesh · No operator · No eigensolver. |
| 7 | **Our approach (pipeline comparison)** | Two pipeline rows: traditional (faded, amber strikethrough on bypassed chips) vs. ours (gradient chips: Point cloud › Neural network › Eigenbasis). Two columns: BYPASSED (amber) / GAINED (emerald). |
| 8 | **Optimal approximation theory** | Signal class $\mathcal{C}_L$, min-max theorem (Aflalo, Brezis, Bruckstein, Kimmel, Sochen 2016) in indigo theorem box. Emerald "So what?" callout: smoothness ⇒ $L=\Delta$ ⇒ optimal basis IS the Laplacian eigenbasis. |

---

## Proposed arc — next slides

| # | Topic | Purpose |
|---|---|---|
| 9 | **Min-max ≡ PCA, signals from $\mathcal{C}_L$** | The dual formulation — averaging out instead of worst-case. Sets up an *expectation* objective, which is what gradient descent likes. |
| 10 | **Probe functions** | Smoothing random functions via Gaussian kernel on kNN graph; "passes the burden from operator choice to probe distribution"; piecewise/polynomial/Schrödinger variants as preview. |
| 11 | **Network architecture** | Transformer extractor on points → per-point features $\Phi_\theta(P) \in \mathbb{R}^{n\times K}$ → QR decomposition → orthonormal basis $Q$. |
| 12 | **$M$-weighted projection** | Why we mix M-weighted projection with Euclidean error norm; first eigenvector = $\sqrt{M}$ encodes density (no separate mass network needed). |
| 13 | **The training loss** | $\mathcal{L}_{rec} = \frac{1}{mK}\sum_{i,k}\|f^{(i)} - f^{(i)}_{\text{proj},k}\|_2^2$; eigenvalues = $1/\max_i\|\text{residual}\|^2$ as inference-time byproduct. |
| 14 | **1D sanity check** | Recover Fourier-like basis on $[0,1]$. |
| 15 | **3D overfitting** | Matches cotangent Laplacian — cosine similarities from Table 1, reconstruction comparison from Fig. 3. |
| 16 | **3D generalization** | Foundation-model trained across SURREAL / SHREC'21 / ABC / FAUST / DeformingThings4D; eclectic test shapes; even handles 3D *volumes* (unseen at training). |
| 17 | **Beyond Laplacians** | Probe family controls implicit operator: piecewise-constant → Walsh-Hadamard, polynomial → polynomial subspace, Schrödinger-like → Hamiltonian basis. |
| 18 | **High-dim manifold learning** | Optimal Approximation Eigenmaps vs. UMAP / t-SNE / PCA / Laplacian Eigenmaps / Isomap on DINOv2 / CLIP embeddings (STL10, CIFAR100, Imagenette, Caltech256). NMI/ARI tables. |
| 19 | **Conclusion + future work + acknowledgments** | Recap; downstream directions (DiffusionNet, LatentFunctionalMaps, FeatUp, scalable dim reduction); thank reviewers + Brezis dedication. |

This is a rough outline — adjust counts, merge / split as needed.

---

## Resuming next session

1. `cd` into this directory.
2. `npm run dev` → open `http://localhost:3030/`.
3. Read this file + skim current `slides.md` to recall design language.
4. Ask Claude: *"what should be the next slide?"* — or pick from the arc table above and say *"build slide N: …"*.
5. Reminder of the math-rendering gotcha (#1 in **Gotchas**) — surround any `$math$` inside a `<div>` with blank lines.
