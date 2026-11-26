"""Face tracking + lip-sync analysis.
Tracks the face box per frame (Haar cascade, smoothed), measures mouth-region motion and
cross-correlates it with the voice envelope to estimate A/V offset globally and per window."""
import cv2, json, sys, subprocess, numpy as np
src, out = sys.argv[1], sys.argv[2]
cap = cv2.VideoCapture(src)
casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
ts, boxes, mouth = [], [], []
prev = None; last = None
while True:
    ok, fr = cap.read()
    if not ok: break
    t = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    H, W = g.shape
    f = casc.detectMultiScale(g, 1.15, 5, minSize=(120, 120))
    if len(f):
        b = max(f, key=lambda r: r[2] * r[3])
        last = b if last is None else (0.6 * np.array(last) + 0.4 * np.array(b))
    box = last if last is not None else (W * .2, H * .2, W * .45, W * .45)
    x, y, w, h = [float(v) for v in box]
    ts.append(t); boxes.append([x / W, y / H, w / W, h / H])
    mx0, mx1 = int(x + w * .25), int(x + w * .75); my0, my1 = int(y + h * .68), int(y + h * 1.0)
    m = cv2.resize(g[max(0,my0):min(H,my1), max(0,mx0):min(W,mx1)], (64, 32)).astype(np.float32)
    mouth.append(0.0 if prev is None else float(np.mean(np.abs(m - prev))))
    prev = m
ts = np.array(ts); mouth = np.array(mouth)
raw = subprocess.run(['ffmpeg','-v','error','-i',src,'-ac','1','-ar','16000','-f','s16le','-'],capture_output=True).stdout
a = np.frombuffer(raw, np.int16) / 32768
def env(t0, t1):
    s, e = int(t0 * 16000), int(t1 * 16000); return np.sqrt(np.mean(a[s:e] ** 2)) if e > s else 0
# resample both on a uniform 100 Hz grid
grid = np.arange(0, ts[-1], 0.01)
mo = np.interp(grid, ts, mouth)
au = np.array([env(t - 0.02, t + 0.02) for t in grid])
def z(x): return (x - x.mean()) / (x.std() + 1e-9)
def bestlag(m, s, maxlag=30):
    best = (-9, 0)
    for L in range(-maxlag, maxlag + 1):   # L>0: video lags audio
        if L >= 0: c = np.mean(z(m[L:]) * z(s[:len(s) - L]))
        else: c = np.mean(z(m[:L]) * z(s[-L:]))
        best = max(best, (c, L))
    return best
c, L = bestlag(mo, au)
print(f"GLOBAL lag {L*10:+d} ms corr {c:.3f}")
wins = []
for w0 in np.arange(0, grid[-1] - 3, 1.5):
    i0, i1 = int(w0 * 100), int((w0 + 3) * 100)
    cw, Lw = bestlag(mo[i0:i1], au[i0:i1], 25)
    wins.append(dict(t=round(float(w0), 2), lag=int(Lw * 10), corr=round(float(cw), 3)))
    print(f"{w0:5.1f}s lag {Lw*10:+4d}ms corr {cw:.2f}")
json.dump(dict(globalLagMs=L * 10, t=[round(float(x), 3) for x in ts], box=[[round(v, 4) for v in b] for b in boxes], windows=wins),
          open(out, "w"))
