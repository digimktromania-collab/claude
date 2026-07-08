/* ═══════════════════════════════════════════════════════════════════════
   UNIVERSUL IORDACHE GEORGIANA — motorul partajat
   Rulează pe toate paginile: fundal cosmic (Three.js), scroll fin (Lenis),
   sincronizare GSAP/ScrollTrigger, meniu fullscreen, dezvăluiri la scroll,
   interacțiunea planetelor pe touch, fallback pentru nucleu.
   ═══════════════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const gata = (fn) => (document.readyState !== 'loading'
    ? fn() : document.addEventListener('DOMContentLoaded', fn));

  /* ─────────────────────────────────────────────────────────────────
     1. FUNDAL COSMIC — stele care pâlpâie + particule aurii (Three.js)
     Un singur câmp de puncte, colorat mixt: crem (stele), auriu
     (particule) și albastru discret. Fiecare punct pâlpâie în ritmul lui
     (fază + viteză proprii), printr-un ShaderMaterial ușor.
     ───────────────────────────────────────────────────────────────── */
  function fundalCosmic() {
    const canvas = document.getElementById('cosmos');
    if (!canvas || typeof THREE === 'undefined') return;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 100);
    camera.position.z = 14;

    const NR = window.innerWidth < 768 ? 520 : 900;   // discret: puține, mici
    const pozitii = new Float32Array(NR * 3);
    const culori  = new Float32Array(NR * 3);
    const scari   = new Float32Array(NR);
    const faze    = new Float32Array(NR);
    const viteze  = new Float32Array(NR);

    const cCrem   = new THREE.Color('#F5F3EE');
    const cAuriu  = new THREE.Color('#D4AF37');
    const cAlb    = new THREE.Color('#8FB3FF');

    for (let i = 0; i < NR; i++) {
      // distribuție într-o cutie adâncă și largă în jurul camerei
      pozitii[i * 3]     = (Math.random() - 0.5) * 54;
      pozitii[i * 3 + 1] = (Math.random() - 0.5) * 40;
      pozitii[i * 3 + 2] = (Math.random() - 0.5) * 40 - 12;

      const r = Math.random();
      // puține particule aurii, și mai puține albastre; restul, stele crem
      const eAuriu = r < 0.05, eAlb = r >= 0.05 && r < 0.08;
      const c = eAuriu ? cAuriu : eAlb ? cAlb : cCrem;
      culori[i * 3] = c.r; culori[i * 3 + 1] = c.g; culori[i * 3 + 2] = c.b;

      // stele mici; particulele aurii doar un pic mai mari — nimic strident
      scari[i]  = (eAuriu ? 1.5 : 0.85) * (0.55 + Math.random() * 0.7);
      faze[i]   = Math.random() * Math.PI * 2;
      viteze[i] = 0.4 + Math.random() * 1.0;
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(pozitii, 3));
    geo.setAttribute('aColor',   new THREE.BufferAttribute(culori, 3));
    geo.setAttribute('aScale',   new THREE.BufferAttribute(scari, 1));
    geo.setAttribute('aPhase',   new THREE.BufferAttribute(faze, 1));
    geo.setAttribute('aSpeed',   new THREE.BufferAttribute(viteze, 1));

    const material = new THREE.ShaderMaterial({
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      uniforms: {
        uTime:  { value: 0 },
        uRatio: { value: renderer.getPixelRatio() }
      },
      vertexShader: `
        attribute vec3 aColor; attribute float aScale;
        attribute float aPhase; attribute float aSpeed;
        uniform float uTime; uniform float uRatio;
        varying vec3 vColor; varying float vTwinkle;
        void main() {
          vColor = aColor;
          vTwinkle = 0.25 + 0.6 * (0.5 + 0.5 * sin(uTime * aSpeed + aPhase));
          vec4 mv = modelViewMatrix * vec4(position, 1.0);
          gl_PointSize = aScale * uRatio * (46.0 / -mv.z) * vTwinkle;
          gl_Position = projectionMatrix * mv;
        }`,
      fragmentShader: `
        varying vec3 vColor; varying float vTwinkle;
        void main() {
          float d = distance(gl_PointCoord, vec2(0.5));
          float a = smoothstep(0.5, 0.0, d);
          // luminozitate discretă — stele fine, nu bliț
          gl_FragColor = vec4(vColor, a * vTwinkle * 0.6);
        }`
    });

    const puncte = new THREE.Points(geo, material);
    scene.add(puncte);

    // parallax fin după mouse
    let mx = 0, my = 0, cx = 0, cy = 0;
    window.addEventListener('mousemove', (e) => {
      mx = (e.clientX / window.innerWidth - 0.5);
      my = (e.clientY / window.innerHeight - 0.5);
    });

    const clock = new THREE.Clock();
    function bucla() {
      const t = clock.getElapsedTime();
      material.uniforms.uTime.value = t;
      // rotire foarte lentă — universul respiră
      puncte.rotation.y = t * 0.012;
      puncte.rotation.x = t * 0.005;
      // parallax lin spre țintă
      cx += (mx - cx) * 0.04; cy += (my - cy) * 0.04;
      camera.position.x = cx * 3.2;
      camera.position.y = -cy * 2.2;
      camera.lookAt(scene.position);
      renderer.render(scene, camera);
      if (!reduceMotion) requestAnimationFrame(bucla);
    }
    bucla();
    if (reduceMotion) renderer.render(scene, camera);

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
      material.uniforms.uRatio.value = renderer.getPixelRatio();
    });
  }

  /* ─────────────────────────────────────────────────────────────────
     2. LENIS — scroll fin, cinematic, sincronizat cu GSAP/ScrollTrigger
     ───────────────────────────────────────────────────────────────── */
  function scrollFin() {
    if (typeof Lenis === 'undefined' || reduceMotion) return null;
    const lenis = new Lenis({
      duration: 1.15,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)), // exponential out
      smoothWheel: true
    });

    // Legăm Lenis de ScrollTrigger (dacă GSAP e prezent)
    if (typeof ScrollTrigger !== 'undefined') {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((time) => lenis.raf(time * 1000));
      gsap.ticker.lagSmoothing(0);   // fără lag smoothing — cerut explicit
    } else {
      function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
      requestAnimationFrame(raf);
    }
    window.__lenis = lenis;   // acces global (ex. pentru meniu / linkuri ancoră)
    return lenis;
  }

  /* ─────────────────────────────────────────────────────────────────
     3. DEZVĂLUIRI LA SCROLL — elementele .reveal apar (fade + rise)
     Folosim ScrollTrigger dacă există, altfel IntersectionObserver.
     ───────────────────────────────────────────────────────────────── */
  function dezvaluiri() {
    const elemente = document.querySelectorAll('.reveal');
    if (!elemente.length) return;

    if (typeof ScrollTrigger !== 'undefined' && !reduceMotion) {
      elemente.forEach((el) => {
        ScrollTrigger.create({
          trigger: el,
          start: 'top 85%',
          onEnter: () => el.classList.add('vizibil'),
          once: true
        });
      });
    } else {
      const io = new IntersectionObserver((intrari) => {
        intrari.forEach((intr) => {
          if (intr.isIntersecting) { intr.target.classList.add('vizibil'); io.unobserve(intr.target); }
        });
      }, { threshold: 0.15 });
      elemente.forEach((el) => io.observe(el));
    }
  }

  /* ─────────────────────────────────────────────────────────────────
     3b. BARA DE PROGRES — o linie aurie fină care crește pe măsură ce
     derulezi pagina. Prezentă pe toate paginile (creată din cod).
     ───────────────────────────────────────────────────────────────── */
  function baraProgres() {
    const bara = document.createElement('div');
    bara.className = 'progres';
    bara.setAttribute('aria-hidden', 'true');
    document.body.appendChild(bara);

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined' && !reduceMotion) {
      gsap.to(bara, {
        scaleX: 1, ease: 'none',
        scrollTrigger: {
          start: 0,
          end: () => document.documentElement.scrollHeight - window.innerHeight,
          scrub: 0.3
        }
      });
    } else {
      const actualizeaza = () => {
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bara.style.transform = 'scaleX(' + (h > 0 ? window.scrollY / h : 0) + ')';
      };
      actualizeaza();
      window.addEventListener('scroll', actualizeaza, { passive: true });
    }
  }

  /* ─────────────────────────────────────────────────────────────────
     4. BARA DE SUS — devine „compactă" după ce pagina e derulată
     ───────────────────────────────────────────────────────────────── */
  function baraCompacta() {
    const bara = document.querySelector('.bara');
    if (!bara) return;
    const verifica = () => bara.classList.toggle('compact', window.scrollY > 40);
    verifica();
    window.addEventListener('scroll', verifica, { passive: true });
  }

  /* ─────────────────────────────────────────────────────────────────
     5. MENIUL FULLSCREEN — deschidere/închidere fluidă (GSAP dacă există)
     ───────────────────────────────────────────────────────────────── */
  function meniu() {
    const buton  = document.querySelector('.meniu-buton');
    const overlay = document.querySelector('.meniu');
    const inchide = document.querySelector('.meniu-inchide');
    if (!buton || !overlay) return;
    const linkuri = overlay.querySelectorAll('a');
    const areGsap = typeof gsap !== 'undefined' && !reduceMotion;

    function deschide() {
      overlay.classList.add('deschis');
      overlay.style.visibility = 'visible';
      if (window.__lenis) window.__lenis.stop();
      if (areGsap) {
        gsap.killTweensOf([overlay, linkuri]);
        gsap.to(overlay, { opacity: 1, duration: 0.5, ease: 'power2.out' });
        gsap.fromTo(linkuri,
          { y: 30, opacity: 0 },
          { y: 0, opacity: 1, duration: 0.6, stagger: 0.06, delay: 0.15, ease: 'power3.out' });
      } else { overlay.style.opacity = 1; }
    }
    function inchideMeniu() {
      if (window.__lenis) window.__lenis.start();
      overlay.classList.remove('deschis');
      if (areGsap) {
        gsap.to(overlay, {
          opacity: 0, duration: 0.4, ease: 'power2.in',
          onComplete: () => { overlay.style.visibility = 'hidden'; }
        });
      } else { overlay.style.opacity = 0; overlay.style.visibility = 'hidden'; }
    }

    buton.addEventListener('click', deschide);
    if (inchide) inchide.addEventListener('click', inchideMeniu);
    linkuri.forEach((l) => l.addEventListener('click', inchideMeniu));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') inchideMeniu(); });
  }

  /* ─────────────────────────────────────────────────────────────────
     6. PLANETELE PE TOUCH — pe ecrane tactile prima atingere arată
     cardul, a doua navighează; atingerea în afară închide cardul.
     ───────────────────────────────────────────────────────────────── */
  function planeteTouch() {
    const planete = document.querySelectorAll('.planeta');
    if (!planete.length) return;
    const eTactil = window.matchMedia('(hover: none)').matches;
    if (!eTactil) return;

    planete.forEach((p) => {
      p.addEventListener('click', (e) => {
        if (!p.classList.contains('activ')) {
          e.preventDefault();
          planete.forEach((q) => q.classList.remove('activ'));
          p.classList.add('activ');
        }
        // dacă e deja activă, lăsăm click-ul (link-ul) să navigheze
      });
    });
    document.addEventListener('click', (e) => {
      if (!e.target.closest('.planeta')) planete.forEach((q) => q.classList.remove('activ'));
    });
  }

  /* ─────────────────────────────────────────────────────────────────
     7. PULSUL DE SEMNALIZARE — planetele „clipesc" la încărcare ca să
     arate că sunt interactive (doar pe desktop, o singură dată).
     ───────────────────────────────────────────────────────────────── */
  function semnalPlanete() {
    if (reduceMotion) return;
    const planete = document.querySelectorAll('.hero .planeta');
    if (!planete.length) return;
    // pornim după ce planetele au terminat intrarea
    setTimeout(() => {
      planete.forEach((p) => {
        p.classList.add('semnal');
        p.addEventListener('animationend', () => p.classList.remove('semnal'), { once: true });
      });
    }, 3400);
  }

  /* ─────────────────────────────────────────────────────────────────
     8. NUCLEUL — dacă assets/nucleu.png lipsește, comutăm pe orbul auriu
     ───────────────────────────────────────────────────────────────── */
  function nucleuFallback() {
    const orb = document.querySelector('.nucleu-orb');
    const img = orb ? orb.querySelector('img') : null;
    if (!orb || !img) return;
    img.addEventListener('error', () => {
      img.remove();
      orb.classList.add('fallback');
    });
    // dacă imaginea s-a încărcat deja din cache dar e „ruptă"
    if (img.complete && img.naturalWidth === 0) {
      img.remove(); orb.classList.add('fallback');
    }
  }

  /* ─────────────────────────────────────────────────────────────────
     Pornire
     ───────────────────────────────────────────────────────────────── */
  gata(() => {
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
      gsap.registerPlugin(ScrollTrigger);
    }
    nucleuFallback();
    fundalCosmic();
    scrollFin();
    dezvaluiri();
    baraProgres();
    baraCompacta();
    meniu();
    planeteTouch();
    semnalPlanete();

    // hook pentru scriptul specific paginii (ex. parallax homepage)
    if (typeof window.__paginaInit === 'function') window.__paginaInit();
  });
})();
