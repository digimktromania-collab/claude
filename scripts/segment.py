"""Person cut-out for the Academia reel.

Reads reels/public/academia/source.mp4, runs human segmentation (rembg u2net_human_seg)
from START_FRAME on, and writes:
  - reels/public/academia/person.webm  (VP9 with alpha: the person, transparent background)
  - analysis/academia_head.json        (per-frame head top / centre, source pixels)
Frames before START_FRAME are written fully transparent (they are never shown).
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageFilter
from rembg import new_session
from rembg.bg import remove

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "reels/public/academia/source.mp4")
OUT = os.path.join(ROOT, "reels/public/academia/person.webm")
START_FRAME = int(sys.argv[1]) if len(sys.argv) > 1 else 300
W, H = 1080, 1920

dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", SRC, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                        "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-b:v", "8M", "-deadline", "realtime", "-cpu-used", "8",
                        "-row-mt", "1", "-auto-alt-ref", "0", OUT], stdin=subprocess.PIPE)
sess = new_session("u2net_human_seg")
heads = []
prev = None
i = 0
empty = np.zeros((H, W, 4), np.uint8).tobytes()
while True:
    buf = dec.stdout.read(W * H * 3)
    if len(buf) < W * H * 3: break
    if i < START_FRAME:
        enc.stdin.write(empty); heads.append(None); i += 1; continue
    rgb = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    im = Image.fromarray(rgb)
    m = remove(im, session=sess, only_mask=True, post_process_mask=True)
    m = np.asarray(m.filter(ImageFilter.GaussianBlur(1.5))).astype(np.float32)
    if prev is not None: m = 0.65 * m + 0.35 * prev       # light temporal smoothing against flicker
    prev = m
    a = np.clip(m, 0, 255).astype(np.uint8)
    rgba = np.dstack([rgb, a])
    enc.stdin.write(rgba.tobytes())
    # head top: first row (from top) with a solid run of person pixels
    rows = (a > 128).sum(1)
    top = int(np.argmax(rows > 40)) if (rows > 40).any() else 0
    band = a[top:top + 160] > 128
    xs = np.nonzero(band.any(0))[0]
    cx = int(xs.mean()) if len(xs) else W // 2
    hw = int(xs.max() - xs.min()) if len(xs) else 400
    heads.append([top, cx, hw])
    if i % 50 == 0: print("frame", i, heads[-1], flush=True)
    i += 1
enc.stdin.close(); enc.wait(); dec.wait()
os.makedirs(os.path.join(ROOT, "analysis"), exist_ok=True)
json.dump(dict(start=START_FRAME, heads=heads), open(os.path.join(ROOT, "analysis/academia_head.json"), "w"))
print("done", i, "frames")
