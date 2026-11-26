import json, sys, wave, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("large-v3", device="cpu", compute_type="int8")
prompt = "Bună! Vestea zilei de inteligență artificială. Claude tocmai ce a lansat Claude Apps. Facebook, TikTok, Instagram. Install App. Fii digital, fii geo."
w=wave.open(src); audio=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
segs, info = m.transcribe(audio, language="ro", word_timestamps=True, vad_filter=False, initial_prompt=prompt, beam_size=5)
words=[]
for s in segs:
    for w in s.words:
        words.append({"text": w.word.strip(), "start": round(w.start,3), "end": round(w.end,3), "prob": round(w.probability,3)})
        print(words[-1], flush=True)
json.dump({"language":"ro","words":words}, open(out,"w"), ensure_ascii=False, indent=1)
