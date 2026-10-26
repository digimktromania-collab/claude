# Generates hf/funnel/index.html from work/words.json
import json, re, unicodedata, html, os
S = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{S}/work/words.json"))
# manual timing fixes for interpolated words
fix = {241: (78.05, 78.45), 242: (78.46, 78.85), 282: (91.58, 91.72), 283: (91.72, 91.86), 284: (91.86, 91.98), 285: (91.98, 92.06), 115: (37.97, 38.09)}
for i, (s, e) in fix.items():
    W[i]["s"], W[i]["e"] = s, e
DUR = 102.95
T = lambda i: W[i]["s"]

def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9-]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))

KEY = re.compile(r"^(funnel|funnel-ul|palnie|palnia|site|site-ul|ghidul|gratuit|e-mail|e-mail-ul|email-ul|reducere|zece|douazeci|suta|campanie|whatsapp|comunitatea|mir)$")

# ---------- caption groups ----------
groups, cur = [], []
for i, w in enumerate(W):
    if cur:
        prev = W[cur[-1]]
        chars = sum(len(W[k]["w"]) for k in cur) + len(w["w"])
        if len(cur) >= 3 or chars > 20 or w["s"] - prev["e"] > 0.3 or re.search(r"[.,!?]$", prev["w"]):
            groups.append(cur); cur = []
    cur.append(i)
groups.append(cur)

cap_html, cap_js = [], []
for g, idx in enumerate(groups):
    gs = max(0.1, W[idx[0]]["s"] - 0.08)
    ge = groups[g + 1] and W[groups[g + 1][0]]["s"] - 0.08 if g + 1 < len(groups) else DUR - 0.05
    ge = min(ge, W[idx[-1]]["e"] + 0.9)
    total = sum(len(W[k]["w"]) for k in idx)
    fs = 66 if total <= 16 else 58
    spans = []
    for k in idx:
        word = W[k]["w"]
        kw = bool(KEY.match(norm(word.strip(".,!?"))))
        spans.append(f'<span id="w{k}" class="w{" kw" if kw else ""}">{html.escape(word)}</span>')
        st = W[k]["s"]
        cap_js.append(f'tl.fromTo("#w{k}",{{opacity:0,y:18,scale:.82}},{{opacity:1,y:0,scale:1,duration:.16,ease:"back.out(2.2)"}},{max(gs, st - 0.04):.2f});')
        if not kw:
            cap_js.append(f'tl.to("#w{k}",{{color:"#D4AF37",duration:.06}},{st:.2f}).to("#w{k}",{{color:"#F5F3EE",duration:.12}},{max(st + 0.1, W[k]["e"]):.2f});')
    cap_html.append(f'<div id="g{g}" class="grp" style="font-size:{fs}px">{" ".join(spans)}</div>')
    cap_js.append(f'tl.set("#g{g}",{{visibility:"visible",opacity:1}},{gs:.2f});')
    cap_js.append(f'tl.to("#g{g}",{{opacity:0,duration:.1,ease:"power2.in"}},{ge - 0.1:.2f}).set("#g{g}",{{visibility:"hidden"}},{ge:.2f});')

# ---------- SVG library (gold/cream line art) ----------
G, C = "#D4AF37", "#F5F3EE"
def person(x, y, c=C, s=1):
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-14" r="9" fill="{c}"/><path d="M-15 14 Q0 -8 15 14 Z" fill="{c}"/></g>'
LAPTOP = f'''<svg viewBox="0 0 320 210" width="300"><rect x="45" y="12" width="230" height="148" rx="12" fill="#141414" stroke="{C}" stroke-width="6"/>
<rect x="62" y="30" width="196" height="16" rx="5" fill="{G}" opacity=".9"/><rect x="62" y="58" width="90" height="72" rx="8" fill="none" stroke="{G}" stroke-width="4"/>
<rect x="165" y="60" width="92" height="9" rx="4" fill="{C}" opacity=".7"/><rect x="165" y="78" width="70" height="9" rx="4" fill="{C}" opacity=".5"/><rect x="165" y="110" width="66" height="20" rx="10" fill="{G}"/>
<path d="M18 172 H302 L285 196 H35 Z" fill="{C}"/></svg>'''
FUNNEL_ICON = f'<svg viewBox="0 0 200 200" width="170"><path d="M20 30 H180 L118 105 V170 L82 186 V105 Z" fill="none" stroke="{G}" stroke-width="9" stroke-linejoin="round"/><path d="M45 55 H155" stroke="{C}" stroke-width="6" opacity=".6"/></svg>'
BOTTLES = f'''<svg viewBox="0 0 320 220" width="300">
<g class="b1"><rect x="40" y="70" width="70" height="140" rx="16" fill="#1b1b1b" stroke="{C}" stroke-width="5"/><rect x="58" y="40" width="34" height="32" rx="6" fill="{G}"/><rect x="52" y="120" width="46" height="40" rx="6" fill="{G}" opacity=".85"/></g>
<g class="b2"><rect x="125" y="40" width="74" height="170" rx="20" fill="#1b1b1b" stroke="{G}" stroke-width="5"/><path d="M147 40 V18 H178 V40" fill="none" stroke="{G}" stroke-width="5"/><path d="M178 22 H200" stroke="{G}" stroke-width="5"/><circle cx="162" cy="125" r="22" fill="none" stroke="{C}" stroke-width="5"/></g>
<g class="b3"><rect x="215" y="105" width="80" height="105" rx="14" fill="#1b1b1b" stroke="{C}" stroke-width="5"/><rect x="210" y="88" width="90" height="22" rx="8" fill="{G}"/><path d="M232 160 H278" stroke="{G}" stroke-width="5"/></g></svg>'''
PHONE_PROFILE = f'''<svg viewBox="0 0 220 300" width="210"><rect x="20" y="6" width="180" height="288" rx="28" fill="#121212" stroke="{C}" stroke-width="6"/>
<circle cx="110" cy="80" r="36" fill="none" stroke="{G}" stroke-width="6"/>{person(110, 86, C, 1.2)}
<rect x="62" y="128" width="96" height="10" rx="5" fill="{C}" opacity=".7"/><rect x="74" y="148" width="72" height="8" rx="4" fill="{C}" opacity=".4"/>
<g class="bio"><rect x="46" y="172" width="128" height="34" rx="17" fill="{G}"/><text x="110" y="195" text-anchor="middle" font-family="Mont" font-weight="800" font-size="16" fill="#080808">🔗 LINK</text></g>
<g opacity=".5"><rect x="36" y="222" width="46" height="60" rx="6" fill="{C}" opacity=".3"/><rect x="88" y="222" width="46" height="60" rx="6" fill="{C}" opacity=".3"/><rect x="140" y="222" width="46" height="60" rx="6" fill="{C}" opacity=".3"/></g></svg>'''
PLAY = f'''<svg viewBox="0 0 220 300" width="200"><rect x="20" y="6" width="180" height="288" rx="28" fill="#121212" stroke="{C}" stroke-width="6"/>
<circle class="pl" cx="110" cy="140" r="46" fill="{G}"/><path d="M98 118 L132 140 L98 162 Z" fill="#080808"/>
<rect x="44" y="236" width="132" height="8" rx="4" fill="{C}" opacity=".35"/><rect class="prog" x="44" y="236" width="132" height="8" rx="4" fill="{G}"/></svg>'''
CURLS = f'''<svg viewBox="0 0 300 220" width="290">{''.join(f'<path class="curl" d="M{x} 10 c 34 10 34 30 0 40 c -34 10 -34 30 0 40 c 34 10 34 30 0 40 c -34 10 -34 30 0 40 c 34 10 34 30 0 40" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>' for x, c in [(60, G), (120, C), (180, G), (240, C)])}</svg>'''
HAIR = f'''<svg viewBox="0 0 300 220" width="290">{''.join(f'<path class="strand" d="M{x} 10 C {x-20} 80 {x+25} 140 {x-5} 210" fill="none" stroke="{c}" stroke-width="7" stroke-linecap="round"/>' for x, c in [(70, C), (110, G), (150, C), (190, G), (230, C)])}
<g class="spark" fill="{G}"><path d="M262 40 l6 16 16 6 -16 6 -6 16 -6 -16 -16 -6 16 -6z"/><path d="M40 150 l4 11 11 4 -11 4 -4 11 -4 -11 -11 -4 11 -4z"/></g></svg>'''
PDF = f'''<svg viewBox="0 0 240 260" width="210"><path d="M40 10 H160 L210 60 V250 H40 Z" fill="#141414" stroke="{C}" stroke-width="6" stroke-linejoin="round"/><path d="M160 10 V60 H210" fill="none" stroke="{C}" stroke-width="6"/>
<rect x="62" y="40" width="70" height="30" rx="6" fill="{G}"/><text x="97" y="62" text-anchor="middle" font-family="Mont" font-weight="900" font-size="20" fill="#080808">PDF</text>
<rect x="62" y="92" width="126" height="9" rx="4" fill="{C}" opacity=".6"/><rect x="62" y="112" width="100" height="9" rx="4" fill="{C}" opacity=".4"/><rect x="62" y="132" width="116" height="9" rx="4" fill="{C}" opacity=".4"/>
<g class="dl"><circle cx="125" cy="200" r="30" fill="{G}"/><path d="M125 184 V214 M112 202 L125 215 L138 202" stroke="#080808" stroke-width="6" fill="none" stroke-linecap="round"/></g>
<g class="tag" opacity="0"><path d="M150 150 H222 L236 172 L222 194 H150 Z" fill="{G}"/><text x="190" y="180" text-anchor="middle" font-family="Mont" font-weight="900" font-size="20" fill="#080808">OFERTĂ</text></g></svg>'''
MAIL = f'<svg viewBox="0 0 120 90" width="120"><rect x="6" y="6" width="108" height="78" rx="12" fill="#141414" stroke="{G}" stroke-width="6"/><path d="M10 12 L60 52 L110 12" fill="none" stroke="{G}" stroke-width="6"/></svg>'
WA = f'<svg viewBox="0 0 110 110" width="110"><path d="M55 8 a46 46 0 1 1 -24 85 l-22 8 8 -21 a46 46 0 0 1 38 -72z" fill="#25D366"/><path d="M40 34 c-4 6 -2 16 8 26 10 10 20 13 26 8 l4 -6 -10 -6 -5 5 c-5 -2 -11 -8 -13 -13 l5 -5 -6 -10z" fill="#fff"/></svg>'
CART = f'<svg viewBox="0 0 120 100" width="110"><path d="M8 14 H26 L40 66 H96 L108 30 H32" fill="none" stroke="{G}" stroke-width="8" stroke-linejoin="round" stroke-linecap="round"/><circle cx="46" cy="84" r="8" fill="{G}"/><circle cx="90" cy="84" r="8" fill="{G}"/></svg>'
CLOCK = f'<svg viewBox="0 0 100 100" width="84"><circle cx="50" cy="50" r="40" fill="#141414" stroke="{C}" stroke-width="7"/><path class="hand" d="M50 50 V22" stroke="{G}" stroke-width="7" stroke-linecap="round"/><path d="M50 50 H70" stroke="{C}" stroke-width="7" stroke-linecap="round"/></svg>'
COMMUNITY = f'''<svg viewBox="0 0 300 240" width="290"><g stroke="{G}" stroke-width="3" opacity=".7" class="links">
{''.join(f'<line x1="150" y1="120" x2="{150+95*__import__("math").cos(a*1.0472):.0f}" y2="{120+95*__import__("math").sin(a*1.0472):.0f}"/>' for a in range(6))}</g>
{person(150, 128, G, 1.5)}{''.join(f'<g class="cp">{person(150+95*__import__("math").cos(a*1.0472), 128+95*__import__("math").sin(a*1.0472), C, 1.1)}</g>' for a in range(6))}</svg>'''

def form(pref, btn):
    return f'''<div class="form"><div class="fld"><span class="lbl">E-mail</span><span class="val" id="{pref}e">ana@exemplu.ro</span></div>
<div class="fld"><span class="lbl">Telefon</span><span class="val" id="{pref}p">07xx xxx xxx</span></div><div class="btn" id="{pref}b">{btn}</div></div>'''

# ---------- cards (right column) ----------
cards = []  # (id, start, end, inner_html, extra_js)
def card(cid, s, e, eyebrow, title, body, js=""):
    cards.append((cid, s, e, f'<div class="eb">{eyebrow}</div><div class="ttl">{title}</div><div class="art">{body}</div>', js))

card("c0", 0, 3.95, "Antreprenor?", 'Ai un <b>site</b>.', f'<div id="c0lap">{LAPTOP}</div>',
     f'tl.fromTo("#c0lap",{{opacity:0,y:30}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{T(4)-.1});')
card("c1", 4.1, 5.95, "Funnel", 'așa-zisa <b>pâlnie</b>', f'<div id="c1f">{FUNNEL_ICON}</div>',
     f'tl.fromTo("#c1f",{{scale:.4,rotation:-12,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.5,ease:"back.out(2)"}},{T(14)});')
card("c2", 6.85, 11.75, "Ca de obicei", 'Explicat <b>simplu</b>', f'<div class="big-q" id="c2q">1·2·3</div>',
     f'tl.fromTo("#c2q",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.45,ease:"back.out(2)"}},{T(26)});')
# website story card
c3 = f'''<div class="stage" id="c3st">{LAPTOP}
<div class="ppl" id="c3ppl"><svg viewBox="0 0 300 60" width="300">{person(40,40,G)}{person(90,40,G)}{person(140,40,G)}</svg></div>
<div class="badge red" id="c3x">✕ nu cumpără</div>
<div class="qm" id="c3q1">?</div><div class="qm" id="c3q2">?</div>
<div class="clock" id="c3c">{CLOCK}</div></div>'''
card("c3", 12.8, 21.9, "Exemplu", 'Vizitatori pe <b>site</b>', c3,
     f'''tl.fromTo("#c3ppl",{{x:-220,opacity:0}},{{x:0,opacity:1,duration:.9,ease:"power2.out"}},{T(44)});
tl.fromTo("#c3x",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2.5)"}},{T(48)});
tl.to("#c3x",{{opacity:0,duration:.2}},{T(55)-.2});
tl.fromTo("#c3q1",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(3)"}},{T(55)});
tl.fromTo("#c3q2",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(3)"}},{T(58)});
tl.to(["#c3q1","#c3q2"],{{opacity:0,duration:.2}},{T(60)-.2});
tl.fromTo("#c3c",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.35,ease:"back.out(2.5)"}},{T(62)});
tl.fromTo("#c3c .hand",{{rotation:0}},{{rotation:300,svgOrigin:"50 50",duration:1.4,ease:"none"}},{T(62)});''')
card("c4", 31.35, 35.1, "Exemplu", 'Produse pentru <b>păr</b>', f'<div id="c4b">{BOTTLES}</div>',
     f'tl.fromTo(["#c4b .b1","#c4b .b2","#c4b .b3"],{{y:60,opacity:0}},{{y:0,opacity:1,stagger:.15,duration:.45,ease:"back.out(1.8)"}},{T(101)});')
card("c5", 35.2, 39.2, "Social media", 'Sub poza de <b>profil</b>', f'<div id="c5p">{PHONE_PROFILE}</div>',
     f'tl.fromTo("#c5p .bio",{{scale:.6,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,duration:.4,ease:"back.out(3)"}},{T(116)});tl.to("#c5p .bio",{{scale:1.12,duration:.25,yoyo:true,repeat:3,transformOrigin:"50% 50%"}},{T(116)+.45});')
card("c6", 39.3, 43.75, "Pasul 1", 'Un <b>video</b> simplu', f'<div id="c6p">{PLAY}</div>',
     f'tl.fromTo("#c6p .pl",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.4,ease:"back.out(3)"}},{T(123)});tl.fromTo("#c6p .prog",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,duration:4,ease:"none"}},{T(123)});')
card("c7", 43.8, 46.95, "Ex. de conținut", '<b>Bucle</b> definite', f'<div id="c7c">{CURLS}</div>',
     f'tl.fromTo("#c7c .curl",{{opacity:0,y:20}},{{opacity:1,y:0,stagger:.12,duration:.5,ease:"power2.out"}},{T(134)-.1});')
card("c8", 47.0, 50.3, "Sau", 'Păr <b>fresh</b>, mai mult timp', f'<div id="c8h">{HAIR}</div>',
     f'tl.fromTo("#c8h .strand",{{opacity:0,y:-20}},{{opacity:1,y:0,stagger:.08,duration:.4}},{T(142)-.1});tl.fromTo("#c8h .spark",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.4,ease:"back.out(3)"}},{T(147)});')
card("c9", 50.35, 53.55, "Rețeta", '<b>3 pași</b> simpli', '<div class="steps"><div class="st" id="s1">1</div><div class="st" id="s2">2</div><div class="st" id="s3">3</div></div>',
     f'tl.fromTo(["#s1","#s2","#s3"],{{scale:0,opacity:0}},{{scale:1,opacity:1,stagger:.18,duration:.4,ease:"back.out(2.5)"}},{T(152)});')
card("c10", 53.6, 55.2, "Call to action", 'Descarcă <b>ghidul gratuit</b>', f'<div id="c10p">{PDF}</div>',
     f'tl.fromTo("#c10p .dl",{{y:-20,opacity:0}},{{y:0,opacity:1,duration:.35,ease:"bounce.out"}},{T(163)});')
card("c11", 55.25, 58.85, "Lead", 'Își lasă <b>datele</b>', form("f1", "Descarcă ghidul ↓"),
     f'''tl.fromTo("#f1e",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.6,ease:"steps(14)"}},{T(169)-.2});
tl.fromTo("#f1p",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.6,ease:"steps(12)"}},{T(170)});
tl.fromTo("#f1b",{{scale:1}},{{scale:.92,duration:.12,yoyo:true,repeat:1}},{T(173)});''')
card("c12", 58.9, 61.3, "În ghid", '<b>Oferte</b> cu produsele tale', f'<div id="c12p">{PDF}</div>',
     f'tl.fromTo("#c12p .tag",{{opacity:0,x:30}},{{opacity:1,x:0,duration:.4,ease:"back.out(2)"}},{T(179)});')
card("c13", 61.3, 68.15, "Varianta 2", 'Video cu tine sau <b>produsul</b>', f'<div class="row2"><div id="c13p">{PLAY}</div></div>',
     f'tl.fromTo("#c13p .pl",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.4,ease:"back.out(3)"}},{T(195)});tl.fromTo("#c13p .prog",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,duration:5,ease:"none"}},{T(195)});')
card("c14", 68.2, 71.9, "Prima comandă", '<b>Reducere</b>', '<div class="disc"><div class="pct" id="p10">-10%</div><div class="pct" id="p20">-20%</div></div>',
     f'''tl.fromTo("#p10",{{scale:0,rotation:-20}},{{scale:1,rotation:-6,duration:.45,ease:"back.out(2.5)"}},{T(213)-.05});
tl.fromTo("#p20",{{scale:0,rotation:20}},{{scale:1,rotation:6,duration:.45,ease:"back.out(2.5)"}},{T(214)});''')
card("c15", 71.95, 75.8, "Înregistrare", 'E-mail + <b>telefon</b>', form("f2", "Vreau reducerea"),
     f'''tl.fromTo("#f2e",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.6,ease:"steps(14)"}},{T(227)-.1});
tl.fromTo("#f2p",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.6,ease:"steps(12)"}},{T(229)});''')
card("c16", 90.35, 93.0, "Acum e rândul tău", 'Pune-l în <b>practică</b> ✓', '<div class="big-q" id="c16k">✓</div>',
     f'tl.fromTo("#c16k",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:.5,ease:"back.out(3)"}},{T(286)-.1});')
card("c17", 93.05, 96.3, "Te aștept", 'Să fii…', '<div class="chips"><div class="chip" id="k1">digital</div><div class="chip" id="k2">geo</div><div class="chip" id="k3">deșteaptă</div></div>',
     f'tl.fromTo("#k1",{{x:60,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"back.out(2)"}},{T(295)});tl.fromTo("#k2",{{x:60,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"back.out(2)"}},{T(298)});tl.fromTo("#k3",{{x:60,opacity:0}},{{x:0,opacity:1,duration:.3,ease:"back.out(2)"}},{T(301)});')
card("c18", 96.35, 100.6, "Alătură-te", 'Comunitatea <b>MIR</b>', f'<div id="c18c">{COMMUNITY}</div><div class="motto" id="c18m">Deșteaptă-te, române!</div>',
     f'''tl.fromTo("#c18c .cp",{{scale:0,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,stagger:.12,duration:.35,ease:"back.out(2)"}},{T(307)});
tl.fromTo("#c18c .links line",{{opacity:0}},{{opacity:1,stagger:.12,duration:.3}},{T(307)+.2});
tl.fromTo("#c18m",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{T(310)-.1});''')
card("c19", 100.65, DUR, "Link", 'Sub poza mea de <b>profil</b> ↑', f'<div id="c19p">{PHONE_PROFILE}</div>',
     f'tl.to("#c19p .bio",{{scale:1.12,duration:.3,yoyo:true,repeat:2,transformOrigin:"50% 50%"}},{T(316)});')

# ---------- split-screen panels ----------
def tier(i, label, sub):
    return f'<div class="tier" id="t{i}"><div class="tn">{i}</div><div><div class="tl">{label}</div><div class="ts">{sub}</div></div></div>'
FUNNEL_BIG = f'''<svg viewBox="0 0 380 560" width="300" id="fbig">
<path d="M20 70 H360 L232 300 V470 L148 510 V300 Z" fill="rgba(212,175,55,.08)" stroke="{G}" stroke-width="7" stroke-linejoin="round"/>
<path d="M70 120 H310" stroke="{C}" stroke-width="3" opacity=".35"/><path d="M118 200 H262" stroke="{C}" stroke-width="3" opacity=".35"/>
{''.join(f'<g class="fp" id="fp{k}">{person(60+k*52, 30, C, 1.5)}</g>' for k in range(6))}
<g id="fout" opacity="0">{person(190, 535, G, 1.6)}</g></svg>'''
split1 = f'''<div class="eb">Aici intervine</div><div class="ttl">Funnel-ul</div>
<div class="fwrap">{FUNNEL_BIG}<div class="flabel top">vizitatori</div><div class="flabel bot" id="fbl">clienți ✓</div></div>
<div class="reasons"><div class="rs" id="r1"><span>↺</span> un motiv să revină</div><div class="rs" id="r2">{CART}<span>un motiv să cumpere</span></div></div>'''
split1_js = "".join(
    f'tl.fromTo("#fp{k}",{{y:0,x:0,opacity:1}},{{y:{230 + (k % 2) * 30},x:{(190 - (60 + k * 52)) * 0.85:.0f},opacity:{1 if k in (2, 3) else 0},duration:1.2,ease:"power2.in"}},{22.9 + k * 0.18:.2f});'
    for k in range(6)) + f'''
tl.fromTo("#fout",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.5,ease:"back.out(2)"}},24.3);
tl.fromTo("#fbl",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.4}},24.4);
tl.fromTo("#r1",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{T(76)-.1});
tl.fromTo("#r2",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{T(85)-.1});
tl.to(["#r1","#r2"],{{opacity:0,duration:.25}},{T(91)-.3});
tl.fromTo("#x1",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.5)"}},{T(91)});'''
split1 += '<div class="exchip" id="x1">→ un exemplu</div>'

split2 = f'''<div class="eb">Și iată</div><div class="ttl">Campania</div>
<div class="camp"><div id="m1">{MAIL}<span>E-mail</span></div><div id="m2">{WA}<span>WhatsApp</span></div></div>
<div class="back" id="bk">{CART}<span>revin pe site<br>și <b>cumpără</b></span></div>
<div class="recap" id="rc"><div class="eb">Asta e pâlnia</div>
{tier(1, "Conținut", "video simplu, util")}{tier(2, "Magnet", "ghid gratuit / -10–20%")}{tier(3, "Contact", "e-mail + telefon")}{tier(4, "Campanie", "e-mail / WhatsApp")}{tier(5, "Vânzare", "clientul revine ✓")}</div>'''
split2_js = f'''tl.fromTo("#m1",{{opacity:0,y:40,scale:.7}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2.2)"}},{T(239)});
tl.fromTo("#m2",{{opacity:0,y:40,scale:.7}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2.2)"}},{T(246)});
tl.fromTo("#bk",{{opacity:0,x:60}},{{opacity:1,x:0,duration:.45,ease:"power3.out"}},{T(253)});
tl.to(["#m1","#m2","#bk"],{{opacity:0,y:-30,duration:.3,ease:"power2.in"}},{T(264)-.35});
tl.fromTo("#s2t",{{opacity:1}},{{opacity:0,duration:.25}},{T(264)-.35});
tl.fromTo("#rc",{{opacity:0}},{{opacity:1,duration:.2}},{T(264)-.05});
''' + "".join(f'tl.fromTo("#t{i}",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(264) + (i - 1) * 0.55:.2f});' for i in range(1, 6))
split2 = split2.replace('<div class="eb">Și iată</div><div class="ttl">Campania</div>', '<div id="s2t"><div class="eb">Și iată</div><div class="ttl">Campania</div></div>')

splits = [("sp1", 21.85, 31.3, split1, split1_js), ("sp2", 75.8, 90.3, split2, split2_js)]

# ---------- assemble ----------
cards_html, js = [], []
for cid, s, e, inner, extra in cards:
    cards_html.append(f'<div id="{cid}" class="clip slot" data-start="{s:.2f}" data-duration="{e - s:.2f}" data-track-index="2"><div class="card" id="{cid}i">{inner}</div></div>')
    if s > 0:
        js.append(f'tl.fromTo("#{cid}i",{{x:90,opacity:0,scale:.96}},{{x:0,opacity:1,scale:1,duration:.45,ease:"power3.out"}},{s:.2f});')
    js.append(f'tl.to("#{cid}i",{{y:-40,opacity:0,duration:.3,ease:"power2.in"}},{e - 0.32:.2f});')
    js.append(extra)
for sid, s, e, inner, extra in splits:
    cards_html.append(f'<div id="{sid}" class="clip split" data-start="{s:.2f}" data-duration="{e - s:.2f}" data-track-index="3" data-layout-allow-overflow><div class="wipe" id="{sid}w"></div><div class="panel" id="{sid}i">{inner}</div></div>')
    # enter: gold bar sweeps in, panel slides behind it; video shifts left
    js.append(f'''tl.fromTo("#{sid}w",{{x:470}},{{x:-30,duration:.45,ease:"power3.inOut"}},{s:.2f});
tl.fromTo("#{sid}i",{{clipPath:"inset(0 0 0 100%)"}},{{clipPath:"inset(0 0 0 0%)",duration:.45,ease:"power3.inOut"}},{s:.2f});
tl.to("#vwrap",{{x:-60,duration:.5,ease:"power3.inOut"}},{s:.2f});
tl.to("#{sid}w",{{opacity:0,duration:.2}},{s + 0.5:.2f});
tl.to("#{sid}i",{{clipPath:"inset(0 100% 0 0)",duration:.4,ease:"power3.inOut"}},{e - 0.42:.2f});
tl.to("#vwrap",{{x:0,duration:.45,ease:"power3.inOut"}},{e - 0.42:.2f});''')
    js.append(extra)

# punch-ins / zooms on the footage (origin near the face)
_z = [(0, 5.9, 1.0, 1.06), (T(66) - 0.05, None, 1.0, 1.0), (T(105), 39.2, 1.0, 1.07), (T(211), 71.9, 1.0, 1.08), (T(290), DUR, 1.0, 1.06)]
js.append('tl.fromTo("#vwrap",{scale:1},{scale:1.06,duration:5.6,ease:"sine.inOut"},0);tl.to("#vwrap",{scale:1,duration:.4,ease:"power2.out"},5.95);')
js.append(f'tl.to("#vwrap",{{scale:1.1,duration:.25,ease:"power3.out"}},{T(17)-.05}).to("#vwrap",{{scale:1,duration:.5,ease:"power2.inOut"}},{T(17)+.5});')
js.append(f'tl.to("#vwrap",{{scale:1.07,duration:3.6,ease:"sine.inOut"}},{T(105)}).to("#vwrap",{{scale:1,duration:.4}},39.2);')
js.append(f'tl.to("#vwrap",{{scale:1.12,duration:.2,ease:"power3.out"}},{T(211)-.05}).to("#vwrap",{{scale:1,duration:.6,ease:"power2.inOut"}},{T(214)+.3});')
js.append(f'tl.to("#vwrap",{{scale:1.08,duration:6,ease:"sine.inOut"}},{T(290)});')

fonts = []
for fam, base, weights, styles in [("Mont", "montserrat", [500, 700, 800, 900], ["normal"]), ("Play", "playfair-display", [600, 700], ["normal", "italic"])]:
    for w in weights:
        for st in styles:
            for sub, rng in [("latin-ext", "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"), ("latin", "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD")]:
                fonts.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};src:url('assets/fonts/{base}-{sub}-{w}-{st}.woff2') format('woff2');unicode-range:{rng};}}")

page = f'''<!doctype html>
<html lang="ro" data-resolution="portrait">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="assets/gsap.min.js"></script>
<style>
{chr(10).join(fonts)}
:root {{ --black:#080808; --gold:#D4AF37; --cream:#F5F3EE; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:var(--black); }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Mont'; color:var(--cream); }}
#bg {{ position:absolute; inset:0; background:var(--black); }}
#vwrap {{ position:absolute; inset:0; transform-origin:300px 520px; }}
#vid {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
#shade {{ position:absolute; left:0; right:0; bottom:0; height:900px; background:linear-gradient(to bottom, rgba(8,8,8,0), rgba(8,8,8,.55) 55%, rgba(8,8,8,.75)); }}
.slot {{ position:absolute; left:664px; top:240px; width:384px; z-index:10; }}
.card {{ background:rgba(8,8,8,.74); border:1.5px solid rgba(212,175,55,.6); border-radius:30px; padding:26px 24px 24px; box-shadow:0 20px 60px rgba(0,0,0,.45); text-align:center; }}
.eb {{ font-weight:700; font-size:21px; letter-spacing:.24em; text-transform:uppercase; color:var(--gold); margin-bottom:8px; }}
.ttl {{ font-family:'Play'; font-weight:700; font-size:44px; line-height:1.08; color:var(--cream); }}
.ttl b {{ color:var(--gold); font-style:italic; font-weight:700; }}
.art {{ margin-top:16px; display:flex; flex-direction:column; align-items:center; }}
.big-q {{ font-family:'Play'; font-weight:700; font-size:110px; color:var(--gold); line-height:1.1; }}
.stage {{ position:relative; width:320px; height:300px; }}
.stage > svg {{ position:absolute; left:10px; top:70px; }}
.ppl {{ position:absolute; left:10px; top:0px; }}
.badge {{ position:absolute; left:40px; top:150px; padding:10px 18px; border-radius:40px; font-weight:800; font-size:26px; }}
.badge.red {{ background:#E5484D; color:#fff; }}
.qm {{ position:absolute; width:62px; height:62px; border-radius:50%; background:var(--gold); color:#080808; font-weight:900; font-size:42px; line-height:62px; }}
#c3q1 {{ left:20px; top:110px; }} #c3q2 {{ left:236px; top:96px; }}
.clock {{ position:absolute; left:220px; top:10px; }}
.steps {{ display:flex; gap:18px; margin-top:12px; }}
.st {{ width:90px; height:90px; border-radius:50%; border:4px solid var(--gold); font-family:'Play'; font-weight:700; font-size:54px; line-height:82px; color:var(--gold); }}
.form {{ width:330px; display:flex; flex-direction:column; gap:14px; text-align:left; }}
.fld {{ background:#141414; border:2px solid rgba(245,243,238,.35); border-radius:16px; padding:10px 16px; }}
.lbl {{ display:block; font-size:17px; font-weight:700; letter-spacing:.12em; text-transform:uppercase; color:var(--gold); }}
.val {{ display:inline-block; font-size:27px; font-weight:600; color:var(--cream); white-space:nowrap; }}
.btn {{ background:var(--gold); color:#080808; font-weight:800; font-size:25px; text-align:center; padding:14px; border-radius:40px; }}
.disc {{ display:flex; gap:10px; margin-top:10px; }}
.pct {{ width:160px; height:160px; border-radius:50%; background:var(--gold); color:#080808; font-weight:900; font-size:54px; line-height:160px; }}
#p20 {{ background:var(--cream); }}
.chips {{ display:flex; flex-direction:column; gap:14px; margin-top:8px; align-items:center; }}
.chip {{ border:2.5px solid var(--gold); border-radius:50px; padding:10px 34px; font-family:'Play'; font-style:italic; font-weight:700; font-size:44px; color:var(--cream); }}
.motto {{ font-family:'Play'; font-style:italic; font-weight:700; font-size:40px; color:var(--gold); margin-top:10px; }}
.split {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:9; pointer-events:none; }}
.panel {{ position:absolute; left:600px; top:0; width:480px; height:1920px; background:linear-gradient(180deg,#0d0d0d,#080808); border-left:3px solid var(--gold); padding:200px 34px 0 34px; text-align:center; }}
.wipe {{ position:absolute; left:600px; top:0; width:26px; height:1920px; background:var(--gold); }}
.panel .ttl {{ font-size:58px; }}
.fwrap {{ position:relative; margin:18px auto 0; width:300px; }}
.flabel {{ position:absolute; font-weight:800; font-size:22px; letter-spacing:.16em; text-transform:uppercase; }}
.flabel.top {{ left:0; right:0; top:60px; color:var(--cream); opacity:.75; }}
.flabel.bot {{ left:0; right:0; top:440px; color:var(--gold); }}
.rs {{ position:absolute; left:34px; right:34px; display:flex; align-items:center; justify-content:center; gap:12px; font-weight:800; font-size:27px; background:rgba(212,175,55,.12); border:2px solid var(--gold); border-radius:20px; padding:12px; }}
.rs svg {{ width:56px; height:auto; }} .rs > span:first-child {{ color:var(--gold); font-size:38px; }}
#r1 {{ top:830px; }} #r2 {{ top:920px; }}
.exchip {{ position:absolute; left:34px; right:34px; top:860px; font-family:'Play'; font-style:italic; font-weight:700; font-size:40px; color:var(--gold); }}
.camp {{ display:flex; justify-content:center; gap:40px; margin-top:60px; }}
.camp > div {{ display:flex; flex-direction:column; align-items:center; gap:10px; font-weight:800; font-size:26px; }}
.back {{ margin:70px auto 0; display:flex; flex-direction:column; align-items:center; gap:14px; font-weight:700; font-size:32px; line-height:1.25; }}
.back b {{ color:var(--gold); }}
.recap {{ position:absolute; left:30px; right:30px; top:200px; text-align:left; }}
.recap .eb {{ text-align:center; font-size:24px; margin-bottom:18px; }}
.tier {{ display:flex; align-items:center; gap:16px; margin:0 auto 14px; border:2px solid rgba(212,175,55,.7); background:rgba(212,175,55,.08); border-radius:18px; padding:12px 16px; }}
#t1 {{ width:100%; }} #t2 {{ width:94%; }} #t3 {{ width:88%; }} #t4 {{ width:82%; }} #t5 {{ width:76%; background:var(--gold); }}
#t5 .tl, #t5 .ts, #t5 .tn {{ color:#080808; border-color:#080808; }}
.tn {{ flex:none; width:46px; height:46px; border-radius:50%; border:3px solid var(--gold); color:var(--gold); font-family:'Play'; font-weight:700; font-size:28px; line-height:40px; text-align:center; }}
.tl {{ font-family:'Play'; font-weight:700; font-size:32px; color:var(--cream); line-height:1.1; }}
.ts {{ font-size:19px; font-weight:600; color:rgba(245,243,238,.75); }}
#captions {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:20; pointer-events:none; }}
.grp {{ position:absolute; left:50px; right:50px; top:1180px; text-align:center; font-weight:800; line-height:1.25; visibility:hidden; opacity:0; }}
.w {{ display:inline-block; color:var(--cream); text-shadow:0 3px 0 rgba(0,0,0,.55), 0 6px 22px rgba(0,0,0,.65); margin:0 4px; }}
.w.kw {{ color:#080808; background:var(--gold); border-radius:14px; padding:0 14px; text-shadow:none; box-shadow:0 8px 24px rgba(0,0,0,.4); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
  <div id="bg"></div>
  <div id="vwrap">
    <video id="vid" class="clip" src="assets/clean.mp4" data-start="0" data-duration="{DUR}" data-track-index="0" data-has-audio="true" data-volume="1" playsinline></video>
    <div id="shade"></div>
  </div>
  {chr(10).join(cards_html)}
  <div id="captions" class="clip" data-start="0" data-duration="{DUR}" data-track-index="4" data-track-kind="captions" data-layout-allow-caption-zone data-layout-allow-overlap>
  {chr(10).join(cap_html)}
  </div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
{chr(10).join(cap_js)}
window.__timelines = window.__timelines || {{}};
window.__timelines["main"] = tl;
</script>
</body>
</html>'''
open(f"{S}/hf/funnel/index.html", "w").write(page)
print("groups", len(groups), "cards", len(cards))
