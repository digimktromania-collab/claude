# Brief de Site — Universul Iordache Georgiana

Documentul tehnic + de conținut care traduce direcția creativă în structura
concretă a site-ului. Ordinea de lucru urmează cele 5 faze din brief-ul inițial.

---

## Stack tehnic

- **HTML / CSS / JavaScript** (fără build step — rulează direct din fișiere).
- **GSAP + ScrollTrigger** — animații și scroll cinematic.
- **Lenis** — scroll fin, catifelat, sincronizat cu ScrollTrigger (lag smoothing dezactivat).
- **Three.js** — câmp de stele, particule aurii, adâncime atmosferică.
- Fonturi: Google Fonts (Playfair Display + Montserrat).
- Librăriile se încarcă din CDN (necesită conexiune la internet la rulare).

---

## Structura de fișiere (țintă)

```
/
├── assets/
│   ├── nucleu.png                    ← portret cinematic Georgiana (NU se modifică)
│   └── planete/
│       ├── planeta-inceput.png       (verde)
│       ├── planeta-marketing.png     (auriu)
│       ├── planeta-ai.png            (mov)
│       ├── planeta-business.png      (albastru)
│       ├── planeta-mir.png           (auriu cu inel — cea mai luminoasă)
│       └── planeta-mentorat.png      (crem)
├── copy/
│   ├── directie-creativa.md          ← ADN-ul brandului
│   └── brief-site.md                 ← acest document
├── website/
│   ├── index.html                    ← homepage (portalul)
│   ├── css/                          ← stiluri partajate
│   ├── js/                           ← logica partajată (univers, scroll, meniu)
│   └── pagini/                       ← paginile-lumi (vezi mai jos)
└── README.md                         ← cum rulezi site-ul local
```

> **NOTĂ IMPORTANTĂ (blocant pentru Faza 2):** la momentul acestui plan,
> fișierele imagine din `assets/` (`nucleu.png` și cele 6 planete) **nu sunt
> încă prezente în repository**. Structura de directoare există, dar imaginile
> trebuie adăugate înainte ca portalul din Faza 2 să le poată folosi. Vezi
> secțiunea „Asset-uri" din README. Există deja un prototip la `/index.html`
> care folosește emoji + gradienți CSS ca substitut temporar.

---

## Harta paginilor (Faza 4)

| Pagină | Fișier | Rol |
|---|---|---|
| Homepage / Portal | `website/index.html` | Nucleu + 6 planete orbitând, sub-secțiuni cinematice. |
| Începe aici | `website/pagini/incepe-aici.html` | „Unde te afli astăzi în călătoria ta?" — busola vizitatorului. |
| Academia MIR | `website/pagini/academia-mir.html` | Oferta premium: ce e, pentru cine, ce include, ce NU e, 597€, CTA + formular. |
| Marketing Digital | `website/pagini/marketing-digital.html` | Ce e, ce include, pentru cine, rezultat, CTA. |
| AI Creativ | `website/pagini/ai-creativ.html` | Ce e, ce include, tool-uri, rezultat, CTA. |
| Am deja un business | `website/pagini/am-un-business.html` | Probleme → soluții → mentorat / strategie / MIR. |
| Mentorat 1:1 | `website/pagini/mentorat.html` | Ce primește, cum funcționează, preț / aplicație, CTA. |
| Despre Georgiana | `website/pagini/despre.html` | Poveste, tranziție, de ce există Universul GEO. Folosește `nucleu.png`. |
| Resurse / Blog | `website/pagini/blog.html` | Categorii, articole-pilon, newsletter. |
| Contact | `website/pagini/contact.html` | Formular, email, social, mesaj scurt. |

---

## Homepage — structura pe verticală (Faza 2 + 3)

1. **HERO / PORTAL** — nucleul auriu viu în centru + 6 planete orbitând.
   - Sub nucleu: „GEORGIANA" / „Universul GEO".
   - Indiciu de interacțiune: „Treci cu mouse-ul peste planete pentru a explora"
     (mobil: „Atinge planetele"). Planetele pulsează de câteva ori la încărcare.
   - Hover → card glassmorphism (nume + descriere). Click → pagina planetei.
2. **Academia MIR** — planeta premium, 597€, CTA. Secțiune „pinned" la scroll.
3. **Metoda** — cum se construiește transformarea, pas cu pas.
4. **Dovadă / autoritate** — DOAR numere reale: „700+ membri în comunitatea MIR".
5. **CTA final** — „Există și o altă cale."

---

## Meniu (Faza 5)

Meniu fullscreen cinematic (deschidere/închidere GSAP fluidă), buton X curat:
**Acasă · Începe aici · Academia MIR · Planetele · Despre Georgiana · Blog · Contact.**

---

## Mobil (Faza 5)

- Sub 768px planetele se rearanjează (constelație / grilă) și **nu acoperă titlul**.
- Texte lizibile, tap pe planete (cardul apare la atingere), tilt dezactivat.
- Optimizări: lazy-load imagini, fără erori în consolă, cod curat.

---

## Descrieri planete (carduri homepage) — text final

| Planetă | Card |
|---|---|
| Sunt la început | „Pentru cine simte că există și o altă cale, dar nu știe de unde să înceapă." |
| Marketing Digital | „Învață să construiești, să vinzi și să te poziționezi online." |
| AI Creativ | „AI din joacă în instrument real: timp, claritate, conținut." |
| Am deja un business | „Ai deja ceva și vrei un sistem mai clar care să lucreze pentru tine." |
| Academia MIR | „Ecosistemul premium: educație, comunitate, strategie. Totul într-un singur loc." |
| Mentorat 1:1 | „Claritate, audit, direcție și un plan personalizat, doar pentru tine." |

---

## Ordinea de execuție

1. **Faza 1** — workspace + fișiere plan → **CHECKPOINT 1 (aprobare)**.
2. **Faza 2** — homepage: nucleu + planete orbitând, carduri, fundal Three.js.
3. **Faza 3** — scroll cinematic (GSAP + ScrollTrigger + Lenis), secțiuni homepage.
4. **Faza 4** — paginile-lumi.
5. **Faza 5** — meniu fullscreen, mobil, verificare, raport final.
