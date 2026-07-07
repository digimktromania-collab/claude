#!/usr/bin/env python3
# Generează cele 9 pagini interioare cu „chrome" partajat (bară, meniu, footer, scripturi).
import os

OUT = "/home/user/claude/website/pagini"
os.makedirs(OUT, exist_ok=True)

# Elementele de meniu: (eticheta, href relativ din pagini/)
MENIU = [
    ("Acasă", "../index.html"),
    ("Începe aici", "incepe-aici.html"),
    ("Academia MIR", "academia-mir.html"),
    ("Planetele", "incepe-aici.html"),
    ("Despre Georgiana", "despre.html"),
    ("Blog", "blog.html"),
    ("Contact", "contact.html"),
]
FOOTER = [
    ("Acasă", "../index.html"),
    ("Începe aici", "incepe-aici.html"),
    ("Academia MIR", "academia-mir.html"),
    ("Despre Georgiana", "despre.html"),
    ("Blog", "blog.html"),
    ("Contact", "contact.html"),
]

def meniu_html(activ):
    def link(et, href):
        cls = ' class="activ"' if et == activ else ''
        return f'<a href="{href}"{cls}>{et}</a>'
    linkuri = "\n    ".join(link(et, href) for et, href in MENIU)
    return f"""  <nav class="meniu" aria-label="Meniu principal">
    <button class="meniu-inchide" aria-label="Închide meniul"></button>
    {linkuri}
    <p class="meniu-nota">Există și o altă cale.</p>
  </nav>"""

def footer_html():
    linkuri = "\n        ".join(f'<a href="{href}">{et}</a>' for et, href in FOOTER)
    return f"""  <footer class="footer">
    <div class="container">
      <a href="../index.html" class="marca">Universul <b>GEO</b></a>
      <nav class="footer-linkuri">
        {linkuri}
      </nav>
      <small>© <span id="an"></span> Universul Iordache Georgiana. Există și o altă cale.</small>
    </div>
  </footer>"""

def pagina(slug, titlu, descriere, culoare, activ, body):
    html = f"""<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{titlu} — Universul GEO</title>
  <meta name="description" content="{descriere}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../css/stil.css">
</head>
<body style="--culoare: {culoare};">
  <div class="fundal-gradient"></div>
  <canvas id="cosmos" aria-hidden="true"></canvas>

  <header class="bara">
    <a href="../index.html" class="marca">Universul <b>GEO</b></a>
    <button class="meniu-buton" aria-label="Deschide meniul"><span></span><span></span><span></span></button>
  </header>

{meniu_html(activ)}

{body}

{footer_html()}

  <script src="../js/vendor/three.min.js"></script>
  <script src="../js/vendor/gsap.min.js"></script>
  <script src="../js/vendor/ScrollTrigger.min.js"></script>
  <script src="../js/vendor/lenis.min.js"></script>
  <script>document.getElementById('an').textContent = new Date().getFullYear();</script>
  <script src="../js/univers.js"></script>
</body>
</html>
"""
    with open(os.path.join(OUT, slug), "w", encoding="utf-8") as f:
        f.write(html)
    print("scris", slug)


# ─────────────────────────────────────────────────────────────────────
# Componente-ajutor pentru corpul paginilor
def hero(img, eyebrow, h1, lead, culoare):
    imgtag = (f'<img class="planeta-mare" src="{img}" alt="{h1}" style="--culoare:{culoare};">'
              if img else "")
    return f"""  <section class="pagina-hero">
    <div class="container">
      {imgtag}
      <p class="eyebrow reveal">{eyebrow}</p>
      <h1 class="reveal">{h1}</h1>
      <p class="lead text-moale reveal">{lead}</p>
    </div>
  </section>"""

def cta(text, href, eticheta, secundar=None):
    b2 = f'<a href="{secundar[1]}" class="buton buton-linie">{secundar[0]}</a>' if secundar else ""
    return f"""  <section class="sectiune final">
    <div class="container">
      <h2 class="reveal semnatura">{text}</h2>
      <div class="reveal" style="margin-top:2rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="{href}" class="buton buton-auriu">{eticheta}</a>
        {b2}
      </div>
    </div>
  </section>"""

def lista(items, nu=False):
    cls = "lista-aurie lista-nu" if nu else "lista-aurie"
    lis = "\n        ".join(f"<li>{i}</li>" for i in items)
    return f'<ul class="{cls}">\n        {lis}\n      </ul>'


# ═════════════════════════════════════════════════════════════════════
# 1 · ÎNCEPE AICI
lumi = [
    ("planeta-inceput.png", "#10B981", "Sunt la început",
     "Pentru cine simte că există și o altă cale, dar nu știe de unde să înceapă.", "incepe-aici.html"),
    ("planeta-marketing.png", "#D4AF37", "Marketing Digital",
     "Învață să construiești, să vinzi și să te poziționezi online.", "marketing-digital.html"),
    ("planeta-ai.png", "#8B5CF6", "AI Creativ & Productivitate",
     "AI din joacă în instrument real: timp, claritate, conținut.", "ai-creativ.html"),
    ("planeta-business.png", "#3B82F6", "Am deja un business",
     "Ai deja ceva și vrei un sistem mai clar care să lucreze pentru tine.", "am-un-business.html"),
    ("planeta-mir.png", "#E8C558", "Academia MIR",
     "Ecosistemul premium: educație, comunitate, strategie. Totul într-un singur loc.", "academia-mir.html"),
    ("planeta-mentorat.png", "#F5F3EE", "Mentorat 1:1",
     "Claritate, audit, direcție și un plan personalizat, doar pentru tine.", "mentorat.html"),
]
carduri = "\n".join(f"""        <a class="pas lume reveal" href="{href}" style="--culoare:{cul};">
          <img src="../../assets/planete/{img}" alt="{nume}" loading="lazy">
          <h3>{nume}</h3>
          <p>{desc}</p>
          <span class="card-cta">Explorează →</span>
        </a>""" for img, cul, nume, desc, href in lumi)

body = hero(None, "Începe aici",
            "Unde te afli astăzi în călătoria ta?",
            "Nu contează cât de departe pare drumul. Contează doar următorul pas. "
            "Alege lumea în care te regăsești acum — restul vine pe rând.", "#D4AF37") + f"""
  <section class="sectiune">
    <div class="container">
      <div class="grila lumi">
{carduri}
      </div>
      <p class="lead text-moale reveal" style="text-align:center;margin:3rem auto 0;max-width:44ch;">
        Nu construim doar afaceri digitale. Construim oameni capabili să își
        construiască propriul viitor.
      </p>
    </div>
  </section>
""" + cta("Există și o altă cale.", "academia-mir.html", "Descoperă Academia MIR",
          ("Vorbește cu noi", "contact.html"))
pagina("incepe-aici.html", "Începe aici", "Unde te afli astăzi în călătoria ta? Alege lumea în care te regăsești.",
       "#D4AF37", "Începe aici", body)


# ═════════════════════════════════════════════════════════════════════
# 2 · ACADEMIA MIR
body = hero("../../assets/planete/planeta-mir.png", "Nucleul premium al ecosistemului",
            "Academia MIR", "Ecosistemul premium: educație, comunitate, strategie. "
            "Totul într-un singur loc.", "#E8C558") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="reveal">
        <p class="eyebrow">Ce este</p>
        <h2>Un loc unde înveți, construiești și nu ești singur.</h2>
        <p class="lead text-moale">Academia MIR nu e un curs pe care îl termini și îl uiți.
        E un ecosistem viu: educație structurată, o comunitate reală și strategie
        aplicată — puse la un loc, ca să ai unde crește pas cu pas.</p>
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Ce include</p>
        {lista([
          "Educație structurată: marketing, AI, poziționare, vânzare.",
          "Comunitate activă — 700+ membri pe același drum.",
          "Strategie și direcție clară, actualizată constant.",
          "Sesiuni, resurse și pași aplicabili imediat.",
        ])}
      </div>
    </div>
  </section>

  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="panou reveal">
        <p class="eyebrow">Pentru cine</p>
        {lista([
          "Ești la început și vrei o cale clară, nu zece drumuri.",
          "Ai deja un business și vrei un sistem care lucrează pentru tine.",
          "Vrei să folosești AI-ul ca instrument real, nu ca joacă.",
          "Cauți oameni serioși alături de care să crești.",
        ])}
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Ce NU este</p>
        {lista([
          "Nu e o promisiune de îmbogățire peste noapte.",
          "Nu e conținut generic pe care îl găsești oriunde.",
          "Nu te face dependent — te învață să fii liber.",
          "Nu e zgomot. Profunzimea bate zgomotul.",
        ], nu=True)}
      </div>
    </div>
  </section>

  <section class="mir">
    <div class="container">
      <p class="eyebrow reveal">Accesul în ecosistem</p>
      <div class="pret reveal">597€ <small>acces la Academia MIR</small></div>
      <p class="reveal semnatura" style="max-width:46ch;margin:1.4rem auto 0;font-size:1.1rem;">
        Universul GEO îți arată că există și o altă cale. Academia MIR te ajută să o construiești.
      </p>
    </div>
  </section>

  <section class="sectiune sectiune-centrata">
    <div class="container" style="max-width:640px;">
      <p class="eyebrow reveal">Apel de claritate</p>
      <h2 class="reveal">Nu ești sigur dacă e pentru tine?</h2>
      <p class="lead text-moale reveal" style="margin-inline:auto;">Lasă-ne câteva detalii.
      Îți răspundem cu un pas concret — chiar dacă nu e MIR.</p>
      <form class="formular reveal" onsubmit="return false;">
        <input type="text" placeholder="Numele tău" required>
        <input type="email" placeholder="Email" required>
        <textarea placeholder="Unde te afli acum și ce ți-ai dori?"></textarea>
        <button type="submit" class="buton buton-auriu" style="justify-content:center;">Cere un apel de claritate</button>
      </form>
    </div>
  </section>
"""
pagina("academia-mir.html", "Academia MIR", "Ecosistemul premium: educație, comunitate, strategie. 597€.",
       "#E8C558", "Academia MIR", body)


# ═════════════════════════════════════════════════════════════════════
# 3 · MARKETING DIGITAL
body = hero("../../assets/planete/planeta-marketing.png", "Marketing Digital Antreprenorial",
            "Construiește, vinde, poziționează-te.",
            "Învață să construiești, să vinzi și să te poziționezi online — cu strategie, "
            "nu cu noroc.", "#D4AF37") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="reveal">
        <p class="eyebrow">Ce este</p>
        <h2>Marketingul ca sistem, nu ca hazard.</h2>
        <p class="lead text-moale">Nu trucuri de moment, ci fundamentele care rămân:
        cum te poziționezi, cum comunici valoarea, cum transformi vizibilitatea în
        clienți și clienții în comunitate.</p>
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Ce include</p>
        {lista([
          "Poziționare clară: cine ești și pentru cine.",
          "Conținut care atrage și construiește încredere.",
          "Funnel simplu, de la vizibilitate la vânzare.",
          "Măsurare: ce merge, ce oprești, ce dublezi.",
        ])}
      </div>
    </div>
  </section>
  <section class="sectiune sectiune-centrata">
    <div class="container">
      <p class="eyebrow reveal">Rezultatul</p>
      <h2 class="reveal">Un sistem de marketing pe care îl înțelegi și îl controlezi.</h2>
      <p class="lead text-moale reveal">Nu mai depinzi de „inspirație”. Ai un drum clar,
      repetabil, care lucrează și când tu te odihnești.</p>
    </div>
  </section>
""" + cta("Există și o altă cale.", "academia-mir.html", "Intră în Academia MIR",
          ("Începe aici", "incepe-aici.html"))
pagina("marketing-digital.html", "Marketing Digital", "Construiește, vinde și poziționează-te online cu strategie.",
       "#D4AF37", None, body)


# ═════════════════════════════════════════════════════════════════════
# 4 · AI CREATIV
body = hero("../../assets/planete/planeta-ai.png", "AI Creativ & Productivitate",
            "AI din joacă în instrument real.",
            "Timp, claritate, conținut. Transformă inteligența artificială dintr-o "
            "curiozitate într-un aliat de zi cu zi.", "#8B5CF6") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="reveal">
        <p class="eyebrow">Ce este</p>
        <h2>AI-ul care îți dă timp înapoi.</h2>
        <p class="lead text-moale">Nu despre a-ți înlocui vocea, ci despre a o amplifica.
        Înveți să folosești AI-ul ca să gândești mai clar, să creezi mai repede și să
        scapi de munca repetitivă.</p>
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Ce include</p>
        {lista([
          "Fluxuri de lucru cu AI pentru conținut și idei.",
          "Prompturi și sisteme pe care le refolosești.",
          "Automatizări simple pentru sarcini repetitive.",
          "Claritate: ce merită automatizat și ce nu.",
        ])}
      </div>
    </div>
  </section>
  <section class="sectiune">
    <div class="container">
      <p class="eyebrow reveal" style="text-align:center;">Instrumente</p>
      <div class="grila">
        <div class="pas reveal"><h3>Scriere &amp; idei</h3><p>De la pagină albă la draft clar, în minute.</p></div>
        <div class="pas reveal"><h3>Imagine &amp; vizual</h3><p>Concepte vizuale coerente cu brandul tău.</p></div>
        <div class="pas reveal"><h3>Organizare</h3><p>Sisteme care îți țin mintea liberă.</p></div>
        <div class="pas reveal"><h3>Automatizare</h3><p>Sarcinile mici, făcute singure.</p></div>
      </div>
    </div>
  </section>
""" + cta("Există și o altă cale.", "academia-mir.html", "Intră în Academia MIR",
          ("Începe aici", "incepe-aici.html"))
pagina("ai-creativ.html", "AI Creativ", "AI din joacă în instrument real: timp, claritate, conținut.",
       "#8B5CF6", None, body)


# ═════════════════════════════════════════════════════════════════════
# 5 · AM DEJA UN BUSINESS
body = hero("../../assets/planete/planeta-business.png", "Am deja un business",
            "Ai construit ceva. Acum vrei un sistem.",
            "Ai deja ceva care funcționează — dar vrei un sistem mai clar, care să "
            "lucreze pentru tine, nu invers.", "#3B82F6") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="panou reveal">
        <p class="eyebrow">Problemele pe care le simți</p>
        {lista([
          "Faci totul singur și timpul nu-ți ajunge.",
          "Vinzi, dar fără un sistem repetabil în spate.",
          "Ai idei multe și direcție puțină.",
          "Crești, dar haotic — și te epuizează.",
        ], nu=True)}
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Ce construim împreună</p>
        {lista([
          "Un sistem clar de marketing și vânzare.",
          "Direcție strategică, prioritizată pe impact.",
          "Procese care nu depind doar de tine.",
          "O comunitate care te ține pe drum.",
        ])}
      </div>
    </div>
  </section>
  <section class="sectiune">
    <div class="container">
      <p class="eyebrow reveal" style="text-align:center;">Trei drumuri, în funcție de ce ai nevoie</p>
      <div class="grila">
        <a class="pas reveal" href="mentorat.html"><div class="nr">01</div><h3>Mentorat 1:1</h3><p>Audit, claritate și un plan doar pentru tine.</p><span class="card-cta">Vezi mentoratul →</span></a>
        <a class="pas reveal" href="marketing-digital.html"><div class="nr">02</div><h3>Strategie de marketing</h3><p>Sistemul care transformă vizibilitatea în clienți.</p><span class="card-cta">Vezi marketingul →</span></a>
        <a class="pas reveal" href="academia-mir.html"><div class="nr">03</div><h3>Academia MIR</h3><p>Ecosistemul complet: educație, comunitate, strategie.</p><span class="card-cta">Vezi Academia MIR →</span></a>
      </div>
    </div>
  </section>
""" + cta("Există și o altă cale.", "academia-mir.html", "Descoperă Academia MIR",
          ("Cere un apel", "contact.html"))
pagina("am-un-business.html", "Am deja un business", "Un sistem mai clar care să lucreze pentru tine.",
       "#3B82F6", None, body)


# ═════════════════════════════════════════════════════════════════════
# 6 · MENTORAT 1:1
body = hero("../../assets/planete/planeta-mentorat.png", "Mentorat 1:1",
            "Claritate, audit, direcție — doar pentru tine.",
            "Un spațiu în care privim împreună unde ești, unde vrei să ajungi și "
            "care e cel mai scurt drum onest între cele două.", "#F5F3EE") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="reveal">
        <p class="eyebrow">Ce primești</p>
        <h2>Un plan pe care îl poți urma luni de zile.</h2>
        <p class="lead text-moale">Nu sfaturi generale, ci direcție personalizată:
        pornim de la situația ta reală și construim un plan clar, cu priorități și
        pași concreți.</p>
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Include</p>
        {lista([
          "Audit onest al situației actuale.",
          "Claritate: ce contează acum și ce lași.",
          "Plan personalizat, cu pași concreți.",
          "Direcție pe care o poți urma singur după.",
        ])}
      </div>
    </div>
  </section>
  <section class="sectiune sectiune-centrata">
    <div class="container">
      <p class="eyebrow reveal">Cum funcționează</p>
      <div class="grila">
        <div class="pas reveal"><div class="nr">01</div><h3>Aplici</h3><p>Ne spui unde ești și ce ți-ai dori.</p></div>
        <div class="pas reveal"><div class="nr">02</div><h3>Ne vedem</h3><p>Facem auditul și conturăm direcția.</p></div>
        <div class="pas reveal"><div class="nr">03</div><h3>Construiești</h3><p>Pleci cu un plan clar și îl aplici.</p></div>
      </div>
      <p class="lead text-moale reveal" style="margin:2.5rem auto 0;max-width:40ch;">
        Mentoratul 1:1 se face prin aplicație — ca să lucrăm doar cu oameni potriviți,
        în număr mic. Prețul îl discutăm în funcție de nevoie.</p>
    </div>
  </section>
""" + cta("Există și o altă cale.", "contact.html", "Aplică pentru mentorat",
          ("Descoperă Academia MIR", "academia-mir.html"))
pagina("mentorat.html", "Mentorat 1:1", "Claritate, audit, direcție și un plan personalizat, doar pentru tine.",
       "#F5F3EE", None, body)


# ═════════════════════════════════════════════════════════════════════
# 7 · DESPRE GEORGIANA (folosește nucleu.png)
body = f"""  <section class="pagina-hero">
    <div class="container">
      <div class="nucleu" style="position:static;display:inline-flex;margin-bottom:2rem;">
        <div class="nucleu-aura"></div>
        <div class="nucleu-orb">
          <img src="../../assets/nucleu.png" alt="Iordache Georgiana">
        </div>
      </div>
      <p class="eyebrow reveal">Despre Georgiana</p>
      <h1 class="reveal">Omul din centrul universului GEO.</h1>
      <p class="lead text-moale reveal">Nu un brand rece, ci un om care a ales altă cale
      — și acum arată drumul și altora.</p>
    </div>
  </section>

  <section class="sectiune">
    <div class="container" style="max-width:760px;">
      <p class="eyebrow reveal">Povestea</p>
      <h2 class="reveal">A existat mereu o altă cale. Doar că nu o vedea nimeni.</h2>
      <p class="lead text-moale reveal">Ca mulți dintre noi, Georgiana a pornit dintr-un
      loc în care „așa se face” părea singura variantă. Tranziția n-a venit dintr-un
      moment magic, ci dintr-o serie de alegeri: să învețe, să construiască, să nu se
      oprească atunci când era mai ușor să renunțe.</p>
      <p class="lead text-moale reveal" style="margin-top:1.2rem;">Din drumul acela s-a
      născut Universul GEO — un loc unde educația, comunitatea și strategia stau la un
      loc, ca nimeni să nu mai fie nevoit să pornească singur, pe întuneric.</p>
    </div>
  </section>

  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="panou reveal">
        <p class="eyebrow">De ce există Universul GEO</p>
        {lista([
          "Ca „altă cale” să nu mai fie doar o vorbă, ci un drum.",
          "Ca oamenii să înceapă cu claritate, nu cu confuzie.",
          "Ca succesul să însemne libertate, nu dependență.",
        ])}
      </div>
      <div class="panou reveal">
        <p class="eyebrow">Autoritate &amp; comunitate</p>
        <div class="dovada" style="text-align:left;">
          <div class="cifra">700+</div>
          <div class="cifra-eticheta">membri în comunitatea MIR</div>
        </div>
        <p class="text-moale" style="margin-top:1rem;">Un ecosistem viu de oameni care
        construiesc altfel — cu răbdare și împreună.</p>
      </div>
    </div>
  </section>

  <section class="sectiune final">
    <div class="container">
      <h2 class="reveal semnatura">Nu construim doar afaceri digitale.<br>Construim oameni.</h2>
      <div class="reveal" style="margin-top:2rem;display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
        <a href="incepe-aici.html" class="buton buton-auriu">Începe aici</a>
        <a href="academia-mir.html" class="buton buton-linie">Descoperă Academia MIR</a>
      </div>
    </div>
  </section>
"""
pagina("despre.html", "Despre Georgiana", "Povestea din spatele universului GEO — de ce există și altă cale.",
       "#D4AF37", "Despre Georgiana", body)


# ═════════════════════════════════════════════════════════════════════
# 8 · BLOG / RESURSE
articole = [
    ("Marketing", "Poziționarea: de ce contează mai mult decât reclama",
     "Înainte să vinzi ceva, oamenii trebuie să înțeleagă cine ești. Fundamentul oricărui marketing sănătos."),
    ("AI", "AI-ul care îți dă timp înapoi, nu ți-l fură",
     "Trei fluxuri simple prin care inteligența artificială devine un aliat de zi cu zi."),
    ("Mindset", "Există și o altă cale — dar începe cu un singur pas",
     "De ce claritatea, nu motivația, e ceea ce te ține pe drum pe termen lung."),
    ("Business", "De la haos la sistem: primul lucru pe care să-l așezi",
     "Dacă faci totul singur, nu ai un business — ai un job foarte solicitant."),
]
carduri_blog = "\n".join(f"""        <a class="pas reveal" href="#">
          <p class="eyebrow">{cat}</p>
          <h3 style="margin-top:0.6rem;">{tit}</h3>
          <p>{rez}</p>
          <span class="card-cta">Citește →</span>
        </a>""" for cat, tit, rez in [(a[0], a[1], a[2]) for a in articole])
body = hero(None, "Resurse & Blog", "Idei care îți lasă mintea mai clară.",
            "Articole-pilon despre marketing, AI, business și drumul către altă cale. "
            "Fără zgomot — doar ce te ajută să faci următorul pas.", "#D4AF37") + f"""
  <section class="sectiune">
    <div class="container">
      <div class="grila">
{carduri_blog}
      </div>
    </div>
  </section>
  <section class="sectiune sectiune-centrata">
    <div class="container" style="max-width:600px;">
      <p class="eyebrow reveal">Newsletter</p>
      <h2 class="reveal">Primește ideile direct, când contează.</h2>
      <p class="lead text-moale reveal" style="margin-inline:auto;">Un email rar, dar care
      merită deschis. Fără spam, fără zgomot.</p>
      <form class="formular reveal" onsubmit="return false;" style="max-width:440px;margin-inline:auto;">
        <input type="email" placeholder="Emailul tău" required>
        <button type="submit" class="buton buton-auriu" style="justify-content:center;">Mă abonez</button>
      </form>
    </div>
  </section>
"""
pagina("blog.html", "Blog & Resurse", "Articole-pilon despre marketing, AI, business și drumul către altă cale.",
       "#D4AF37", "Blog", body)


# ═════════════════════════════════════════════════════════════════════
# 9 · CONTACT
body = hero(None, "Contact", "Hai să vorbim.",
            "Fie că știi exact ce vrei, fie că simți doar că trebuie să fie și altfel, "
            "scrie-ne. Îți răspundem cu un pas concret.", "#D4AF37") + f"""
  <section class="sectiune">
    <div class="container doua-coloane">
      <div class="reveal">
        <p class="eyebrow">Scrie-ne direct</p>
        <h2>Un mesaj scurt e de ajuns pentru început.</h2>
        <p class="lead text-moale">Spune-ne unde te afli acum și ce ți-ai dori. Nu trebuie
        să ai totul clar — de asta suntem aici.</p>
        <p style="margin-top:1.6rem;">
          <a href="mailto:contact@universulgeo.ro" class="semnatura" style="font-size:1.2rem;">contact@universulgeo.ro</a>
        </p>
        <nav class="footer-linkuri" style="justify-content:flex-start;margin-top:1.4rem;">
          <a href="#">Instagram</a><a href="#">Facebook</a><a href="#">YouTube</a><a href="#">TikTok</a>
        </nav>
      </div>
      <form class="panou formular reveal" onsubmit="return false;">
        <input type="text" placeholder="Numele tău" required>
        <input type="email" placeholder="Email" required>
        <input type="text" placeholder="Subiect (opțional)">
        <textarea placeholder="Mesajul tău"></textarea>
        <button type="submit" class="buton buton-auriu" style="justify-content:center;">Trimite mesajul</button>
      </form>
    </div>
  </section>
"""
pagina("contact.html", "Contact", "Scrie-ne — îți răspundem cu un pas concret.",
       "#D4AF37", "Contact", body)

print("GATA — toate paginile generate.")
