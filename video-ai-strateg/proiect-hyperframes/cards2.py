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
