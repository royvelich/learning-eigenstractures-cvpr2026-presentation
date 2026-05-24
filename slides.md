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

<div class="text-sm muted max-w-3xl">
<sup>1</sup>Technion — Israel Institute of Technology &nbsp;&nbsp;·&nbsp;&nbsp;
<sup>2</sup>Technical University of Munich &nbsp;&nbsp;·&nbsp;&nbsp;
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

<h2 class="!text-xl !leading-snug !mb-2 max-w-4xl font-serif" style="color: var(--c-fg-muted)">
At every point, the <span class="lbo">Laplacian</span> asks
</h2>

<h1 class="!text-3xl !leading-tight max-w-5xl font-serif grad italic">
"how different am I from my neighbours?"
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

<!-- f-cloud: starts large/centred, scales down & slides left on click 1 -->
<div
  v-motion
  :initial="{ x: 0, scale: 1 }"
  :click-1="{ x: -150, scale: 0.50 }"
  class="absolute"
  style="top: 137px; left: 260px;"
>
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_coloured.png`"
    style="width: 460px; display: block;"
    alt="f, the input function"
  />
</div>

<!-- Δ on the left -->
<div v-click="1" class="absolute math-grad"
     style="top: 50%; left: 130px; font-size: 60px; transform: translateY(calc(-50% + 8px));">

$\Delta$

</div>

<!-- ( opening paren -->
<div v-click="1" class="absolute"
     style="top: 50%; left: 205px; font-size: 60px; color: var(--c-fg-muted); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  (
</div>

<!-- ) closing paren -->
<div v-click="1" class="absolute"
     style="top: 50%; left: 450px; font-size: 60px; color: var(--c-fg-muted); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  )
</div>

<!-- = sign -->
<div v-click="2" class="absolute"
     style="top: 50%; left: 510px; font-size: 48px; color: var(--c-fg); font-family: 'EB Garamond', serif; transform: translateY(-50%);">
  =
</div>

<!-- Δf-cloud, the output -->
<img v-click="3"
  :src="`${$slidev.configs.base ?? '/'}applications/data_manifold_laplacian_full.png`"
  class="absolute"
  style="top: 50%; left: 560px; transform: translateY(-50%); width: 230px;"
  alt="Δf, the Laplacian output"
/>

<!-- Bottom caption -->
<div v-click="3" class="absolute left-0 right-0 text-center" style="bottom: 80px;">

the Laplacian <em>eats</em> a function and returns another

</div>

<!-- Eigendecomposition motivator -->
<div v-click="4" class="absolute left-0 right-0 text-center" style="bottom: 32px;">

it's an operator — so we can ask for its <span class="lbo">spectrum</span>: eigenfunctions and eigenvalues.

</div>

</div>

---
layout: default
class: text-center
---

<div class="h-full flex flex-col pt-4 pb-4 px-6 text-center">

<div class="eyebrow mb-1">
Primer · in Euclidean space
</div>

<h2 class="!text-xl !leading-snug !mb-3 font-serif" style="color: var(--c-fg)">
Same question — the neighbourhood is a <span class="lbo">unit ball</span>.
</h2>

<div class="flex-1 min-h-0 grid grid-cols-2 gap-x-8 gap-y-3" style="grid-template-rows: 1fr auto;">

<div class="min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_euclidean_1d.png`"
    class="max-h-full max-w-full object-contain"
    alt="Laplacian setup on R — focal x0 with interval neighbourhood"
  />
</div>

<div class="min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_euclidean_2d.png`"
    class="max-h-full max-w-full object-contain"
    alt="Laplacian setup on R^2 — focal x0 with disk neighbourhood"
  />
</div>

<div class="text-center flex items-center justify-center" style="font-size: 20px;">

$\Delta f = \dfrac{d^2 f}{dx^2}$

</div>

<div class="text-center flex items-center justify-center" style="font-size: 20px;">

$\Delta f = \dfrac{\partial^2 f}{\partial u^2} + \dfrac{\partial^2 f}{\partial v^2}$

</div>

</div>

</div>

---
layout: default
class: text-center
---

<div class="h-full flex flex-col pt-2 pb-2 px-2 text-center">

<div class="eyebrow mb-0">
Primer · on a curved domain
</div>

<h2 class="!text-lg !leading-snug !mb-1 font-serif" style="color: var(--c-fg)">
Same question — the domain itself is now a <span class="lbo">curved manifold</span>.
</h2>

<div class="flex-1 min-h-0 flex items-center justify-center">
  <img
    :src="`${$slidev.configs.base ?? '/'}applications/lap_curved_2d.png`"
    class="max-h-full max-w-full object-contain"
    style="height: 100%;"
    alt="curved domain M with the function f as a sheet floating above it"
  />
</div>

<div class="text-center mt-1" style="font-size: 18px;">

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
  <img :src="`${$slidev.configs.base ?? '/'}applications/app_02_corr_cat.png`" alt="Shape correspondence" />
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

<div class="h-full flex flex-col pt-6 pb-4 px-2">

<div class="eyebrow mb-2 text-center">
Background &nbsp;·&nbsp; The traditional pipeline
</div>

<h2 class="!text-2xl !leading-snug !mb-8 font-serif text-center" style="color: var(--c-fg)">
Computing the Laplacian eigenstructure, <span class="grad">step by step</span>
</h2>

<div class="flex-1 min-h-0 pipe-grid">

<!-- Titles (row 1) -->
<div class="pipe-title" style="grid-column: 1; grid-row: 1;" v-click="1">Triangulation</div>
<div class="pipe-title" style="grid-column: 3; grid-row: 1;" v-click="3">Stiffness &amp; Mass</div>
<div class="pipe-title" style="grid-column: 5; grid-row: 1;" v-click="4">Eigensolve</div>
<div class="pipe-title" style="grid-column: 7; grid-row: 1;" v-click="5">Eigenbasis</div>

<!-- Arrows span the content row -->
<div class="pipe-arrow" style="grid-column: 2; grid-row: 2;" v-click="3">›</div>
<div class="pipe-arrow" style="grid-column: 4; grid-row: 2;" v-click="4">›</div>
<div class="pipe-arrow" style="grid-column: 6; grid-row: 2;" v-click="5">›</div>

<!-- Content (row 2) -->
<div class="pipe-img-wrap relative" style="grid-column: 1; grid-row: 2;">
  <img
    v-click="1"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_vertices.png`"
    class="absolute inset-0 m-auto"
    style="max-height: 100%; max-width: 100%; object-fit: contain;"
    alt="Vertices"
  />
  <img
    v-click="2"
    :src="`${$slidev.configs.base ?? '/'}applications/pipeline_triangulation.png`"
    class="absolute inset-0 m-auto"
    style="max-height: 100%; max-width: 100%; object-fit: contain;"
    alt="Triangle mesh"
  />
</div>

<div class="pipe-img-wrap" style="grid-column: 3; grid-row: 2;" v-click="3">
  <img :src="`${$slidev.configs.base ?? '/'}applications/pipeline_voronoi_cot.png`" alt="Voronoi cell and cotangent angles" />
</div>

<div class="pipe-eq-only" style="grid-column: 5; grid-row: 2;" v-click="4">

$$S\boldsymbol{\phi} = \lambda\, M\boldsymbol{\phi}$$

</div>

<div class="pipe-eq-only" style="grid-column: 7; grid-row: 2;" v-click="5">

$\{\boldsymbol{\phi}_i\}$ &nbsp;,&nbsp; $\{\lambda_i\}$

</div>

<!-- Captions (row 3) -->
<div class="pipe-caption" style="grid-column: 1; grid-row: 3;">&nbsp;</div>
<div class="pipe-caption" style="grid-column: 3; grid-row: 3;" v-click="3">

$M$ &nbsp;,&nbsp; $S$

</div>
<div class="pipe-caption" style="grid-column: 5; grid-row: 3;">&nbsp;</div>
<div class="pipe-caption" style="grid-column: 7; grid-row: 3;">&nbsp;</div>

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
---

<div class="h-full flex flex-col pt-6 pb-4 px-2">

<div class="eyebrow mb-2 text-center">
Background &nbsp;·&nbsp; Where the pipeline breaks down
</div>

<h2 class="!text-2xl !leading-snug !mb-8 font-serif text-center" style="color: var(--c-fg)">
Three <span class="grad">unavoidable bottlenecks</span>.
</h2>

<div class="grid grid-cols-3 gap-8 flex-1 min-h-0 bottleneck-grid">

<div class="bottleneck-tile">
  <div class="bottleneck-img-wrap">
    <img :src="`${$slidev.configs.base ?? '/'}applications/pipeline_triangulation.png`" alt="Triangulation of a 2-manifold" />
  </div>
  <div class="bottleneck-cap">

Hard-coded $d_\text{int} = 2$

</div>
</div>

<div class="bottleneck-tile">
  <div class="bottleneck-img-wrap">
    <img :src="`${$slidev.configs.base ?? '/'}applications/bottleneck_high_d_graph.png`" alt="High-dimensional graph" />
  </div>
  <div class="bottleneck-cap">

Doesn't scale to $\mathbb{R}^n$

</div>
</div>

<div class="bottleneck-tile">
  <div class="bottleneck-img-wrap">
    <img :src="`${$slidev.configs.base ?? '/'}applications/bottleneck_no_grad.png`" alt="No backpropagation" />
  </div>
  <div class="bottleneck-cap">

Not differentiable

</div>
</div>

</div>

<div class="text-center mt-6 text-sm muted italic">

We need a pipeline that is <span style="color: var(--c-fg-body); font-style: normal; font-weight: 600;">dimension-agnostic</span>, <span style="color: var(--c-fg-body); font-style: normal; font-weight: 600;">mesh-free</span>, and <span style="color: var(--c-fg-body); font-style: normal; font-weight: 600;">end-to-end differentiable</span>.

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
.bottleneck-cap {
  margin-top: 0.6rem;
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--c-fg);
  text-align: center;
  letter-spacing: -0.005em;
  min-height: 2.6em;
  display: flex;
  align-items: center;
  justify-content: center;
}
.bottleneck-cap p {
  margin: 0;
}
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

<div class="pipeline-block mb-4" v-click="1">

<div class="pipeline-row-label">Traditional</div>

<div class="pipeline-row-static">
  <div class="chip chip-hero">Point cloud</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }">Triangulation</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }">Stiffness &amp; Mass</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero" :class="{ 'chip-bypassed': $clicks >= 2 }">Eigensolve</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero">Eigenbasis</div>
</div>

</div>

<div class="pipeline-block mb-8" v-click="3">

<div class="pipeline-row-label ours-label">Ours</div>

<div class="pipeline-row-static">
  <div class="chip chip-hero">Point cloud</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero chip-net">Neural network</div>
  <div class="chip-arrow chip-arrow-hero">›</div>
  <div class="chip chip-hero">Eigenbasis</div>
</div>

</div>

<div class="grid grid-cols-2 gap-6 max-w-4xl mx-auto w-full" v-click="4">

<div class="benefit-card">

<div class="benefit-label bypass-label">Bypassed</div>

- No mesh or triangulation
- No operator assembly ($S,\, M$)
- No numerical eigensolver

</div>

<div class="benefit-card">

<div class="benefit-label gain-label">Gained</div>

- Works on raw point clouds
- Dimension-agnostic
- End-to-end differentiable

</div>

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
---

<div class="h-full flex flex-col pt-4 pb-3 px-2">

<div class="eyebrow mb-1 text-center">
Optimal approximation theory &nbsp;·&nbsp; Aflalo, Brezis et&nbsp;al. (2016)
</div>

<h2 class="!text-2xl !leading-snug !mb-3 font-serif text-center" style="color: var(--c-fg)">
Recover the <span class="grad">eigenbasis</span> <em>and</em> the <span class="grad">eigenvalues</span> of <i>L</i>.
</h2>

<div class="setup-cascade mb-4">

<div class="setup-chip" v-click="1">

**SPD operator** $L$

<div class="chip-sub">whose eigenbasis we want to learn</div>

</div>

<div class="setup-chip" v-click="2">

**Signal class** $\mathcal{C}_L = \{f : \|f\|_L^2 \le 1\}$

<div class="chip-sub">functions with bounded <i>L</i>-energy</div>

</div>

<div class="setup-chip" v-click="3">

**Distribution** $p_L$

<div class="chip-sub">uniform measure over <i>C</i><sub><i>L</i></sub></div>

</div>

</div>

<div class="theorem-lead mb-3" v-click="4">

The theorem says:

</div>

<div class="outcome-box train mb-3" v-click="4">

<div class="outcome-label">Eigenbasis</div>

The basis $\{b_i\}$ that minimizes the **expected** reconstruction error over $p_L$ is the **first $k$ eigenvectors of $L$**.

</div>

<div class="outcome-box theory mt-auto" v-click="5">

<div class="outcome-label">Eigenvalues</div>

At the eigenbasis, the **worst-case** reconstruction error over $\mathcal{C}_L$ is $\alpha_k = 1/\lambda_k$ &mdash; the **$k$-th eigenvalue** of $L$.

</div>

</div>

<style>
.setup-cascade {
  display: flex;
  align-items: stretch;
  justify-content: center;
  gap: 0.4rem;
}
.setup-chip {
  flex: 1 1 0;
  border: 1px solid var(--c-border);
  border-left: 3px solid var(--c-brand-from);
  background: var(--c-bg-soft);
  padding: 0.5rem 0.7rem;
  border-radius: 8px;
  text-align: center;
  font-size: 0.85rem;
  line-height: 1.35;
  color: var(--c-fg);
}
.setup-chip p {
  margin: 0;
}
.chip-sub {
  font-size: 0.72rem;
  color: var(--c-fg-muted);
  font-style: italic;
  margin-top: 0.2rem;
}
.theorem-lead {
  text-align: center;
  font-size: 0.88rem;
  line-height: 1.5;
  color: var(--c-fg-body);
  font-style: italic;
}
.outcome-box {
  border: 1px solid var(--c-border);
  background: var(--c-bg-soft);
  padding: 0.85rem 1.2rem;
  border-radius: 8px;
  font-size: 0.95rem;
  line-height: 1.55;
  color: var(--c-fg-body);
  text-align: center;
}
.outcome-box.theory {
  border-left: 3px solid var(--c-danger);
  background: rgba(185, 28, 28, 0.05);
}
.outcome-box.train {
  border-left: 3px solid var(--c-link);
  background: rgba(29, 78, 216, 0.05);
}
.outcome-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.62rem;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 0.3rem;
}
.outcome-box.theory .outcome-label { color: var(--c-danger); }
.outcome-box.train .outcome-label { color: var(--c-link); }
</style>

---
layout: default
class: text-center
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
