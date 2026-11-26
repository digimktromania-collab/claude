"""Build the edit decision list for the Claude Apps reel.

Inputs : transcript.raw.json (Whisper word timestamps), pause list (energy based)
Outputs: transcript.json            (corrected words, source + output timeline)
         reels/src/data/timeline.json (segments, captions, zooms, scenes, sfx)
         reels/src/Cuts.tsx          (hard-coded <Video> clips, one per jump-cut segment)
         timeline.md                 (human-readable list of moments)
"""
import json, subprocess, sys, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
PAD = 0.07          # keep this much air on each side of a cut
MIN_PAUSE = 0.30    # pauses longer than this are cut

raw = json.load(open(os.path.join(ROOT, "transcript.raw.json")))["words"]
W = [dict(text=w["text"], start=float(w["start"]), end=float(w["end"])) for w in raw]

# ---------- 1. text corrections (match the script the user gave) ----------
def split(i, a, b, frac=0.5):
    w = W[i]; m = w["start"] + (w["end"] - w["start"]) * frac
    W[i:i + 1] = [dict(text=a, start=w["start"], end=m), dict(text=b, start=m, end=w["end"])]

def merge(i, j, text):
    W[i:j + 1] = [dict(text=text, start=W[i]["start"], end=W[j]["end"])]

# apply from the end so indices stay valid
W[211]["text"] = "deșteaptă-te,"
merge(210, 211, "Deșteaptă-te,")
merge(175, 177, "într-adevăr,")
W[169]["text"] = "install"
W[127]["text"] = "Faci"
merge(124, 125, "team-ului")
merge(111, 112, "share-uiești,")
W[80]["text"] = "îmi"; W[81]["text"] = "aducă"
W[75]["text"] = "Creează"
W[73]["end"] = 25.1; W[74].update(start=25.1, end=25.62, text="2.")
W[55]["text"] = "Creează"
merge(27, 28, "a-ți")
split(10, "fiind", "că", 0.6)
for w in W:
    if w["text"] == "Crează": w["text"] = "Creează"
for i, w in enumerate(W):
    if w["text"] == "Creează" and w["start"] > 55.9: break

def find(seq, after=0.0):
    """index of first word sequence (case/punct-insensitive) starting at/after `after` seconds"""
    norm = lambda s: re.sub(r"[^\wăâîșțĂÂÎȘȚ-]", "", s.lower())
    toks = [norm(t) for t in seq.split()]
    for i in range(len(W) - len(toks) + 1):
        if W[i]["start"] + 1e-6 < after: continue
        if all(norm(W[i + k]["text"]) == toks[k] for k in range(len(toks))):
            return i
    raise ValueError(seq)

# ---------- 2. pauses -> keep segments ----------
energy = json.loads(subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/pauses.py"),
                                    os.path.join(ROOT, "reels/public/voice.mp4"), "8"],
                                   capture_output=True, text=True).stdout)
gaps = [[W[i]["end"], W[i + 1]["start"]] for i in range(len(W) - 1)
        if W[i + 1]["start"] - W[i]["end"] > MIN_PAUSE]
pauses = sorted(energy + gaps)
merged = []
for s, e in pauses:
    if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
    else: merged.append([s, e])
SRC_END = 72.6
cuts = [[0.0, max(0.0, W[0]["start"])]] if W[0]["start"] > 0.1 else []
cuts += [[s + PAD, e - PAD] for s, e in merged if e - s > MIN_PAUSE and (e - PAD) - (s + PAD) > 0.05]
cuts = [[0.0, e] if s < 0.15 else [s, e] for s, e in cuts]
segs, cur = [], 0.0
for s, e in cuts:
    if s > cur: segs.append([cur, s])
    cur = max(cur, e)
segs.append([cur, SRC_END])

# frame-quantised segments
out_f = 0; SEG = []
for s, e in segs:
    tb = round(s * FPS); dur = round(e * FPS) - tb
    if dur <= 0: continue
    SEG.append(dict(srcStart=tb / FPS, srcEnd=(tb + dur) / FPS, trimBefore=tb, from_=out_f, dur=dur))
    out_f += dur
TOTAL = out_f

def remap(t):
    for g in SEG:
        if g["srcStart"] - 1e-6 <= t <= g["srcEnd"] + 1e-6:
            return (g["from_"] + (t - g["srcStart"]) * FPS) / FPS
    # inside a cut: snap to next segment start
    for g in SEG:
        if t < g["srcStart"]: return g["from_"] / FPS
    return TOTAL / FPS

for w in W:
    w["oStart"] = round(remap(w["start"]), 3); w["oEnd"] = round(remap(w["end"]), 3)

# ---------- 3. keywords (italic serif) ----------
KEY = {"inteligență", "artificială.", "extraordinară", "gratuit.", "Apps.", "simple.", "prompt.",
       "desktop", "redimensiona", "Facebook,", "TikTok", "Instagram.", "aminte", "18", "notificare",
       "share-uiești,", "împărtășești", "team-ului", "promptul,", "comandă,", "artefact.", "Install",
       "App.", "simplu", "copil", "comentarii", "idei", "digital,", "geo,", "Deșteaptă-te,", "române!", "idei,", "1.", "2."}
for w in W: w["key"] = w["text"] in KEY

# ---------- 4. caption pages: 3-4 words, break on punctuation / pauses ----------
clauses, cur = [], []
for i, w in enumerate(W):
    cur.append(i)
    nxt = W[i + 1] if i + 1 < len(W) else None
    if w["text"][-1] in ".,!?" or not nxt or nxt["oStart"] - w["oEnd"] > 0.25:
        clauses.append(cur); cur = []
# glue tiny clauses (1 word) onto the following/previous clause when it stays <= 4 words
glued = []
for c in clauses:
    if glued and (len(c) == 1 or len(glued[-1]) == 1) and len(glued[-1]) + len(c) <= 4 \
            and W[glued[-1][-1]]["text"][-1] not in ".!?":
        glued[-1] += c
    else: glued.append(c)
def chunk(c):
    n = len(c)
    if n <= 4: return [c]
    k = -(-n // 4)                      # number of chunks of max 4
    sizes = [n // k + (1 if r < n % k else 0) for r in range(k)]
    out, p = [], 0
    for z in sizes: out.append(c[p:p + z]); p += z
    return out
fixed = [ch for c in glued for ch in chunk(c)]
captions = []
for k, p in enumerate(fixed):
    start = W[p[0]]["oStart"]
    end = W[fixed[k + 1][0]]["oStart"] if k + 1 < len(fixed) else W[p[-1]]["oEnd"] + 0.4
    end = min(end, W[p[-1]]["oEnd"] + 0.6)
    captions.append(dict(start=round(start, 3), end=round(end, 3),
                         words=[dict(text=W[i]["text"], start=W[i]["oStart"], end=W[i]["oEnd"], key=W[i]["key"]) for i in p]))

# ---------- 5. punch-in zooms on important phrases (alternate 106% / 110%) ----------
PHRASES = [("Vestea zilei", "artificială."), ("O veste", "gratuit."), ("Claude tocmai", "Apps."),
           ("două aplicații", "simple."), ("Creează o aplicație care să o", "Instagram."),
           ("Creează o aplicație care să îmi", "tu."), ("Această aplicație", "numai."),
           ("Întâi și", "comandă,"), ("faci click", "App."), ("Este foarte", "ani."),
           ("Vreau să", "tu."), ("Nu uita,", "române!")]
zooms = []
pos = 0.0
for n, (a, b) in enumerate(PHRASES):
    i = find(a, pos); j = find(b, W[i]["start"]); pos = W[j]["end"]
    zooms.append(dict(start=W[i]["oStart"], end=W[j]["oEnd"], scale=1.06 if n % 2 == 0 else 1.10,
                      label=" ".join(x["text"] for x in W[i:j + 1])))

# ---------- 6. scenes (graphics) anchored to words ----------
def t(seq, after=0.0, end=False):
    i = find(seq, after); j = i + len(seq.split()) - 1
    return W[j]["oEnd"] if end else W[i]["oStart"]

def ts(seq, after=0.0):  # source time, for anchoring searches
    return W[find(seq, after)]["start"]

S = {}
S["hook"] = dict(start=0.0, end=t("artificială.", end=True) + 0.15)
S["plans"] = dict(start=t("și cu planul"), end=t("gratuit.", end=True) + 0.25, free=t("gratuit."))
S["window"] = dict(start=t("Claude tocmai"), end=t("Înainte") - 0.05, icon=t("Claude Apps."))
a1 = ts("Creează o aplicație care să o")
S["card1"] = dict(start=t("Creează o aplicație care să o"), end=t("Instagram.", a1, True) + 0.2,
                  icon="🖼️", label="Ideea #1",
                  prompt="Creează o aplicație pe desktop care redimensionează pozele pentru Facebook, TikTok și Instagram.")
S["platforms"] = dict(start=t("pe desktop", a1), end=t("Instagram.", a1, True) + 0.2)
a2 = ts("Creează o aplicație care să îmi")
S["card2"] = dict(start=t("Creează o aplicație care să îmi"), end=t("tu.", a2, True) + 0.2, icon="⏰", label="Ideea #2",
                  prompt="Creează o aplicație care să-mi amintească în fiecare zi să postez pe TikTok la ora 18:00.")
S["card2"]["end"] = min(S["card2"]["end"], t("Această aplicație") - 0.05)
S["features"] = dict(start=t("Această aplicație"), end=t("numai.", end=True) + 0.1,
                     bell=t("notificare"), menu=t("și nu numai."), keys=t("numai."))
S["warning"] = dict(start=t("Bineînțeles"), end=t("tău.", end=True) + 0.1, green=t("împărtășești"))
S["riser"] = dict(start=S["warning"]["start"] - 1.2)
a3 = ts("Întâi și întâi")
S["card3"] = dict(start=t("Întâi și întâi") - 0.6, end=t("artefact.", end=True) + 0.15, icon="✍️", label="Ideea #3 · a ta",
                  prompt="Creează o aplicație care… (ideea ta aici)",
                  steps=[t("creezi promptul,"), t("îi trimiți"), t("lucrează")])
a4 = ts("Când a terminat, faci")
S["install"] = dict(start=t("Când a terminat, faci"), end=t("app.", ts("install app."), True) + 0.15,
                    click=t("faci click"), dots=t("cele trei butoane"), underline=t("Install App."))
S["card3"]["end"] = min(S["card3"]["end"], S["install"]["start"] - 0.05)
S["cta"] = dict(start=t("Vreau să te"), end=t("Nu uita,") - 0.05, comments=t("comentarii"))
# extra beats to fill the talking-head gaps
S["ideas"] = dict(start=t("îți dau câteva idei,"), end=t("simple.", end=True) + 0.3, two=t("două aplicații"))
S["oneprompt"] = dict(start=t("un simplu prompt."), end=t("Creează o aplicație care să o") - 0.08)
S["appflow"] = dict(start=t("Creează app,"), end=t("Este foarte,") - 0.05, install=t("install app.", ts("Creează app,")))
S["kid"] = dict(start=t("Este foarte,"), simplu=t("foarte simplu"), kid=t("copil"), end=t("Vreau să te") - 0.05, five=t("5 ani."))
S["outro"] = dict(start=t("Nu uita,"), end=TOTAL / FPS, digital=t("digital,"), geo=t("geo,"),
                  wake=t("Deșteaptă-te,"), ro=t("române!"))

# ---------- 7. SFX events ----------
sfx = [dict(t=0.0, type="whoosh")]
sfx += [dict(t=S["plans"]["start"], type="whoosh"), dict(t=S["plans"]["free"], type="pop")]
sfx += [dict(t=S["window"]["start"], type="whoosh"), dict(t=S["window"]["icon"], type="pop")]
sfx += [dict(t=S["card1"]["start"], type="whoosh"), dict(t=S["platforms"]["start"], type="pop")]
sfx += [dict(t=S["card2"]["start"], type="whoosh")]
sfx += [dict(t=S["features"]["start"], type="whoosh"), dict(t=S["features"]["bell"], type="ding"),
        dict(t=S["features"]["menu"], type="pop"), dict(t=S["features"]["keys"], type="pop")]
sfx += [dict(t=S["riser"]["start"], type="riser"), dict(t=S["warning"]["start"], type="whoosh"),
        dict(t=S["warning"]["green"], type="whoosh")]
sfx += [dict(t=S["card3"]["start"], type="whoosh")] + [dict(t=x, type="click") for x in S["card3"]["steps"]]
sfx += [dict(t=S["install"]["start"], type="whoosh"), dict(t=S["install"]["click"], type="click"),
        dict(t=S["install"]["dots"], type="pop"), dict(t=S["install"]["underline"], type="pop")]
sfx += [dict(t=S["cta"]["start"], type="whoosh"), dict(t=S["cta"]["comments"], type="pop")]
sfx += [dict(t=S["ideas"]["two"], type="pop"), dict(t=S["oneprompt"]["start"], type="click"),
        dict(t=S["appflow"]["start"], type="pop"), dict(t=S["appflow"]["install"], type="pop"),
        dict(t=S["kid"]["start"], type="whoosh"), dict(t=S["kid"]["kid"], type="pop"), dict(t=S["kid"]["five"], type="pop"),
        dict(t=S["outro"]["start"], type="whoosh"), dict(t=S["outro"]["digital"], type="pop"),
        dict(t=S["outro"]["geo"], type="pop"), dict(t=S["outro"]["wake"] - 0.05, type="whoosh"),
        dict(t=S["outro"]["ro"], type="ding")]
sfx = sorted([dict(t=round(max(0, e["t"]), 3), type=e["type"]) for e in sfx], key=lambda e: e["t"])

# speech activity (for music ducking)
speech = []
for w in W:
    if speech and w["oStart"] - speech[-1][1] < 0.35: speech[-1][1] = w["oEnd"]
    else: speech.append([w["oStart"], w["oEnd"]])

# ---------- face track + "fog" over the face where lip-sync measured off ----------
FACE = json.load(open(os.path.join(ROOT, "analysis/face.json")))
import numpy as _np
ft = _np.array(FACE["t"]); fb = _np.array(FACE["box"])
def src_of(k):
    for g in SEG:
        if g["from_"] <= k < g["from_"] + g["dur"]:
            return g["srcStart"] + (k - g["from_"]) / FPS
    return SEG[-1]["srcEnd"]
face_box = []
for k in range(TOTAL):
    tt = src_of(k)
    x, y, w, h = [float(_np.interp(tt, ft, fb[:, c])) for c in range(4)]
    face_box.append([round((x + w / 2) * 1080), round((y + h / 2) * 1920), round(w * 1080), round(h * 1920)])
bad = sorted([[w["t"] + 0.4, w["t"] + 2.6] for w in FACE["windows"] if w["corr"] >= 0.25 and abs(w["lag"]) >= 120])
mb = []
for a, b in bad:
    if mb and a <= mb[-1][1]: mb[-1][1] = max(mb[-1][1], b)
    else: mb.append([a, b])
fog = []
for a, b in mb:
    for g in SEG:
        s0, s1 = max(a, g["srcStart"]), min(b, g["srcEnd"])
        if s1 > s0:
            o0 = g["from_"] / FPS + (s0 - g["srcStart"]); o1 = g["from_"] / FPS + (s1 - g["srcStart"])
            if fog and o0 - fog[-1][1] < 0.35: fog[-1][1] = o1
            else: fog.append([o0, o1])
fog = [[round(a, 2), round(b, 2)] for a, b in fog if b - a >= 0.5]

# ---------- write ----------
json.dump(dict(language="ro", model="whisper large-v3 (faster-whisper, int8)",
               words=[dict(text=w["text"], start=round(w["start"], 3), end=round(w["end"], 3),
                           outStart=w["oStart"], outEnd=w["oEnd"], keyword=w["key"]) for w in W]),
          open(os.path.join(ROOT, "transcript.json"), "w"), ensure_ascii=False, indent=1)
os.makedirs(os.path.join(ROOT, "reels/src/data"), exist_ok=True)
json.dump(dict(fps=FPS, durationInFrames=TOTAL, captions=captions, zooms=zooms, scenes=S, sfx=sfx, speech=speech, fog=fog, faceBox=face_box),
          open(os.path.join(ROOT, "reels/src/data/timeline.json"), "w"), ensure_ascii=False, indent=1)

clips = "\n".join(
    f'      <Video name="Clip {k + 1} ({g["srcStart"]:.2f}s–{g["srcEnd"]:.2f}s)" src={{SRC}} trimBefore={{{g["trimBefore"]}}} from={{{g["from_"]}}} durationInFrames={{{g["dur"]}}} style={{STYLE}} muted={{muted}} />'
    for k, g in enumerate(SEG))
open(os.path.join(ROOT, "reels/src/Cuts.tsx"), "w").write(f'''// Generated by scripts/build_timeline.py — jump cuts (pauses > {MIN_PAUSE}s removed).
// Each clip is a hard-coded node so it can be nudged in Remotion Studio.
import {{ Video }} from "@remotion/media";
import {{ AbsoluteFill, staticFile }} from "remotion";

const SRC = staticFile("voice.mp4");
const STYLE: React.CSSProperties = {{ width: "100%", height: "100%", objectFit: "cover" }};

export const Cuts: React.FC<{{ muted?: boolean }}> = ({{ muted = false }}) => {{
  return (
    <AbsoluteFill>
{clips}
    </AbsoluteFill>
  );
}};
''')

# ---------- human readable timeline ----------
def fmt(x): return f"{int(x // 60)}:{x % 60:05.2f}"
removed = sum(e - s for s, e in cuts)
lines = [f"# Timeline — Claude Apps reel", "",
         f"- Durată sursă: 72.6s → durată finală: **{TOTAL / FPS:.2f}s** ({TOTAL} cadre @ {FPS} fps)",
         f"- Jump cuts: **{len(SEG) - 1}** tăieturi, {removed:.2f}s de pauze eliminate", ""]
                                                                         cuts=len(SEG) - 1, removed=removed), ensure_ascii=False))
print('fog', fog)
print(f"segments={len(SEG)} total={TOTAL / FPS:.2f}s removed={removed:.2f}s captions={len(captions)}")
for k, v in S.items(): print(f"{k:10s} {fmt(v['start'])}" + (f" → {fmt(v['end'])}" if 'end' in v else ""))
