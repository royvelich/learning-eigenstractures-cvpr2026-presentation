---
theme: seriph
title: Learning Eigenstructures of Unstructured Data Manifolds
info: |
  ## Learning Eigenstructures of Unstructured Data Manifolds
  CVPR 2026 — Oral
  Roy Velich, Arkadi Piven, David Bensaïd, Daniel Cremers, Thomas Dagès, Ron Kimmel
colorSchema: light
class: text-center
highlighter: shiki
lineNumbers: false
drawings:
  persist: false
transition: slide-left
mdc: true
fonts:
  sans: 'Inter'
  serif: 'EB Garamond'
  mono: 'JetBrains Mono'
---

<!-- CVPR 2026 logo as a large background watermark, anchored to the top -->
<div class="absolute inset-0 flex items-start justify-center pointer-events-none z-0 pt-8">
  <img
    :src="`${$slidev.configs.base ?? '/'}cvpr2026_logo.png`"
    alt=""
    class="w-[85%] max-h-[40%] object-contain"
    style="opacity: 0.18;"
  />
</div>

<div class="relative z-10 flex flex-col items-center justify-center h-full">

<div class="eyebrow mb-6">
CVPR 2026 &nbsp;·&nbsp; Oral Presentation
</div>

<h1 class="!text-5xl !leading-tight !mb-8 max-w-4xl grad">
Learning Eigenstructures of<br/>Unstructured Data Manifolds
</h1>

<div class="text-lg mb-2" style="color: var(--c-fg-body)">
Roy Velich<sup>1</sup> &nbsp;·&nbsp; Arkadi Piven<sup>1</sup> &nbsp;·&nbsp; David Bensaïd<sup>1</sup>
</div>
<div class="text-lg mb-6" style="color: var(--c-fg-body)">
Daniel Cremers<sup>2,3</sup> &nbsp;·&nbsp; Thomas Dagès<sup>1,2,3</sup> &nbsp;·&nbsp; Ron Kimmel<sup>1</sup>
</div>

<div class="text-sm muted max-w-5xl whitespace-nowrap">
<sup>1</sup>Technion — Israel Institute of Technology &nbsp;·&nbsp;
<sup>2</sup>Technical University of Munich &nbsp;·&nbsp;
<sup>3</sup>Munich Center for Machine Learning
</div>

</div>

<div class="abs-b w-full text-center pb-6 text-xs italic muted z-10">
In memory of Haïm Brezis (1944 – 2024)
</div>

---
layout: default
class: text-center
---

<div class="flex flex-col items-center h-full pt-5 pb-4 text-center">

<div class="eyebrow mb-3">
Primer · the Laplacian, intuitively
</div>

<div class="relative w-[78%] max-w-[560px]" style="aspect-ratio: 5.6 / 3.4;">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_grey.png`"
    class="absolute inset-0 w-full h-full object-contain"
    v-click.hide="1"
  />
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_coloured.png`"
    class="absolute inset-0 w-full h-full object-contain"
    v-click="[1, 2]"
  />
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_focal.png`"
    class="absolute inset-0 w-full h-full object-contain"
    v-click="[2, 4]"
  />
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_laplacian.png`"
    class="absolute inset-0 w-full h-full object-contain"
    v-click="4"
  />
</div>

<div v-click="3" class="mt-4">

<h1 class="!text-3xl !leading-tight max-w-5xl font-serif grad italic">
deviation from local average
</h1>

</div>

</div>

---
layout: default
class: text-center
---

<div class="h-full relative">

<div class="absolute top-6 left-0 right-0 text-center">
  <div class="eyebrow">Primer · the Laplacian as an operator</div>
</div>

<!-- Click 1: header line appears -->
<div v-click="1" class="absolute left-0 right-0 text-center text-2xl !leading-snug" style="top: 60px;">

it's a linear, positive semi-definite (PSD) operator

</div>

<!-- Click 2: f-cloud appears at centre. Click 3: f-cloud scales down & slides left. -->
<div
  v-click="2"
  v-motion
  :initial="{ x: 0, scale: 1 }"
  :click-3="{ x: -150, scale: 0.50 }"
  class="absolute"
  style="top: 137px; left: 260px;"
>
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_coloured.png`"
    style="width: 460px; display: block;"
    alt="f, the input function"
  />
</div>

<!-- Δ on the left (click 3) -->
<div v-click="3" class="absolute math-grad"
     style="top: 50%; left: 130px; font-size: 60px; transform: translateY(calc(-50% + 8px));">

$\Delta$

</div>

<!-- ( opening paren -->
<div v-click="3" class="absolute"
     style="top: 50%; left: 205px; font-size: 60px; color: var(--c-fg-muted); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  (
</div>

<!-- ) closing paren -->
<div v-click="3" class="absolute"
     style="top: 50%; left: 450px; font-size: 60px; color: var(--c-fg-muted); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  )
</div>

<!-- = sign (click 4) -->
<div v-click="4" class="absolute"
     style="top: 50%; left: 510px; font-size: 48px; color: var(--c-fg); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  =
</div>

<!-- Δf-cloud, the output (click 5) -->
<img v-click="5"
  :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_laplacian_full.png`"
  class="absolute"
  style="top: 50%; left: 560px; transform: translateY(-50%); width: 230px;"
  alt="Δf, the Laplacian output"
/>

<!-- Eigendecomposition motivator: appears AFTER the illustration is built (click 6). -->
<div v-click="6" class="absolute left-0 right-0 text-center text-2xl !leading-snug" style="bottom: 40px;">

its <span class="lbo">spectral decomposition</span> consists of <em>eigenfunctions</em> and <em>eigenvalues</em>

</div>

</div>

---
layout: default
class: text-center
clicks: 23
---

<div class="h-full flex flex-col pt-2 pb-1 px-6 text-center">

<div class="eyebrow mb-0">
Primer · in Euclidean space
</div>

<h2 class="!text-xl !leading-snug !mb-1 font-serif" style="color: var(--c-fg)">
Same question — the neighbourhood is a <span class="lbo">unit ball</span>.
</h2>

<div class="flex-1 min-h-0 grid grid-cols-2 gap-x-8 gap-y-0" style="grid-template-rows: 1fr auto auto;">

<!-- Reveal 1D first (clicks 1–10), then 2D (clicks 12–21).
     Per-side progression: function → red point → red ball → Δf > 0
     → blue point → blue ball → Δf < 0 → grey point → grey ball → Δf ≈ 0.
     The Laplacian formula for each side appears only AFTER that side's
     diagram is fully revealed (1D math: click 11, 2D math: click 22).
     The unifying div-of-grad statement comes last, click 23. -->
<div class="min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_euclidean_1d_stage_${Math.min(Math.max($clicks - 1, 0), 9)}.png`"
    :style="{ opacity: $clicks >= 1 ? 1 : 0 }"
    class="max-h-full max-w-full object-contain"
    alt="Laplacian setup on R — focal x0 with interval neighbourhood"
  />
</div>

<div class="min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_euclidean_2d_stage_${Math.min(Math.max($clicks - 12, 0), 9)}.png`"
    :style="{ opacity: $clicks >= 12 ? 1 : 0 }"
    class="max-h-full max-w-full object-contain"
    alt="Laplacian setup on R^2 — focal x0 with disk neighbourhood"
  />
</div>

<div class="text-center flex items-center justify-center" :style="{ opacity: $clicks >= 11 ? 1 : 0, fontSize: '14px' }">

$\Delta f = \dfrac{d^2 f}{dx^2}$

</div>

<div class="text-center flex items-center justify-center" :style="{ opacity: $clicks >= 22 ? 1 : 0, fontSize: '14px' }">

$\Delta f = \dfrac{\partial^2 f}{\partial u^2} + \dfrac{\partial^2 f}{\partial v^2}$

</div>

<div class="text-center flex items-center justify-center" :style="{ opacity: $clicks >= 23 ? 1 : 0, fontSize: '22px', gridColumn: '1 / -1' }">

in general, $\Delta f \;=\; \operatorname{div}\bigl(\operatorname{grad} f\bigr)$ &nbsp;—&nbsp; the <span class="lbo">divergence of the gradient</span>.

</div>

</div>

</div>

---
layout: default
class: text-center
clicks: 11
---

<div class="h-full flex flex-col pt-2 pb-2 px-2 text-center">

<div class="eyebrow mb-0">
Primer · on a curved domain
</div>

<h2 class="!text-lg !leading-snug !mb-1 font-serif" style="color: var(--c-fg)">
Same question — the domain itself is now a <span class="lbo">curved manifold</span>.
</h2>

<!-- Click-driven reveal (clicks 1–10) of the same staged scene used in
     gen_16: domain + f-sheet, then red / blue / grey focal points with
     their geodesic disks and Δf labels. The LBO formula appears only
     after the diagram is fully revealed (click 11). -->
<div class="flex-1 min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_curved_2d_stage_${Math.min(Math.max($clicks - 1, 0), 9)}.png`"
    :style="{ opacity: $clicks >= 1 ? 1 : 0, height: '100%' }"
    class="max-h-full max-w-full object-contain"
    alt="curved domain M with the function f as a sheet floating above it"
  />
</div>

<div class="text-center mt-1" :style="{ opacity: $clicks >= 11 ? 1 : 0, fontSize: '18px' }">

$\Delta_M f \;=\; \operatorname{div}_M\!\big(\nabla_M f\big)$ &nbsp;·&nbsp; the <span class="lbo">Laplace–Beltrami operator</span> (LBO)

</div>

</div>

---
layout: default
class: text-center
---

<div class="flex flex-col items-center h-full pt-6 pb-4 text-center">

<div class="eyebrow mb-3">
Motivation
</div>

<h2 class="!text-3xl !leading-snug !mb-4 max-w-5xl font-serif">
The <span class="lbo">LBO</span> is the <em>swiss knife</em> of geometry processing.
</h2>

<div class="flex-1 min-h-0 w-full flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}laplace_beltrami_swiss_knife_transparent.png`"
    alt="The LBO as a Swiss army knife of geometry processing"
    class="max-h-full max-w-full object-contain drop-shadow-xl"
  />
</div>

</div>

---
layout: default
class: text-left
---

<div class="h-full flex flex-col pt-6 pb-4 px-2">

<div class="eyebrow mb-2 text-center">
Motivation &nbsp;·&nbsp; What its eigendecomposition unlocks
</div>

<h2 class="!text-2xl !leading-snug !mb-6 font-serif text-center" style="color: var(--c-fg)">
A single spectral basis &mdash; <span class="grad">many families of tools</span>.
</h2>

<div class="grid grid-cols-3 gap-x-6 gap-y-2 flex-1 min-h-0">

<div class="app-tile" v-click="1">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_01_descriptors.png`" alt="Shape descriptors" />
  <div class="app-cap">Shape descriptors</div>
</div>

<div class="app-tile" v-click="2">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_02_corr_lion.png`" alt="Shape correspondence" />
  <div class="app-cap">Shape correspondence</div>
</div>

<div class="app-tile" v-click="3">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_03_manifold_learning.png`" alt="Manifold learning" />
  <div class="app-cap">Manifold learning</div>
</div>

<div class="app-tile" v-click="4">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_05_geometry_processing.png`" alt="Geodesics" />
  <div class="app-cap">Geodesics</div>
</div>

<div class="app-tile" v-click="5">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_07_mesh_smoothing.png`" alt="Mesh smoothing" />
  <div class="app-cap">Mesh smoothing</div>
</div>

<div class="app-tile" v-click="6">
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_09_arap_horse.png`" alt="Shape deformation" />
  <div class="app-cap">Shape deformation</div>
</div>

</div>

<div v-click="7" class="text-center mt-3 muted italic" style="font-size: 0.95rem;">
…and more.
</div>

</div>

<style>
.app-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-height: 0;
}
.app-tile img {
  flex: 1 1 0;
  min-height: 0;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.app-cap {
  font-weight: 600;
  font-size: 0.85rem;
  color: var(--c-fg);
  margin-top: 0.25rem;
  letter-spacing: -0.005em;
  text-align: center;
}
</style>

---
layout: default
class: text-left
---

<div class="h-full flex flex-col pt-2 pb-2 px-2">

<div class="eyebrow mb-0 text-center">
Background &nbsp;·&nbsp; Two pipelines for the same eigenstructure
</div>

<h2 class="!text-2xl !leading-snug !mb-1 font-serif text-center" style="color: var(--c-fg)">
Computing the Laplacian eigenstructure, <span class="grad">two ways</span>
</h2>

<div class="flex-1 min-h-0 pipe-grid-2">

<!-- Stage titles (row 1) -->
<div class="pipe-title" style="grid-column: 2; grid-row: 1;" v-click="1">Neighborhood extraction</div>
<div class="pipe-title" style="grid-column: 4; grid-row: 1;" v-click="3">Operator extraction</div>
<div class="pipe-title" style="grid-column: 6; grid-row: 1;" v-click="4">Eigensolve</div>
<div class="pipe-title" style="grid-column: 8; grid-row: 1;" v-click="5">Eigenbasis</div>

<!-- Vertical branch labels (column 1) -->
<div class="pipe-branch-label" style="grid-column: 1; grid-row: 2;">

2-manifold in $\mathbb{R}^3$

</div>
<div class="pipe-branch-label" style="grid-column: 1; grid-row: 3;">

$k$-manifold embedded in $\mathbb{R}^n$

</div>

<!-- Vertical separators between stages (span both content rows). -->
<div class="pipe-sep" style="grid-column: 3; grid-row: 2 / span 2;"></div>
<div class="pipe-sep" style="grid-column: 5; grid-row: 2 / span 2;"></div>
<div class="pipe-sep" style="grid-column: 7; grid-row: 2 / span 2;"></div>

<!-- ──────── UPPER ROW : mesh / cotangent (row 2) ──────── -->
<div class="pipe-img-wrap relative" style="grid-column: 2; grid-row: 2;">
  <img
    v-click="1"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_vertices.png`"
    class="absolute inset-0 m-auto pipe-img"
    alt="Vertices"
  />
  <img
    v-click="2"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_triangulation.png`"
    class="absolute inset-0 m-auto pipe-img"
    alt="Triangle mesh"
  />
</div>

<div class="pipe-img-wrap" style="grid-column: 4; grid-row: 2;" v-click="3">
  <img :src="`${$slidev.configs.base ?? '/'}applications/pipeline_voronoi_cot.png`" class="pipe-img" alt="Voronoi cell and cotangent angles" />
</div>

<div class="pipe-eq-only" style="grid-column: 6; grid-row: 2;" v-click="4">

$S\boldsymbol{\phi} = \lambda\, M\boldsymbol{\phi}$

</div>

<div class="pipe-eq-only" style="grid-column: 8; grid-row: 2;" v-click="5">

$\{\boldsymbol{\phi}_i\},\; \{\lambda_i\}$

</div>

<!-- ──────── LOWER ROW : graph / Belkin–Niyogi (row 3) ──────── -->
<!-- Same vertices as upper row; just connect k-NN edges (spokes only —
     NO triangulation). -->
<div class="pipe-img-wrap relative" style="grid-column: 2; grid-row: 3;">
  <img
    v-click="6"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_vertices.png`"
    class="absolute inset-0 m-auto pipe-img"
    alt="Point cloud"
  />
  <img
    v-click="7"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_knn_graph.png`"
    class="absolute inset-0 m-auto pipe-img"
    alt="k-NN graph (spokes only — not a triangulation)"
  />
</div>

<div class="pipe-img-wrap" style="grid-column: 4; grid-row: 3;" v-click="8">
  <img :src="`${$slidev.configs.base ?? '/'}applications/pipeline_heat_weights.png`" class="pipe-img" alt="Heat-kernel edge weights and degree" />
</div>

<div class="pipe-eq-only" style="grid-column: 6; grid-row: 3;" v-click="9">

$L\mathbf{y} = \lambda\, D\mathbf{y}$

</div>

<div class="pipe-eq-only" style="grid-column: 8; grid-row: 3;" v-click="10">

$\{\mathbf{y}_i\},\; \{\lambda_i\}$

</div>

</div>

</div>

<style>
.pipe-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr;
  grid-template-rows: auto 1fr auto;
  column-gap: 0.5rem;
  row-gap: 0.4rem;
  width: 100%;
  align-items: stretch;
}
.pipe-grid-2 {
  /* Column 1: branch labels (2-manifold / k-manifold), vertical text.
     Columns 2, 4, 6, 8: stage content. Columns 3, 5, 7: thin separators. */
  display: grid;
  grid-template-columns: auto 1fr auto 1fr auto 1fr auto 1fr;
  grid-template-rows: auto 1fr 1fr;
  column-gap: 0.6rem;
  row-gap: 0.2rem;
  width: 100%;
  height: 100%;
  align-items: stretch;
}
.pipe-branch-label {
  align-self: center;
  justify-self: start;
  text-align: left;
  font-style: italic;
  font-size: 0.95rem;
  color: var(--c-fg-muted);
  letter-spacing: -0.005em;
  padding-right: 0.5rem;
  max-width: 9.5rem;
  line-height: 1.15;
}
.pipe-branch-label p { margin: 0; padding: 0; }
.pipe-branch-label .katex { font-size: inherit; color: inherit; }
.pipe-sep {
  width: 1px;
  background: var(--c-fg-subtle);
  opacity: 0.45;
  justify-self: center;
  align-self: stretch;
}
.pipe-img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.pipe-title {
  font-weight: 700;
  font-size: 1rem;
  color: var(--c-fg);
  letter-spacing: -0.01em;
  line-height: 1.2;
  text-align: center;
}
.pipe-img-wrap {
  min-height: 0;
  min-width: 0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.pipe-img-wrap img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.pipe-eq-only {
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  font-size: 1.2rem;
  color: var(--c-fg-body);
}
.pipe-caption {
  text-align: center;
  font-size: 1.2rem;
  color: var(--c-fg-body);
  min-height: 1.4em;
}
.pipe-arrow {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 200;
  color: var(--c-fg-subtle);
  line-height: 1;
  padding: 0 0.1rem;
  font-family: 'EB Garamond', serif;
}

.assumption-callout {
  border-left: 3px solid var(--c-accent);
  background: rgba(180, 83, 9, 0.06);
  padding: 0.7rem 1rem;
  border-radius: 4px;
}
.assumption-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--c-accent);
  margin-bottom: 0.25rem;
}
.assumption-text {
  color: var(--c-fg-body);
  font-size: 0.9rem;
  line-height: 1.5;
}
</style>

---
layout: default
class: text-left
clicks: 6
---

<div class="h-full flex flex-col pt-6 pb-4 px-2">

<div class="eyebrow mb-2 text-center">
Background &nbsp;·&nbsp; What the traditional pipeline really is
</div>

<h2 class="!text-2xl !leading-snug !mb-8 font-serif text-center" style="color: var(--c-fg)">
Explicit, discrete, and <span class="grad">not differentiable</span>.
</h2>

<div class="grid grid-cols-3 gap-8 flex-1 min-h-0 bottleneck-grid">

<div class="bottleneck-tile" v-click="1">
  <div class="bottleneck-img-wrap bottleneck-delta">

$\Delta$

  </div>
  <div class="bottleneck-cap">
    <div class="cap-line" :class="{ 'crossed': $clicks >= 4 }">explicit</div>
    <div class="cap-line cap-new" v-if="$clicks >= 4">implicit</div>
  </div>
</div>

<div class="bottleneck-tile" v-click="2">
  <div class="bottleneck-img-wrap">
    <img :src="`${$slidev.configs.base ?? '/'}applications/pipeline_triangulation.png`" alt="Triangulation of a 2-manifold" />
  </div>
  <div class="bottleneck-cap">
    <div class="cap-line" :class="{ 'crossed': $clicks >= 5 }">discrete</div>
    <div class="cap-line cap-new" v-if="$clicks >= 5">continuous</div>
  </div>
</div>

<div class="bottleneck-tile" v-click="3">
  <div class="bottleneck-img-wrap">
    <img :src="`${$slidev.configs.base ?? '/'}applications/bottleneck_no_grad.png`" alt="No backpropagation" />
  </div>
  <div class="bottleneck-cap">
    <div class="cap-line" :class="{ 'crossed': $clicks >= 6 }">not differentiable</div>
    <div class="cap-line cap-new" v-if="$clicks >= 6">differentiable</div>
  </div>
</div>

</div>

</div>

<style>
.bottleneck-tile {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  min-height: 0;
}
.bottleneck-img-wrap {
  flex: 1 1 0;
  min-height: 0;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}
.bottleneck-img-wrap img {
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.bottleneck-img-wrap img {
  /* Slightly smaller images so the captions can breathe. */
  max-height: 78%;
  max-width: 78%;
  object-fit: contain;
}
.bottleneck-cap {
  margin-top: 0.8rem;
  font-weight: 700;
  font-size: 1.7rem;
  color: var(--c-fg);
  text-align: center;
  letter-spacing: -0.005em;
  min-height: 3.4em;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 0.2rem;
  line-height: 1.15;
}
.bottleneck-cap p {
  margin: 0;
}
.cap-line {
  transition: text-decoration 200ms ease, color 200ms ease;
}
.cap-line.crossed {
  text-decoration: line-through;
  text-decoration-thickness: 3px;
  color: var(--c-fg-subtle);
}
.cap-new {
  background-image: linear-gradient(135deg, var(--c-brand-from), var(--c-brand-to));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}
.bottleneck-delta {
  /* Render the big Δ symbol at the same vertical size as the other column
     images. Slightly smaller now so the larger captions have more room. */
  font-size: 11rem;
  font-weight: 200;
  line-height: 0.9;
  color: var(--c-fg);
  letter-spacing: 0;
}
.bottleneck-delta .katex { font-size: inherit; color: inherit; }
.bottleneck-delta p { margin: 0; padding: 0; line-height: 1; }
</style>

---
layout: default
class: text-left
---

<div class="h-full flex flex-col pt-6 pb-4 px-2">

<div class="eyebrow mb-2 text-center">
Our approach
</div>

<h2 class="!text-2xl !leading-snug !mb-8 font-serif text-center" style="color: var(--c-fg)">
Skip the operator. <span class="grad">Learn the eigenbasis directly.</span>
</h2>

<!-- Both rows share one CSS grid so the chips align column-by-column.
     Row 1: Traditional label (centered above its chips, spans all chip cols).
     Row 2: Traditional chips.
     Row 3: Ours label.
     Row 4: Ours chips. -->
<div class="pipeline-shared-grid mb-8">

<!-- Traditional label + chips (clicks 1 / 2) -->
<div class="pipeline-row-label" style="grid-column: 1 / -1; grid-row: 1;" v-click="1">Traditional</div>
<div class="chip chip-hero" style="grid-column: 1; grid-row: 2;" v-click="1">Point cloud</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 2; grid-row: 2;" v-click="1">›</div>
<div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }" style="grid-column: 3; grid-row: 2;" v-click="1">Neighborhood extraction</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 4; grid-row: 2;" v-click="1">›</div>
<div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }" style="grid-column: 5; grid-row: 2;" v-click="1">Operator extraction</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 6; grid-row: 2;" v-click="1">›</div>
<div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }" style="grid-column: 7; grid-row: 2;" v-click="1">Eigensolve</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 8; grid-row: 2;" v-click="1">›</div>
<div class="chip chip-hero" style="grid-column: 9; grid-row: 2;" v-click="1">Eigenbasis</div>

<!-- Ours label + chips (click 3). Neural network spans grid columns 3..7,
     left edge = "Neighborhood extraction" left, right edge = "Eigensolve" right. -->
<div class="pipeline-row-label ours-label" style="grid-column: 1 / -1; grid-row: 3;" v-click="3">Ours</div>
<div class="chip chip-hero" style="grid-column: 1; grid-row: 4;" v-click="3">Point cloud</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 2; grid-row: 4;" v-click="3">›</div>
<div class="chip chip-hero chip-net" style="grid-column: 3 / span 5; grid-row: 4;" v-click="3">Neural network</div>
<div class="chip-arrow chip-arrow-hero" style="grid-column: 8; grid-row: 4;" v-click="3">›</div>
<div class="chip chip-hero" style="grid-column: 9; grid-row: 4;" v-click="3">Eigenbasis</div>

</div>

</div>

<style>
.pipeline-block {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.pipeline-row-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--c-fg-subtle);
  text-align: center;
  margin-bottom: 0.4rem;
}
.ours-label {
  color: var(--c-brand-from);
  font-weight: 600;
}
.pipeline-row-static {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.pipeline-row-grid {
  /* 5 stage columns (1, 3, 5, 7, 9) interleaved with 4 arrow columns
     (2, 4, 6, 8) — same template for both rows so the Ours' wide
     "Neural network" chip (spans 3 / span 5) lines up exactly with the
     three middle Traditional stages plus the two arrows between them. */
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr auto 1fr;
  align-items: center;
  justify-items: stretch;
  column-gap: 0.5rem;
}
.pipeline-row-grid .chip {
  justify-self: stretch;
  text-align: center;
}
.pipeline-row-grid .chip-arrow {
  justify-self: center;
}
.pipeline-shared-grid {
  /* Single grid for BOTH pipeline rows so the 5 stage columns share
     widths between rows. All chip + arrow columns are content-sized
     (auto) so each chip is only as wide as its text + padding — the
     two middle chips (Neighborhood / Operator extraction) shrink to
     fit their text instead of stretching to a 1fr share. The whole
     row is then centred via justify-content. The Ours-row "Neural
     network" chip spans grid columns 3..7, so its left edge sits at
     "Neighborhood extraction"'s left edge and its right edge at
     "Eigensolve"'s right edge. */
  display: grid;
  grid-template-columns: auto auto auto auto auto auto auto auto auto;
  grid-template-rows: auto auto auto auto;
  column-gap: 0.5rem;
  row-gap: 0.45rem;
  align-items: center;
  justify-items: stretch;
  justify-content: center;
}
.pipeline-shared-grid .chip {
  justify-self: stretch;
  text-align: center;
  padding: 0.5rem 0.6rem;
  font-size: 0.92rem;
  /* Allow long labels ("Neighborhood extraction", "Operator extraction")
     to wrap onto two lines so the chip stays NARROWER. All chips share a
     min-height so single-line and two-line chips line up nicely. */
  white-space: normal;
  word-break: normal;
  overflow-wrap: break-word;
  max-width: 110px;
  min-height: 3.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1.15;
}
.pipeline-shared-grid .chip-net {
  /* Neural network spans 5 columns — let it stretch across the full
     spanned width instead of being clamped by the per-chip max-width. */
  max-width: none;
  padding: 0.5rem 0.8rem;
}
.pipeline-shared-grid .chip-arrow { justify-self: center; }
.pipeline-shared-grid .pipeline-row-label {
  justify-self: center;
  text-align: center;
  margin-bottom: 0;
}
/* Vertical breathing room between the Traditional row and the Ours row */
.pipeline-shared-grid .ours-label {
  margin-top: 2.8rem;
}
.chip-bypassed {
  opacity: 0.55;
  text-decoration: line-through;
  text-decoration-color: #b91c1c;
  text-decoration-thickness: 3px;
  box-shadow: none;
  transition: opacity 220ms ease, text-decoration-color 220ms ease;
}

.chip {
  padding: 0.4rem 0.85rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  background: var(--c-bg-soft);
  font-size: 0.82rem;
  color: var(--c-fg-body);
  white-space: nowrap;
}
.chip-skip {
  text-decoration: line-through;
  text-decoration-color: var(--c-accent);
  text-decoration-thickness: 2px;
  color: var(--c-fg-subtle);
}
.chip-arrow {
  color: var(--c-fg-subtle);
  font-size: 1.3rem;
  font-family: 'EB Garamond', serif;
  line-height: 1;
}
.trad-row { opacity: 0.7; }

.chip-hero {
  padding: 0.55rem 1.1rem;
  font-size: 0.95rem;
  font-weight: 600;
  color: white;
  background-image: linear-gradient(135deg, var(--c-brand-from), var(--c-brand-to));
  border: none;
  box-shadow: 0 4px 12px rgba(43, 88, 118, 0.18);
}
.chip-net {
  padding: 0.55rem 1.6rem;
  font-weight: 700;
}
.chip-arrow-hero {
  color: var(--c-brand-to);
  font-size: 1.6rem;
  font-weight: 600;
}

.benefit-card {
  padding: 0.85rem 1.1rem;
  border: 1px solid var(--c-border);
  border-radius: 10px;
  background: var(--c-bg-soft);
}
.benefit-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.65rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-bottom: 0.5rem;
  font-weight: 600;
}
.bypass-label { color: var(--c-accent); }
.gain-label   { color: var(--c-success); }

.benefit-card ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}
.benefit-card li {
  position: relative;
  padding-left: 1rem;
  margin-top: 0.3rem;
  font-size: 0.88rem;
  color: var(--c-fg-body);
  line-height: 1.45;
}
.benefit-card li:first-child { margin-top: 0; }
.benefit-card li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.55rem;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--c-fg-subtle);
}
.bypass-label + ul li::before { background: var(--c-accent); }
.gain-label   + ul li::before { background: var(--c-success); }
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Foundation &nbsp;·&nbsp; PCA's defining identity
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
Maximizing variance <span class="grad">&hArr;</span> minimizing reconstruction error.
</h2>

<div class="setup-row mb-3">

Project signal $f$ on <strong>any</strong> orthonormal basis $\{b_i\}_{i=1}^k$ &nbsp;&rarr;&nbsp; decompose $f = \mathrm{proj} + \mathrm{residual}$.

</div>

<div class="grid grid-cols-[1fr_auto_1fr] items-stretch gap-3 mb-3">

<div class="duality-box">

<div class="duality-label">Maximize what we keep</div>

<div class="def-line">

$\mathrm{proj} = \sum_{i=1}^k \langle f, b_i\rangle b_i$

</div>

<div class="eq-row">

$$\max_{\{b_i\}}\; \|\mathrm{proj}\|^2$$

</div>

Captured variance / projection energy.

</div>

<div class="equiv">&hArr;</div>

<div class="duality-box">

<div class="duality-label">Minimize what we miss</div>

<div class="def-line">

$\mathrm{residual} = f - \sum_{i=1}^k \langle f, b_i\rangle b_i$

</div>

<div class="eq-row">

$$\min_{\{b_i\}}\; \|\mathrm{residual}\|^2$$

</div>

Reconstruction / least-squares loss.

</div>

</div>

<div class="why-line mt-auto">

<span class="why-label">Why?</span> &nbsp;Pythagoras: $\|f\|^2 = \|\mathrm{proj}\|^2 + \|\mathrm{residual}\|^2$, and $\|f\|^2$ is fixed &mdash; <strong>what we lose mirrors what we keep</strong>.

</div>

</div>

<style>
.setup-row {
  text-align: center;
  font-size: 0.88rem;
  line-height: 1.4;
  color: var(--c-fg-body);
}
.duality-box {
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.7rem 1.0rem;
  border-radius: 8px;
  font-size: 0.85rem;
  line-height: 1.45;
  color: var(--c-fg-body);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.duality-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 600;
  margin-bottom: 0.35rem;
}
.why-line {
  text-align: center;
  font-size: 0.85rem;
  line-height: 1.45;
  color: var(--c-fg-body);
  border-left: 3px solid var(--c-success);
  background: rgba(4, 120, 87, 0.06);
  padding: 0.5rem 1.0rem;
  border-radius: 4px;
}
.why-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--c-success);
  font-weight: 600;
}
</style>

---
layout: default
class: text-left
clicks: 10
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Optimal approximation theory &nbsp;·&nbsp; Aflalo, Brezis et&nbsp;al. (2016)
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Recover the <span class="grad">eigenbasis</span> <em>and</em> the <span class="grad">eigenvalues</span> of <i>L</i>.
</h2>

<!-- Click-by-click reveal — two sequential build-ups on the same canvas.
     Each PNG shares the same alpha-tight crop, so swapping the visible
     image by $clicks just adds (or resets) content without nudging
     anything else on screen.
       Sequence A (flat basis):
         click 0 → blank
         click 1 → xyz axes + v
         click 2 → flat basis + grid + v   (axes removed)
         click 3 → + projections c1 b1, c2 b2
         click 4 → + reconstructed v_proj
         click 5 → + residual v - v_proj
       Sequence B (slightly tilted basis):
         click 6 → axes + v                (clean reset)
         click 7 → tilted basis + tilted grid + v
         click 8 → + tilted projections
         click 9 → + tilted v_proj
         click 10 → + tilted (smaller) residual -->
<div class="flex-1 min-h-0 relative px-4 optimal-stage-host">
  <div class="absolute inset-0 flex items-center justify-center">
    <div class="optimal-stage-wrap">
      <img v-for="n in 10" :key="n"
           v-click="[n, n + 1]"
           class="optimal-stage"
           :src="`${$slidev.configs.base ?? '/'}applications/optimal_basis_step${n}.png`"
           :alt="`stage ${n}`" />
    </div>
  </div>
</div>

</div>

<style>
.optimal-stage-wrap {
  position: relative;
  height: 100%;
  /* aspect ratio matches the cropped APNG canvases (717 / 677 ≈ 1.059) */
  aspect-ratio: 717 / 677;
}
.caption-row {
  position: relative;
  min-height: 1.6em;       /* reserve a single line of caption space */
  text-align: center;
  font-size: 0.95rem;
  color: var(--c-fg-body);
}
.caption-line {
  position: absolute;
  inset: 0;
  transition: opacity 200ms ease;
}
.caption-line p { margin: 0; }
.optimal-stage {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: opacity 250ms ease;
}
</style>

---
layout: default
class: text-left
clicks: 6
---

<div class="h-full flex flex-col pt-4 pb-3 px-2 relative">

<div class="eyebrow mb-1 text-center">
Constructive special case &nbsp;·&nbsp; Euclidean domains with boundary
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
On a curve or an image, this eigenbasis is the <span class="grad">DCT</span>.
</h2>

<!-- Click flow:
       click 1 → 1D sample signal fades in
       click 2 → 1D cosine modes fade in (smooth reveal)
       click 3 → 2D sample image fades in
       click 4 → 2D cosine product modes fade in
       click 5 → 1D signal + 2D image fade out AND modes glide up to the
                 top of their column (modes don't change size)
       click 6 → "Neumann eigenbasis" caption fades in below the modes -->
<div class="flex-1 min-h-0 grid grid-cols-[1.15fr_1fr] gap-10 px-6 items-stretch"
     :class="{ 'modes-up': $clicks >= 5 }">

<!-- 1D — the curve [0, L] -->
<div class="dct-col">
  <img class="dct-sample dct-reveal" :class="{ 'is-on': $clicks >= 1 && $clicks < 5 }"
       :src="`${$slidev.configs.base ?? '/'}applications/dct_1d_sample.png`"
       alt="A smooth 1D signal on [0, L]" />
  <img class="dct-basis dct-reveal" :class="{ 'is-on': $clicks >= 2 }"
       :src="`${$slidev.configs.base ?? '/'}applications/dct_1d_basis.png`"
       alt="1D DCT cosine modes on [0, L]" />

  <div class="dct-formula dct-reveal" :class="{ 'is-on': $clicks >= 2 }">

  $\varphi_n(x) = \cos\!\left(\dfrac{n\pi x}{L}\right)$

  </div>
</div>

<!-- 2D — the image rectangle -->
<div class="dct-col">
  <img class="dct-sample dct-reveal" :class="{ 'is-on': $clicks >= 3 && $clicks < 5 }"
       :src="`${$slidev.configs.base ?? '/'}applications/dct_2d_sample.png`"
       alt="A natural image (imagenette)" />
  <img class="dct-basis dct-reveal" :class="{ 'is-on': $clicks >= 4 }"
       :src="`${$slidev.configs.base ?? '/'}applications/dct_2d_basis.png`"
       alt="2D DCT product modes on a rectangle" />

  <div class="dct-formula dct-reveal" :class="{ 'is-on': $clicks >= 4 }">

  $\varphi_{n,m}(x, y) = \cos\!\left(\dfrac{n\pi x}{L_x}\right)\cos\!\left(\dfrac{m\pi y}{L_y}\right)$

  </div>
</div>

</div>

<!-- Click 6 — the modes' identity, revealed below them. Absolutely
     positioned so the slot doesn't shrink the grid above. -->
<div class="dct-takeaway dct-reveal text-center"
     :class="{ 'is-on': $clicks >= 6 }">

Euclidean Laplacian eigenbasis &nbsp;·&nbsp; <span class="grad">Neumann</span> BC

</div>

</div>

<style>
.dct-col {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 0.9rem;
  width: 100%;
  height: 100%;
  min-height: 0;
}
/* Sample row: identical fixed display height in both columns so the
   1D signal panel and the 2D image panel line up at the same height
   on the slide. */
.dct-sample {
  flex: 0 0 auto;
  height: 8vh;
  max-width: 100%;
  object-fit: contain;
}
/* Basis grid: fills the remaining vertical space below the sample.
   On click 5 (.modes-up on the wrapper grid), translate the basis AND
   formula up by exactly (sample height + column gap) so the modes
   slide to the top of the column without changing size. */
.dct-basis {
  flex: 1 1 0;
  min-height: 0;
  max-width: 100%;
  object-fit: contain;
  transition: transform 520ms ease;
}
.modes-up .dct-basis {
  transform: translateY(calc(-8vh - 0.9rem));
}
/* Math expression of the modes, just below their grid. */
.dct-formula {
  flex: 0 0 auto;
  text-align: center;
  font-size: 0.85rem;
  color: var(--c-fg);
  margin-top: 0.15rem;
  transition: transform 520ms ease;
}
.modes-up .dct-formula {
  transform: translateY(calc(-8vh - 0.9rem));
}
.dct-formula p { margin: 0; }
.dct-formula .katex { font-size: 0.95em; }
/* Takeaway caption (click 6) — out of flow so it doesn't steal vertical
   space from the basis grid above. Anchored to the bottom of the slide
   wrapper (which is position: relative). */
.dct-takeaway {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 1rem;
  font-size: 1.45rem;
  font-weight: 500;
  line-height: 1.3;
  color: var(--c-fg);
}
.dct-takeaway .grad { font-weight: 600; }
/* Smooth click-driven fade for each piece. The vertical slots are
   reserved from frame 0 (CSS keeps the elements in the flex flow)
   so the basis grid doesn't jump in once it appears.
   Both opacity AND transform are listed here so the .modes-up
   translateY on .dct-basis / .dct-formula is animated (single
   `transition` declaration wins the cascade). */
.dct-reveal {
  opacity: 0;
  transition: opacity 420ms ease, transform 520ms ease;
}
.dct-reveal.is-on {
  opacity: 1;
}
/* webkit-background-clip: text clips the gradient flush with the glyph
   bbox — serif horizontals on letters like the T in "DCT" extend a sliver
   past that, so a small right padding keeps them from being sliced. */
h2 .grad {
  padding-right: 0.08em;
}
</style>

---
layout: default
class: text-left
clicks: 4
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Theorem &nbsp;·&nbsp; Aflalo, Brezis et&nbsp;al. (2016)
</div>

<h2 class="!text-2xl !leading-snug !mb-5 font-serif text-center" style="color: var(--c-fg)">
The optimal <i>k</i>-term basis is the <span class="grad">eigenbasis of <i>L</i></span>.
</h2>

<!-- Click 1 — the smooth-signal class C_L. -->
<div class="thm-row" v-click="1">

<div class="thm-label">Smooth-signal class</div>

$$\mathcal{C}_L \;=\; \bigl\{\, f \;:\; \langle f,\, L f\rangle \le 1 \,\bigr\}$$

</div>

<!-- Click 2 — p_L as the uniform distribution over C_L. -->
<div class="thm-row" v-click="2">

<div class="thm-label">Uniform distribution over the class</div>

$$p_L \;=\; \mathrm{Uniform}(\mathcal{C}_L)$$

</div>

<!-- Clicks 3 & 4 — the two theorems shown side-by-side. -->
<div class="grid grid-cols-2 gap-4 mt-3">

<!-- Click 3 — the theorem itself: optimal k-truncated basis = first k
     eigenvectors of L. -->
<div class="thm-card" v-click="3">

<div class="thm-tag">Theorem &nbsp;·&nbsp; optimal <i>k</i>-term basis</div>

$$
\arg\!\min_{\{b_i\}_{i=1}^k}\; \mathbb{E}_{f \sim p_L}\, \bigl\|f - \Pi_k f\bigr\|^2
\;=\; \{\varphi_1, \dots, \varphi_k\}
$$

the first $k$ eigenvectors of $L$.

</div>

<!-- Click 4 — the matching error bound on the same basis. -->
<div class="thm-card thm-card-bound" v-click="4">

<div class="thm-tag">Theorem &nbsp;·&nbsp; worst-case error</div>

$$
\max_{f \in \mathcal{C}_L}\; \bigl\|f - \Pi_k f\bigr\|^2 \;=\; \tfrac{1}{\lambda_{k+1}}
$$

under the optimal basis.

</div>

</div>

</div>

<style>
.thm-row {
  text-align: center;
  font-size: 1.0rem;
  color: var(--c-fg);
  padding: 0.4rem 0;
}
.thm-row .katex-display { margin: 0.25rem 0; }
.thm-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 600;
  margin-bottom: 0.2rem;
}
.thm-card {
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.85rem 1.0rem;
  border-radius: 8px;
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--c-fg-body);
  text-align: center;
}
.thm-card-bound {
  border-left-color: var(--c-success);
  background: rgba(4, 120, 87, 0.06);
}
.thm-card-bound .thm-tag { color: var(--c-success); }
.thm-card .katex-display { margin: 0.35rem 0; }
.thm-tag {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 600;
  margin-bottom: 0.4rem;
}
.thm-foot {
  text-align: center;
  font-size: 1.05rem;
  color: var(--c-fg-body);
  border-left: 3px solid var(--c-success);
  background: rgba(4, 120, 87, 0.06);
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
}
.thm-foot strong { color: var(--c-success); font-weight: 600; }
h2 .grad { padding-right: 0.08em; }
</style>

---
layout: default
class: text-left
clicks: 7
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Optimal approximation theory &nbsp;·&nbsp; signals on a manifold
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
From a vector to a <span class="grad">smooth signal on a sampled manifold</span>.
</h2>

<div class="flex-1 min-h-0 flex flex-col items-center justify-center gap-4 px-4">
<div class="flex items-center justify-center gap-6 pc-row">
<div class="pc-group" :style="{ opacity: $clicks >= 1 ? 1 : 0 }">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_mesh.png`" alt="armadillo mesh" />
<div class="pc-brace-spacer"></div>
<div class="pc-cap">smooth manifold</div>
</div>
<div class="pc-group" :style="{ opacity: $clicks >= 2 ? 1 : 0 }">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points.png`" alt="armadillo point cloud" />
<div class="pc-brace-spacer"></div>
<div class="pc-cap">sampled manifold</div>
</div>
<div class="pc-group" :style="{ opacity: $clicks >= 3 ? 1 : 0 }">
<div class="pc-signals-block">
<div class="pc-signals-row">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01.png`" alt="signal 1" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02.png`" alt="signal 2" />
<span class="pc-dots">⋯</span>
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_03.png`" alt="signal 3" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_04.png`" alt="signal 4" />
</div>
<svg class="pc-brace" viewBox="0 0 100 6" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M 0.5 0.5 Q 0.5 4.5 3 4.5 L 48 4.5 Q 50 4.5 50 6 Q 50 4.5 52 4.5 L 97 4.5 Q 99.5 4.5 99.5 0.5" stroke="currentColor" stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round" /></svg>
</div>
<div class="pc-cap">smooth scalar functions</div>
</div>
</div>
<div class="pc-basis-row">
<div class="pc-basis-set" :style="{ opacity: $clicks === 4 ? 1 : 0 }">
<div class="pc-signals-row">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_0.png`" alt="basis 1 · 0" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_1.png`" alt="basis 1 · 1" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_2.png`" alt="basis 1 · 2" />
<span class="pc-dots">⋯</span>
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_47.png`" alt="basis 1 · 47" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_48.png`" alt="basis 1 · 48" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_1_49.png`" alt="basis 1 · 49" />
</div>
<svg class="pc-brace" viewBox="0 0 100 6" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M 0.5 0.5 Q 0.5 4.5 3 4.5 L 48 4.5 Q 50 4.5 50 6 Q 50 4.5 52 4.5 L 97 4.5 Q 99.5 4.5 99.5 0.5" stroke="currentColor" stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round" /></svg>
<div class="pc-cap">orthogonal basis #1</div>
</div>
<div class="pc-basis-set" :style="{ opacity: $clicks === 5 ? 1 : 0 }">
<div class="pc-signals-row">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_0.png`" alt="basis 2 · 0" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_1.png`" alt="basis 2 · 1" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_2.png`" alt="basis 2 · 2" />
<span class="pc-dots">⋯</span>
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_47.png`" alt="basis 2 · 47" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_48.png`" alt="basis 2 · 48" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_49.png`" alt="basis 2 · 49" />
</div>
<svg class="pc-brace" viewBox="0 0 100 6" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M 0.5 0.5 Q 0.5 4.5 3 4.5 L 48 4.5 Q 50 4.5 50 6 Q 50 4.5 52 4.5 L 97 4.5 Q 99.5 4.5 99.5 0.5" stroke="currentColor" stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round" /></svg>
<div class="pc-cap">orthogonal basis #2</div>
</div>
<div class="pc-basis-set" :style="{ opacity: $clicks === 6 ? 1 : 0 }">
<div class="pc-signals-row">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_0.png`" alt="basis 3 · 0" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_1.png`" alt="basis 3 · 1" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_2.png`" alt="basis 3 · 2" />
<span class="pc-dots">⋯</span>
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_47.png`" alt="basis 3 · 47" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_48.png`" alt="basis 3 · 48" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_3_49.png`" alt="basis 3 · 49" />
</div>
<svg class="pc-brace" viewBox="0 0 100 6" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M 0.5 0.5 Q 0.5 4.5 3 4.5 L 48 4.5 Q 50 4.5 50 6 Q 50 4.5 52 4.5 L 97 4.5 Q 99.5 4.5 99.5 0.5" stroke="currentColor" stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round" /></svg>
<div class="pc-cap">orthogonal basis #3</div>
</div>
<div class="pc-basis-set" :style="{ opacity: $clicks === 7 ? 1 : 0, transform: $clicks === 7 ? 'scale(1.12)' : 'scale(0.92)' }">
<div class="pc-signals-row">
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_0.png`" alt="LBO basis · 0" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_1.png`" alt="LBO basis · 1" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_2.png`" alt="LBO basis · 2" />
<span class="pc-dots">⋯</span>
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_47.png`" alt="LBO basis · 47" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_48.png`" alt="LBO basis · 48" />
<img class="pc-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_4_49.png`" alt="LBO basis · 49" />
</div>
<svg class="pc-brace" viewBox="0 0 100 6" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path d="M 0.5 0.5 Q 0.5 4.5 3 4.5 L 48 4.5 Q 50 4.5 50 6 Q 50 4.5 52 4.5 L 97 4.5 Q 99.5 4.5 99.5 0.5" stroke="currentColor" stroke-width="1.4" fill="none" vector-effect="non-scaling-stroke" stroke-linecap="round" /></svg>
<div class="pc-cap pc-cap-hero"><span class="grad">LBO eigenbasis</span></div>
</div>
</div>
</div>

</div>

<style>
.pc-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: opacity 450ms ease;
}
.pc-signals-block {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
.pc-signals-row {
  display: flex;
  gap: 0.4rem;
  align-items: center;
  justify-content: center;
}
.pc-brace {
  width: 100%;
  height: 12px;
  margin-top: 0.3rem;
  color: var(--c-fg-muted);
  display: block;
}
.pc-cap-hero {
  /* slightly bigger + drops the muted italic styling of regular captions */
  font-size: 1.05rem;
  font-style: normal;
  font-weight: 700;
  color: var(--c-fg);
}
.pc-dots {
  font-size: 1.6rem;
  line-height: 1;
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  padding-left: 0.3rem;
  align-self: center;
  letter-spacing: 0.05em;
}
.pc-brace-spacer {
  /* Reserves the same vertical space the brace occupies, so the
     "smooth manifold" / "sampled manifold" captions sit on the same
     baseline as "smooth scalar functions". */
  height: 12px;
  margin-top: 0.3rem;
}
.pc-basis-row {
  position: relative;
  width: 100%;
  height: 160px;
}
.pc-basis-set {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform-origin: center center;
  transition: opacity 350ms ease,
              transform 520ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
.pc-img {
  /* Single shared size so every thumbnail (mesh, point cloud, signals, basis) is identical. */
  max-width: 110px;
  max-height: 110px;
  width: auto;
  height: auto;
  object-fit: contain;
}
.pc-cap {
  margin-top: 0.5rem;
  font-size: 0.9rem;
  font-style: italic;
  color: var(--c-fg-muted);
  text-align: center;
}
</style>

---
layout: default
class: text-left
clicks: 23
---

<script setup>
import { onMounted, nextTick } from 'vue'

// (kept for now; unused after the projection row was replaced by v-motion clones)
async function alignProj() {
  await nextTick()

  // Wait for the slide images to actually have layout dimensions.
  for (let attempt = 0; attempt < 30; attempt++) {
    const eigen = document.querySelector('.ml-thumb-box img[alt="phi_0"]')
    if (eigen && eigen.getBoundingClientRect().width > 0) break
    await new Promise((r) => setTimeout(r, 50))
  }
  await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))

  let eigenBox = null
  document.querySelectorAll('.ml-thumb-box').forEach((box) => {
    if (box.querySelector('img[alt="phi_0"]')) eigenBox = box
  })
  if (!eigenBox) return

  const eigenImgs = eigenBox.querySelectorAll('img.ml-thumb')
  if (eigenImgs.length !== 4) return
  const eigenRects = Array.from(eigenImgs).map((img) => img.getBoundingClientRect())

  // -- Click 6 clones: 4 copies of signal_01 fly from scalar row down onto
  //    each eigen. Set --tx on each clone = horizontal offset (in slide
  //    pixels) from clone's natural position to its corresponding eigen.
  const clones = document.querySelectorAll('.ml-clone')
  if (clones.length === 4) {
    clones.forEach((clone, idx) => {
      const cloneRect = clone.getBoundingClientRect()
      const eigenRect = eigenRects[idx]
      const tx = eigenRect.left - cloneRect.left
      clone.style.setProperty('--tx', `${tx}px`)
    })
  }

  const projRow = document.querySelector('.ml-proj-row')
  if (!projRow) return

  const projImgs = projRow.querySelectorAll('.ml-proj-img')
  if (projImgs.length !== 4) return

  projImgs.forEach((projImg, idx) => {
    const projRect = projImg.getBoundingClientRect()
    const eigenRect = eigenRects[idx]
    const sx = (eigenRect.left + eigenRect.width / 2) - (projRect.left + projRect.width / 2)
    const sy = (eigenRect.top + eigenRect.height / 2) - (projRect.top + projRect.height / 2)
    projImg.style.setProperty('--sx', `${sx}px`)
    projImg.style.setProperty('--sy', `${sy}px`)
  })

  const projRowRect = projRow.getBoundingClientRect()
  const rowCenterX = projRowRect.left + projRowRect.width / 2
  projImgs.forEach((projImg) => {
    const rect = projImg.getBoundingClientRect()
    const cx = rowCenterX - (rect.left + rect.width / 2)
    projImg.style.setProperty('--cx', `${cx}px`)
  })

  const dotsElem = projRow.querySelector('.ml-proj-dots-inline')
  if (!dotsElem) return
  const itemsForGaps = [projImgs[0], projImgs[1], dotsElem, projImgs[2], projImgs[3]]
  const itemRects = itemsForGaps.map((el) => el.getBoundingClientRect())
  const plusElems = projRow.querySelectorAll('.ml-proj-plus')
  for (let i = 0; i < plusElems.length && i < itemRects.length - 1; i++) {
    const midX = (itemRects[i].right + itemRects[i + 1].left) / 2
    const leftInRow = midX - projRowRect.left
    plusElems[i].style.setProperty('--left', `${leftInRow}px`)
  }
}

onMounted(() => {
  alignProj()
})
</script>

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Method &nbsp;·&nbsp; pipeline overview
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Our <span class="grad">pipeline</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center px-2 ml-stage">
<div class="ml-grid" :style="{ transform: $clicks >= 4 ? 'translateY(-90px)' : 'translateY(0)' }">

<!-- Input (spans both rows) -->
<div class="ml-box ml-input" :style="{ opacity: $clicks >= 1 ? 1 : 0 }">
<img class="ml-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" alt="armadillo point cloud" />
</div>

<!-- Fork split (single tail from input → two arrowheads at row centres) -->
<div class="ml-arrow-split" :style="{ opacity: $clicks >= 2 ? 1 : 0 }">
<svg viewBox="0 0 80 200" width="80" height="200" xmlns="http://www.w3.org/2000/svg">
<path d="M 2 100 L 32 100" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" />
<path d="M 32 45 L 32 155" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" />
<path d="M 32 45 L 64 45" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="butt" />
<path d="M 64 40 L 74 45 L 64 50 Z" fill="currentColor" />
<path d="M 32 155 L 64 155" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="butt" />
<path d="M 64 150 L 74 155 L 64 160 Z" fill="currentColor" />
</svg>
</div>
<!-- Row 1: upper branch -->
<div class="ml-box ml-card" :style="{ opacity: $clicks >= 2 ? 1 : 0 }">Smooth function<br/>sampler</div>
<div class="ml-arrow-h" :style="{ opacity: $clicks >= 2 ? 1 : 0 }">
<svg viewBox="0 0 40 16" width="40" height="16" xmlns="http://www.w3.org/2000/svg">
<path d="M 2 8 L 28 8" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="butt" />
<path d="M 28 3 L 38 8 L 28 13 Z" fill="currentColor" />
</svg>
</div>
<div class="ml-thumb-wrap" :style="{ opacity: $clicks >= 2 ? 1 : 0 }">
<div class="ml-box ml-thumb-box">
<span class="ml-thumb-cell" :class="{ masked: $clicks >= 13 && $clicks < 21 }"><img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="smooth function 1" /></span>
<span class="ml-thumb-cell" :class="{ masked: $clicks >= 5 && $clicks < 13 }"><img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="smooth function 2" /></span>
<div class="ml-dots" :class="{ masked: $clicks >= 5 && $clicks < 21 }">

$\cdots$

</div>
<span class="ml-thumb-cell" :class="{ masked: $clicks >= 5 && $clicks < 21 }"><img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_03_tight.png`" alt="smooth function 3" /></span>
<span class="ml-thumb-cell" :class="{ masked: $clicks >= 5 && $clicks < 21 }"><img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_04_tight.png`" alt="smooth function 4" /></span>
<!-- Underbrace labeling the smooth functions row as {f_i}. -->
<div class="ml-underbrace">

$\underbrace{\hspace{200px}}_{\text{smooth probe functions } \{f_i\}}$

</div>
</div>
</div>

<!-- Row 2: lower branch -->
<div class="ml-box ml-card" :style="{ opacity: $clicks >= 3 ? 1 : 0 }">Neural<br/>network</div>
<div class="ml-arrow-h" :style="{ opacity: $clicks >= 3 ? 1 : 0 }">
<svg viewBox="0 0 40 16" width="40" height="16" xmlns="http://www.w3.org/2000/svg">
<path d="M 2 8 L 28 8" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="butt" />
<path d="M 28 3 L 38 8 L 28 13 Z" fill="currentColor" />
</svg>
</div>
<div class="ml-thumb-wrap" :style="{ opacity: $clicks >= 3 ? 1 : 0 }">
<div class="ml-box ml-thumb-box" :class="{ 'loss-fade-out': $clicks >= 23 }">
<!-- Each eigen cell hosts a click-6 clone of signal_01. v-motion :initial offset = source position relative to this cell. Source = signal_01 at scalar row col 1, i.e. one row up (y = -110) and offset LEFT by this cell's column-left within the thumb-box: 0, 91.4, 219.2, 310.6 for cols 1, 2, 4, 5. -->
<span class="ml-thumb-cell">
  <img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_0_tight.png`" alt="phi_0" />
  <img class="ml-pl-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-6="{ x: 0, y: 0, opacity: 1 }" :click-7="{ x: 0, y: 140, opacity: 1 }" :click-8="{ x: -30, y: 140, opacity: 1 }" :click-9="{ x: 155, y: 140, opacity: 0 }" :src="$clicks >= 7 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_proj_i0_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="" />
  <img class="ml-pl-clone" v-motion :initial="{ x: 91.4, y: -140, opacity: 0 }" :click-14="{ x: 0, y: 0, opacity: 1 }" :click-15="{ x: 0, y: 140, opacity: 1 }" :click-16="{ x: -30, y: 140, opacity: 1 }" :click-17="{ x: 155, y: 140, opacity: 0 }" :src="$clicks >= 15 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_proj_i0_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="" />
</span>
<span class="ml-thumb-cell">
  <img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_1_tight.png`" alt="phi_1" />
  <img class="ml-pl-clone" v-motion :initial="{ x: -91.4, y: -140, opacity: 0 }" :click-6="{ x: 0, y: 0, opacity: 1 }" :click-7="{ x: 0, y: 140, opacity: 1 }" :click-8="{ x: -15, y: 140, opacity: 1 }" :click-9="{ x: 64, y: 140, opacity: 0 }" :src="$clicks >= 7 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_proj_i1_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="" />
  <img class="ml-pl-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-14="{ x: 0, y: 0, opacity: 1 }" :click-15="{ x: 0, y: 140, opacity: 1 }" :click-16="{ x: -15, y: 140, opacity: 1 }" :click-17="{ x: 64, y: 140, opacity: 0 }" :src="$clicks >= 15 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_proj_i1_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="" />
</span>
<div class="ml-dots">

$\cdots$

</div>
<span class="ml-thumb-cell">
  <img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_48_tight.png`" alt="phi_48" />
  <img class="ml-pl-clone" v-motion :initial="{ x: -219.2, y: -140, opacity: 0 }" :click-6="{ x: 0, y: 0, opacity: 1 }" :click-7="{ x: 0, y: 140, opacity: 1 }" :click-8="{ x: 15, y: 140, opacity: 1 }" :click-9="{ x: -64, y: 140, opacity: 0 }" :src="$clicks >= 7 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_proj_i48_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="" />
  <img class="ml-pl-clone" v-motion :initial="{ x: -127.8, y: -140, opacity: 0 }" :click-14="{ x: 0, y: 0, opacity: 1 }" :click-15="{ x: 0, y: 140, opacity: 1 }" :click-16="{ x: 15, y: 140, opacity: 1 }" :click-17="{ x: -64, y: 140, opacity: 0 }" :src="$clicks >= 15 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_proj_i48_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="" />
</span>
<span class="ml-thumb-cell">
  <img class="ml-thumb" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_basis_2_49_tight.png`" alt="phi_49" />
  <img class="ml-pl-clone" v-motion :initial="{ x: -310.6, y: -140, opacity: 0 }" :click-6="{ x: 0, y: 0, opacity: 1 }" :click-7="{ x: 0, y: 140, opacity: 1 }" :click-8="{ x: 30, y: 140, opacity: 1 }" :click-9="{ x: -155, y: 140, opacity: 0 }" :src="$clicks >= 7 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_proj_i49_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="" />
  <img class="ml-pl-clone" v-motion :initial="{ x: -219.2, y: -140, opacity: 0 }" :click-14="{ x: 0, y: 0, opacity: 1 }" :click-15="{ x: 0, y: 140, opacity: 1 }" :click-16="{ x: 30, y: 140, opacity: 1 }" :click-17="{ x: -155, y: 140, opacity: 0 }" :src="$clicks >= 15 ? `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_proj_i49_tight.png` : `${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="" />
</span>
<!-- Underbrace labeling the eigen row as the predicted eigenbasis {b_i}. -->
<div class="ml-underbrace">

$\underbrace{\hspace{200px}}_{\text{predicted } K\text{-truncated eigenbasis } \{b_i\}_{i=1}^{K}}$

</div>
<!-- Row-3 dots (the projection row, below the eigens). Appears 50ms after click 7. Positioned at the dots-column x (left: 182.8) and row-3 y (top: 110) of the eigen thumb-box. On click 9 fades out in place. -->
<div class="ml-pl-row3-dots" :class="{ shown: $clicks >= 7, collapsing: $clicks >= 9 }">

$\cdots$

</div>
<!-- '+' signs between row-3 items (click 8), rendered by KaTeX. On click 9 they translate to row center (--dx-collapse) and fade out. -->
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 8, collapsing: $clicks >= 9 }" style="left: 66px; --dx-collapse: 132px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 8, collapsing: $clicks >= 9 }" style="left: 172px; --dx-collapse: 26px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 8, collapsing: $clicks >= 9 }" style="left: 224px; --dx-collapse: -26px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 8, collapsing: $clicks >= 9 }" style="left: 330px; --dx-collapse: -132px;">

$+$

</div>
<!-- Signal_01 loss-expression container. The 5 children stay at their original
     CSS positions; on click 12 the container as a whole translateX+scales,
     keeping the INTERNAL spacing tight (gaps shrink proportionally with scale). -->
<div class="ml-pl-loss-group" :class="{ 'shifted-l': $clicks >= 12 }">
<!-- Sum image: k=50 reconstruction of signal_01. Row 3 center (top:110, left:155.3 → centered on x=197.8). -->
<img class="ml-pl-sum" :class="{ shown: $clicks >= 9 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_recon_k5_tight.png`" alt="" />
<!-- Click 10: 'f' clone animates DOWN from signal_01 (row 1 col 1) to left:30, top:110. -->
<img class="ml-pl-f-clone" v-motion :initial="{ x: -30, y: -280, scale: 1, opacity: 0 }" :click-10="{ x: 0, y: 0, scale: 1, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" alt="" />
<div class="ml-pl-minus" :class="{ shown: $clicks >= 10 }" style="left: 135px;">

$-$

</div>
<!-- Click 11: ‖ ‖² brackets. -->
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 11 }" style="left: 2px; top: 130px;">

$\|$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 11 }" style="left: 242px; top: 130px;">

$\|^2$

</div>
</div>
<!-- ============================================================
     SIGNAL_02 FLOW (clicks 13–19). Mirrors the signal_01 flow at
     clicks 5–11 with the same absolute positions inside the eigen
     thumb-box — the signal_01 expression has already shifted-left
     out of this region by click 12, so the positions are free. -->
<!-- Row-3 dots and + signs for signal_02. Shown click 15/16; collapse at click 17. -->
<div class="ml-pl-row3-dots" :class="{ shown: $clicks >= 15, collapsing: $clicks >= 17 }">

$\cdots$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 16, collapsing: $clicks >= 17 }" style="left: 66px; --dx-collapse: 132px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 16, collapsing: $clicks >= 17 }" style="left: 172px; --dx-collapse: 26px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 16, collapsing: $clicks >= 17 }" style="left: 224px; --dx-collapse: -26px;">

$+$

</div>
<div class="ml-pl-row3-plus" :class="{ shown: $clicks >= 16, collapsing: $clicks >= 17 }" style="left: 330px; --dx-collapse: -132px;">

$+$

</div>
<!-- Signal_02 loss-expression container. Same idea: container-level transform
     on click 20 shifts+scales the whole expression as a unit. -->
<div class="ml-pl-loss-group" :class="{ 'shifted-m': $clicks >= 20 }">
<!-- Sum image: k=50 reconstruction of signal_02. Click 17. -->
<img class="ml-pl-sum" :class="{ shown: $clicks >= 17 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_recon_k5_tight.png`" alt="" />
<!-- f2 clone animates DOWN from signal_02 (row 1 col 2). Source offset = (91.4 - 30, -110 - 110) = (61.4, -220). Click 18. -->
<img class="ml-pl-f-clone" v-motion :initial="{ x: 61.4, y: -280, scale: 1, opacity: 0 }" :click-18="{ x: 0, y: 0, scale: 1, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_02_tight.png`" alt="" />
<div class="ml-pl-minus" :class="{ shown: $clicks >= 18 }" style="left: 135px;">

$-$

</div>
<!-- Norm brackets for signal_02. Click 19. -->
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 19 }" style="left: 2px; top: 130px;">

$\|$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 19 }" style="left: 242px; top: 130px;">

$\|^2$

</div>
</div>
<!-- "+" sign between the two shifted loss expressions, click 20. Sits in the gap between signal_01's right bracket (≈ thumb-box x -195) and signal_02's left bracket (≈ thumb-box x -156). -->
<div class="ml-pl-plus-between" :class="{ shown: $clicks >= 20 }" style="left: -284px;">

$+$

</div>
<!-- ============================================================
     Click 21: two more loss expressions (signal_03, signal_04) appear
     directly at their final positions (no flow). Static containers
     pre-positioned with shifted-3 / shifted-4 transforms. -->
<div class="ml-pl-loss-group shifted-3">
<img class="ml-pl-sum" :class="{ shown: $clicks >= 21 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_03_recon_k5_tight.png`" alt="" />
<img class="ml-pl-f-clone" :style="{ opacity: $clicks >= 21 ? 1 : 0, transition: 'opacity 500ms ease 250ms' }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_03_tight.png`" alt="" />
<div class="ml-pl-minus" :class="{ shown: $clicks >= 21 }" style="left: 135px;">

$-$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 21 }" style="left: 2px; top: 130px;">

$\|$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 21 }" style="left: 242px; top: 130px;">

$\|^2$

</div>
</div>
<div class="ml-pl-loss-group shifted-4">
<img class="ml-pl-sum" :class="{ shown: $clicks >= 21 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_04_recon_k5_tight.png`" alt="" />
<img class="ml-pl-f-clone" :style="{ opacity: $clicks >= 21 ? 1 : 0, transition: 'opacity 500ms ease 250ms' }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_04_tight.png`" alt="" />
<div class="ml-pl-minus" :class="{ shown: $clicks >= 21 }" style="left: 135px;">

$-$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 21 }" style="left: 2px; top: 130px;">

$\|$

</div>
<div class="ml-pl-norm-bracket" :class="{ shown: $clicks >= 21 }" style="left: 242px; top: 130px;">

$\|^2$

</div>
</div>
<!-- Middle of the sum (click 21): + ⋯ + between sig2 and sig3.
     Gap widened (sig1, sig2 shifted left by 30) for breathing room. -->
<div class="ml-pl-plus-between" :class="{ shown: $clicks >= 21 }" style="left: -65px;">

$+$

</div>
<div class="ml-pl-plus-between" :class="{ shown: $clicks >= 21 }" style="left: -36px;">

$\cdots$

</div>
<div class="ml-pl-plus-between" :class="{ shown: $clicks >= 21 }" style="left: -7px;">

$+$

</div>
<!-- + sign between sig3-sig4 (click 21). -->
<div class="ml-pl-plus-between" :class="{ shown: $clicks >= 21 }" style="left: 216px;">

$+$

</div>
<!-- Click 22: underbrace below the full sum labeling the loss. The sum spans
     thumb-box x≈[-489, 417], center ≈ -36. Width ~905 visually. -->
<div class="ml-loss-underbrace" :class="{ shown: $clicks >= 22 }" style="left: -30px; top: 200px;">

$\underbrace{\hspace{420px}}_{\sum_i \bigl\| f_i - \sum_{j=1}^{K} \langle f_i, b_j\rangle b_j \bigr\|^2}$

</div>
</div>
</div>

</div>

<!-- Click 23: final loss expression. Replaces the four squared-norm
     expressions and their underbrace (which all fade out together) with
     the FULL ordered-basis loss: outer sum over k=1..K of the previous
     underbrace expression (now with inner sum j=1..k). Centered on the
     slide horizontally and on the slot where the small expressions sat
     vertically. -->
<div class="ml-final-loss" :class="{ shown: $clicks >= 23 }">

$\mathcal{L}\bigl(\{b_i\}_{i=1}^{K}\bigr) = \sum_{k=1}^{K} \left( \sum_i \bigl\| f_i - \sum_{j=1}^{k} \langle f_i, b_j\rangle b_j \bigr\|^2 \right)$

</div>
</div>

<!-- Click 7: each .ml-pl-clone (currently sitting on its eigen at end of click 6) translates further DOWN by 110px into a virtual "row 3" below the eigens. Same image (signal_01) — the row 3 visualization is just the clones moving straight down. -->


</div>

<style>
.ml-stage {
  position: relative;
}
/* Projection row: identical FLEX layout to the eigen thumb-box (4 imgs +
   1 .ml-dots span, gap 0.4rem). Centered horizontally on the slide. Each
   img's --sx/--sy/--cx CSS variables are set at runtime by a script that
   measures the eigen positions, so the imgs start their motion exactly at
   the corresponding eigen centers. */
.ml-proj-row {
  position: absolute;
  left: 50%;
  bottom: 5rem;
  transform: translateX(-50%);
  display: flex;
  gap: 0.4rem;
  align-items: center;
  pointer-events: none;
}
.ml-proj-img {
  width: 85px;
  height: 85px;
  object-fit: contain;
  opacity: 0;
  transform-origin: center center;
  transform: translate(var(--sx, 0px), var(--sy, 0px)) scale(0.45);
  flex-shrink: 0;
}
.ml-proj-row.visible .ml-proj-img {
  animation: ml-proj-img-emerge 1.1s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
.ml-proj-row.collapsing .ml-proj-img {
  animation: ml-proj-img-collapse 600ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
@keyframes ml-proj-img-emerge {
  0%   { opacity: 0;    transform: translate(var(--sx, 0px), var(--sy, 0px)) scale(0.45); }
  18%  { opacity: 0.95; transform: translate(var(--sx, 0px), var(--sy, 0px)) scale(0.55); }
  100% { opacity: 1;    transform: translate(0, 0) scale(1); }
}
@keyframes ml-proj-img-collapse {
  0%   { opacity: 1; transform: translate(0, 0) scale(1); }
  100% { opacity: 0; transform: translate(var(--cx, 0px), 0) scale(1); }
}
.ml-proj-dots-inline {
  opacity: 0;
  transition: opacity 400ms ease 0.7s;
  flex-shrink: 0;
}
.ml-proj-row.visible .ml-proj-dots-inline { opacity: 1; }
.ml-proj-row.collapsing .ml-proj-dots-inline { opacity: 0; transition: opacity 400ms ease; }
.ml-proj-plus {
  position: absolute;
  top: 50%;
  left: var(--left, 0px);
  transform: translate(-50%, -50%);
  font-size: 1.6rem;
  line-height: 1;
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  opacity: 0;
  pointer-events: none;
  transition: opacity 400ms ease;
}
.ml-proj-plus.visible { opacity: 1; }
.ml-proj-plus.collapsing { opacity: 0; }
.ml-loss-expr {
  position: absolute;
  left: 50%;
  bottom: 5rem;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none;
}
.ml-loss-sum {
  width: 85px;
  height: 85px;
  object-fit: contain;
  opacity: 0;
  transition: opacity 500ms ease 350ms;
  flex-shrink: 0;
}
.ml-loss-expr.visible .ml-loss-sum { opacity: 1; }

.ml-loss-f-cell {
  position: relative;
  width: 85px;
  height: 85px;
  max-width: 0;
  flex-shrink: 0;
  overflow: visible;
  transition: max-width 600ms cubic-bezier(0.4, 0, 0.2, 1);
}
.ml-loss-f-img {
  position: absolute;
  top: 0;
  left: 0;
  width: 85px;
  height: 85px;
  object-fit: contain;
  opacity: 0;
  transform: translate(var(--fx, 0px), var(--fy, 0px));
  transition: transform 700ms cubic-bezier(0.4, 0, 0.2, 1),
              opacity 500ms ease;
}
.ml-loss-expr.expanded .ml-loss-f-cell { max-width: 85px; }
.ml-loss-expr.expanded .ml-loss-f-img {
  opacity: 1;
  transform: translate(0, 0);
}
.ml-loss-minus {
  font-size: 1.8rem;
  color: var(--c-fg);
  line-height: 1;
  max-width: 0;
  opacity: 0;
  overflow: hidden;
  white-space: nowrap;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  transition: max-width 600ms cubic-bezier(0.4, 0, 0.2, 1), opacity 400ms ease;
}
.ml-norm-bracket {
  font-size: 3.4rem;
  color: var(--c-fg);
  line-height: 1;
  max-width: 0;
  opacity: 0;
  overflow: hidden;
  white-space: nowrap;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  transition: max-width 600ms cubic-bezier(0.4, 0, 0.2, 1), opacity 400ms ease;
}
.ml-norm-bracket p,
.ml-loss-minus p {
  margin: 0;
  padding: 0;
  line-height: 1;
}
.ml-norm-bracket .katex,
.ml-loss-minus .katex {
  font-size: inherit;
}
.ml-loss-expr.expanded .ml-loss-minus { max-width: 1.8rem; opacity: 1; }
.ml-loss-expr.expanded .ml-norm-bracket { max-width: 3rem; opacity: 1; }
/* (orphan rules from earlier iterations removed) */
.ml-grid {
  display: grid;
  grid-template-columns: auto auto auto auto auto;
  grid-template-rows: 90px 90px;
  align-items: center;
  column-gap: 0.6rem;
  row-gap: 50px;
  transition: transform 600ms cubic-bezier(0.4, 0, 0.2, 1);
}
.ml-arrow-split {
  grid-column: 2;
  grid-row: 1 / span 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-fg-subtle);
  transition: opacity 350ms ease;
}
.ml-arrow-split svg { width: 80px; height: 200px; }
.ml-input {
  grid-column: 1;
  grid-row: 1 / span 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0.4rem;
  transition: opacity 350ms ease;
}
.ml-img {
  width: 200px;
  height: auto;
  object-fit: contain;
}
.ml-arrow-h {
  color: var(--c-fg-subtle);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: opacity 350ms ease;
}
.ml-box {
  display: flex;
  align-items: center;
  justify-content: center;
}
.ml-card {
  border-radius: 10px;
  background-image: linear-gradient(135deg, var(--c-brand-from), var(--c-brand-to));
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(43, 88, 118, 0.22);
  padding: 0.85rem 0.7rem;
  font-size: 1.05rem;
  font-weight: 700;
  text-align: center;
  line-height: 1.25;
  letter-spacing: -0.005em;
  min-width: 0;
  transition: opacity 350ms ease;
}
.ml-thumb-wrap {
  position: relative;
  transition: opacity 350ms ease;
}
.ml-thumb-box {
  /* Explicit CSS Grid: deterministic column widths so the eigen / scalar
     positions are exact constants regardless of font / dots rendering. With
     gap: 0.4rem (6.4px), the column left edges are:
       col 1: 0
       col 2: 85 + 6.4 = 91.4px
       col 3 (dots): 91.4 + 85 + 6.4 = 182.8px
       col 4: 182.8 + 30 + 6.4 = 219.2px
       col 5: 219.2 + 85 + 6.4 = 310.6px */
  display: grid;
  grid-template-columns: 85px 85px 30px 85px 85px;
  gap: 0.4rem;
  align-items: center;
  justify-items: center;
  position: relative;
}
.ml-clone {
  position: absolute;
  top: 0;
  width: 85px;
  height: 85px;
  object-fit: contain;
  opacity: 0;
  pointer-events: none;
  transform: translate(0, 0);
}
.ml-clone.flying {
  animation: ml-clone-fly 1.3s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
/* Click-6 clone of signal_01 placed inside each eigen .ml-thumb-cell. v-motion
   animates it IN from a per-clone source offset (matching signal_01's
   position in the scalar row, one row above). Final state: translate(0,0)
   over the eigen img. */
.ml-pl-clone {
  position: absolute;
  top: 0;
  left: 0;
  width: 85px;
  height: 85px;
  object-fit: contain;
  pointer-events: none;
}
/* Row-3 dots (between proj_i1 and proj_i48 after click 7). Positioned in the
   eigen thumb-box coordinate frame at (left=182.8, top=110) — matching the
   dots column x and one row-step below the eigen row. Fades in 50ms after
   click 7, matching the test-slide pattern. */
.ml-pl-row3-dots {
  position: absolute;
  left: 182.8px;
  top: 140px;
  width: 30px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0 0.15rem;
  opacity: 0;
  pointer-events: none;
  transition: opacity 350ms ease;
}
.ml-pl-row3-dots.shown {
  opacity: 1;
  transition-delay: 50ms;
}
/* '+' signs in row 3 (click 8). Same vertical band as the row-3 dots (top: 110, height: 85, centered). Each instance positions itself at its 'left' via translateX(-50%) so the inline `style="left: ..."` value is the *centre* x of the '+' character. */
.ml-pl-row3-plus {
  position: absolute;
  top: 140px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-fg-subtle);
  font-size: 1.2rem;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  transform: translateX(-50%);
  transition: opacity 350ms ease;
}
.ml-pl-row3-plus.shown { opacity: 1; }
.ml-pl-row3-plus {
  /* Re-declare so the transition includes transform too. */
  transition: opacity 350ms ease, transform 500ms cubic-bezier(0.4, 0, 0.2, 1);
}
.ml-pl-row3-plus.collapsing {
  opacity: 0;
  transform: translateX(-50%) translateX(var(--dx-collapse, 0px));
}
.ml-pl-row3-dots.collapsing {
  opacity: 0;
  transition-delay: 0ms;
}
.ml-pl-sum {
  position: absolute;
  top: 140px;
  left: 155.3px;
  width: 85px;
  height: 85px;
  object-fit: contain;
  opacity: 0;
  pointer-events: none;
  transition: opacity 500ms ease 250ms,
              transform 1200ms cubic-bezier(0.65, 0, 0.35, 1);
}
.ml-pl-sum.shown { opacity: 1; }
/* Loss-expression container: a transform-able wrapper for the 5 elements
   (sum, f-clone, minus, ‖, ‖²). A single transform on this container
   shifts and scales the WHOLE expression as a unit — internal spacing
   shrinks proportionally with the scale instead of growing.
   transform-origin: 0 0 means the container scales toward the eigen
   thumb-box top-left corner. */
.ml-pl-loss-group {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  /* Pivot the scale around y=110 (the row of sum/f/minus) so the
     vertical position of the expression is preserved under scale. */
  transform-origin: 0 140px;
  transition: transform 1200ms cubic-bezier(0.65, 0, 0.35, 1);
}
.ml-pl-loss-group.shifted-l { transform: translateX(-490px) translateY(10px) scale(0.7); }
.ml-pl-loss-group.shifted-m { transform: translateX(-270px) translateY(10px) scale(0.7); }
/* Final slots for signal_03 and signal_04 loss expressions (click 21).
   Same scale + same gap (~220 between adjacent expressions). */
.ml-pl-loss-group.shifted-3 { transform: translateX(10px) translateY(10px) scale(0.7); }
.ml-pl-loss-group.shifted-4 { transform: translateX(230px) translateY(10px) scale(0.7); }
/* "+" sign that joins the two loss expressions. Same look/timing as
   .ml-pl-minus but its own absolute slot between them. */
.ml-pl-plus-between {
  position: absolute;
  top: 130px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-fg);
  font-size: 1.4rem;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  transform: translateX(-50%);
  transition: opacity 500ms ease 400ms;
}
.ml-pl-plus-between.shown { opacity: 1; }
.ml-pl-plus-between p { margin: 0; padding: 0; line-height: 1; }
.ml-pl-plus-between .katex { font-size: inherit; color: inherit; }
/* f clone: lives in the eigen thumb-box at natural (left=30, top=110). v-motion animates it from signal_01 (eigen-thumb-box coord (0,-110), so :initial offset (-30, -220) relative to natural) to (0, 0) on click 10. */
.ml-pl-f-clone {
  position: absolute;
  top: 140px;
  left: 30px;
  width: 85px;
  height: 85px;
  object-fit: contain;
  pointer-events: none;
}
/* Minus sign between f and sum, KaTeX rendered. */
.ml-pl-minus {
  position: absolute;
  top: 140px;
  height: 85px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--c-fg);
  font-size: 1.4rem;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  transform: translateX(-50%);
  transition: opacity 350ms ease, transform 1200ms cubic-bezier(0.65, 0, 0.35, 1);
}
.ml-pl-minus.shown { opacity: 1; }
.ml-pl-minus p { margin: 0; padding: 0; line-height: 1; }
.ml-pl-minus .katex { font-size: inherit; color: inherit; }
/* Norm brackets ‖ and ‖² wrapping the f − sum expression (click 11). Tall enough to span the ~85px height. KaTeX renders them at math font; we just give them a slot. */
.ml-pl-norm-bracket {
  position: absolute;
  top: 140px;
  height: 85px;
  display: flex;
  align-items: center;
  color: var(--c-fg);
  font-size: 3.4rem;
  line-height: 1;
  opacity: 0;
  pointer-events: none;
  transition: opacity 350ms ease, transform 1200ms cubic-bezier(0.65, 0, 0.35, 1);
}
.ml-pl-norm-bracket.shown { opacity: 1; }
/* Underbrace labels below the smooth-functions row (row 1) and the
   predicted-eigenbasis row (row 2). Absolute-positioned just below the
   thumb cells (which span y=0..85), so the brace sits in the row-gap area. */
.ml-underbrace {
  position: absolute;
  top: 70px;
  left: 50%;
  transform: translateX(-50%);
  color: var(--c-fg-subtle);
  font-size: 1.3rem;
  line-height: 1;
  pointer-events: none;
  white-space: nowrap;
}
.ml-underbrace p { margin: 0; padding: 0; line-height: 1; }
.ml-underbrace .katex { font-size: inherit; color: inherit; }
/* Underbrace labeling the FULL sum at click 22. Positioned absolutely
   within the eigen thumb-box, centered on the sum's horizontal centre. */
.ml-loss-underbrace {
  position: absolute;
  transform: translateX(-50%);
  color: var(--c-fg);
  font-size: 1.4rem;
  line-height: 1;
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 500ms ease 400ms;
}
.ml-loss-underbrace.shown { opacity: 1; }
.ml-loss-underbrace p { margin: 0; padding: 0; line-height: 1; }
.ml-loss-underbrace .katex { font-size: inherit; color: inherit; }
/* Click 23: fade out all four squared-norm expressions, the +/⋯ chain,
   and the loss underbrace together by toggling a class on the row-2 thumb-box. */
.ml-thumb-box.loss-fade-out .ml-pl-loss-group,
.ml-thumb-box.loss-fade-out .ml-pl-plus-between,
.ml-thumb-box.loss-fade-out .ml-loss-underbrace {
  opacity: 0;
  transition: opacity 500ms ease;
}
/* Click 23: the final ordered-basis loss expression, displayed large and
   centered on the slide (sibling of the grid inside ml-stage). */
.ml-final-loss {
  position: absolute;
  bottom: 12%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 1.6rem;
  color: var(--c-fg);
  pointer-events: none;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 700ms ease 600ms;
  z-index: 5;
}
.ml-final-loss.shown { opacity: 1; }
.ml-final-loss p { margin: 0; padding: 0; line-height: 1; }
.ml-final-loss .katex { font-size: inherit; color: inherit; }
.ml-pl-norm-bracket p { margin: 0; padding: 0; line-height: 1; }
.ml-pl-norm-bracket .katex { font-size: inherit; color: inherit; }
/* Shrink the ² superscript via CSS transform so the exponent
   POSITION is preserved (transform-origin at the baseline = bottom)
   while only the glyph size shrinks. */
.ml-pl-norm-bracket .msupsub {
  display: inline-block;
  transform: scale(0.7) translateY(-0.25em);
  transform-origin: 0 0;
}
.ml-pl-row3-plus p,
.ml-dots p,
.ml-pl-row3-dots p { margin: 0; padding: 0; line-height: 1; }
.ml-pl-row3-plus .katex,
.ml-dots .katex,
.ml-pl-row3-dots .katex { font-size: inherit; color: inherit; }
@keyframes ml-clone-fly {
  0%   { opacity: 0;   transform: translate(0, 0); }
  8%   { opacity: 0.95; transform: translate(0, 0); }
  100% { opacity: 0;   transform: translate(var(--tx), 110px); }
}
.ml-thumb {
  width: 85px;
  height: 85px;
  object-fit: contain;
  display: block;
  transition: opacity 400ms ease, filter 400ms ease;
}
.ml-thumb-cell {
  position: relative;
  display: inline-block;
  line-height: 0;
}
.ml-thumb-cell.masked .ml-thumb {
  opacity: 0.18;
}
.ml-dots { transition: opacity 400ms ease; }
.ml-dots.masked { opacity: 0.18; }
.ml-dots {
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  font-size: 1.2rem;
  line-height: 1;
  padding: 0 0.15rem;
}
</style>

---
layout: default
class: text-left
clicks: 2
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; single-shape training
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Our predicted basis matches the <span class="grad">cotangent Laplacian</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">

<div class="grid gap-1 items-center justify-items-center" style="grid-template-columns: 50px repeat(12, 60px); grid-auto-rows: 60px;">

<div></div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{2}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{3}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{4}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{5}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{6}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{7}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{10}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{25}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{40}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=5$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=25$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=45$

</div>

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_lion_ours_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_botijo_ours_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_armadillo_ours_k_45.png`" />

</div>

</div>

</div>

---
layout: default
class: text-left
clicks: 2
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; single-shape training
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Our predicted basis matches the <span class="grad">cotangent Laplacian</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">

<div class="grid gap-1 items-center justify-items-center" style="grid-template-columns: 50px repeat(12, 60px); grid-auto-rows: 60px;">

<div></div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{2}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{3}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{4}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{5}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{6}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{7}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{10}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{25}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{40}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=5$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=25$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=45$

</div>

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_heptotoroid_ours_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_26.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_v_41.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_wrench_ours_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_cot_lap_k_45.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_4.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_6.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_7.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[360ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[420ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[480ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_v_40.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[540ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_k_5.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[600ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_k_25.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[660ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/overfit_cells/overfit_pegaso_ours_k_45.png`" />

</div>

</div>

</div>

---
layout: default
class: text-left
clicks: 2
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; generalization across shapes
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Our predicted basis matches the <span class="grad">cotangent Laplacian</span> on <em>unseen</em> shapes.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">

<div class="grid gap-1 items-center justify-items-center" style="grid-template-columns: 50px repeat(6, 60px); grid-auto-rows: 60px;">

<div></div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{2}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{3}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{11}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$\mathbf{v}_{31}$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=10$

</div>
<div class="text-sm text-center transition-opacity duration-300 translate-y-6" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">

$k=50$

</div>

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_cot_lap_k_50.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s1_ours_k_50.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_cot_lap_k_50.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s2_ours_k_50.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'">Cot.&nbsp;Lap.</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 1 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_cot_lap_k_50.png`" />

<div class="text-xs text-right w-full pr-1 whitespace-nowrap transition-opacity duration-300 -translate-x-[10px]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'">Ours</div>
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[0ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_v_2.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[60ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_v_3.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[120ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_v_11.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[180ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_v_31.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[240ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_k_10.png`" />
<img class="w-[60px] h-[60px] object-contain block transition-opacity duration-300 delay-[300ms]" :class="$clicks >= 2 ? 'opacity-100' : 'opacity-0'" :src="`${$slidev.configs.base ?? '/'}applications/generalization_cells/gen_g1_s3_ours_k_50.png`" />

</div>

</div>

</div>

---
layout: default
class: text-center
hide: true
---

<div class="h-full flex flex-col items-center justify-center px-12">

<div class="eyebrow mb-10">
The question
</div>

<h1 class="!text-4xl !leading-[1.6] font-serif max-w-5xl" style="color: var(--c-fg)">
So how do we <span class="grad">learn</span> an<br/>
ordered eigenbasis of <i>L</i><br/>
in practice?
</h1>

</div>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Method &nbsp;·&nbsp; Training recipe
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
The training algorithm.
</h2>

<div class="algo-step" v-click="1">

<span class="step-num">1</span> The network predicts a basis $\{b_i\}_{i=1}^{K}$ from the input manifold sample.

</div>

<div class="algo-step" v-click="2">

<span class="step-num">2</span> Sample a batch $B$ of signals $f \sim p_L$ defined on the same manifold sample.

</div>

<div class="algo-step" v-click="3">

<span class="step-num">3</span> For each prefix length $k$, compute the reconstruction error $\;r_k(f) = \big\| f - \sum_{i=1}^k \langle f, b_i\rangle b_i \big\|^2$.

</div>

<div class="algo-step" v-click="4">

<span class="step-num">4</span> Backpropagate the loss $\mathcal{L} = \sum_{k=1}^{K} \frac{1}{|B|}\sum_{f \in B} r_k(f)$ through the network.

</div>

<div class="algo-step inference mt-auto" v-click="5">

<span class="step-num">5</span> <span class="phase-tag">At inference</span> &mdash; estimate the eigenvalues: $\lambda_k \approx 1 / \max_f r_k(f)$ &nbsp;(max over a batch of signals).

</div>

</div>

<style>
.algo-step {
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.55rem 1rem 0.55rem 0.7rem;
  border-radius: 6px;
  margin-bottom: 0.5rem;
  font-size: 0.88rem;
  line-height: 1.45;
  color: var(--c-fg-body);
}
.step-num {
  display: inline-block;
  width: 1.55rem;
  height: 1.55rem;
  line-height: 1.55rem;
  text-align: center;
  background: var(--c-brand-from);
  color: #fff;
  border-radius: 50%;
  font-weight: 700;
  font-size: 0.78rem;
  margin-right: 0.55rem;
  vertical-align: middle;
}
.algo-step.inference {
  border-left-color: var(--c-success);
  background: rgba(4, 120, 87, 0.05);
}
.algo-step.inference .step-num {
  background: var(--c-success);
}
.phase-tag {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.66rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--c-success);
  font-weight: 600;
  margin-right: 0.2rem;
}
</style>

---
layout: default
class: text-center
hide: true
---

<div class="h-full flex flex-col items-center justify-center px-12">

<div class="eyebrow mb-10">
The question
</div>

<h1 class="!text-4xl !leading-[1.6] font-serif max-w-5xl" style="color: var(--c-fg)">
So how do we adapt this for the<br/>
<span class="grad">LBO eigendecomposition</span>?
</h1>

</div>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Method &nbsp;·&nbsp; LBO specialization
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Plug in <span class="grad">&Delta;</span>.
</h2>

<div class="flow-step" v-click="1">

Plug $L = \Delta$ (the **Laplace&ndash;Beltrami operator**).

</div>

<div class="flow-step" v-click="2">

$\Delta$ measures smoothness &nbsp;&rArr;&nbsp; $\mathcal{C}_L$ is the family of **smooth-enough** signals.

</div>

<div class="grid grid-cols-2 gap-3 versions-grid" v-click="3">

<div class="flow-step">

<div class="version-label">Non-symmetric</div>

<div class="eq-row">

$$\Delta \;=\; M^{-1} S$$

</div>

</div>

<div class="flow-step">

<div class="version-label">Normalized symmetric</div>

<div class="eq-row">

$$\Delta_{\text{sym}} \;=\; M^{-1/2}\, S\, M^{-1/2}$$

</div>

</div>

</div>

<div class="flow-step finale mt-auto" v-click="4">

We aim for $\Delta_{\text{sym}}$: **Euclidean orthogonal eigenvectors** + **first eigenvector encodes vertex mass**.

</div>

</div>

<style>
.flow-step {
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.6rem 1.0rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  font-size: 0.92rem;
  line-height: 1.5;
  color: var(--c-fg-body);
}
.flow-step.finale {
  border-left-color: var(--c-success);
  background: rgba(4, 120, 87, 0.06);
}
.versions-grid {
  margin-bottom: 0.5rem;
}
.versions-grid .flow-step {
  margin-bottom: 0;
  text-align: center;
  padding: 0.55rem 0.8rem;
}
.version-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 600;
  margin-bottom: 0.25rem;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-2 text-center">
Method &nbsp;·&nbsp; Pipeline
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
The full <span class="grad">pipeline</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">
  <div class="pipeline-stage">
    <img
      :src="`${$slidev.configs.base ?? '/'}pipeline.png`"
      class="pipeline-img"
      alt="Method pipeline"
    />
    <div class="hl-rect upper-branch" v-click="[1, 2]"></div>
    <div class="hl-rect lower-branch" v-click="[2, 3]"></div>
    <div class="hl-rect right-part" v-click="3"></div>
  </div>
</div>

<div class="branch-desc-area">

<div class="branch-desc upper-desc" v-click="[1, 2]">

<span class="branch-label upper-label">Signal smoothing</span> &mdash; we sample $f \sim p_L$ by Gaussian-smoothing random noise on the manifold sample.

</div>

<div class="branch-desc lower-desc" v-click="[2, 3]">

<span class="branch-label lower-label">Eigenbasis prediction</span> &mdash; network + QR turn the manifold sample into the predicted eigenbasis of $\Delta_{\text{sym}}$.

</div>

<div class="branch-desc right-desc" v-click="3">

<span class="branch-label right-label">Reconstruction loss</span> &mdash; $M$-weighted projection of the signals onto the predicted basis gives the loss $\mathcal{L}_{\text{rec}}$.

</div>

</div>

</div>

<style>
.pipeline-stage {
  position: relative;
  display: inline-block;
  max-height: 100%;
  max-width: 100%;
}
.pipeline-img {
  display: block;
  max-height: 100%;
  max-width: 100%;
  object-fit: contain;
}
.hl-rect {
  position: absolute;
  border: 3px solid #c2410c;
  border-radius: 8px;
  pointer-events: none;
}
.hl-rect.upper-branch {
  top: -5%;
  left: -1%;
  width: 77.5%;
  height: 52%;
}
.hl-rect.lower-branch {
  top: 51%;
  left: -1%;
  width: 77.5%;
  height: 52%;
  border-color: #2B5876;
}
.hl-rect.right-part {
  top: -5%;
  left: 76%;
  width: 25%;
  height: 108%;
  border-color: #047857;
}
.branch-desc-area {
  display: grid;
  grid-template-columns: 1fr;
  margin-top: 0.6rem;
}
.branch-desc-area .branch-desc {
  grid-column: 1;
  grid-row: 1;
}
.branch-desc {
  padding: 0.55rem 1rem;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  font-size: 0.85rem;
  line-height: 1.45;
  color: var(--c-fg-body);
  text-align: center;
}
.branch-desc.upper-desc {
  border-left: 3px solid #c2410c;
  background: rgba(194, 65, 12, 0.06);
}
.branch-desc.lower-desc {
  border-left: 3px solid #2B5876;
  background: rgba(43, 88, 118, 0.06);
}
.branch-desc.right-desc {
  border-left: 3px solid #047857;
  background: rgba(4, 120, 87, 0.06);
}
.branch-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.66rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  font-weight: 700;
  margin-right: 0.4rem;
}
.branch-label.upper-label { color: #c2410c; }
.branch-label.lower-label { color: #2B5876; }
.branch-label.right-label { color: #047857; }
</style>

---
layout: default
class: text-center
hide: true
---

<div class="h-full relative flex flex-col items-center justify-center px-12">

<div class="eyebrow mb-6 relative z-10">
Results &nbsp;·&nbsp; 3D overfitting
</div>

<h1 class="!text-4xl !leading-[1.4] font-serif max-w-5xl !mb-8 relative z-10" style="color: var(--c-fg)">
Learning the <span class="grad">eigenbasis of a single 3D shape</span>.
</h1>

<img
  :src="`${$slidev.configs.base ?? '/'}thumbs/pegaso.png`"
  class="h-48 object-contain relative z-10"
  alt="Pegaso shape"
/>

</div>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; 3D overfitting
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
Cosine similarity &amp; <span class="grad">eigenvalue discrepancy</span>.
</h2>

<div class="overfitting-table">

| Shape | &nbsp; | $k \le 10$ | $k \le 20$ | $k \le 50$ | $\lambda$ discrepancy |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Armadillo    | <img :src="`${$slidev.configs.base ?? '/'}thumbs/armadillo.png`"    class="thumb" /> | 0.968 | 0.967 | 0.773 | 0.200 $\pm$ 0.126 |
| Bimba        | <img :src="`${$slidev.configs.base ?? '/'}thumbs/bimba.png`"        class="thumb" /> | 0.964 | 0.945 | 0.822 | 0.093 $\pm$ 0.145 |
| Botijo       | <img :src="`${$slidev.configs.base ?? '/'}thumbs/botijo.png`"       class="thumb" /> | 0.972 | 0.955 | 0.813 | 0.153 $\pm$ 0.092 |
| Elephant     | <img :src="`${$slidev.configs.base ?? '/'}thumbs/elephant.png`"     class="thumb" /> | 0.979 | 0.866 | 0.687 | 0.105 $\pm$ 0.123 |
| Fertility    | <img :src="`${$slidev.configs.base ?? '/'}thumbs/fertility.png`"    class="thumb" /> | 0.874 | 0.866 | 0.720 | 0.083 $\pm$ 0.106 |
| Kitten       | <img :src="`${$slidev.configs.base ?? '/'}thumbs/kitten.png`"       class="thumb" /> | 0.993 | 0.988 | 0.981 | 0.088 $\pm$ 0.104 |
| Laurent Hand | <img :src="`${$slidev.configs.base ?? '/'}thumbs/laurent_hand.png`" class="thumb" /> | 0.823 | 0.696 | 0.568 | 0.066 $\pm$ 0.078 |
| Lion         | <img :src="`${$slidev.configs.base ?? '/'}thumbs/lion.png`"         class="thumb" /> | 0.951 | 0.908 | 0.822 | 0.067 $\pm$ 0.086 |
| Pegaso       | <img :src="`${$slidev.configs.base ?? '/'}thumbs/pegaso.png`"       class="thumb" /> | 0.932 | 0.797 | 0.544 | 0.142 $\pm$ 0.140 |

</div>

<div class="table-caption mt-2 text-center">
Avg. cosine similarity between predicted and oracle eigenfunctions, and mean relative eigenvalue discrepancy.
</div>

</div>

<style>
.overfitting-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.76rem;
}
.overfitting-table th,
.overfitting-table td {
  padding: 0.16rem 0.6rem;
  border-top: 1px solid var(--c-border);
}
.overfitting-table thead th {
  border-top: none;
  border-bottom: 2px solid var(--c-fg);
  font-weight: 700;
  color: var(--c-fg);
}
.overfitting-table tbody tr:last-child td {
  border-bottom: 2px solid var(--c-fg);
}
.overfitting-table .thumb {
  height: 32px;
  width: auto;
  object-fit: contain;
  display: inline-block;
}
.table-caption {
  font-size: 0.74rem;
  color: var(--c-fg-muted);
  font-style: italic;
  line-height: 1.35;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-row gap-3">

<div class="title-col">
  <div class="eyebrow mb-2">Results &nbsp;·&nbsp; 3D overfitting</div>
  <h2 class="!text-lg !leading-snug !mb-0 font-serif" style="color: var(--c-fg)">
    Predicted vs. <span class="grad">oracle eigenfunctions</span> (I).
  </h2>
</div>

<div class="flex-1 min-w-0 flex items-center pr-6">
  <img
    :src="`${$slidev.configs.base ?? '/'}supp_overfit1@0.5x.png`"
    class="h-full w-full object-contain object-right"
    alt="Overfitting eigenfunctions, part I"
  />
</div>

</div>

<style>
.slidev-layout {
  padding: 0.75rem !important;
}
.title-col {
  width: 14rem;
  flex-shrink: 0;
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-row gap-3">

<div class="title-col">
  <div class="eyebrow mb-2">Results &nbsp;·&nbsp; 3D overfitting</div>
  <h2 class="!text-lg !leading-snug !mb-0 font-serif" style="color: var(--c-fg)">
    Predicted vs. <span class="grad">oracle eigenfunctions</span> (II).
  </h2>
</div>

<div class="flex-1 min-w-0 flex items-center pr-6">
  <img
    :src="`${$slidev.configs.base ?? '/'}supp_overfit2@0.5x.png`"
    class="h-full w-full object-contain object-right"
    alt="Overfitting eigenfunctions, part II"
  />
</div>

</div>

<style>
.slidev-layout {
  padding: 0.75rem !important;
}
.title-col {
  width: 14rem;
  flex-shrink: 0;
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-row gap-3">

<div class="title-col">
  <div class="eyebrow mb-2">Results &nbsp;·&nbsp; 3D overfitting</div>
  <h2 class="!text-lg !leading-snug !mb-0 font-serif" style="color: var(--c-fg)">
    <span class="grad">Predicted metric</span>.
  </h2>
</div>

<div class="flex-1 min-w-0 flex items-center pr-6">
  <img
    :src="`${$slidev.configs.base ?? '/'}supp_metric@0.5x.png`"
    class="h-full w-full object-contain object-right"
    alt="Evaluation metric"
  />
</div>

</div>

<style>
.slidev-layout {
  padding: 0.75rem !important;
}
.title-col {
  width: 14rem;
  flex-shrink: 0;
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}
</style>

---
layout: default
class: text-center
hide: true
---

<div class="h-full relative flex flex-col items-center justify-center px-12">

<img :src="`${$slidev.configs.base ?? '/'}thumbs/bimba.png`"          class="thumb-deco" style="top: 6%;   left: 4%;"  />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/horse.png`"          class="thumb-deco" style="top: 8%;   right: 6%;" />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/heptoroid.png`"      class="thumb-deco" style="top: 45%;  left: 2%;"  />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/eros.png`"           class="thumb-deco" style="top: 48%;  right: 3%;" />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/beetle.png`"         class="thumb-deco" style="bottom: 8%; left: 14%;" />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/fertility.png`"      class="thumb-deco" style="bottom: 6%; right: 12%;"/>
<img :src="`${$slidev.configs.base ?? '/'}thumbs/woodenfish.png`"     class="thumb-deco" style="top: 5%;   left: 38%;" />
<img :src="`${$slidev.configs.base ?? '/'}thumbs/wrench.png`"         class="thumb-deco" style="bottom: 5%; left: 44%;" />

<div class="eyebrow mb-6 relative z-10">
Results &nbsp;·&nbsp; 3D generalization
</div>

<h1 class="!text-4xl !leading-[1.4] font-serif max-w-5xl !mb-0 relative z-10" style="color: var(--c-fg)">
Attempting to <span class="grad">generalize</span>&hellip;
</h1>

</div>

<style>
.thumb-deco {
  position: absolute;
  height: 145px;
  width: auto;
  object-fit: contain;
  opacity: 0.85;
  z-index: 0;
  pointer-events: none;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-row gap-3">

<div class="title-col">
  <div class="eyebrow mb-2">Results &nbsp;·&nbsp; 3D generalization</div>
  <h2 class="!text-lg !leading-snug !mb-0 font-serif" style="color: var(--c-fg)">
    Predicted vs. <span class="grad">oracle eigenfunctions</span>.
  </h2>
</div>

<div class="flex-1 min-w-0 flex items-center pr-6">
  <img
    :src="`${$slidev.configs.base ?? '/'}generalization_qualitative@0.5x.png`"
    class="h-full w-full object-contain object-right"
    alt="Generalization qualitative"
  />
</div>

</div>

<style>
.slidev-layout {
  padding: 0.75rem !important;
}
.title-col {
  width: 14rem;
  flex-shrink: 0;
  padding-left: 1.5rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: left;
}
</style>

---
layout: default
class: text-center
hide: true
---

<div class="h-full relative flex flex-col items-center justify-center px-12">

<img
  :src="`${$slidev.configs.base ?? '/'}image_manifold.png`"
  class="manifold-bg"
  alt="Image manifold backdrop"
/>

<div class="eyebrow mb-6 relative z-10">
Results &nbsp;·&nbsp; Image manifold
</div>

<h1 class="!text-4xl !leading-[1.4] font-serif max-w-5xl !mb-0 relative z-10" style="color: var(--c-fg)">
Learning the <span class="grad">eigenbasis of the image manifold</span>.
</h1>

</div>

<style>
.slidev-layout {
  padding: 0 !important;
}
.manifold-bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.25;
  z-index: 0;
  pointer-events: none;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Method &nbsp;·&nbsp; Image manifold
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
Setup.
</h2>

<div class="dataset-strip mb-3">
  <img :src="`${$slidev.configs.base ?? '/'}datasets/imagenette_1.jpg`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/imagenette_2.jpg`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/imagenette_3.jpg`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/imagenette_4.jpg`" class="ds-thumb" />
  <span class="ds-divider"></span>
  <img :src="`${$slidev.configs.base ?? '/'}datasets/stl10_1.png`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/stl10_2.png`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/stl10_3.png`" class="ds-thumb" />
  <img :src="`${$slidev.configs.base ?? '/'}datasets/stl10_4.png`" class="ds-thumb" />
</div>

<div class="flow-step" v-click="1">

**Datasets** &mdash; Imagenette and STL10.

</div>

<div class="flow-step" v-click="2">

**Embed each image** &mdash; CLIP (512-d) and DINOv2 (768-d) features.

</div>

<div class="flow-step" v-click="3">

**Train** &mdash; run the same eigenbasis pipeline on sampled subsets of the embeddings.

</div>

<div class="flow-step finale" v-click="4">

**Test** &mdash; compare on dimensionality reduction against UMAP, t-SNE, PCA, and Laplacian eigenmaps.

</div>

</div>

<style>
.dataset-strip {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.4rem;
}
.dataset-strip .ds-thumb {
  height: 52px;
  width: 52px;
  object-fit: cover;
  border-radius: 4px;
  border: 1px solid var(--c-border);
}
.dataset-strip .ds-divider {
  display: inline-block;
  width: 1px;
  height: 36px;
  background: var(--c-border);
  margin: 0 0.4rem;
}
.flow-step {
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.55rem 1.0rem;
  border-radius: 8px;
  margin-bottom: 0.4rem;
  font-size: 0.88rem;
  line-height: 1.45;
  color: var(--c-fg-body);
}
.flow-step.finale {
  border-left-color: var(--c-success);
  background: rgba(4, 120, 87, 0.06);
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-3 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; Image manifold
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
<span class="grad">Imagenette</span> clusters.
</h2>

<div class="cluster-grid">
  <div class="cluster-cell">
    <div class="cluster-label">CLIP</div>
    <img
      :src="`${$slidev.configs.base ?? '/'}supp_imagenette_clip_cluster1@3x.png`"
      class="cluster-img"
      alt="Imagenette CLIP cluster"
    />
  </div>
  <div class="cluster-cell">
    <div class="cluster-label">DINOv2</div>
    <img
      :src="`${$slidev.configs.base ?? '/'}supp_imagenette_dino_cluster1@3x.png`"
      class="cluster-img"
      alt="Imagenette DINOv2 cluster"
    />
  </div>
</div>

</div>

<style>
.cluster-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
}
.cluster-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 0;
}
.cluster-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 700;
  margin-bottom: 0.35rem;
}
.cluster-img {
  flex: 1;
  min-height: 0;
  max-width: 100%;
  object-fit: contain;
}
.cluster-cell + .cluster-cell {
  border-left: 1px solid var(--c-border);
  padding-left: 0.8rem;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-3 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; Image manifold
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
<span class="grad">STL10</span> clusters.
</h2>

<div class="cluster-grid">
  <div class="cluster-cell">
    <div class="cluster-label">CLIP</div>
    <img
      :src="`${$slidev.configs.base ?? '/'}supp_stl10_clip_cluster1@3x.png`"
      class="cluster-img"
      alt="STL10 CLIP cluster"
    />
  </div>
  <div class="cluster-cell">
    <div class="cluster-label">DINOv2</div>
    <img
      :src="`${$slidev.configs.base ?? '/'}supp_stl10_dino_cluster1@3x.png`"
      class="cluster-img"
      alt="STL10 DINOv2 cluster"
    />
  </div>
</div>

</div>

<style>
.cluster-grid {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.6rem;
}
.cluster-cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 0;
}
.cluster-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.7rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 700;
  margin-bottom: 0.35rem;
}
.cluster-img {
  flex: 1;
  min-height: 0;
  max-width: 100%;
  object-fit: contain;
}
.cluster-cell + .cluster-cell {
  border-left: 1px solid var(--c-border);
  padding-left: 0.8rem;
}
</style>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-3 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Results &nbsp;·&nbsp; Image manifold
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
Quantitative comparison &mdash; <span class="grad">NMI &amp; ARI</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}comparison_barchart_nmi_ari.png`"
    class="h-full w-full object-contain"
    alt="NMI and ARI bar chart"
  />
</div>

</div>

---
layout: default
class: text-left
hide: true
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Conclusion &nbsp;·&nbsp; Trade-offs
</div>

<h2 class="!text-2xl !leading-snug !mb-4 font-serif text-center" style="color: var(--c-fg)">
Trade-offs vs. the <span class="grad">traditional pipeline</span>.
</h2>

<div class="tradeoff-grid">

<div class="tradeoff-box gains">

<div class="tradeoff-label">What we gain</div>

- **Mesh-free** &mdash; works from a raw sample of any manifold
- **Differentiable** &mdash; end-to-end into deep-learning pipelines
- **Generalizes** &mdash; one trained model handles many shapes
- **Operator-agnostic** &mdash; probe choice picks the spectral basis
- **High-dim ready** &mdash; sidesteps discretization in &gt;3D

</div>

<div class="tradeoff-box costs">

<div class="tradeoff-label">What we trade</div>

- **Probe design** replaces operator construction (simpler in high-dim)
- **Training cost** &mdash; &sim;8&nbsp;min overfit / 24&nbsp;h generalization (one-time)
- **Approximate basis** &mdash; close to, not identical to, cotangent Laplacian
- **Exact eigenvalues** need hyperparameter tuning (the basis itself is robust)

</div>

</div>

<div class="bottom-line mt-auto">

<div class="bottom-line-label">Net</div>

We swap **operator construction** for **probe design** &mdash; a favorable trade as the manifold dimension grows.

</div>

</div>

<style>
.tradeoff-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.8rem;
  margin-bottom: 0.8rem;
}
.tradeoff-box {
  border: 1px solid var(--c-border);
  background: var(--c-bg-soft);
  padding: 0.7rem 1.1rem;
  border-radius: 8px;
  font-size: 0.82rem;
  line-height: 1.5;
  color: var(--c-fg-body);
}
.tradeoff-box.gains {
  border-left: 3px solid var(--c-success);
  background: rgba(4, 120, 87, 0.05);
}
.tradeoff-box.costs {
  border-left: 3px solid var(--c-accent);
  background: rgba(180, 83, 9, 0.05);
}
.tradeoff-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 700;
  margin-bottom: 0.5rem;
}
.tradeoff-box.gains .tradeoff-label { color: var(--c-success); }
.tradeoff-box.costs .tradeoff-label { color: var(--c-accent); }
.tradeoff-box ul {
  margin: 0;
  padding-left: 1.1rem;
}
.tradeoff-box li {
  margin-bottom: 0.2rem;
}
.bottom-line {
  text-align: center;
  font-size: 0.92rem;
  line-height: 1.5;
  color: var(--c-fg);
  border: 1px solid rgba(78, 67, 118, 0.45);
  border-left: 3px solid var(--c-brand-from);
  background: rgba(78, 67, 118, 0.06);
  padding: 0.65rem 1.0rem;
  border-radius: 8px;
}
.bottom-line-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--c-brand-from);
  font-weight: 700;
  margin-bottom: 0.3rem;
}
</style>

---
layout: default
class: text-center
hide: true
---

<div class="absolute inset-0 flex items-start justify-center pointer-events-none z-0 pt-8">
  <img
    :src="`${$slidev.configs.base ?? '/'}cvpr2026_logo.png`"
    alt=""
    class="w-[85%] max-h-[40%] object-contain"
    style="opacity: 0.18;"
  />
</div>

<div class="relative z-10 flex flex-col items-center justify-center h-full">

<h1 class="!text-6xl !leading-tight !mb-6 grad">
Thank you!
</h1>

<div class="text-xl mb-8" style="color: var(--c-fg-body)">
Questions?
</div>

<div class="text-sm muted">
Roy Velich &nbsp;·&nbsp; Arkadi Piven &nbsp;·&nbsp; David Bensa&iuml;d &nbsp;·&nbsp; Daniel Cremers &nbsp;·&nbsp; Thomas Dag&egrave;s &nbsp;·&nbsp; Ron Kimmel
</div>

</div>

<div class="abs-b w-full text-center pb-6 text-xs italic muted z-10">
In memory of Ha&iuml;m Brezis (1944 &ndash; 2024)
</div>

---
layout: default
class: text-center
clicks: 3
hide: true
---

<!--
ANIMATION TEST — Standard Slidev pattern for "element A flies to element B".

Grid layout (5 columns, gap 10px):
  col 1: img (100px),  left edge 0
  col 2: img (100px),  left edge 110
  col 3: dots (30px),  left edge 220
  col 4: img (100px),  left edge 260
  col 5: img (100px),  left edge 370

Click 1: clones in row 2 col i animate IN from row 1 col 1 (x=0). Sources:
  col 1: (   0, -110)
  col 2: (-110, -110)
  col 4: (-260, -110)
  col 5: (-370, -110)
Click 2: row 3 armadillos animate IN from row 2 (directly above) with opacity.
  Row 3 dots: CSS transition with transition-delay: 800ms so they fade in
  AFTER the armadillos land.
Click 3: '+' signs appear between consecutive row-3 items. Positioned
  absolutely at the gap midpoints (x = 105, 215, 255, 365).
-->

<h2 class="!text-2xl !leading-snug !mb-4 font-serif">
Animation test &mdash; armadillo clones
</h2>

<div class="atest-grid">
<!-- Row 1 -->
<div class="atest-cell"><img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" /></div>
<div class="atest-cell"><img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" /></div>
<div class="atest-dots-cell">⋯</div>
<div class="atest-cell"><img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" /></div>
<div class="atest-cell"><img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" /></div>

<!-- Row 2 — each cell hosts a clone overlay -->
<div class="atest-cell">
  <img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
  <img class="atest-clone" v-motion :initial="{ x: 0, y: -110 }" :click-1="{ x: 0, y: 0 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" />
</div>
<div class="atest-cell">
  <img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
  <img class="atest-clone" v-motion :initial="{ x: -110, y: -110 }" :click-1="{ x: 0, y: 0 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" />
</div>
<div class="atest-dots-cell">⋯</div>
<div class="atest-cell">
  <img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
  <img class="atest-clone" v-motion :initial="{ x: -260, y: -110 }" :click-1="{ x: 0, y: 0 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" />
</div>
<div class="atest-cell">
  <img class="atest-img" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
  <img class="atest-clone" v-motion :initial="{ x: -370, y: -110 }" :click-1="{ x: 0, y: 0 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_signal_diff_01_tight.png`" />
</div>

<!-- Row 3 — armadillos animate IN from row 2 (directly above) on click 2.
     On click 3 they translate outward (-30, -15, +15, +30) to widen the
     gaps so the '+' signs can sit comfortably between them and the dots. -->
<div class="atest-cell">
  <img class="atest-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-2="{ x: 0, y: 0, opacity: 1 }" :click-3="{ x: -30, y: 0, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
</div>
<div class="atest-cell">
  <img class="atest-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-2="{ x: 0, y: 0, opacity: 1 }" :click-3="{ x: -15, y: 0, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
</div>
<div class="atest-dots-cell atest-dots-row3" :class="{ shown: $clicks >= 2 }">⋯</div>
<div class="atest-cell">
  <img class="atest-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-2="{ x: 0, y: 0, opacity: 1 }" :click-3="{ x: 15, y: 0, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
</div>
<div class="atest-cell">
  <img class="atest-clone" v-motion :initial="{ x: 0, y: -140, opacity: 0 }" :click-2="{ x: 0, y: 0, opacity: 1 }" :click-3="{ x: 30, y: 0, opacity: 1 }" :src="`${$slidev.configs.base ?? '/'}applications/manifold_pc_points_tight.png`" />
</div>

<!-- '+' signs at the WIDENED midpoints (after the row-3 armadillos spread out on click 3). Original gap midpoints (105, 215, 255, 365) shift to (82.5, 207.5, 262.5, 387.5). -->
<span class="atest-plus" :class="{ shown: $clicks >= 3 }" style="left: 82.5px;">+</span>
<span class="atest-plus" :class="{ shown: $clicks >= 3 }" style="left: 207.5px;">+</span>
<span class="atest-plus" :class="{ shown: $clicks >= 3 }" style="left: 262.5px;">+</span>
<span class="atest-plus" :class="{ shown: $clicks >= 3 }" style="left: 387.5px;">+</span>
</div>

<div class="text-sm muted mt-6">Click 1: clones of row-1 col 1 fly to row 2. Click 2: row 3 armadillos appear; dots fade in at the end. Click 3: '+' signs appear between row-3 armadillos.</div>

<style>
.atest-grid {
  position: relative;
  display: grid;
  grid-template-columns: 100px 100px 30px 100px 100px;
  grid-template-rows: repeat(3, 100px);
  gap: 10px;
  /* Explicit width = 100*4 + 30 + 10*4 = 470. Without this, the grid container
     stretches to fill its parent and absolute children get positioned relative
     to the container edge (not the track edge). */
  width: 470px;
  margin: 0 auto;
}
.atest-cell {
  position: relative;
  width: 100px;
  height: 100px;
}
.atest-img {
  width: 100px;
  height: 100px;
  object-fit: contain;
  display: block;
}
.atest-clone {
  position: absolute;
  top: 0;
  left: 0;
  width: 100px;
  height: 100px;
  object-fit: contain;
}
.atest-dots-cell {
  width: 30px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.6rem;
  line-height: 1;
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  letter-spacing: 0.05em;
}
.atest-dots-row3 {
  opacity: 0;
  transition: opacity 350ms ease;
  transition-delay: 0ms;
}
.atest-dots-row3.shown {
  opacity: 1;
  transition-delay: 50ms;
}
.atest-plus {
  position: absolute;
  /* Row 3 occupies y = 220..320 (rows 1-2 plus their gaps). Center the
     character vertically with a 100px-tall flex box. */
  top: 220px;
  height: 100px;
  display: flex;
  align-items: center;
  font-size: 1.4rem;
  line-height: 1;
  color: var(--c-fg-subtle);
  font-family: 'EB Garamond', serif;
  opacity: 0;
  transform: translateX(-50%);
  transition: opacity 350ms ease;
  pointer-events: none;
}
.atest-plus.shown { opacity: 1; }
</style>
