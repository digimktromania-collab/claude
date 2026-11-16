#!/usr/bin/env python3
"""Video-editor toolkit (FFmpeg + faster-whisper). Run: python3 ve.py <command> --help

Commands
  prep        copy the original into a safe work folder (never touches the original)
  transcribe  every word with its start/end time -> words.json + transcript.txt
  plan        find retakes, restarts and pauses > 0.5 s -> keep.json (review it!)
  analyze     brightness + grain check, with an honest fix/reshoot verdict
  split       cut one long recording into several files at given times
  render      cut, reframe (vertical/wide), level audio, brand captions, export at max quality
"""
import argparse, datetime, json, os, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
BRAND = json.loads((SKILL / "brand" / "brand.json").read_text())
FONTS = SKILL / "brand" / "fonts"
CLOUD_MARKERS = ("Mobile Documents", "iCloud", "CloudStorage", "Dropbox", "OneDrive", "Google Drive", "GoogleDrive")
REDO = re.compile(
    r"\b(let'?s (redo|do) (that|this|it)( again| over)?|let me (redo|start|try) (that|this|it|again|over)|"
    r"start (that |it )?over|one more time|take (two|2|three|3)|scratch that|from the top|"
    r"hai s[aă] (reiau|o iau|mai [iî]ncerc)|o (mai )?iau de la (cap[aă]t|[iî]nceput)|[iî]nc[aă] o dat[aă]|reiau)\b", re.I)


def sh(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd)[:300], file=sys.stderr)
    return subprocess.run([str(c) for c in cmd], check=True, **kw)


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                         check=True, capture_output=True, text=True).stdout
    j = json.loads(out)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), None)
    w, h = (int(v["width"]), int(v["height"])) if v else (0, 0)
    rot = 0
    for sd in (v or {}).get("side_data_list", []):
        rot = int(sd.get("rotation", 0) or 0)
    rot = int((v or {}).get("tags", {}).get("rotate", rot))
    if abs(rot) % 180 == 90:
        w, h = h, w
    num, den = ((v or {}).get("avg_frame_rate") or "30/1").split("/")
    fps = float(num) / float(den or 1) if float(num) else 30.0
    return {"w": w, "h": h, "fps": fps, "dur": float(j["format"]["duration"]), "audio": a is not None}


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.sub(r"[^\w' ]", "", "".join(c for c in t if not unicodedata.combining(c))).strip()


# ---------------------------------------------------------------- prep
def cmd_prep(a):
    src = Path(a.original).expanduser().resolve()
    root = Path(a.root).expanduser().resolve()
    if any(m.lower() in str(root).lower() for m in CLOUD_MARKERS):
        sys.exit(f"Work root {root} is inside a cloud-synced folder. Pick a local one (default ~/VideoWork).")
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    work = root / f"{re.sub(r'[^A-Za-z0-9_-]+', '_', src.stem)}-{stamp}"
    work.mkdir(parents=True)
    need = src.stat().st_size * 3
    free = shutil.disk_usage(work).free
    if free < need:
        print(f"WARNING: only {free/1e9:.1f} GB free, about {need/1e9:.1f} GB recommended.")
    dst = work / ("source" + src.suffix.lower())
    shutil.copy2(src, dst)
    (work / "ORIGINAL_PATH.txt").write_text(str(src))
    print(json.dumps({"work": str(work), "copy": str(dst), "original": str(src), **probe(dst)}, indent=2))


# ---------------------------------------------------------------- transcribe
def cmd_transcribe(a):
    from faster_whisper import WhisperModel
    work = Path(a.out).parent
    wav = work / "audio16k.wav"
    sh(["ffmpeg", "-y", "-v", "error", "-i", a.video, "-vn", "-ac", "1", "-ar", "16000", wav])
    model = WhisperModel(a.model, device="cpu", compute_type="int8")
    segs, info = model.transcribe(str(wav), word_timestamps=True, vad_filter=False,
                                  language=a.lang, condition_on_previous_text=False,
                                  task="transcribe")
    out, lines = [], []
    for s in segs:
        words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3), "p": round(w.probability, 2)}
                 for w in (s.words or []) if w.word.strip()]
        out.append({"s": round(s.start, 3), "e": round(s.end, 3), "text": s.text.strip(), "words": words})
        lines.append(f"[{s.start:7.2f} - {s.end:7.2f}] {s.text.strip()}")
    Path(a.out).write_text(json.dumps({"language": info.language, "segments": out}, ensure_ascii=False, indent=1))
    (work / "transcript.txt").write_text("\n".join(lines))
    print(f"language={info.language}  segments={len(out)}  -> {a.out}")
    print("\n".join(lines))


# ---------------------------------------------------------------- plan
def sentences(data):
    """Split Whisper segments further at . ? ! so each item is one spoken sentence/attempt."""
    sents = []
    for seg in data["segments"]:
        cur = []
        for w in seg["words"]:
            cur.append(w)
            if re.search(r"[.?!…]$", w["w"]):
                sents.append(cur); cur = []
        if cur:
            sents.append(cur)
    return sents


def cmd_plan(a):
    data = json.loads(Path(a.words).read_text())
    sents = sentences(data)
    drop, reasons = set(), {}
    text = [" ".join(w["w"] for w in s) for s in sents]
    keys = [norm(t).split() for t in text]
    for i, t in enumerate(text):
        if REDO.search(norm(t)) or REDO.search(t.lower()):
            drop.add(i); reasons[i] = "said redo"
            if i > 0:
                drop.add(i - 1); reasons.setdefault(i - 1, "take before 'redo'")
    for i in range(len(sents) - 1):
        k = min(3, len(keys[i]), len(keys[i + 1]))
        if k >= 2 and keys[i][:k] == keys[i + 1][:k]:
            drop.add(i); reasons.setdefault(i, "restarted - later take kept")
        elif len(keys[i]) <= 4 and keys[i] and keys[i + 1][:len(keys[i])] == keys[i]:
            drop.add(i); reasons.setdefault(i, "false start")
    kept = []
    for i, s in enumerate(sents):
        if i in drop:
            continue
        ws = list(s)
        # stutter inside a sentence: "I want to I want to say" -> drop first copy
        changed = True
        while changed:
            changed = False
            nk = [norm(w["w"]) for w in ws]
            for n in (4, 3, 2, 1):
                for j in range(len(ws) - 2 * n + 1):
                    if nk[j:j + n] == nk[j + n:j + 2 * n] and all(nk[j:j + n]):
                        if n == 1 and nk[j] in ("very", "really", "so", "foarte", "mult", "ha", "no", "nu", "da"):
                            continue
                        del ws[j:j + n]; changed = True; break
                if changed:
                    break
        kept.extend(ws)
    segs = []
    for w in kept:
        if segs and w["s"] - segs[-1]["last"] <= a.pause:
            segs[-1]["last"] = w["e"]
        else:
            segs.append({"first": w["s"], "last": w["e"]})
    keep = []
    for s in segs:
        st, en = max(0.0, s["first"] - a.pad), s["last"] + a.pad
        if keep and st <= keep[-1][1]:
            keep[-1][1] = en
        else:
            keep.append([round(st, 3), round(en, 3)])
    allw = [w for s in sents for w in s]
    split_cands = [{"at": round((x["e"] + y["s"]) / 2, 2), "silence": round(y["s"] - x["e"], 2)}
                   for x, y in zip(allw, allw[1:]) if y["s"] - x["e"] >= a.split_gap]
    dropped = [{"start": sents[i][0]["s"], "end": sents[i][-1]["e"], "text": text[i], "reason": reasons[i]}
               for i in sorted(drop)]
    orig = allw[-1]["e"] - allw[0]["s"] if allw else 0
    new = sum(e - s for s, e in keep)
    plan = {"segments": keep, "dropped": dropped, "split_candidates": split_cands,
            "stats": {"speech_span": round(orig, 2), "kept": round(new, 2), "removed": round(orig - new, 2)}}
    Path(a.out).write_text(json.dumps(plan, ensure_ascii=False, indent=1))
    print(f"kept {len(keep)} pieces, {new:.1f}s of {orig:.1f}s  -> {a.out}")
    for d in dropped:
        print(f"  CUT  {d['start']:7.2f}  ({d['reason']}): {d['text']}")
    for c in split_cands:
        print(f"  SPLIT? silence {c['silence']}s at {c['at']}s")


# ---------------------------------------------------------------- analyze
def cmd_analyze(a):
    import numpy as np
    info = probe(a.video)
    W, H = 320, int(320 * info["h"] / max(info["w"], 1)) // 2 * 2
    n = 8
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf",
                          f"fps={n / max(info['dur'], 0.1):.4f},scale={W}:{H},format=gray",
                          "-frames:v", str(n), "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)
    bright = float(fr.mean())
    k = 3
    pad = np.pad(fr, ((0, 0), (k, k), (k, k)), mode="edge")
    blur = sum(pad[:, dy:dy + H, dx:dx + W] for dy in range(2 * k + 1) for dx in range(2 * k + 1)) / (2 * k + 1) ** 2
    noise = float(np.median(np.abs(fr - blur)))
    dark = bright < 70
    very_dark = bright < 40
    grainy = noise > 4.5
    verdict = "looks fine - no fix needed"
    if dark or grainy:
        verdict = "fixable - I will brighten and/or denoise it"
    if very_dark and grainy:
        verdict = "RESHOOT recommended - too dark and grainy; fixing will look muddy. Add a light facing you (window or ring light)."
    elif very_dark:
        verdict = "fixable but borderline - brightening this much adds grain; a reshoot with more light would look clearly better"
    print(json.dumps({"brightness_0_255": round(bright, 1), "grain_score": round(noise, 2), "dark": dark,
                      "grainy": grainy, "verdict": verdict, **info}, indent=2))


# ---------------------------------------------------------------- split
def cmd_split(a):
    cuts = [0.0] + [float(x) for x in a.at.split(",")] + [probe(a.video)["dur"]]
    out = Path(a.outdir); out.mkdir(parents=True, exist_ok=True)
    for i, (s, e) in enumerate(zip(cuts, cuts[1:]), 1):
        dst = out / f"part{i:02d}.mp4"
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", a.video,
            "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000", dst])
        print(dst)


# ---------------------------------------------------------------- captions
def ass_color(hexc):
    h = hexc.lstrip("#")
    return f"&H00{h[4:6]}{h[2:4]}{h[0:2]}".upper()


def remap(words, segments):
    """Move word times from the source timeline to the cut timeline; drop words that were cut."""
    out, offset = [], 0.0
    for s, e in segments:
        for w in words:
            if w["s"] >= s - 0.02 and w["e"] <= e + 0.02:
                out.append({"w": w["w"], "s": w["s"] - s + offset, "e": min(w["e"], e) - s + offset})
        offset += e - s
    return out


def build_ass(words, W, H, path):
    vertical = H > W
    size = round(H * (0.048 if vertical else 0.058))
    maxw = 3 if vertical else 5
    marg_v = round(H * (0.24 if vertical else 0.08))
    cream, gold, black = (ass_color(BRAND["colors"][k]) for k in ("text", "primary", "secondary"))
    font = BRAND["fonts"]["captions"]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font},{size},{cream},{gold},{black},&H80080808,-1,0,0,0,100,100,1,0,1,{max(3, size // 14)},{max(1, size // 30)},2,{round(W*0.1)},{round(W*0.1)},{marg_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= maxw or w["s"] - cur[-1]["e"] > 0.35 or re.search(r"[.?!,;:]$", cur[-1]["w"])):
            groups.append(cur); cur = []
        cur.append(w)
    if cur:
        groups.append(cur)

    def t(x):
        x = max(0, x); return f"{int(x // 3600)}:{int(x % 3600 // 60):02d}:{x % 60:05.2f}"

    def clean(s):
        return s.replace("{", "(").replace("}", ")").replace("\\", "/")

    ev = []
    for gi, g in enumerate(groups):
        g_end = g[-1]["e"] + 0.15
        if gi + 1 < len(groups):
            g_end = min(g_end, groups[gi + 1][0]["s"])
        for i, w in enumerate(g):
            st = w["s"] if i else g[0]["s"]
            en = g[i + 1]["s"] if i + 1 < len(g) else g_end
            if en <= st:
                continue
            parts = []
            for j, x in enumerate(g):
                txt = clean(x["w"])
                if j == i:
                    parts.append(r"{\c" + gold + r"&\fscx108\fscy108}" + txt + r"{\c" + cream + r"&\fscx100\fscy100}")
                else:
                    parts.append(txt)
            fade = r"{\fad(80,0)}" if i == 0 else ""
            ev.append(f"Dialogue: 0,{t(st)},{t(en)},Cap,,0,0,0,,{fade}{' '.join(parts)}")
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    return len(groups)


# ---------------------------------------------------------------- render
def target_size(fmt, info):
    w, h = info["w"], info["h"]
    if fmt == "vertical":
        return (2160, 3840) if min(w, h) >= 2160 and max(w, h) >= 3840 else (1080, 1920)
    if fmt == "wide":
        return (3840, 2160) if max(w, h) >= 3840 and min(w, h) >= 2160 else (1920, 1080)
    if fmt == "square":
        return (1080, 1080)
    return (w // 2 * 2, h // 2 * 2)


def unique(p):
    p = Path(p); n = 2
    while p.exists():
        p = p.with_name(f"{p.stem.rsplit(' v', 1)[0]} v{n}{p.suffix}"); n += 1
    return p


def cmd_render(a):
    src = Path(a.video).resolve()
    info = probe(src)
    work = Path(a.work).resolve() if a.work else src.parent
    segs = json.loads(Path(a.keep).read_text())["segments"] if a.keep else [[0.0, info["dur"]]]
    segs = [[max(0, s), min(e, info["dur"])] for s, e in segs if e > s]
    W, H = target_size(a.format, info)
    fps = round(info["fps"], 3)
    lines, n = [], len(segs)
    for i, (s, e) in enumerate(segs):
        lines.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}];")
        if info["audio"]:
            lvl = ",loudnorm=I=-16:TP=-1.5:LRA=7" if a.level_segments else ""
            lines.append(f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,aresample=48000{lvl},"
                         f"afade=t=in:d=0.012,afade=t=out:st={max(0, e - s - 0.012):.3f}:d=0.012[a{i}];")
    ins = "".join(f"[v{i}]" + (f"[a{i}]" if info["audio"] else "") for i in range(n))
    lines.append(f"{ins}concat=n={n}:v=1:a={1 if info['audio'] else 0}[vc]" + ("[ac];" if info["audio"] else ";"))
    vf = []
    if a.fix_light:
        vf.append("hqdn3d=3:2:6:4,eq=brightness=0.05:contrast=1.06:gamma=1.18:saturation=1.06")
    vf.append(f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},setsar=1,fps={fps}")
    ass = None
    if a.captions:
        data = json.loads(Path(a.words).read_text())
        words = [w for sg in data["segments"] for w in sg["words"]]
        ass = work / "captions.ass"
        g = build_ass(remap(words, segs), W, H, ass)
        print(f"captions: {g} caption groups -> {ass}", file=sys.stderr)
        esc = lambda p: str(p).replace("\\", "/").replace(":", r"\:").replace("'", r"\'")
        vf.append(f"subtitles='{esc(ass)}':fontsdir='{esc(FONTS)}'")
    vchain = "[vc]" + ",".join(vf)
    if a.logo:
        lw = round(W * 0.14)
        lines.append(vchain + "[vb];")
        lines.append(f"movie='{a.logo}',scale={lw}:-1,format=rgba,colorchannelmixer=aa=0.9[lg];")
        lines.append(f"[vb][lg]overlay=W-w-{round(W*0.06)}:{round(H*0.05)}[vout]" + (";" if info["audio"] else ""))
    else:
        lines.append(vchain + "[vout]" + (";" if info["audio"] else ""))
    if info["audio"]:
        lines.append("[ac]loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[aout]")
    fscript = work / "filter.txt"
    fscript.write_text("\n".join(lines))
    out = unique(a.out)
    cmd = ["ffmpeg", "-y", "-v", "error", "-stats", "-i", src, "-filter_complex_script", fscript, "-map", "[vout]"]
    if info["audio"]:
        cmd += ["-map", "[aout]", "-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
    cmd += ["-c:v", "libx264", "-preset", "slow", "-crf", "16", "-profile:v", "high", "-pix_fmt", "yuv420p",
            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-movflags", "+faststart", out]
    sh(cmd)
    print(json.dumps({"saved": str(out), "size": f"{W}x{H}", **{k: v for k, v in probe(out).items() if k in ("dur", "fps")}}))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    x = sp.add_parser("prep"); x.add_argument("original"); x.add_argument("--root", default="~/VideoWork")
    x = sp.add_parser("transcribe"); x.add_argument("video"); x.add_argument("--out", required=True)
    x.add_argument("--model", default="small", help="tiny/base/small/medium/large-v3 (bigger = slower, more accurate)")
    x.add_argument("--lang", default=None, help="e.g. ro, en (default: auto-detect)")
    x = sp.add_parser("plan"); x.add_argument("words"); x.add_argument("--out", required=True)
    x.add_argument("--pause", type=float, default=0.5); x.add_argument("--pad", type=float, default=0.12)
    x.add_argument("--split-gap", type=float, default=4.0)
    x = sp.add_parser("analyze"); x.add_argument("video")
    x = sp.add_parser("split"); x.add_argument("video"); x.add_argument("--at", required=True); x.add_argument("--outdir", required=True)
    x = sp.add_parser("render"); x.add_argument("video"); x.add_argument("--out", required=True)
    x.add_argument("--keep"); x.add_argument("--words"); x.add_argument("--work")
    x.add_argument("--format", choices=["vertical", "wide", "square", "source"], default="vertical")
    x.add_argument("--captions", action="store_true"); x.add_argument("--fix-light", action="store_true")
    x.add_argument("--level-segments", action="store_true", help="level each kept piece on its own (AI voice + real voice)")
    x.add_argument("--logo")
    a = p.parse_args()
    globals()["cmd_" + a.cmd](a)


if __name__ == "__main__":
    main()
