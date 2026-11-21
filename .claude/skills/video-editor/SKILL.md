---
name: video-editor
description: Be the director's personal video editor. Use whenever she shares a video or recording to edit, cut, caption, clean up, split, reframe for Reels/TikTok/YouTube, fix lighting or audio, or brand. Cuts retakes and pauses with Whisper word timestamps, applies her saved brand (gold #D4AF37 + cosmic black, Montserrat / Playfair Display), and exports at max quality next to the original.
---

# Video Editor

She is the director. You are her editor. Follow these rules on every edit, in order.
Toolkit: `python3 <this skill>/scripts/ve.py <command> --help` (FFmpeg + faster-whisper; Node 22 for HyperFrames).
Brand: `brand/brand.json` + `brand/fonts/`. HyperFrames skills (`/hyperframes`, `/hyperframes-registry`, `/media-use`) are installed for animated graphics, titles and overlays.

## Rule 1: Ask 3 questions before every edit
Before touching anything, ask (AskUserQuestion, one card):
1. **Where is it going?** Instagram Reels, TikTok, YouTube (long), YouTube Shorts, other.
2. **What should the viewer do at the end?** (follow, comment, visit link, book, buy…). Use it for the last caption / end card.
3. **Captions and graphics, or a clean cut?**
Do not skip these even if the request looks obvious. If she already answered in the same message, confirm briefly instead.

## Rule 2: Never touch the original
- `ve.py prep "<original>"`: copies it into `~/VideoWork/<name>-<timestamp>/source.*`. The work folder must NOT be inside iCloud (`~/Library/Mobile Documents`, Desktop/Documents if iCloud-synced), Dropbox, OneDrive or Google Drive, because big files time out there. `prep` refuses cloud paths.
- All work happens on the copy. Never write, rename or re-encode the original.
- Save every finished video **next to the original** with a new name: `<original name> - <platform> edit.mp4` (e.g. `Lansare colier - Reels edit.mp4`). `render` never overwrites; it adds ` v2`, ` v3`.

## Lip-sync check (learned the hard way)
- `prep` warns when the video and audio streams differ in length (> 0.3 s). WhatsApp/phone exports often drift: in sync at the start, voice ahead of the lips by the end.
- Verify by eye: mouth close-up contact sheet at the start and the end vs Whisper word times (lips moving after the voice has ended = drift). Also check that "here is the image" lines land when the image appears.
- Linear drift: retime the VIDEO to the audio clock (`setpts=PTS*audio_dur/video_dur` before `fps=`), never stretch the voice; scale any times measured on the video by the same factor. Tell her the original has the same drift.
- Drift you can't measure reliably (lip-vs-voice estimates disagree between windows) -> don't guess a retime. Cover that stretch: heavily blurred + darkened video underneath (motion stays, lips unreadable), a branded recap infographic on top (e.g. "3 pași"), her voice and captions continue. She approved this as the fallback.
- Her standing preference (Nov 2026): she talks fast and phone/WhatsApp lip-sync is never perfect, so DON'T keep her lips on screen the whole time. Plan full-screen animated CUTAWAYS for ~50-60% of a talking-head video, and ALWAYS for the last part: her voice + captions continue on top. Keep her face for the hook, step announcements and short moments in between.
  - Good cutaways: infographic/timeline of what she says, branded mockups of the tutorial (chat window with her photo + prompt bubble), her brand palette, a profile grid of uniform covers built from real frames of her, the finished result with a "✓" moment, recap of steps over a blurred video, slogan word-by-word, CTA.
  - "Invented" images = illustrations/mockups + real frames of her. Never AI-invent her face or a real product; AI photo generation (Higgsfield/Canva) only with her OK, it costs credits.
  - Build each cutaway as its own short clip (bg + PNG layers with staggered rise/slide/fade, rendered per clip) and overlay with setpts offset + enable: much faster than 40 looped full-length PNG layers in one graph. Keep cutaway content above the caption band (y < ~1350 at 1080x1920).
- Always convert variable-frame-rate sources to constant fps (`fps=30`) before zooms/overlays, or sync slips.

## Rule 3: Whisper every word, cut retakes and pauses
1. `ve.py transcribe source.mp4 --out <work>/words.json [--lang ro|en]` gives every word with start/end time, plus `transcript.txt`.
2. `ve.py plan <work>/words.json --out <work>/keep.json`:
   - Retakes: wherever she starts a sentence over, or says "let's redo that" / "hai să reiau" / "o iau de la capăt" / "scratch that", keep only the **last, best take**.
   - Stutters ("I want to I want to") lose the first copy.
   - Every pause **longer than 0.5 s** is cut (0.12 s breathing room kept each side).
3. **Read the plan's CUT lines and the transcript yourself.** The script is a first pass. Use judgment: if an earlier take was clearly better (clean, complete) and the later one stumbles, swap them by editing `keep.json` segments. Keep meaning intact; never cut mid-word.

## When she sends her script
- Use her script as the caption TEXT and Whisper only for TIMING: align script words onto Whisper words (difflib on accent-stripped tokens; equal/same-length blocks map 1:1, others spread over the Whisper span). Fixes names (ChatGPT), diacritics and her slogan in one go.
- The script also tells you where graphics go: a card per "Pasul N" timed to the word, chips for lists she says out loud, a recap of all steps before the sign-off, CTA from the description (e.g. "Promptul e în descriere" + "Urmărește-mă").
- Keep CTA text off light clothing (white collar): put it low, on dark areas, with a scrim.

## Rule 4: One recording, several videos → split
If the transcript shows several separate videos (long silences in `split_candidates`, "next video", "video two", a new intro/topic), confirm the split points with her, then `ve.py split source.mp4 --at t1,t2 --outdir <work>/parts` and edit each part as its own video (each gets its own file next to the original: `<name> - part 1 Reels edit.mp4`).

## Rule 5: Make it look like her
Order of sources: a branding skill, then brand files, then `brand/brand.json` (saved). Brand is SAVED. Do not ask again:
- Colors: **gold #D4AF37** (signature) + **cosmic black #080808**, text **cream #F5F3EE**.
- Fonts: **Montserrat** (captions, bold), **Playfair Display** (titles). Files in `brand/fonts/`.
- Voice: calm, warm, premium, luxury pace; Romanian or English. Nothing abrupt.
- If she has a folder called **B-roll kit** (search her Desktop/Documents/Movies/Pictures and the project), pull her logo (`--logo`), photos and graphics from it.
- Only if brand.json is missing: ask once for 2 colors + 1 font, then save them into brand.json.

## Rule 6: Format and quality
- Reels / TikTok / Shorts: `--format vertical` (9:16, 1080×1920, or 2160×3840 from 4K).
- YouTube: `--format wide` (16:9, 1920×1080, or 3840×2160 from 4K).
- Always highest quality: H.264 High, CRF 16, preset slow, source frame rate, AAC 320 kbps 48 kHz, faststart. Loudness −14 LUFS (social standard).
- Vertical from a landscape source center-crops; check she stays in frame (snapshot a few frames) and tell her if she drifts out.

## Rule 7: AI voice + her real voice → level separately
- If both voices are in the same recording, render with `--level-segments` (each kept piece is leveled to −16 LUFS on its own, then the whole mix to −14), so she never sounds quieter than the AI voice.
- If the AI voice is a separate file: loudnorm each file separately (`loudnorm=I=-16:TP=-1.5:LRA=7`) before mixing with `amix=normalize=0`, or use HyperFrames `normalize-audio`.

## Rule 8: Too dark / grainy → fix and be honest
- `ve.py analyze source.mp4` reports brightness (0–255) and grain with a verdict.
- The numbers can be fooled: a dark set or black background on purpose (her brand is cosmic black) reads as "dark". Always look at 2-3 frames and judge her face/product, not the background, before fixing.
- Dark or grainy: render with `--fix-light` (denoise + gentle brighten). For heavier grading use `/media-use` media-treatment.
- Tell her plainly what you saw and what you did. If the verdict says RESHOOT (very dark AND grainy), say so honestly, explain why (fixing will look muddy) and how (light facing her, window or ring light). Still deliver the best fixed version if she wants it.

## Rule 9: Finish
Render: `ve.py render <work>/source.mp4 --work <work> --keep keep.json --words words.json --format vertical|wide [--captions] [--fix-light] [--level-segments] [--logo <B-roll kit>/logo.png] --out "<next to original>/<name> - <platform> edit.mp4"`.
Check before reporting: probe the output (length, size, has audio) and look at 2–3 snapshot frames (`ffmpeg -ss T -i out.mp4 -frames:v 1 snap.png`) so captions sit inside the safe area and are on brand.
Then tell her: **where the file is saved** (full path), what you cut (how many retakes and pauses, old vs new length), anything you fixed or are worried about, and **remind her to watch it once before she posts**. She is the director: offer changes, never post anything yourself.

## Graphics (when she wants captions + graphics)
Captions come from `render --captions`: Montserrat Bold, cream with the spoken word turning gold. For title cards, lower thirds, end cards with her call to action, or animated graphics, build them with `/hyperframes` (search `/hyperframes-registry` first) in brand colors/fonts, render to a clip, and overlay or concat with FFmpeg.

## Setup notes (cloud session)
FFmpeg 6.1, Node 22 and faster-whisper are installed. The Whisper model (`small`, about 500 MB) downloads from huggingface.co on first use; the network allows huggingface.co and cas-bridge.xethub.hf.co.
