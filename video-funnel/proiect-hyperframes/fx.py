# Sound effects + gentle light-sweep transitions, shared by build.py (video 1) and build2.py (video 2).
# exec()'d from inside the build scripts after the cards/splits are assembled; uses cards, splits, js,
# cards_html, T, DUR, S, OUT from the caller.
import shutil, subprocess
SFX_SRC = f"{S}/hf/node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx"
os.makedirs(f"{OUT}/assets/sfx", exist_ok=True)
for f in ("whoosh", "whoosh-cinematic", "pop", "sparkle", "typing", "click-soft", "impact-bass-1"):
    shutil.copy(f"{SFX_SRC}/{f}.mp3", f"{OUT}/assets/sfx/{f}.mp3")
# two softer takes of the whoosh (pitch-shifted, low-passed) so repeated slides don't sound identical
for name, rate in (("whoosh-lo", 0.86), ("whoosh-hi", 1.12)):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{SFX_SRC}/whoosh.mp3", "-af",
                    f"asetrate=44100*{rate},aresample=44100,lowpass=f=6500", f"{OUT}/assets/sfx/{name}.mp3"], check=True)
shutil.copy(f"{SFX_SRC}/CREDITS.md", f"{OUT}/assets/sfx/CREDITS.md")

# peak offset (s) inside each file, measured with `npx hyperframes audio <file> --json`
PEAK = {"whoosh": .162, "whoosh-lo": .19, "whoosh-hi": .145, "whoosh-cinematic": 2.503, "pop": .12,
        "sparkle": .027, "typing": .0, "click-soft": .073, "impact-bass-1": .073}
cues = []  # (file, visual_time, volume)
def cue(f, t, vol):
    cues.append((f, t, vol))

takes = ["whoosh-lo", "whoosh-hi", "whoosh"]
for k, (cid, s, e, inner, extra) in enumerate(cards):
    if s > 0:
        cue(takes[k % 3], s + 0.2, 0.16)
for sid, s, e, inner, extra in splits:
    cue("whoosh-cinematic", s + 0.25, 0.22)
    cue("whoosh-lo", e - 0.22, 0.14)
for f, t, v in EXTRA_SFX:
    cue(f, t, v)

sfx_html = []
for n, (f, t, vol) in enumerate(sorted(cues, key=lambda c: c[1])):
    st = max(0.0, t + 1 / 30 - PEAK[f])  # peak lands one frame after the picture
    sfx_html.append(f'<audio id="sfx{n}" src="assets/sfx/{f}.mp3" data-start="{st:.3f}" data-volume="{vol}" data-track-index="{6 + n % 3}"></audio>')
cards_html.extend(sfx_html)

# gentle transitions: a soft warm light sweep across the frame at each section change
cards_html.append(f'<div id="leak" class="clip" data-start="0" data-duration="{DUR}" data-track-index="5" data-layout-ignore>' + "".join(f'<div class="lk" id="lk{i}"></div>' for i in range(len(LEAKS))) + '</div>')
for i, t in enumerate(LEAKS):
    js.append(f'tl.fromTo("#lk{i}",{{x:-1100,opacity:0}},{{x:1100,duration:1.0,ease:"sine.inOut"}},{t - 0.5:.2f});'
              f'tl.fromTo("#lk{i}",{{opacity:0}},{{opacity:1,duration:.3,ease:"sine.out"}},{t - 0.5:.2f});'
              f'tl.to("#lk{i}",{{opacity:0,duration:.35,ease:"sine.in"}},{t + 0.15:.2f});')
LEAK_CSS = ("#leak { position:absolute; inset:0; z-index:8; pointer-events:none; overflow:hidden; }"
            ".lk { position:absolute; left:-300px; top:-200px; width:1680px; height:2320px; opacity:0;"
            " background:linear-gradient(105deg, rgba(255,226,170,0) 30%, rgba(255,214,140,.24) 45%, rgba(255,244,220,.36) 50%, rgba(255,214,140,.24) 55%, rgba(255,226,170,0) 70%);"
            " mix-blend-mode:soft-light; }")
print("sfx cues", len(cues), "leaks", len(LEAKS))
