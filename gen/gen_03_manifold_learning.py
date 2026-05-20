"""Card 03 — Manifold Learning. Swiss roll + its Laplacian Eigenmaps embedding."""
from _common import OUT_DIR
from sklearn.datasets import make_swiss_roll
from sklearn.manifold import SpectralEmbedding
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

X, color = make_swiss_roll(n_samples=2500, noise=0.05, random_state=0)
emb = SpectralEmbedding(n_components=2, n_neighbors=12, random_state=0).fit_transform(X)

fig = plt.figure(figsize=(10, 5), facecolor="none")
ax1 = fig.add_subplot(1, 2, 1, projection="3d", facecolor="none")
ax1.scatter(X[:, 0], X[:, 1], X[:, 2], c=color, cmap="Spectral", s=8, depthshade=False)
ax1.set_axis_off()
ax1.view_init(elev=10, azim=-72)

ax2 = fig.add_subplot(1, 2, 2, facecolor="none")
ax2.scatter(emb[:, 0], emb[:, 1], c=color, cmap="Spectral", s=8)
ax2.set_axis_off()
ax2.set_aspect("equal")

plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0.02)
out = OUT_DIR / "app_03_manifold_learning.png"
plt.savefig(str(out), dpi=180, transparent=True, bbox_inches="tight", pad_inches=0.05)
plt.close()
print(f"[ok] {out.relative_to(out.parents[2])}")
