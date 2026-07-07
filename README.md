# Universul Iordache Georgiana

> Un portal cinematic, condus de scroll, către universul GEO — un nucleu auriu
> (Georgiana) în jurul căruia orbitează șase lumi (comunitățile ecosistemului).
>
> **„Există și o altă cale."**

Nu e un site obișnuit. E o poartă. Filozofia: *premium, elegant, cinematic,
cosmic, cald, sofisticat.* Profunzimea bate zgomotul.

---

## Structura proiectului

```
├── assets/
│   ├── nucleu.png              Portretul Georgianei (de adăugat — vezi mai jos)
│   └── planete/                Cele 6 planete (PNG cu fundal transparent)
├── copy/
│   ├── directie-creativa.md    ADN-ul brandului (ton, culori, principii)
│   └── brief-site.md           Arhitectura site-ului, pagină cu pagină
├── website/                    ★ SITE-UL ★
│   ├── index.html              Homepage — portalul (nucleu + planete orbitând)
│   ├── css/stil.css            Sistemul de design complet
│   ├── js/
│   │   ├── univers.js          Motorul partajat (Three.js, Lenis, GSAP, meniu)
│   │   └── vendor/             Librăriile găzduite local (three, gsap, lenis)
│   └── pagini/                 Cele 9 pagini-lumi
├── scripts/genereaza-pagini.py Generatorul paginilor interioare
├── index.html                  Prototip vechi (NU se folosește)
└── README.md                   Acest fișier
```

---

## ⚠️ Asset-uri necesare (blocant pentru Faza 2)

Portalul final folosește imagini reale, pregătite în prealabil. Directoarele
există, dar **fișierele imagine nu sunt încă în repository** și trebuie adăugate:

| Fișier | Descriere |
|---|---|
| `assets/nucleu.png` | Portret cinematic auriu al Georgianei — inima universului. **Nu se modifică.** |
| `assets/planete/planeta-inceput.png` | Planetă verde → „Sunt la început" |
| `assets/planete/planeta-marketing.png` | Planetă aurie → „Marketing Digital Antreprenorial" |
| `assets/planete/planeta-ai.png` | Planetă mov → „AI Creativ & Productivitate" |
| `assets/planete/planeta-business.png` | Planetă albastră → „Am deja un business" |
| `assets/planete/planeta-mir.png` | Planetă aurie cu inel (cea mai luminoasă) → „Academia MIR" |
| `assets/planete/planeta-mentorat.png` | Planetă crem → „Mentorat 1:1" |

Până la adăugarea lor, prototipul din `/index.html` folosește emoji și gradienți
CSS ca substitut vizual, ca să poată fi văzută mișcarea și structura.

---

## Cum rulezi site-ul local

Site-ul e static (HTML/CSS/JS), dar folosește librării din CDN și încarcă
imagini, deci trebuie servit peste HTTP (nu deschis direct ca `file://`).

Dintr-un terminal, în rădăcina proiectului:

```bash
# Varianta 1 — Python (preinstalat pe majoritatea sistemelor)
python3 -m http.server 8000

# Varianta 2 — Node
npx serve .
```

Apoi deschide în browser: <http://localhost:8000/website/index.html>

> Librăriile Three.js, GSAP, ScrollTrigger și Lenis sunt **găzduite local** în
> `website/js/vendor/` — site-ul funcționează și fără CDN, offline. Singura
> resursă externă rămasă sunt fonturile Google (cu fallback elegant serif/sans).

---

## Stack tehnic

HTML · CSS · JavaScript · GSAP + ScrollTrigger · Lenis · Three.js ·
Google Fonts (Playfair Display + Montserrat).

---

## Stadiul lucrului

- [x] **Faza 1** — workspace + documente de plan.
- [x] **Faza 2** — homepage: nucleu + 6 planete orbitând, carduri, fundal Three.js.
- [x] **Faza 3** — scroll cinematic (GSAP + ScrollTrigger + Lenis), secțiuni homepage.
- [x] **Faza 4** — cele 9 pagini-lumi.
- [x] **Faza 5** — meniu fullscreen, mobil, verificare.

**Rămâne de adăugat:** `assets/nucleu.png` (portretul Georgianei). Până atunci,
nucleul afișează un orb auriu de rezervă, generat prin cod.

Vezi `copy/directie-creativa.md` și `copy/brief-site.md` pentru detalii.
