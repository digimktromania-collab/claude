# Generates hf/funnel/index.html from work2/words.json
import json, re, unicodedata, html, os
S = os.path.dirname(os.path.abspath(__file__))
W = json.load(open(f"{S}/work2/words.json"))
# manual timing fixes for interpolated words
fix = {}
for i, (s, e) in fix.items():
    W[i]["s"], W[i]["e"] = s, e
DUR = 53.9
T = lambda i: W[i]["s"]

def norm(w):
    w = unicodedata.normalize("NFD", w.lower())
    return re.sub(r"[^a-z0-9-]", "", "".join(c for c in w if unicodedata.category(c) != "Mn"))

KEY = re.compile(r"^(inteligentei|inteligenta|artificiale|artificiala|treizeci|idei|traseu|traseul|tiktok|oferta|trei|subiecte|indemn|call|action|intrebarile|intrebari|strategul|instrument|buyer|persona|comunitatea|digitala|desteapta-te|romane|avatarul|pix)$")

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
        kw = bool(KEY.match(norm(word.strip(".,!?")))) or word.strip("?") == "AI"
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

# ---------- cards (right column) — video 2: AI ca instrument, tu ca strateg ----------
cards = []
def card(cid, s, e, eyebrow, title, body, js=""):
    cards.append((cid, s, e, f'<div class="eb">{eyebrow}</div><div class="ttl">{title}</div><div class="art">{body}</div>', js))

AI_CHIP = f'''<svg viewBox="0 0 200 200" width="150"><rect x="45" y="45" width="110" height="110" rx="20" fill="#141414" stroke="{G}" stroke-width="7"/>
{''.join(f'<path d="M{x} 20 V45 M{x} 155 V180 M20 {x} H45 M155 {x} H180" stroke="{C}" stroke-width="6" stroke-linecap="round"/>' for x in (75, 100, 125))}
<text x="100" y="118" text-anchor="middle" font-family="Mont" font-weight="900" font-size="46" fill="{G}">AI</text></svg>'''
IDEAS = ''.join(f'<div class="idea" id="id{k}">💡</div>' for k in range(6))
ROUTE = f'''<svg viewBox="0 0 320 170" width="300"><path id="rpath" d="M30 130 C 90 130 90 40 160 40 S 240 130 290 70" fill="none" stroke="{C}" stroke-width="5" stroke-dasharray="4 14" stroke-linecap="round" opacity=".7"/>
<g id="rpin"><path d="M290 70 c-18 -20 -22 -30 -22 -40 a22 22 0 0 1 44 0 c0 10 -4 20 -22 40z" fill="{G}"/><circle cx="290" cy="30" r="8" fill="#080808"/></g>
<g id="rman">{person(30, 135, C, 1.3)}</g></svg>'''
EYE = f'<svg viewBox="0 0 120 70" width="96"><path d="M6 35 Q60 -12 114 35 Q60 82 6 35Z" fill="#141414" stroke="{C}" stroke-width="6"/><circle cx="60" cy="35" r="16" fill="{G}"/><circle cx="60" cy="35" r="6" fill="#080808"/></svg>'
PAPER = f'''<svg viewBox="0 0 300 230" width="290"><rect x="40" y="14" width="180" height="210" rx="10" fill="{C}" transform="rotate(-4 130 120)"/>
{''.join(f'<path class="ln" d="M70 {60+k*34} H{190-(k%2)*30}" stroke="#555" stroke-width="7" stroke-linecap="round" transform="rotate(-4 130 120)"/>' for k in range(4))}
<g id="pen"><path d="M232 40 L272 0 L292 20 L252 60 Z" fill="{G}"/><path d="M232 40 L252 60 L222 72 Z" fill="#141414"/><path d="M272 0 L292 20" stroke="#141414" stroke-width="4"/></g></svg>'''
PROMPT = f'''<div class="prompt"><div class="pl1">Vând <span class="slot2" id="pv">[produsul tău]</span></div>
<div class="pl1">pentru <span class="slot2" id="pp">[publicul tău]</span></div>
<div class="pav" id="pav"><span class="avc">{f'<svg viewBox="0 0 60 60" width="46"><circle cx="30" cy="30" r="28" fill="none" stroke="{G}" stroke-width="4"/>{person(30, 36, G, 1.1)}</svg>'}</span>avatarul tău</div></div>'''
CHAT = f'''<div class="chat"><div class="bub ai" id="b1">Ce produs vinzi?</div><div class="bub ai" id="b2">Cine e clientul ideal?</div><div class="stamp" id="b3">Și atât ✓</div></div>'''
PERSONA = f'''<svg viewBox="0 0 300 200" width="290"><rect x="10" y="10" width="280" height="180" rx="22" fill="#141414" stroke="{G}" stroke-width="5"/>
<circle cx="80" cy="90" r="44" fill="none" stroke="{G}" stroke-width="5"/>{person(80, 100, C, 2)}
{''.join(f'<rect class="pa" x="146" y="{50+k*30}" width="{110-k*18}" height="12" rx="6" fill="{C if k else G}" opacity="{1 if k==0 else .55}"/>' for k in range(4))}
<rect x="40" y="152" width="80" height="22" rx="11" fill="{G}"/></svg>'''
QBUB = f'<svg viewBox="0 0 200 170" width="190"><path d="M20 20 H180 V120 H80 L40 155 V120 H20 Z" fill="#141414" stroke="{G}" stroke-width="7" stroke-linejoin="round"/><text x="100" y="95" text-anchor="middle" font-family="Play" font-weight="700" font-size="76" fill="{G}">?</text></svg>'

card("c0", 0, 4.25, "Înainte să-i ceri AI-ului", 'Încă <b>30</b> de idei?', f'<div class="aiwrap">{AI_CHIP}<div class="ideas">{IDEAS}</div></div>',
     "".join(f'tl.fromTo("#id{k}",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:.3,ease:"back.out(3)"}},{T(6) + k*0.12:.2f});' for k in range(6)))
card("c1", 4.3, 8.0, "Mai întâi", 'Unde <b>ajunge</b> omul?', f'<div id="c1r">{ROUTE}</div><div class="eye" id="c1e">{EYE}<span>după ce te vede</span></div>',
     f'''tl.fromTo("#rman",{{x:0,y:0}},{{x:250,y:-62,duration:1.3,ease:"power2.inOut"}},{T(14)});
tl.fromTo("#rpin",{{scale:0,transformOrigin:"50% 100%"}},{{scale:1,duration:.4,ease:"back.out(3)"}},{T(16)});
tl.fromTo("#c1e",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.35,ease:"power3.out"}},{T(18)});''')
card("c2", 8.05, 10.6, "Exercițiu", 'Ia un <b>pix</b> și o hârtie', f'<div id="c2p">{PAPER}</div>',
     f'''tl.fromTo("#c2p .ln",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,stagger:.35,duration:.3,ease:"none"}},{T(31)});
tl.fromTo("#pen",{{x:-140,y:40}},{{x:-40,y:150,duration:1.5,ease:"none"}},{T(31)});''')
card("c3", 10.64, 17.05, "Scrie așa", 'Promptul <b>tău</b>', PROMPT,
     f'''tl.fromTo("#pv",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.5)"}},{T(42)});
tl.fromTo("#pp",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.35,ease:"back.out(2.5)"}},{T(50)});
tl.fromTo("#pav",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{T(54)});''')
card("c4", 28.05, 32.3, "Instrucțiune finală", 'Pune-mi <b>întrebări</b>', CHAT,
     f'''tl.fromTo("#b1",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.35,ease:"back.out(2)"}},{T(97)});
tl.fromTo("#b2",{{opacity:0,x:40}},{{opacity:1,x:0,duration:.35,ease:"back.out(2)"}},{T(100)});
tl.fromTo("#b3",{{opacity:0,scale:1.6,rotation:-12}},{{opacity:1,scale:1,rotation:-6,duration:.3,ease:"power4.out"}},{T(102)});''')
card("c5", 44.95, 46.15, "Cunoaște-ți clientul", '<b>Buyer</b> persona', f'<div id="c5p">{PERSONA}</div>',
     f'tl.fromTo("#c5p .pa",{{scaleX:0,transformOrigin:"0 50%"}},{{scaleX:1,stagger:.1,duration:.3}},{T(141)});')
card("c6", 46.19, 48.4, "Întrebarea mea", 'Tu cum folosești <b>AI</b>?', f'<div id="c6q">{QBUB}</div>',
     f'tl.fromTo("#c6q",{{scale:0,rotation:-15}},{{scale:1,rotation:0,duration:.45,ease:"back.out(2.5)"}},{T(145)});')
card("c7", 48.45, DUR, "Te aștept", 'Comunitatea <b>digitală</b>', f'<div id="c7c">{COMMUNITY}</div><div class="motto" id="c7m">Deșteaptă-te, române!</div>',
     f'''tl.fromTo("#c7c .cp",{{scale:0,opacity:0,transformOrigin:"50% 50%"}},{{scale:1,opacity:1,stagger:.12,duration:.35,ease:"back.out(2)"}},{T(157)});
tl.fromTo("#c7c .links line",{{opacity:0}},{{opacity:1,stagger:.12,duration:.3}},{T(157)+.2});
tl.fromTo("#c7m",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:"power3.out"}},{T(159)-.1});''')

# ---------- split-screen panels ----------
def item(i, ic, label):
    return f'<div class="tier" id="{i}"><div class="tn">{ic}</div><div><div class="tl">{label}</div></div></div>'
TT = f'<svg viewBox="0 0 60 60" width="64"><rect width="60" height="60" rx="14" fill="#141414" stroke="{C}" stroke-width="3"/><path d="M34 14 V38 a8 8 0 1 1 -8 -8" fill="none" stroke="#25F4EE" stroke-width="5" transform="translate(-1.5 -1.5)"/><path d="M34 14 V38 a8 8 0 1 1 -8 -8" fill="none" stroke="#FE2C55" stroke-width="5" transform="translate(1.5 1.5)"/><path d="M34 14 V38 a8 8 0 1 1 -8 -8 M34 14 c2 7 7 10 12 10" fill="none" stroke="#fff" stroke-width="5"/></svg>'
OFFER = f'<svg viewBox="0 0 60 60" width="64"><rect width="60" height="60" rx="14" fill="{G}"/><path d="M16 14 H38 L46 22 V46 H16 Z" fill="none" stroke="#080808" stroke-width="4"/><path d="M22 28 H40 M22 36 H34" stroke="#080808" stroke-width="4"/></svg>'
split1 = f'''<div class="eb">Construiește</div><div class="ttl">Traseul</div>
<div class="route2"><div class="node" id="n1">{TT}<span>Video TikTok</span></div>
<svg viewBox="0 0 20 150" width="20" height="150" class="vline"><path id="vl" d="M10 0 V150" stroke="{G}" stroke-width="5" stroke-dasharray="6 10"/></svg>
<div class="node" id="n2">{OFFER}<span>Cerere de ofertă</span></div></div>
<div class="list" id="lst">{item("i1", "3", "subiecte de video")}{item("i2", "1", "singur îndemn (CTA)")}{item("i3", "?", "întrebări pt. prima conversație")}</div>'''
split1_js = f'''tl.fromTo("#n1",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.5)"}},{T(69)});
tl.fromTo("#vl",{{strokeDashoffset:160,opacity:0}},{{strokeDashoffset:0,opacity:1,duration:.9,ease:"none"}},{T(71)-.2});
tl.fromTo("#n2",{{opacity:0,scale:.6}},{{opacity:1,scale:1,duration:.4,ease:"back.out(2.5)"}},{T(73)});
tl.fromTo("#i1",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(77)});
tl.fromTo("#i2",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(82)});
tl.fromTo("#i3",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(91)});'''

WRENCH = f'<svg viewBox="0 0 100 100" width="90"><path d="M64 10 a24 24 0 0 0 -22 32 L12 72 a8 8 0 0 0 16 16 L58 58 a24 24 0 0 0 32 -22 l-14 14 -14 -4 -4 -14z" fill="none" stroke="{C}" stroke-width="6" stroke-linejoin="round"/></svg>'
KING = f'<svg viewBox="0 0 100 110" width="90"><path d="M50 6 V22 M42 14 H58" stroke="{G}" stroke-width="6" stroke-linecap="round"/><path d="M30 40 Q50 22 70 40 L62 80 H38 Z" fill="{G}"/><rect x="24" y="82" width="52" height="16" rx="5" fill="{G}"/></svg>'
split2 = f'''<div id="sA"><div class="eb">Ține minte</div>
<div class="duo"><div class="tile" id="tA">{AI_CHIP}<div class="tl">AI = instrument</div>{WRENCH}</div>
<div class="tile gold" id="tB">{KING}<div class="tl">Tu = <b>strategul</b></div></div></div></div>
<div id="sB" class="stg"><div class="eb">AI te poate ajuta</div>
{item("h1", "✓", "să proiectezi traseul")}{item("h2", "✓", "să redactezi mesajele")}</div>
<div id="sC" class="stg"><div class="eb">Tu verifici mereu</div>
{item("v1", "✓", "se potrivesc ție?")}{item("v2", "✓", "dar audienței tale?")}</div>'''
split2_js = f'''tl.fromTo("#tA",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.4,ease:"power3.out"}},{T(108)});
tl.fromTo("#tB",{{opacity:0,y:40,scale:.9}},{{opacity:1,y:0,scale:1,duration:.45,ease:"back.out(2)"}},{T(113)});
tl.to("#sA",{{opacity:0,y:-40,duration:.3,ease:"power2.in"}},{T(115)-.3});
tl.fromTo("#sB",{{opacity:0}},{{opacity:1,duration:.2}},{T(115)});
tl.fromTo("#h1",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(119)});
tl.fromTo("#h2",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(122)});
tl.to("#sB",{{opacity:0,y:-40,duration:.3,ease:"power2.in"}},{T(125)-.3});
tl.fromTo("#sC",{{opacity:0}},{{opacity:1,duration:.2}},{T(125)});
tl.fromTo("#v1",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(133)});
tl.fromTo("#v2",{{opacity:0,x:50}},{{opacity:1,x:0,duration:.35,ease:"power3.out"}},{T(138)});'''

splits = [("sp1", 17.05, 28.0, split1, split1_js), ("sp2", 32.25, 44.9, split2, split2_js)]
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
js.append('tl.fromTo("#vwrap",{scale:1},{scale:1.07,duration:4.2,ease:"sine.inOut"},0);tl.to("#vwrap",{scale:1,duration:.4,ease:"power2.out"},4.3);')
js.append(f'tl.to("#vwrap",{{scale:1.1,duration:.25,ease:"power3.out"}},{T(26)-.05}).to("#vwrap",{{scale:1,duration:.5,ease:"power2.inOut"}},{T(26)+.6});')
js.append(f'tl.to("#vwrap",{{scale:1.08,duration:.3,ease:"power3.out"}},{T(111)-.05}).to("#vwrap",{{scale:1,duration:.6,ease:"power2.inOut"}},{T(114)+.6});')
js.append(f'tl.to("#vwrap",{{scale:1.1,duration:.25,ease:"power3.out"}},{T(143)-.05}).to("#vwrap",{{scale:1,duration:.5,ease:"power2.inOut"}},{T(149)});')
js.append(f'tl.to("#vwrap",{{scale:1.06,duration:5,ease:"sine.inOut"}},{T(150)});')
OUT = f"{S}/hf/ai"
EXTRA_SFX = [("pop", T(6), .16), ("pop", T(16), .2), ("pop", T(18), .14), ("typing", T(42) - .3, .12),
  ("pop", T(42), .18), ("pop", T(50), .18), ("pop", T(54), .16), ("pop", T(69), .2), ("pop", T(73), .2),
  ("click-soft", T(77), .2), ("click-soft", T(82), .2), ("click-soft", T(91), .2),
  ("pop", T(97), .16), ("pop", T(100), .16), ("pop", T(102), .22), ("pop", T(108), .18),
  ("impact-bass-1", T(113), .24), ("click-soft", T(119), .2), ("click-soft", T(122), .2),
  ("click-soft", T(133), .2), ("click-soft", T(138), .2), ("pop", T(145), .2), ("sparkle", T(159) - .1, .2)]
LEAKS = [4.3, 8.05, 10.64, 28.05, 44.95, 48.45]
exec(open(f"{S}/fx.py").read())
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
#vwrap {{ position:absolute; inset:0; transform-origin:300px 680px; }}
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
.aiwrap {{ position:relative; width:320px; height:220px; display:flex; justify-content:center; align-items:center; }}
.ideas {{ position:absolute; inset:0; }}
.idea {{ position:absolute; font-size:44px; }}
#id0 {{ left:10px; top:10px; }} #id1 {{ right:14px; top:4px; }} #id2 {{ left:0; top:100px; }} #id3 {{ right:0; top:96px; }} #id4 {{ left:36px; bottom:0; }} #id5 {{ right:40px; bottom:0; }}
.eye {{ display:flex; align-items:center; justify-content:center; gap:12px; font-weight:800; font-size:26px; margin-top:10px; }}
.prompt {{ width:336px; background:#0f0f0f; border:2px solid rgba(245,243,238,.3); border-radius:18px; padding:18px; text-align:left; font-size:30px; font-weight:700; line-height:1.5; }}
.slot2 {{ display:inline-block; color:#080808; background:var(--gold); border-radius:10px; padding:0 10px; font-size:27px; }}
.pav {{ display:flex; align-items:center; gap:12px; margin-top:12px; font-weight:800; font-size:27px; color:var(--gold); }}
.chat {{ width:336px; display:flex; flex-direction:column; gap:14px; align-items:flex-start; }}
.bub {{ background:#1a1a1a; border:2px solid var(--gold); border-radius:22px 22px 22px 6px; padding:12px 18px; font-weight:700; font-size:28px; text-align:left; }}
.stamp {{ align-self:center; margin-top:8px; border:4px solid var(--gold); color:var(--gold); border-radius:14px; padding:6px 20px; font-family:'Play'; font-weight:700; font-size:40px; }}
.route2 {{ display:flex; flex-direction:column; align-items:center; margin-top:30px; }}
.node {{ display:flex; align-items:center; gap:16px; font-weight:800; font-size:31px; }}
.vline {{ margin:8px 0; }}
.list {{ margin-top:46px; }}
.list .tl {{ font-family:'Mont'; font-weight:700; font-size:30px; text-align:left; }}
.stg {{ position:absolute; left:34px; right:34px; top:240px; }}
.stg .tier {{ margin-bottom:22px; }} .stg .tl {{ font-family:'Mont'; font-weight:800; font-size:31px; text-align:left; }}
.stg .eb {{ font-size:25px; margin-bottom:30px; }}
.duo {{ display:flex; flex-direction:column; gap:28px; margin-top:26px; }}
.tile {{ display:flex; flex-direction:column; align-items:center; gap:10px; border:2px solid rgba(245,243,238,.35); border-radius:24px; padding:20px; }}
.tile .tl {{ font-family:'Play'; font-weight:700; font-size:40px; }}
.tile.gold {{ border-color:var(--gold); background:rgba(212,175,55,.1); }} .tile b {{ color:var(--gold); font-style:italic; }}
{LEAK_CSS}
#captions {{ position:absolute; left:0; top:0; width:1080px; height:1920px; z-index:20; pointer-events:none; }}
.grp {{ position:absolute; left:50px; right:50px; top:1250px; text-align:center; font-weight:800; line-height:1.25; visibility:hidden; opacity:0; }}
.w {{ display:inline-block; color:var(--cream); background:rgba(8,8,8,.72); border-radius:14px; padding:0 14px; margin:4px 2px; box-shadow:0 8px 24px rgba(0,0,0,.35); }}
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
open(f"{S}/hf/ai/index.html", "w").write(page)
print("groups", len(groups), "cards", len(cards))
