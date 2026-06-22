"""What a correspondence buys you — transfer signals across the map.

Texture and segmentation are transferred between two horse poses (shared
topology → exact transfer); the running animations are the classic
deformation-transfer pair (horse gallop → camel gallop).

Outputs (public/applications/):
  corr_tex_a.png  / corr_tex_b.png    a checker texture, pose A -> pose B
  corr_seg_a.png  / corr_seg_b.png    a part segmentation, pose A -> pose B
  corr_anim_horse.gif / corr_anim_camel.gif   looping gallop animations
"""
from _common import OUT_DIR, DEFTRANSFER, load_mesh
import numpy as np
import gen_24_shape_descriptors as d

POSE_A = d.POSE_A          # horse-gallop-03
POSE_B = d.POSE_B          # horse-gallop-20


def _to_rgb(hex_list):
    return np.array([[int(h[i:i+2], 16) / 255 for i in (1, 3, 5)] for h in hex_list])


# ===========================================================================
def build_texture():
    Va, Fa = load_mesh(POSE_A)
    Vb, Fb = load_mesh(POSE_B)
    # 3-D checker computed on pose A, carried to pose B by shared vertex indexing
    F = 16.0
    cells = (np.floor(Va[:, 0] * F) + np.floor(Va[:, 1] * F) + np.floor(Va[:, 2] * F))
    checker = (cells % 2).astype(bool)
    c1, c2 = _to_rgb(["#2B5876", "#f1e4c3"])     # teal / cream
    col = np.where(checker[:, None], c1, c2)
    d.render_field(Va, Fa, col, None, None, str(OUT_DIR / "corr_tex_a.png"), rgb=True)
    d.render_field(Vb, Fb, col, None, None, str(OUT_DIR / "corr_tex_b.png"), rgb=True)
    print("[ok] corr_tex_a/b.png")


# ===========================================================================
def build_segmentation():
    Va, Fa = load_mesh(POSE_A)
    Vb, Fb = load_mesh(POSE_B)
    z, y = Va[:, 2], Va[:, 1]

    # confined local parts on a neutral base; gaps left between them so the
    # segments don't touch (0 = unlabeled / grey)
    seg = np.zeros(len(Va), dtype=int)
    seg[z > 0.21] = 1                                       # head (muzzle / face)
    seg[(np.abs(z) < 0.11) & (y > 0.05)] = 2               # torso / back
    seg[(y < -0.07) & (z > 0.05)] = 3                      # front legs (lower)
    seg[(y < -0.07) & (z < -0.12)] = 4                     # hind legs (lower)
    seg[(z < -0.46) & (y > -0.02)] = 5                     # tail

    base = _to_rgb(["#cbd0d6"])[0]
    colors = _to_rgb(["#ef4444", "#3b82f6", "#22c55e", "#f59e0b", "#a855f7"])
    col = np.tile(base, (len(Va), 1))
    m = seg > 0
    col[m] = colors[seg[m] - 1]
    d.render_field(Va, Fa, col, None, None, str(OUT_DIR / "corr_seg_a.png"), rgb=True)
    d.render_field(Vb, Fb, col, None, None, str(OUT_DIR / "corr_seg_b.png"), rgb=True)
    print("[ok] corr_seg_a/b.png  (segments:", np.bincount(seg), ")")


# ===========================================================================
def _load_centered_uniform(path, scale):
    """Load raw, center at centroid, scale by a fixed factor (no per-frame resize)."""
    import trimesh
    m = trimesh.load(str(path), process=False, force="mesh")
    V = np.asarray(m.vertices, np.float64)
    F = np.asarray(m.faces, np.int32)
    V = (V - V.mean(0)) * scale
    return V, F


def build_anim(folder, prefix, n_frames, step, out_name):
    import pyvista as pv
    from PIL import Image
    import glob, os

    files = sorted(glob.glob(str(DEFTRANSFER / folder / f"{prefix}*.obj")))[::step][:n_frames]
    # fixed scale from the first frame's diagonal so the shape doesn't pulse
    m0V = np.asarray(__import__("trimesh").load(files[0], process=False, force="mesh").vertices)
    scale = 1.0 / np.linalg.norm(m0V.max(0) - m0V.min(0))

    # one global camera that fits all frames (union of bounds), with margin
    frames = [_load_centered_uniform(f, scale) for f in files]
    allV = np.vstack([V for V, _ in frames])
    cam = [(1.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0)]

    raw = []
    for V, F in frames:
        faces = np.hstack([np.full((len(F), 1), 3, np.int64), F.astype(np.int64)]).ravel()
        p = pv.Plotter(off_screen=True, window_size=(960, 620))
        p.set_background("white")
        p.add_mesh(pv.PolyData(V, faces), color="#c9ccd1", smooth_shading=True,
                   ambient=0.35, diffuse=0.72, specular=0.15)
        # bound the view to the union box so the gallop stays centered & in-frame
        p.add_mesh(pv.PolyData(allV[::37]), opacity=0.0)   # invisible extent anchor
        p.camera_position = cam
        p.reset_camera()
        p.camera.zoom(1.15)
        p.enable_anti_aliasing("msaa")
        raw.append(p.screenshot(transparent_background=False, return_img=True))
        p.close()

    # crop every frame to a single (union) content box so the horse fills the frame
    def content_box(a):
        mask = (a[:, :, :3] < 245).any(2)
        ys, xs = np.where(mask)
        return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

    boxes = [content_box(a) for a in raw]
    pad = 8
    x0 = max(min(b[0] for b in boxes) - pad, 0)
    y0 = max(min(b[1] for b in boxes) - pad, 0)
    x1 = min(max(b[2] for b in boxes) + pad, raw[0].shape[1])
    y1 = min(max(b[3] for b in boxes) + pad, raw[0].shape[0])
    imgs = [Image.fromarray(a[y0:y1, x0:x1]).convert(
        "P", palette=Image.ADAPTIVE, colors=128) for a in raw]

    out = OUT_DIR / out_name
    imgs[0].save(str(out), save_all=True, append_images=imgs[1:], loop=0,
                 duration=70, disposal=2, optimize=True)
    print(f"[ok] {out_name}  ({len(imgs)} frames, crop {x1-x0}x{y1-y0})")


if __name__ == "__main__":
    build_texture()
    build_segmentation()
    build_anim("horse-gallop", "horse-gallop", 25, 2, "corr_anim_horse.gif")
    build_anim("camel-gallop", "camel-gallop", 24, 2, "corr_anim_camel.gif")
