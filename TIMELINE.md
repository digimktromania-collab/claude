# Claude Apps — timeline (preview v1)

Durata finală: **64.7s**, 1080×1920, 30 fps. Sursa avea 72.8s. Am făcut 16 jump cuts și am scos 7.9s de pauze (orice pauză > 0.3s, lăsând 0.07s de aer la fiecare tăietură).
Timpii de mai jos sunt pe timeline-ul **final**, după tăieturi.

| # | Timp | Ce se aude | Ce apare pe ecran | SFX |
|---|------|------------|-------------------|-----|
| 1 | 0:00.0 – 0:02.5 | „Bună! Vestea zilei de inteligență artificială” | **HOOK**: logo Claude (se rotește la intrare), bandă portocalie „Claude *Apps*” și pastila „⚡ Vestea zilei în AI” | whoosh 0:00.0 |
| 2 | 0:04.5 – 0:05.6 | „…și cu planul gratuit” | **Toate planurile**: badge-urile Free / Pro / Max / Team intră pe rând, iar în jurul lui **Free** se desenează un cerc | whoosh 0:04.5 · pop 0:05.1 (cerc) |
| 3 | 0:05.7 – 0:07.5 | „Claude tocmai ce a lansat Claude Apps” | **Infografic**: fereastră de app (Photo Resizer) + iconiță care face pop, „fereastra ei + *iconiță*” | whoosh 0:05.7 · pop 0:06.9 (iconiță) |
| — | 0:07.5 – 0:15.3 | „Înainte de a-ți spune… Aplicația 1… un simplu prompt” | doar tu, cu subtitrări și zoom-uri | — |
| 4 | 0:15.3 – 0:22.1 | Aplicația 1 (redimensionare poze) | **Card #1** 🖼️: promptul se scrie typewriter. La „pe desktop” (0:17.1) intră rândul **Mac și Windows** (logo Apple + Windows) | whoosh 0:15.3 · pop 0:17.1 |
| 5 | 0:23.2 – 0:30.0 | Aplicația 2 (reminder TikTok la 18) | **Card #2** ⏰ cu prompt typewriter | whoosh 0:23.2 |
| 6 | 0:30.0 – 0:32.6 | „îți va trimite notificare și nu numai” | 3 iconițe pe rând: 🔔 Notificări (0:31.2, clopoțelul se clatină) → 🖥️ Bara de meniu (0:31.9) → ⌨️ Scurtături (0:32.2) | whoosh · **ding** 0:31.2 · pop · pop |
| 7 | 0:31.4 | (riser înainte de avertisment) | — | **riser** 1.2s |
| 8 | 0:32.6 – 0:38.0 | „poți să o share-uiești… cu membrii team-ului tău” | **AVERTISMENT**: fundal întunecat, „⚠️ ATENȚIE”, card roșu care tremură „Anthropic *nu verifică* aplicațiile”, apoi la „împărtășești” (0:34.9) card verde „Dă-i doar *permisiunile* necesare” | whoosh 0:32.6 · whoosh 0:34.9 |
| 9 | 0:38.2 – 0:46.8 | „Întâi creezi promptul, îi trimiți… lucrează în artefact” | **Card #3** ✍️ „Ideea #3 · a ta”: prompt typewriter, plus pașii ① ② ③ care se bifează pe rând | whoosh · click 0:39.5 / 0:40.7 / 0:45.1 |
| 10 | 0:46.8 – 0:51.2 | „faci click pe cele trei butoane și apeși pe Install App” | **install-steps.png** urcă (slide-up) cu umbră. Text mare în centru **„CLICK ⋯”** (0:47.7), cerc pe ⋯ (0:48.2), marker animat sub **„Install as app”** (0:50.1) | whoosh · click · pop (cerc) · pop (marker) |
| — | 0:51.2 – 0:56.4 | „Creează app, install app. Este foarte simplu…” | doar tu, cu subtitrări și zoom-uri | — |
| 11 | 0:56.4 – 1:04.7 | „Vreau să te întorci în comentarii…” până la final | **CTA**: card 💬 „Scrie **APP** *în comentarii*”, pulsează ușor și rămâne până la final | whoosh 0:56.4 · pop 0:57.0 |

**Punch-in zoom** (alternează 106% și 110%, intră în 3 cadre): 0:00.3 · 0:02.4 · 0:05.7 · 0:10.7 · 0:15.3 · 0:23.2 · 0:30.0 · 0:38.8 · 0:47.7 · 0:52.9 · 0:56.4 · 1:00.4

**Audio**
- Vocea e normalizată la −14 LUFS. Mixul final are −13.9 LUFS integrat.
- SFX-urile sunt la −18 dB față de vârfurile vocii.
- Muzica lo-fi stă la −28 dB sub voce cât timp vorbești și urcă la −20 dB doar în goluri (ducking).

**Subtitrări**: 3–4 cuvinte pe ecran, Inter Black, în treimea de jos. Cuvântul rostit e colorat #D97757. Cuvintele-cheie sunt în *Instrument Serif italic* (ex. inteligență, gratuit, Apps, desktop, TikTok, notificare, artefact, comentarii, digital, geo).

## De decis înainte de randarea finală

1. **„click dreapta” nu apare în vocea ta.** Tu spui „faci click pe **cele trei butoane**”. De aceea am pus „CLICK ⋯” în loc de „RIGHT-CLICK”. Dacă vrei totuși RIGHT-CLICK, schimb un singur rând.
2. **„fereastră și iconiță”, „Mac și Windows” și „toate planurile” nu sunt rostite.** Le-am legat de cele mai apropiate momente: „lansat Claude Apps”, „pe desktop” și „planul gratuit”.
3. **Avertismentul nu e rostit.** L-am pus peste partea despre share („cu cine vrei tu, cu membrii team-ului”), unde are sens tematic, cu riser înainte.
4. **În video sunt doar 2 exemple, nu 3.** Al 3-lea card e „Ideea ta” cu pașii (prompt → trimite → artefact).
5. **Asset-uri lipsă.** `assets/install-steps.png` și `assets/sfx/` nu existau, așa că le-am generat: un mockup de meniu și SFX + muzică sintetizate. Dacă ai fișierele tale, pune-le cu aceleași nume și le înlocuiesc.
6. **Corecturi în transcript**, după scriptul tău: „Crează” → „Creează”, „Aș lucrul ăsta” → „Faci lucrul ăsta”, „la adevăr” → „într-adevăr”. Ultimele cuvinte le-am lăsat „fii deșteaptă, te române!”, cum ai scris tu. Spune-mi dacă trebuie altfel.
