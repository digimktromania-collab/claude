"""Edit decision list for the 'o simplă poză în Claude' reel (Academia Digitală).

Story (her order is already good):
  hook (window)  -> prompt 1 roz pudrat -> ȘI GATA (pink background)
                 -> prompt 2 copaci     -> ȘI GATA (trees grow from her head, she zooms out a bit)
                 -> prompt 3 cascadă    -> ȘI GATA (her posts pour down behind her)
                 -> "exemplu simplu"    -> CTA Academia Digitală «Deșteaptă-te, Române!»
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
PAD = 0.07
MIN_PAUSE = 0.30
BEAT_AFTER_GATA = 0.35   # let each reveal breathe

W = json.load(open(os.path.join(ROOT, "academia.transcript.raw.json")))["words"]
W = [dict(text=w["text"], s=float(w["start"]), e=float(w["end"])) for w in W]
def merge(i, j, text): W[i:j + 1] = [dict(text=text, s=W[i]["s"], e=W[j]["e"])]
merge(98, 101, "Deșteaptă-te,"); W[98 if W[98]["text"] == "Deșteaptă-te," else 99]
W[-1]["text"] = "Române!"
merge(27, 28, "într-o")
W[25]["text"] = "schimbă-mi"
for w in W:
    if w["text"] in ("Claude,", "Claude"): pass

def find(seq, after=0):
    import re
    norm = lambda s: re.sub(r"[^\wăâîșțĂÂÎȘȚ-]", "", s.lower())
    toks = [norm(x) for x in seq.split()]
    for i in range(after, len(W) - len(toks) + 1):
        if all(norm(W[i + k]["text"]) == toks[k] for k in range(len(toks))): return i
    raise ValueError(seq)

# ---------- cuts ----------
energy = json.loads(subprocess.run([sys.executable, "-I", os.path.join(ROOT, "scripts/pauses.py"),
                                    os.path.join(ROOT, "reels/public/academia/source.mp4"), "8"], capture_output=True, text=True).stdout)
gaps = [[W[k]["e"], W[k + 1]["s"]] for k in range(len(W) - 1) if W[k + 1]["s"] - W[k]["e"] > MIN_PAUSE]
ps = sorted(energy + gaps)
merged = []
for s, e in ps:
    if merged and s <= merged[-1][1]: merged[-1][1] = max(merged[-1][1], e)
    else: merged.append([s, e])
gata_ends = [w["e"] for w in W if w["text"] == "gata!"]
SRC_END = W[-1]["e"] + 0.45
keep, cur = [], max(0.0, W[0]["s"] - 0.05)
for s, e in merged:
    s2 = s + PAD
    if any(abs(s - g) < 0.25 for g in gata_ends): s2 = s + BEAT_AFTER_GATA
    e2 = e - PAD
    if e2 - s2 > 0.05 and s2 > cur and e2 < SRC_END:
        keep.append([cur, s2]); cur = e2
keep.append([cur, SRC_END])
SEG, out_f = [], 0
for s, e in keep:
    tb = round(s * FPS); dur = round(e * FPS) - tb
    if dur <= 0: continue
    SEG.append(dict(srcStart=tb / FPS, srcEnd=(tb + dur) / FPS, trimBefore=tb, from_=out_f, dur=dur)); out_f += dur
TOTAL = out_f

def remap(t):
    for g in SEG:
        if g["srcStart"] - 1e-6 <= t <= g["srcEnd"] + 1e-6: return (g["from_"] + (t - g["srcStart"]) * FPS) / FPS
    for g in SEG:
        if t < g["srcStart"]: return g["from_"] / FPS
    return TOTAL / FPS
for w in W: w["o"] = round(remap(w["s"]), 3); w["oe"] = round(remap(w["e"]), 3)
ot = lambda k: W[k]["o"]
oe = lambda k: W[k]["oe"]

# ---------- moments ----------
i_p1, i_p1e = find("schimbă-mi"), find("pudrat.")
i_g1 = find("Și gata!")
i_p2, i_p2e = find("vreau să crească"), find("meu.")
i_g2 = find("Și gata!", i_g1 + 2)
i_p3, i_p3e = find("vreau să văd"), find("cascadă.")
i_g3 = find("Și gata!", i_g2 + 2)
i_ex = find("Acesta,")
i_acad = find("Academia")
i_wake = find("Deșteaptă-te,")
E = dict(
    hook=dict(start=0.0, end=ot(find("Doar"))),
    mic=ot(find("microfoane")), cam=ot(find("cameră")),
    
    prompts=[
        dict(n=1, start=ot(i_p1) - 0.03, words=list(range(i_p1, i_p1e + 1)), end=ot(i_g1) - 0.02, send=oe(i_p1e)),
        dict(n=2, start=ot(i_p2) - 0.03, words=list(range(i_p2, i_p2e + 1)), end=ot(i_g2) - 0.02, send=oe(i_p2e)),
        dict(n=3, start=ot(i_p3) - 0.03, words=list(range(i_p3, i_p3e + 1)), end=ot(i_g3) - 0.02, send=oe(i_p3e)),
    ],
    pink=ot(i_g1), trees=ot(i_g2), cascade=ot(i_g3),
    gata=[dict(start=ot(i), end=oe(i + 1) + 0.3) for i in (i_g1, i_g2, i_g3)],
    example=ot(i_ex), academy=dict(start=ot(i_acad) - 0.1, wake=ot(i_wake), ro=ot(len(W) - 1)),
)
for p in E["prompts"]:
    p["words"] = [dict(text=W[k]["text"], start=W[k]["o"]) for k in p["words"]]

# captions: 3-4 words, but not while a prompt bubble / gata / academy card shows the words
hidden = [(p["start"], p["end"]) for p in E["prompts"]] + [(g["start"], g["end"]) for g in E["gata"]] + [(E["academy"]["start"], TOTAL / FPS)]
def is_hidden(t): return any(a - 1e-3 <= t < b for a, b in hidden)
KEYS = {"poză", "Claude,", "Claude", "scumpe", "scumpă.", "simplu", "AI", "general.", "înveți"}
vis = [w for w in W if not is_hidden(w["o"])]
# avoid an orphan last word of a sentence: "Doar îi spun ce | vreau." -> "Doar îi spun | ce vreau."
pages, cur = [], []
for n, w in enumerate(vis):
    cur.append(w)
    nxt = vis[n + 1] if n + 1 < len(vis) else None
    if len(cur) >= 4 or w["text"][-1] in ".!?" or (w["text"][-1] == "," and len(cur) >= 2) or not nxt or nxt["o"] - w["oe"] > 0.4:
        pages.append(cur); cur = []
for n in range(1, len(pages)):
    if len(pages[n]) == 1 and len(pages[n - 1]) >= 3 and pages[n - 1][-1]["text"][-1] not in ".!?,":
        pages[n].insert(0, pages[n - 1].pop())
captions = []
for n, p in enumerate(pages):
    end = min(pages[n + 1][0]["o"] if n + 1 < len(pages) else p[-1]["oe"] + 0.3, p[-1]["oe"] + 0.5)
    captions.append(dict(start=p[0]["o"], end=round(end, 3),
                         words=[dict(text=w["text"], start=w["o"], end=w["oe"], key=w["text"] in KEYS) for w in p]))

# ---------- head track (source px) mapped onto output frames ----------
HD = json.load(open(os.path.join(ROOT, "analysis/academia_head.json")))
heads = HD["heads"]
def src_frame(fr):
    for g in SEG:
        if g["from_"] <= fr < g["from_"] + g["dur"]: return g["trimBefore"] + (fr - g["from_"])
    return SEG[-1]["trimBefore"] + SEG[-1]["dur"] - 1
head = []
for fr in range(TOTAL):
    sf = min(src_frame(fr), len(heads) - 1)
    head.append(heads[sf] if heads[sf] else [300, 540, 420])
# smooth over 9 frames
sm = []
for i in range(len(head)):
    win = head[max(0, i - 4): i + 5]
    sm.append([round(sum(h[c] for h in win) / len(win)) for c in range(3)])

# person cut-out only needed from just before the pink reveal
PERSON_FROM = max(0, round(E["pink"] * FPS) - 20)

# ---------- SFX ----------
sfx = [dict(t=0.0, type="whoosh"), dict(t=E["mic"], type="pop"), dict(t=E["cam"], type="pop")]
for p in E["prompts"]:
    sfx += [dict(t=p["start"], type="pop"), dict(t=p["words"][0]["start"] + 0.05, type="typing", dur=p["send"] - p["words"][0]["start"] - 0.1),
            dict(t=p["send"], type="send")]
sfx += [dict(t=E["pink"], type="sparkle"), dict(t=E["trees"], type="grow"), dict(t=E["cascade"], type="cascade"),
        dict(t=E["academy"]["start"], type="sting"), dict(t=E["academy"]["ro"], type="ding")]
sfx = sorted([dict(t=round(e["t"], 3), type=e["type"], dur=round(e.get("dur", 0), 3)) for e in sfx], key=lambda e: e["t"])

speech = []
for w in W:
    if speech and w["o"] - speech[-1][1] < 0.35: speech[-1][1] = w["oe"]
    else: speech.append([w["o"], w["oe"]])

os.makedirs(os.path.join(ROOT, "reels/src/academia"), exist_ok=True)
json.dump(dict(fps=FPS, durationInFrames=TOTAL, events=E, captions=captions, sfx=sfx, speech=speech, head=sm, personFrom=PERSON_FROM),
          open(os.path.join(ROOT, "reels/src/academia/data.json"), "w"), ensure_ascii=False)
json.dump(dict(language="ro", words=[dict(text=w["text"], start=round(w["s"], 3), end=round(w["e"], 3), outStart=w["o"], outEnd=w["oe"]) for w in W]),
          open(os.path.join(ROOT, "academia.transcript.json"), "w"), ensure_ascii=False, indent=1)

base = "\n".join(f'      <Video name="Clip {k + 1} ({g["srcStart"]:.2f}s–{g["srcEnd"]:.2f}s)" src={{SRC}} trimBefore={{{g["trimBefore"]}}} from={{{g["from_"]}}} durationInFrames={{{g["dur"]}}} style={{STYLE}} />'
                 for k, g in enumerate(SEG))
person = "\n".join(f'      <Sequence name="Person {k + 1}" from={{{g["from_"]}}} durationInFrames={{{g["dur"]}}}>\n        <OffthreadVideo src={{PERSON}} startFrom={{{g["trimBefore"]}}} transparent muted style={{STYLE}} />\n      </Sequence>'
                   for k, g in enumerate(SEG) if g["from_"] + g["dur"] > PERSON_FROM)
open(os.path.join(ROOT, "reels/src/academia/Cuts.tsx"), "w").write(f'''// Generated by scripts/build_academia.py — jump cuts (pauses > {MIN_PAUSE}s removed).
import {{ Video }} from "@remotion/media";
import {{ AbsoluteFill, OffthreadVideo, Sequence, staticFile }} from "remotion";

const SRC = staticFile("academia/source.mp4");
const PERSON = staticFile("academia/person.webm");
const STYLE: React.CSSProperties = {{ width: "100%", height: "100%", objectFit: "cover" }};

/** original footage (with its real background) */
export const BaseCuts: React.FC = () => (
    <AbsoluteFill>
{base}
    </AbsoluteFill>
);

/** the same clips, person only (transparent background) */
export const PersonCuts: React.FC = () => (
    <AbsoluteFill>
{person}
    </AbsoluteFill>
);
''')
fmt = lambda x: f"{int(x // 60)}:{x % 60:05.2f}"
print(f"clips={len(SEG)} total={TOTAL / FPS:.2f}s personFrom={PERSON_FROM}")
print("pink", fmt(E["pink"]), "trees", fmt(E["trees"]), "cascade", fmt(E["cascade"]), "academy", fmt(E["academy"]["start"]))
print(" | ".join(" ".join(w["text"] for w in c["words"]) for c in captions))
