"""Intro primer — the Laplacian in 1D.

Two candidate figures:
  lap_1d_stencil.png  — neighbour-stencil / chord construction
  lap_1d_stacked.png  — f(x) above, f''(x) = Δf below
"""
from _common import OUT_DIR
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["mathtext.fontset"] = "cm"  # Computer Modern — the LaTeX look

INDIGO = "#4E4376"
RED = "#b91c1c"
BLUE = "#1d4ed8"
GRAY = "#94a3b8"


def f(x):
    return 1.0 * np.exp(-((x + 1.5) ** 2) / (2 * 0.62 ** 2)) \
        - 0.92 * np.exp(-((x - 1.5) ** 2) / (2 * 0.72 ** 2))


xs = np.linspace(-3.6, 3.6, 800)
ys = f(xs)

# ---- Figure A: neighbour-stencil / chord --------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.7))
ax.plot(xs, ys, color=INDIGO, lw=3.2, zorder=2)

for x0, h, col, lbl in [(-1.5, 0.95, RED, r"$\Delta f < 0$"),
                        (1.5, 1.05, BLUE, r"$\Delta f > 0$")]:
    xn = np.array([x0 - h, x0 + h])
    yn = f(xn)
    avg = yn.mean()
    ax.plot(xn, yn, "--", color=GRAY, lw=1.8, zorder=3)              # chord
    ax.scatter(xn, yn, color=GRAY, s=42, zorder=4)                    # neighbours
    ax.scatter([x0], [f(x0)], color=col, s=95, zorder=5)             # centre point
    ax.scatter([x0], [avg], color=GRAY, s=42, zorder=4)             # chord midpoint
    ax.annotate("", xy=(x0, avg), xytext=(x0, f(x0)),
                arrowprops=dict(arrowstyle="<->", color=col, lw=2.2), zorder=4)
    off = 0.20 if x0 < 0 else 0.20
    ax.text(x0 + off, (avg + f(x0)) / 2, lbl, color=col, fontsize=14,
            va="center", ha="left", fontweight="bold")

ax.text(-1.5, f(-1.5) + 0.16, "hill — $f$ above its neighbours", color=RED,
        fontsize=10.5, ha="center")
ax.text(1.5, f(1.5) - 0.20, "valley — $f$ below its neighbours", color=BLUE,
        fontsize=10.5, ha="center")

# coordinate axes — x is the 1-D Euclidean domain, f-axis vertical at the left
AXc = "#0f172a"
ax.annotate("", xy=(4.0, 0.0), xytext=(-3.75, 0.0),
            arrowprops=dict(arrowstyle="-|>", color=AXc, lw=1.7), zorder=1)
ax.text(4.10, 0.0, "$x$", fontsize=14, va="center")
ax.annotate("", xy=(-3.55, ys.max() + 0.36), xytext=(-3.55, ys.min() - 0.30),
            arrowprops=dict(arrowstyle="-|>", color=AXc, lw=1.7), zorder=1)
ax.text(-3.55, ys.max() + 0.52, "$f(x)$", fontsize=14, ha="center")

ax.set_xlim(-4.0, 4.6)
ax.set_ylim(ys.min() - 0.45, ys.max() + 0.72)
ax.axis("off")
plt.tight_layout()
plt.savefig(str(OUT_DIR / "lap_1d_stencil.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.05)
plt.close()
print("[ok] lap_1d_stencil.png")

# ---- Figure B: f(x) above, f''(x) below ---------------------------------
fpp = np.gradient(np.gradient(ys, xs), xs)
fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.6), sharex=True,
                             gridspec_kw=dict(height_ratios=[1, 1], hspace=0.12))
AXc = "#0f172a"


def x_axis(a):
    """Draw a labelled x-axis arrow along the f = 0 line of a panel."""
    a.annotate("", xy=(4.0, 0.0), xytext=(-3.75, 0.0),
               arrowprops=dict(arrowstyle="-|>", color=AXc, lw=1.6), zorder=1)
    a.text(4.10, 0.0, "$x$", fontsize=13, va="center")


a1.plot(xs, ys, color=INDIGO, lw=3.2)
x_axis(a1)
a1.set_title(r"$f(x)$", fontsize=13, color=INDIGO, loc="left")
a1.axis("off")

a2.fill_between(xs, fpp, 0, where=fpp < 0, color=RED, alpha=0.30)
a2.fill_between(xs, fpp, 0, where=fpp > 0, color=BLUE, alpha=0.30)
a2.plot(xs, fpp, color="#0f172a", lw=2.6)
x_axis(a2)
a2.set_title(r"$\Delta f = f''(x)$", fontsize=13, color="#0f172a", loc="left")
a2.axis("off")
plt.savefig(str(OUT_DIR / "lap_1d_stacked.png"), dpi=200, transparent=True,
            bbox_inches="tight", pad_inches=0.05)
plt.close()
print("[ok] lap_1d_stacked.png")
