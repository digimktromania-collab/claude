/* ═════════════════════════════════════════════════════════════
   UNIVERSUL GEO — motorul de mișcare
   un singur requestAnimationFrame conduce tot: scroll (Lenis),
   stele, orbite, cursor, parallax — nimic nu concurează.
   ═════════════════════════════════════════════════════════════ */
(() => {
  'use strict';

  const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const FINE_POINTER = window.matchMedia('(pointer: fine)').matches;
  const COARSE = window.matchMedia('(pointer: coarse)').matches;
  const lerp = (a, b, t) => a + (b - a) * t;
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

  /* ─────────────── DATELE UNIVERSULUI ─────────────── */

  const WORLDS = [
    {
      slug: 'abia-incep',
      name: 'Abia încep',
      desc: 'Primul pas în online, fără haos. Fundamentele marketingului digital, așezate pas cu pas — de la zero absolut până la primele rezultate.',
      ring: 0, phase: 0.65, size: 32,
      tint: '#8fae9c', tintHi: '#e9f2ec', glow: 'rgba(143,174,156,0.8)'
    },
    {
      slug: 'marketing-antreprenorial',
      name: 'Marketing Digital Antreprenorial',
      desc: 'Strategie, conținut și vânzare pentru antreprenori. Nu doar postări — un sistem de marketing care lucrează pentru afacerea ta.',
      ring: 1, phase: 2.3, size: 42,
      tint: '#16b581', tintHi: '#c9f5e4', glow: 'rgba(22,181,129,0.85)'
    },
    {
      slug: 'ai-creativ',
      name: 'AI Creativ & Productivitate',
      desc: 'Instrumentele AI care îți înmulțesc timpul: creezi mai mult, muncești mai puțin și rămâi mereu cu un pas înaintea celorlalți.',
      ring: 2, phase: 4.1, size: 38,
      tint: '#2e8b8b', tintHi: '#d7f0f0', glow: 'rgba(70,170,170,0.8)'
    },
    {
      slug: 'am-deja-o-afacere',
      name: 'Am deja o afacere',
      desc: 'Pentru cei care au trecut de început: structură, claritate și sisteme de creștere care scalează fără să te consume.',
      ring: 0, phase: 0.65 + Math.PI, size: 36,
      tint: '#c9a24b', tintHi: '#f6e8c6', glow: 'rgba(201,162,75,0.85)'
    },
    {
      slug: 'sistemul-mir',
      name: 'Sistemul MIR',
      desc: 'Metoda semnătură a universului — cadrul complet care leagă totul, de la idee la rezultat. Inima Academiei, disponibilă și de sine stătător.',
      ring: 1, phase: 2.3 + Math.PI, size: 46,
      tint: '#d8c69a', tintHi: '#fdf6e2', glow: 'rgba(216,198,154,0.9)'
    },
    {
      slug: 'mentorat',
      name: 'Mentorat 1:1',
      desc: 'Lucrezi direct cu Georgiana. Strategie personalizată, feedback fără menajamente și o transformare pe care o simți în cifre.',
      ring: 2, phase: 4.1 + Math.PI, size: 30,
      tint: '#b8a6d9', tintHi: '#efe9f9', glow: 'rgba(184,166,217,0.8)'
    }
  ];

  const ACADEMIA = {
    slug: 'academia',
    name: 'Academia MIR',
    desc: 'Nucleul universului: toate cele șase lumi, comunitatea, actualizările și tot ce urmează — într-un singur loc, pentru totdeauna.'
  };

  const RING_FRACTIONS = [0.42, 0.66, 0.9];   // rază orizontală, ca fracție din W/2
  const FLATTEN = 0.42;                       // elipsa: ry = rx * FLATTEN
  const RING_SPEEDS = [0.16, 0.105, 0.072];   // radiani / secundă

  /* ─────────────── SPARGEREA LITERELOR ─────────────── */

  function splitLetters(el) {
    const text = el.textContent;
    el.textContent = '';
    let i = 0;
    for (const ch of text) {
      if (ch === ' ') { el.appendChild(document.createTextNode(' ')); continue; }
      const wrap = document.createElement('span');
      wrap.className = 'l-wrap';
      const inner = document.createElement('span');
      inner.className = 'l';
      inner.textContent = ch;
      inner.style.transitionDelay = `${i * 0.045}s`;
      wrap.appendChild(inner);
      el.appendChild(wrap);
      i++;
    }
  }

  splitLetters(document.getElementById('preloader-word'));
  splitLetters(document.getElementById('hero-name'));

  /* ─────────────── LENIS ─────────────── */

  const lenis = new Lenis({
    lerp: 0.09,
    wheelMultiplier: 1,
    smoothWheel: !REDUCED
  });

  /* ─────────────── PRELOADER ─────────────── */

  const preloader = document.getElementById('preloader');
  lenis.stop();
  document.body.classList.add('no-scroll');

  const beginIntro = () => {
    preloader.classList.add('is-in');
    const settle = REDUCED ? 300 : 2350;
    setTimeout(() => {
      preloader.classList.add('is-done');
      document.body.classList.add('is-loaded');
      document.body.classList.remove('no-scroll');
      lenis.start();
      setTimeout(() => preloader.remove(), 1400);
    }, settle);
  };

  Promise.race([
    document.fonts ? document.fonts.ready : Promise.resolve(),
    new Promise(res => setTimeout(res, 900))
  ]).then(() => requestAnimationFrame(() => requestAnimationFrame(beginIntro)));

  /* ─────────────── STELELE ─────────────── */

  const canvas = document.getElementById('stars');
  const ctx = canvas.getContext('2d');
  let vw = 0, vh = 0, dpr = 1;
  let stars = [];
  let comet = null;
  let nextCometAt = 8000 + Math.random() * 8000;

  // sprite pre-randat pentru stelele cu halou (shadowBlur pe fiecare cadru e scump)
  const glowSprite = document.createElement('canvas');
  (function makeSprite() {
    const s = 64;
    glowSprite.width = glowSprite.height = s;
    const g = glowSprite.getContext('2d');
    const grad = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
    grad.addColorStop(0, 'rgba(240,235,223,0.9)');
    grad.addColorStop(0.25, 'rgba(240,235,223,0.28)');
    grad.addColorStop(1, 'rgba(240,235,223,0)');
    g.fillStyle = grad;
    g.fillRect(0, 0, s, s);
  })();

  function buildStars() {
    const count = Math.round((vw * vh) / 6500);
    stars = [];
    for (let i = 0; i < count; i++) {
      const depth = Math.random();                 // 0 = departe, 1 = aproape
      stars.push({
        x: Math.random() * vw,
        y: Math.random() * vh,
        depth,
        r: 0.4 + depth * 1.1,
        base: 0.12 + Math.random() * 0.5,
        amp: 0.08 + Math.random() * 0.4,
        speed: 0.3 + Math.random() * 1.4,
        phase: Math.random() * Math.PI * 2,
        glow: Math.random() < 0.07
      });
    }
  }

  // vigneta, pre-randată o dată la redimensionare (un strat DOM mai puțin)
  const vignette = document.createElement('canvas');
  function bakeVignette() {
    vignette.width = Math.max(2, Math.round(vw / 3));
    vignette.height = Math.max(2, Math.round(vh / 3));
    const g = vignette.getContext('2d');
    const w = vignette.width, h = vignette.height;
    g.clearRect(0, 0, w, h);
    g.save();
    g.translate(w / 2, h * 0.42);
    g.scale(1.3, 1);
    const grad = g.createRadialGradient(0, 0, 0, 0, 0, h * 0.95);
    grad.addColorStop(0, 'rgba(0,0,0,0)');
    grad.addColorStop(0.55, 'rgba(0,0,0,0)');
    grad.addColorStop(1, 'rgba(0,0,0,0.55)');
    g.fillStyle = grad;
    g.fillRect(-w, -h, w * 2, h * 2.4);
    g.restore();
  }

  function resizeCanvas() {
    vw = window.innerWidth;
    vh = window.innerHeight;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(vw * dpr);
    canvas.height = Math.round(vh * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    buildStars();
    bakeVignette();
  }

  function drawStars(t, px, py) {
    ctx.clearRect(0, 0, vw, vh);
    ctx.fillStyle = '#f0ebdf';
    for (let i = 0; i < stars.length; i++) {
      const s = stars[i];
      const a = REDUCED ? s.base : clamp(s.base + s.amp * Math.sin(t * 0.001 * s.speed + s.phase), 0.03, 1);
      const ox = px * (4 + s.depth * 18);
      const oy = py * (3 + s.depth * 13);
      let x = s.x + ox, y = s.y + oy;
      if (s.glow) {
        const size = 10 + s.depth * 16;
        ctx.globalAlpha = a * 0.85;
        ctx.drawImage(glowSprite, x - size / 2, y - size / 2, size, size);
      } else {
        ctx.globalAlpha = a;
        ctx.fillRect(x, y, s.r, s.r);
      }
    }
    ctx.globalAlpha = 1;
    ctx.drawImage(vignette, 0, 0, vw, vh);

    // cometă rară, discretă
    if (!REDUCED) {
      if (!comet && t > nextCometAt) {
        const fromX = vw * (0.15 + Math.random() * 0.7);
        comet = { x: fromX, y: -30, vx: (Math.random() - 0.3) * 260, vy: 320 + Math.random() * 160, life: 1, t };
      }
      if (comet) {
        const dt = 1 / 60;
        comet.x += comet.vx * dt;
        comet.y += comet.vy * dt;
        comet.life -= dt * 0.55;
        if (comet.life <= 0 || comet.y > vh + 60) {
          comet = null;
          nextCometAt = t + 9000 + Math.random() * 12000;
        } else {
          const tail = 90;
          const nx = comet.vx, ny = comet.vy;
          const len = Math.hypot(nx, ny);
          const grad = ctx.createLinearGradient(
            comet.x, comet.y,
            comet.x - (nx / len) * tail, comet.y - (ny / len) * tail
          );
          grad.addColorStop(0, `rgba(240,235,223,${0.7 * comet.life})`);
          grad.addColorStop(1, 'rgba(240,235,223,0)');
          ctx.strokeStyle = grad;
          ctx.lineWidth = 1.1;
          ctx.beginPath();
          ctx.moveTo(comet.x, comet.y);
          ctx.lineTo(comet.x - (nx / len) * tail, comet.y - (ny / len) * tail);
          ctx.stroke();
        }
      }
    }
  }

  /* ─────────────── SISTEMUL SOLAR ─────────────── */

  const system = document.getElementById('system');
  const heroTilt = document.getElementById('hero-tilt');
  const rings = system.querySelectorAll('.ring');
  const card = document.getElementById('offer-card');
  const cardIndex = document.getElementById('card-index');
  const cardTitle = document.getElementById('card-title');
  const cardDesc = document.getElementById('card-desc');

  const planets = WORLDS.map((w, i) => {
    const btn = document.createElement('button');
    btn.className = 'planet';
    btn.dataset.world = w.slug;
    btn.dataset.index = i;
    btn.setAttribute('aria-label', `${w.name} — deschide lumea`);
    btn.style.setProperty('--size', `${w.size}px`);
    btn.style.setProperty('--tint', w.tint);
    btn.style.setProperty('--tint-hi', w.tintHi);
    btn.style.setProperty('--glow', w.glow);
    btn.style.setProperty('--glow-soft', w.glow.replace(/[\d.]+\)$/, '0.35)'));
    btn.style.setProperty('--ping-delay', `${2.6 + i * 0.4}s`);
    btn.style.transitionDelay = `${0.9 + i * 0.12}s`;
    btn.innerHTML = `
      <span class="planet__num">0${i + 1}</span>
      <span class="planet__body"></span>
      <span class="planet__pulse" aria-hidden="true"></span>`;
    system.appendChild(btn);
    return {
      el: btn,
      body: btn.querySelector('.planet__body'),
      angle: w.phase,
      ring: w.ring,
      speedMul: 1,
      speedTarget: 1,
      x: 0, y: 0
    };
  });

  let sysW = 0, sysH = 0;
  function layoutSystem() {
    const rect = system.getBoundingClientRect();
    sysW = rect.width;
    sysH = rect.height;
    const maxRx = sysW / 2 - 10;
    RING_FRACTIONS.forEach((f, i) => {
      const rx = maxRx * f;
      const ry = rx * FLATTEN;
      rings[i].style.width = `${rx * 2}px`;
      rings[i].style.height = `${ry * 2}px`;
    });
  }

  let hovered = -1;

  function updatePlanets(dt, t) {
    const maxRx = sysW / 2 - 10;
    const sysRect = system.getBoundingClientRect();
    const cx = sysRect.left + sysW / 2;
    const cy = sysRect.top + sysH / 2;

    for (let i = 0; i < planets.length; i++) {
      const p = planets[i];
      p.speedMul = lerp(p.speedMul, p.speedTarget, 1 - Math.exp(-dt * 4));
      if (!REDUCED) p.angle += RING_SPEEDS[p.ring] * p.speedMul * dt;

      const rx = maxRx * RING_FRACTIONS[p.ring];
      const ry = rx * FLATTEN;
      const sin = Math.sin(p.angle);
      const x = sysW / 2 + rx * Math.cos(p.angle);
      const y = sysH / 2 + ry * sin;
      const depth = (sin + 1) / 2;                    // 0 = spate, 1 = față
      const scale = 0.78 + depth * 0.4;

      p.x = cx + rx * Math.cos(p.angle);
      p.y = cy + ry * sin;
      p.el.style.transform = `translate3d(${x}px, ${y}px, 0) scale(${scale})`;
      p.el.style.zIndex = sin > 0 ? 5 : 1;
      p.body.style.opacity = 0.7 + depth * 0.3;
    }

    // cardul urmărește planeta activă
    if (hovered >= 0) positionCard(planets[hovered]);
  }

  function fillCard(i) {
    const w = WORLDS[i];
    cardIndex.textContent = `0${i + 1}`;
    cardTitle.textContent = w.name;
    cardDesc.textContent = w.desc;
  }

  function positionCard(p) {
    const cw = card.offsetWidth, ch = card.offsetHeight;
    let x = p.x + 40;
    let y = p.y - ch / 2;
    if (x + cw > window.innerWidth - 20) x = p.x - cw - 40;
    y = clamp(y, 16, window.innerHeight - ch - 16);
    card.style.left = `${x}px`;
    card.style.top = `${y}px`;
  }

  planets.forEach((p, i) => {
    p.el.addEventListener('pointerenter', (e) => {
      if (e.pointerType !== 'mouse') return;   // pe touch, cardul apare la tap
      hovered = i;
      p.speedTarget = 0.07;
      p.el.classList.add('is-hot');
      fillCard(i);
      positionCard(p);
      card.classList.add('is-on');
      card.setAttribute('aria-hidden', 'false');
    });
    p.el.addEventListener('pointerleave', (e) => {
      if (e.pointerType !== 'mouse') return;
      if (hovered === i) hovered = -1;
      p.speedTarget = 1;
      p.el.classList.remove('is-hot');
      card.classList.remove('is-on');
      card.setAttribute('aria-hidden', 'true');
    });
  });

  /* --- pe ecrane tactile: prima atingere arată cardul, a doua deschide lumea --- */

  let touchIdx = -1;

  function showTouchCard(i) {
    if (touchIdx >= 0 && touchIdx !== i) resetTouchPlanet(touchIdx);
    touchIdx = i;
    const p = planets[i];
    p.speedTarget = 0.07;
    p.el.classList.add('is-hot');
    fillCard(i);
    const cw = card.offsetWidth, ch = card.offsetHeight;
    card.style.left = `${Math.round((window.innerWidth - cw) / 2)}px`;
    card.style.top = `${window.innerHeight - ch - 20}px`;
    card.classList.add('is-on', 'is-touch');
    card.setAttribute('aria-hidden', 'false');
  }

  function resetTouchPlanet(i) {
    planets[i].speedTarget = 1;
    planets[i].el.classList.remove('is-hot');
  }

  function hideTouchCard() {
    if (touchIdx < 0) return;
    resetTouchPlanet(touchIdx);
    touchIdx = -1;
    card.classList.remove('is-on', 'is-touch');
    card.setAttribute('aria-hidden', 'true');
  }

  /* ─────────────── LUMILE (paginile dedicate — placeholder) ─────────────── */

  const world = document.getElementById('world');
  const worldIndex = document.getElementById('world-index');
  const worldTitle = document.getElementById('world-title');
  const worldDesc = document.getElementById('world-desc');
  let worldOpen = false;

  function openWorld(slug, ox, oy) {
    const i = WORLDS.findIndex(w => w.slug === slug);
    const data = i >= 0 ? WORLDS[i] : ACADEMIA;
    worldIndex.textContent = i >= 0 ? `0${i + 1}` : '☉';
    worldTitle.textContent = data.name;
    worldDesc.textContent = data.desc;
    world.style.setProperty('--wx', `${(ox / window.innerWidth) * 100}%`);
    world.style.setProperty('--wy', `${(oy / window.innerHeight) * 100}%`);
    world.classList.add('is-open');
    world.setAttribute('aria-hidden', 'false');
    worldOpen = true;
    lenis.stop();
    document.body.classList.add('no-scroll');
    history.replaceState(null, '', `#${data.slug}`);
    hideTouchCard();
    card.classList.remove('is-on');
  }

  function closeWorld() {
    if (!worldOpen) return;
    world.classList.remove('is-open');
    world.setAttribute('aria-hidden', 'true');
    worldOpen = false;
    lenis.start();
    document.body.classList.remove('no-scroll');
    history.replaceState(null, '', location.pathname);
  }

  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-world]');
    if (trigger) {
      e.preventDefault();
      const isTouchTap = e.pointerType ? e.pointerType !== 'mouse' : COARSE;
      if (isTouchTap && trigger.classList.contains('planet')) {
        const i = +trigger.dataset.index;
        if (touchIdx !== i) { showTouchCard(i); return; }   // prima atingere: cardul
        hideTouchCard();                                     // a doua: intră în lume
      }
      const rect = trigger.getBoundingClientRect();
      openWorld(trigger.dataset.world, rect.left + rect.width / 2, rect.top + rect.height / 2);
      return;
    }
    // atingerea cardului deschide lumea; atingerea în afara lui îl închide
    if (touchIdx >= 0) {
      if (e.target.closest('.offer-card')) {
        const i = touchIdx;
        hideTouchCard();
        const r = planets[i].el.getBoundingClientRect();
        openWorld(WORLDS[i].slug, r.left + r.width / 2, r.top + r.height / 2);
      } else {
        hideTouchCard();
      }
    }
  });
  document.getElementById('world-close').addEventListener('click', closeWorld);
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeWorld(); });

  // deschidere directă prin #hash (linkuri către lumi)
  if (location.hash) {
    const slug = location.hash.slice(1);
    if (slug === ACADEMIA.slug || WORLDS.some(w => w.slug === slug)) {
      setTimeout(() => openWorld(slug, window.innerWidth / 2, window.innerHeight / 2), 3400);
    }
  }

  /* ─────────────── INDEXUL LUMILOR (secțiunea listă) ─────────────── */

  const list = document.getElementById('worlds-list');
  WORLDS.forEach((w, i) => {
    const row = document.createElement('button');
    row.className = 'world-row';
    row.dataset.world = w.slug;
    row.dataset.hover = '';
    row.innerHTML = `
      <span class="world-row__num">0${i + 1}</span>
      <span class="world-row__name">${w.name}</span>
      <span class="world-row__sep"><i></i>disponibil și separat</span>
      <span class="world-row__arrow">→</span>`;
    list.appendChild(row);
  });

  /* ─────────────── CURSOR ─────────────── */

  const cursor = document.getElementById('cursor');
  const mouse = { x: innerWidth / 2, y: innerHeight / 2 };
  const dotPos = { x: mouse.x, y: mouse.y };
  const ringPos = { x: mouse.x, y: mouse.y };
  const dotWritten = { x: -1e4, y: -1e4 };
  const ringWritten = { x: -1e4, y: -1e4 };
  const dotEl = cursor.querySelector('.cursor__dot');
  const ringEl = cursor.querySelector('.cursor__ring');
  let cursorSeen = false;

  window.addEventListener('pointermove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
    if (!cursorSeen && FINE_POINTER) {
      cursorSeen = true;
      dotPos.x = ringPos.x = mouse.x;
      dotPos.y = ringPos.y = mouse.y;
      document.body.classList.add('cursor-on');
    }
  }, { passive: true });

  document.addEventListener('pointerover', (e) => {
    if (e.target.closest('[data-hover], .planet, .sun, a, button')) {
      document.body.classList.add('cursor-hover');
    }
  });
  document.addEventListener('pointerout', (e) => {
    if (e.target.closest('[data-hover], .planet, .sun, a, button')) {
      document.body.classList.remove('cursor-hover');
    }
  });
  window.addEventListener('pointerdown', () => document.body.classList.add('cursor-down'));
  window.addEventListener('pointerup', () => document.body.classList.remove('cursor-down'));

  /* ─────────────── CONTOARELE ─────────────── */

  const easeOutExpo = (t) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t));

  function runCounter(el) {
    const target = parseInt(el.dataset.count, 10);
    const dur = 1900;
    const t0 = performance.now();
    (function tick(now) {
      const k = clamp((now - t0) / dur, 0, 1);
      el.textContent = Math.round(easeOutExpo(k) * target);
      if (k < 1) requestAnimationFrame(tick);
    })(t0);
  }

  const counterIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        runCounter(en.target);
        counterIO.unobserve(en.target);
      }
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('.stat__num').forEach((el) => counterIO.observe(el));

  /* ─────────────── REVEALS LA SCROLL ─────────────── */

  // liniile mascate (overflow: hidden) sunt complet decupate înainte de reveal,
  // deci observăm masca-părinte, nu linia în sine
  const revealIO = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      const line = en.target.classList.contains('line-mask')
        ? en.target.querySelector('.reveal-line')
        : en.target;
      line.classList.add('in');
      revealIO.unobserve(en.target);
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('.reveal, .line-mask').forEach((el) => revealIO.observe(el));

  /* ─────────────── BUCLA PRINCIPALĂ ─────────────── */

  const par = { x: 0, y: 0 };    // parallax lin (-1 … 1)
  let lastT = performance.now();
  let heroVisible = true;
  let lastTiltX = 99, lastTiltY = 99;
  let frameNo = 0;

  // motorul orbital doarme când sistemul solar iese din ecran
  const heroIO = new IntersectionObserver((entries) => {
    heroVisible = entries[0].isIntersecting;
  }, { threshold: 0 });
  heroIO.observe(document.getElementById('univers'));

  function frame(t) {
    const dt = clamp((t - lastT) / 1000, 0, 0.05);
    lastT = t;

    lenis.raf(t);

    // parallax catifelat spre poziția mouse-ului
    const targetX = (mouse.x / innerWidth - 0.5) * 2;
    const targetY = (mouse.y / innerHeight - 0.5) * 2;
    const k = 1 - Math.exp(-dt * 3.2);
    par.x = lerp(par.x, targetX, k);
    par.y = lerp(par.y, targetY, k);

    // stelele pâlpâie la 30Hz când parallax-ul e liniștit — imperceptibil, dar mai ieftin
    frameNo++;
    const parMoving = Math.abs(par.x - targetX) > 0.004 || Math.abs(par.y - targetY) > 0.004;
    if (parMoving || frameNo % 2 === 0) drawStars(t, -par.x, -par.y);

    if (heroVisible && !worldOpen) {
      updatePlanets(dt, t);

      // scriem transformarea doar când s-a mișcat ceva perceptibil
      if (!REDUCED && FINE_POINTER &&
          (Math.abs(par.x - lastTiltX) > 0.0008 || Math.abs(par.y - lastTiltY) > 0.0008)) {
        lastTiltX = par.x; lastTiltY = par.y;
        heroTilt.style.transform =
          `perspective(1400px) rotateY(${(par.x * 2.4).toFixed(3)}deg) rotateX(${(-par.y * 2.2).toFixed(3)}deg)` +
          ` translate3d(${(par.x * 10).toFixed(2)}px, ${(par.y * 8).toFixed(2)}px, 0)`;
      }
    }

    if (FINE_POINTER && cursorSeen) {
      dotPos.x = lerp(dotPos.x, mouse.x, 1 - Math.exp(-dt * 30));
      dotPos.y = lerp(dotPos.y, mouse.y, 1 - Math.exp(-dt * 30));
      ringPos.x = lerp(ringPos.x, mouse.x, 1 - Math.exp(-dt * 11));
      ringPos.y = lerp(ringPos.y, mouse.y, 1 - Math.exp(-dt * 11));
      if (Math.abs(ringPos.x - ringWritten.x) > 0.04 || Math.abs(ringPos.y - ringWritten.y) > 0.04 ||
          Math.abs(dotPos.x - dotWritten.x) > 0.04 || Math.abs(dotPos.y - dotWritten.y) > 0.04) {
        dotEl.style.transform = `translate3d(${dotPos.x}px, ${dotPos.y}px, 0)`;
        ringEl.style.transform = `translate3d(${ringPos.x}px, ${ringPos.y}px, 0)`;
        dotWritten.x = dotPos.x; dotWritten.y = dotPos.y;
        ringWritten.x = ringPos.x; ringWritten.y = ringPos.y;
      }
    }

    requestAnimationFrame(frame);
  }

  /* ─────────────── PORNIRE ─────────────── */

  function onResize() {
    resizeCanvas();
    layoutSystem();
  }
  window.addEventListener('resize', onResize, { passive: true });
  onResize();
  requestAnimationFrame(frame);
})();
