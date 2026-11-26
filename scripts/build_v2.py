"""v2 edit: re-ordered story, split-screen layout (graphics never on the face).

Story:
  HOOK (full)     Claude a lansat Claude Apps + merge pe planul gratuit
  ① IDEI (split)  2 idei -> #1 resize poze -> #2 reminder TikTok -> notificare -> share
  ② CUM (split)   prompt -> artefact -> ⋯ -> Install App -> recap
  ③ FINAL (full)  simplu -> comentarii -> Deșteaptă-te, române!
"""
import json, os, subprocess, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
PAD = 0.07
MIN_PAUSE = 0.30

W = json.load(open(os.path.join(ROOT, "transcript.json")))["words"]
for w in W:
    w["s"], w["e"] = w["start"], w["end"]

# word-index ranges (inclusive) of the source, in the NEW order
BLOCKS = [
    ("hook_launch", "full", 19, 25),
    ("hook_free", "full", 6, 18),
    ("ideas", "split", 35, 42),
    ("app1_label", "split", 43, 44),
    ("app1", "split", 55, 72),
    ("app2", "split", 73, 96),
    ("notif", "split", 97, 105),
    ("share", "split", 106, 124),
    ("how_prompt", "split", 128, 138),
    ("how_artifact", "split", 147, 150),
    ("how_install", "split", 151, 164),
    ("recap", "split", 165, 168),
    ("simple", "full", 169, 180),
    ("cta", "full", 181, 199),
    ("outro", "full", 200, 207),
]
CAPITALIZE = {35: "Îți", 147: "El"}

energy = json.loads(subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/pauses.py"),
                                    os.path.join(ROOT, "reels/public/voice.mp4"), "8"],
                                   capture_output=True, text=True).stdout)

SEG, out_f, blocks = [], 0, []
word_out = {}
for name, mode, i, j in BLOCKS:
    prev_end = W[i - 1]["e"] if i > 0 else 0.0
    next_start = W[j + 1]["s"] if j + 1 < len(W) else W[j]["e"] + 0.4
    a = W[i]["s"] - min(0.06, max(0.0, W[i]["s"] - prev_end) * 0.5)
    b = W[j]["e"] + min(0.14, max(0.0, next_start - W[j]["e"]) * 0.6)
    # pauses inside the block: energy based + whisper gaps
    gaps = [[W[k]["e"], W[k + 1]["s"]] for k in range(i, j) if W[k + 1]["s"] - W[k]["e"] > MIN_PAUSE]
    ps = sorted([p for p in energy if p[0] > a and p[1] < b] + gaps)
    merged = []
    for s, e in ps:
        if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
        else: merged.append([s, e])
    keep, cur = [], a
    for s, e in merged:
        s2, e2 = s + PAD, e - PAD
        if e2 - s2 > 0.05 and s2 > cur:
            keep.append([cur, s2]); cur = e2
    keep.append([cur, b])
    b_start = out_f
    for s, e in keep:
        tb = round(s * FPS); dur = round(e * FPS) - tb
        if dur <= 0: continue
        SEG.append(dict(srcStart=tb / FPS, srcEnd=(tb + dur) / FPS, trimBefore=tb, from_=out_f, dur=dur, block=name))
        out_f += dur
    blocks.append(dict(name=name, mode=mode, start=b_start / FPS, end=out_f / FPS, i=i, j=j))
TOTAL = out_f

def remap(t, block):
    segs = [g for g in SEG if g["block"] == block]
    for g in segs:
        if g["srcStart"] - 1e-6 <= t <= g["srcEnd"] + 1e-6:
            return (g["from_"] + (t - g["srcStart"]) * FPS) / FPS
    for g in segs:
        if t < g["srcStart"]: return g["from_"] / FPS
    return (segs[-1]["from_"] + segs[-1]["dur"]) / FPS

words = []
for bl in blocks:
    for k in range(bl["i"], bl["j"] + 1):
        w = W[k]
        txt = CAPITALIZE.get(k, w["text"])
        o = dict(k=k, text=txt, start=round(remap(w["s"], bl["name"]), 3), end=round(remap(w["e"], bl["name"]), 3),
                 key=w["keyword"], block=bl["name"], mode=bl["mode"])
        words.append(o); word_out[k] = o

KEYS = {"Apps.", "gratuit.", "extraordinară", "simple.", "desktop", "redimensiona", "aminte", "18", "notificare",
        "share-uiești,", "team-ului", "promptul,", "artefact.", "Install", "App.", "simplu", "comentarii",
        "digital,", "geo,", "Deșteaptă-te,", "române!", "idei,"}
for w in words: w["key"] = w["text"] in KEYS

# captions: per block, clause aware, 3-4 words
def chunk(c):
    n = len(c)
    if n <= 4: return [c]
    k = -(-n // 4); sizes = [n // k + (1 if r < n % k else 0) for r in range(k)]
    out, p = [], 0
    for z in sizes: out.append(c[p:p + z]); p += z
    return out
captions = []
for bl in blocks:
    ws = [w for w in words if w["block"] == bl["name"]]
    clauses, cur = [], []
    for idx, w in enumerate(ws):
        cur.append(w)
        if w["text"][-1] in ".,!?" or idx == len(ws) - 1:
            clauses.append(cur); cur = []
    glued = []
    for c in clauses:
        if glued and (len(c) == 1 or len(glued[-1]) == 1) and len(glued[-1]) + len(c) <= 4 \
                and glued[-1][-1]["text"][-1] not in ".!?":
            glued[-1] += c
        else: glued.append(c)
    pages = [ch for c in glued for ch in chunk(c)]
    for n, p in enumerate(pages):
        end = pages[n + 1][0]["start"] if n + 1 < len(pages) else bl["end"]
        captions.append(dict(start=p[0]["start"], end=round(end, 3), mode=bl["mode"],
                             words=[dict(text=w["text"], start=w["start"], end=w["end"], key=w["key"]) for w in p]))

def ot(k): return word_out[k]["start"]
def oe(k): return word_out[k]["end"]
B = {b["name"]: b for b in blocks}

# scene anchors (output seconds)
S = dict(
    hook=dict(start=0.0, end=B["hook_free"]["end"], free=ot(17)),
    ideas=dict(start=B["ideas"]["start"], end=B["ideas"]["end"], two=ot(39)),
    app1=dict(start=B["app1_label"]["start"], end=B["app1"]["end"], prompt=ot(55), desktop=ot(63),
              fb=ot(69), tt=ot(70), ig=ot(72)),
    app2=dict(start=B["app2"]["start"], end=B["app2"]["end"], prompt=ot(75), clock=ot(91)),
    notif=dict(start=B["notif"]["start"], end=B["notif"]["end"], banner=ot(102)),
    share=dict(start=B["share"]["start"], end=B["share"]["end"], btn=ot(111), people=ot(116), team=ot(123)),
    how=dict(start=B["how_prompt"]["start"], end=B["recap"]["start"], s1=ot(128), send=ot(134),
             s2=B["how_artifact"]["start"], s3=B["how_install"]["start"], dots=ot(155), install=ot(163)),
    recap=dict(start=B["recap"]["start"], end=B["recap"]["end"], second=ot(167)),
    simple=dict(start=B["simple"]["start"], end=B["simple"]["end"], kid=ot(177)),
    cta=dict(start=B["cta"]["start"], end=B["cta"]["end"], comments=ot(186)),
    outro=dict(start=B["outro"]["start"], end=TOTAL / FPS, digital=ot(203), geo=ot(205), wake=ot(206), ro=ot(207)),
)

# layout modes (merge consecutive blocks with same mode)
modes = []
for b in blocks:
    if modes and modes[-1]["mode"] == b["mode"]: modes[-1]["end"] = b["end"]
    else: modes.append(dict(mode=b["mode"], start=b["start"], end=b["end"]))

# punch-in zooms: full-mode sentences, alternating
zooms = []
for n, nm in enumerate(["hook_launch", "hook_free", "simple", "cta", "outro"]):
    zooms.append(dict(start=B[nm]["start"], end=B[nm]["end"], scale=1.06 if n % 2 == 0 else 1.10))

# SFX
sfx = [dict(t=0.0, type="whoosh"), dict(t=S["hook"]["free"], type="pop")]
for m in modes[1:]: sfx.append(dict(t=m["start"], type="whoosh"))
sfx += [dict(t=S["ideas"]["two"], type="pop"),
        dict(t=S["app1"]["start"], type="whoosh"), dict(t=S["app1"]["fb"], type="pop"), dict(t=S["app1"]["tt"], type="pop"),
        dict(t=S["app1"]["ig"], type="pop"), dict(t=S["app2"]["start"], type="whoosh"), dict(t=S["app2"]["clock"], type="pop"),
        dict(t=S["notif"]["banner"], type="ding"), dict(t=S["share"]["start"], type="whoosh"), dict(t=S["share"]["people"], type="pop"),
        dict(t=S["how"]["send"], type="click"), dict(t=S["how"]["s2"], type="whoosh"), dict(t=S["how"]["s3"], type="whoosh"),
        dict(t=S["how"]["dots"], type="click"), dict(t=S["how"]["install"], type="click"), dict(t=S["how"]["install"] + 0.1, type="pop"),
        dict(t=S["recap"]["second"], type="pop"), dict(t=S["simple"]["kid"], type="pop"),
        dict(t=S["cta"]["comments"], type="pop"), dict(t=S["outro"]["wake"], type="whoosh"), dict(t=S["outro"]["ro"], type="ding")]
sfx = sorted([dict(t=round(e["t"], 3), type=e["type"]) for e in sfx], key=lambda e: e["t"])
# drop near-duplicates (same type within 0.25s)
dd = []
for e in sfx:
    if dd and dd[-1]["type"] == e["type"] and e["t"] - dd[-1]["t"] < 0.25: continue
    dd.append(e)
sfx = dd

speech = []
for w in words:
    if speech and w["start"] - speech[-1][1] < 0.35: speech[-1][1] = w["end"]
    else: speech.append([w["start"], w["end"]])

# face track, heavily smoothed (~0.8s) so the split-screen framing doesn't wobble
FACE = json.load(open(os.path.join(ROOT, "analysis/face.json")))
ft = np.array(FACE["t"]); fb = np.array(FACE["box"])
k = 25; kern = np.ones(k) / k
fbs = np.stack([np.convolve(np.pad(fb[:, c], (k // 2, k // 2), mode="edge"), kern, "valid") for c in range(4)], 1)
def src_of(fr):
    for g in SEG:
        if g["from_"] <= fr < g["from_"] + g["dur"]:
            return g["srcStart"] + (fr - g["from_"]) / FPS
    return SEG[-1]["srcEnd"]
face_box = []
for fr in range(TOTAL):
    tt = src_of(fr)
    x, y, w_, h = [float(np.interp(tt, ft, fbs[:, c])) for c in range(4)]
    face_box.append([round((x + w_ / 2) * 1080), round((y + h / 2) * 1920), round(w_ * 1080), round(h * 1920)])

os.makedirs(os.path.join(ROOT, "reels/src/data"), exist_ok=True)
json.dump(dict(fps=FPS, durationInFrames=TOTAL, blocks=[{k2: v for k2, v in b.items() if k2 not in ("i", "j")} for b in blocks],
               modes=modes, captions=captions, zooms=zooms, scenes=S, sfx=sfx, speech=speech, faceBox=face_box),
          open(os.path.join(ROOT, "reels/src/data/timeline.json"), "w"), ensure_ascii=False)

clips = "\n".join(
    f'      <Video name="{g["block"]} ({g["srcStart"]:.2f}s–{g["srcEnd"]:.2f}s)" src={{SRC}} trimBefore={{{g["trimBefore"]}}} from={{{g["from_"]}}} durationInFrames={{{g["dur"]}}} style={{STYLE}} />'
    for g in SEG)
open(os.path.join(ROOT, "reels/src/Cuts.tsx"), "w").write(f'''// Generated by scripts/build_v2.py — re-ordered story + jump cuts (pauses > {MIN_PAUSE}s removed).
// Each clip is a hard-coded node so it can be nudged in Remotion Studio.
import {{ Video }} from "@remotion/media";
import {{ AbsoluteFill, staticFile }} from "remotion";

const SRC = staticFile("voice.mp4");
const STYLE: React.CSSProperties = {{ width: "100%", height: "100%", objectFit: "cover" }};

export const Cuts: React.FC = () => {{
  return (
    <AbsoluteFill>
{clips}
    </AbsoluteFill>
  );
}};
''')
fmt = lambda x: f"{int(x // 60)}:{x % 60:05.2f}"
print(f"clips={len(SEG)} total={TOTAL / FPS:.2f}s")
for b in blocks: print(f"{fmt(b['start'])}-{fmt(b['end'])} {b['mode']:5s} {b['name']}")
