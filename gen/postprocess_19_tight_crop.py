"""
Post-process: re-crop the existing optimal-basis stage PNGs and the
camera-oscillation APNG to a TIGHT shared alpha bbox (zero padding).

We compute the union alpha bbox across all 9 stage PNGs *and* every
APNG frame so all images stay perfectly co-registered (overlaying them
in the slide produces no jitter).

Run with the gen venv's python:
    gen/.venv/Scripts/python.exe gen/postprocess_19_tight_crop.py
"""
from pathlib import Path
from PIL import Image, ImageSequence

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "public" / "applications"

step_files = [OUT_DIR / f"optimal_basis_step{n}.png" for n in range(1, 10)]
anim_file  = OUT_DIR / "optimal_basis_step9_anim.png"


def merge(union, b):
    if b is None:
        return union
    if union is None:
        return list(b)
    return [
        min(union[0], b[0]),
        min(union[1], b[1]),
        max(union[2], b[2]),
        max(union[3], b[3]),
    ]


union = None

# Stage PNGs (stills)
for f in step_files:
    im = Image.open(f).convert("RGBA")
    union = merge(union, im.getchannel("A").getbbox())

# APNG frames
im_anim_src = Image.open(anim_file)
for frame in ImageSequence.Iterator(im_anim_src):
    union = merge(union, frame.convert("RGBA").getchannel("A").getbbox())

if union is None:
    raise SystemExit("[err] no non-empty alpha found in any image")

print(f"[ok] union alpha bbox = {tuple(union)}  size = "
      f"{union[2]-union[0]} x {union[3]-union[1]}")

# Crop stills
for f in step_files:
    im = Image.open(f).convert("RGBA")
    im.crop(union).save(f)
    print(f"[ok] cropped {f.name} -> {im.crop(union).size}")

# Crop APNG: load every frame, crop, re-save preserving per-frame duration
src = Image.open(anim_file)
frames = []
durations = []
for frame in ImageSequence.Iterator(src):
    rgba = frame.convert("RGBA").crop(union)
    frames.append(rgba)
    durations.append(frame.info.get("duration", 60))

frames[0].save(
    anim_file,
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    disposal=2,
    optimize=False,
)
print(f"[ok] cropped APNG {anim_file.name} -> {frames[0].size}  "
      f"frames={len(frames)}")
