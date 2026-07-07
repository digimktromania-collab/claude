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
├── assets/            Imaginile universului (nucleu + planete) — vezi mai jos
├── copy/              Documentele de strategie și conținut
│   ├── directie-creativa.md   ADN-ul brandului (ton, culori, principii)
│   └── brief-site.md          Arhitectura site-ului, pagină cu pagină
├── website/           Site-ul propriu-zis (se construiește din Faza 2)
├── index.html         Prototip actual al portalului (emoji + gradienți CSS)
└── README.md          Acest fișier
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

Apoi deschide în browser:

- Prototip actual: <http://localhost:8000/index.html>
- Homepage (din Faza 2): <http://localhost:8000/website/index.html>

> Librăriile GSAP, ScrollTrigger, Lenis și Three.js se încarcă din CDN, deci e
> nevoie de conexiune la internet la prima rulare.

---

## Stack tehnic

HTML · CSS · JavaScript · GSAP + ScrollTrigger · Lenis · Three.js ·
Google Fonts (Playfair Display + Montserrat).

---

## Stadiul lucrului

- [x] **Faza 1** — workspace + documente de plan (`copy/`, `README.md`).
- [ ] **Faza 2** — homepage: nucleu + planete orbitând, carduri, fundal Three.js.
- [ ] **Faza 3** — scroll cinematic (GSAP + ScrollTrigger + Lenis).
- [ ] **Faza 4** — paginile-lumi.
- [ ] **Faza 5** — meniu fullscreen, mobil, verificare, raport final.

Vezi `copy/directie-creativa.md` și `copy/brief-site.md` pentru detalii.
