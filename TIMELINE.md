# Claude Apps — timeline (v2, final)

Exportul final e `out/ClaudeApps-final.mp4`: 1080×1920, 30 fps, H.264, 64.7s, −13.9 LUFS.

## Ce s-a schimbat față de v1

**Lip sync.** Fișierul WhatsApp avea frame rate variabil (~29.7 fps), cu ~80 de cadre pierdute (sărituri de 65–98 ms). L-am convertit la 30 fps constant, cu interpolare de mișcare peste cadrele lipsă. După conversie am măsurat din nou sincronizarea buze–sunet: am comparat mișcarea gurii cu sunetul, pe ferestre de 3s. Desincronizarea a dispărut aproape peste tot.

**Ceață pe față** acolo unde decalajul a rămas peste 120 ms (cu încredere bună în măsurătoare). Fața e urmărită automat pe fiecare cadru, iar ceața intră și iese lin:

| Timp final | Context |
|---|---|
| 0:04.6 – 0:06.8 | „planul gratuit… Claude a lansat” |
| 0:23.2 – 0:25.3 | începutul cardului #2 |
| 0:30.1 – 0:33.8 | notificări, apoi intrarea în avertisment |
| 1:00.4 – 1:02.2 | „Nu uita, fii digital, fii geo” |

**Finalul** e „Deșteaptă-te, române!”, cu diacritice. E tipografie animată: „Fii *digital*.” → „Fii *GEO*.” → „Deșteaptă-te,” → „*române!*”, apoi o bandă tricoloră și un ding. CTA-ul „Scrie APP în comentarii” rămâne sus, ca pastilă, până la final.

**Grafice noi în golurile fără grafică:**

| Timp | Ce apare |
|---|---|
| 0:09.7 | „**2** idei de *aplicații*, foarte simple ✓” |
| 0:14.4 | bară de prompt „un *simplu* prompt ↑” |
| 0:51.2 | „Creează app → Install app” |
| 0:52.9 | ștampila „FOARTE *simplu*” + „👶 chiar și la 5 ani” |

**Finisaje:**
- color grading ușor (contrast și saturație) și vignetă;
- bară de progres sus, pentru retenție;
- punch-in zoom centrat pe fața ta, urmărită automat.

## Toate momentele (timeline final)

| Timp | Grafică | SFX |
|---|---|---|
| 0:00.0 | HOOK: logo Claude + bandă „Claude *Apps*” | whoosh |
| 0:04.5 | Free / Pro / Max / Team, cu cerc pe Free | whoosh, pop |
| 0:05.7 | fereastră de app + iconiță | whoosh, pop |
| 0:09.7 | 2 idei | pop |
| 0:14.4 | 1 prompt | click |
| 0:15.3 | Card #1 typewriter, apoi Mac + Windows la 0:17.1 | whoosh, pop |
| 0:23.2 | Card #2 typewriter | whoosh |
| 0:30.0 | 🔔 → 🖥️ → ⌨️ | whoosh, ding, pop, pop |
| 0:31.4 | riser | riser |
| 0:32.6 | AVERTISMENT: card roșu, apoi card verde la 0:34.9 | whoosh ×2 |
| 0:38.2 | Card #3 cu pașii ① ② ③ | whoosh, click ×3 |
| 0:46.8 | install-steps.png, „CLICK ⋯”, cerc pe ⋯, marker sub „Install as app” | whoosh, click, pop, pop |
| 0:51.2 | Creează app → Install app | pop, pop |
| 0:52.9 | FOARTE simplu · 5 ani | whoosh, pop, pop |
| 0:56.4 | CTA „Scrie APP în comentarii” | whoosh, pop |
| 1:00.4 | Outro „Deșteaptă-te, române!” | whoosh, pop, pop, whoosh, ding |

**Audio:**
- vocea e normalizată la −14 LUFS;
- SFX-urile sunt la −18 dB față de voce;
- muzica lo-fi e la −28 dB sub voce, cu ducking.
