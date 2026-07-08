import { motion, useReducedMotion } from 'framer-motion'

/**
 * Geo AI Academy — dark luxury hero.
 *
 * Design language: editorial, quiet confidence. Gold is used sparingly, as
 * emphasis only. Every animation degrades gracefully when the visitor prefers
 * reduced motion (Framer Motion's `useReducedMotion` + a CSS fallback in
 * index.css cover both JS- and CSS-driven layers).
 */

const BRAND = 'Geo AI Academy'

// The headline, split into words so each can fade + rise on its own beat.
// `gold: true` marks the single emphasised word.
const HEADLINE = [
  [
    { text: 'The' },
    { text: 'Quiet' },
    { text: 'Art' },
    { text: 'of' },
  ],
  [
    { text: 'Digital' },
    { text: 'Mastery', gold: true },
  ],
]

export default function Hero() {
  const reduce = useReducedMotion()

  // Parent orchestrates the staggered reveal of its children.
  const container = {
    hidden: {},
    show: {
      transition: {
        // No stagger / delay when reduced motion is requested.
        staggerChildren: reduce ? 0 : 0.1,
        delayChildren: reduce ? 0 : 0.15,
      },
    },
  }

  // Each word fades in and rises. Reduced motion → a plain fade, no travel.
  const word = {
    hidden: { opacity: 0, y: reduce ? 0 : '0.9em' },
    show: {
      opacity: 1,
      y: '0em',
      transition: { duration: reduce ? 0.2 : 0.9, ease: [0.22, 1, 0.36, 1] },
    },
  }

  const fade = {
    hidden: { opacity: 0, y: reduce ? 0 : 14 },
    show: {
      opacity: 1,
      y: 0,
      transition: { duration: reduce ? 0.2 : 0.9, ease: [0.22, 1, 0.36, 1] },
    },
  }

  return (
    <section className="relative flex min-h-[100svh] w-full items-center justify-center overflow-hidden bg-ink px-6">
      {/* ── Slow-pulsing gold radial glow, anchored behind the headline ── */}
      <motion.div
        aria-hidden="true"
        className="pointer-events-none absolute left-1/2 top-1/2 -z-0 h-[80vmin] w-[80vmin] -translate-x-1/2 -translate-y-1/2 rounded-full"
        style={{
          background:
            'radial-gradient(circle, rgba(212,175,55,0.16) 0%, rgba(212,175,55,0.06) 38%, rgba(212,175,55,0) 68%)',
        }}
        animate={
          reduce
            ? { opacity: 0.6 }
            : { opacity: [0.45, 0.85, 0.45], scale: [1, 1.08, 1] }
        }
        transition={
          reduce
            ? undefined
            : { duration: 4, ease: 'easeInOut', repeat: Infinity }
        }
      />

      {/* ── Centered content ── */}
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="relative z-10 mx-auto flex max-w-3xl flex-col items-center text-center"
      >
        {/* Eyebrow */}
        <motion.p
          variants={fade}
          className="mb-8 text-[0.7rem] font-light uppercase tracking-[0.42em] text-gold sm:text-xs"
        >
          Premium Digital Education
        </motion.p>

        {/* Headline — two lines, word-by-word reveal */}
        <h1 className="font-display text-[2.75rem] font-medium tracking-[0.04em] text-cream sm:text-6xl md:text-7xl md:tracking-[0.06em]">
          {HEADLINE.map((line, li) => (
            <span key={li} className="block leading-[1.08]">
              {line.map((w, wi) => (
                // Mask each word so it rises up from behind an invisible edge.
                <span
                  key={wi}
                  className="inline-block overflow-hidden align-bottom"
                >
                  <motion.span
                    variants={word}
                    className={`inline-block pb-[0.08em] ${
                      w.gold ? 'text-gold' : ''
                    }`}
                  >
                    {w.text}
                  </motion.span>
                  {/* Preserve spacing between words */}
                  {wi < line.length - 1 && <span>&nbsp;</span>}
                </span>
              ))}
            </span>
          ))}
        </h1>

        {/* Subheadline */}
        <motion.p
          variants={fade}
          className="mt-8 max-w-xl font-serifItalic text-lg italic leading-relaxed text-cream/60 sm:text-xl md:text-2xl"
        >
          An intimate academy where ambition is refined into craft — and craft
          into mastery.
        </motion.p>

        {/* Primary CTA — pill, gold border, transparent fill → fills gold on hover */}
        <motion.div variants={fade} className="mt-12">
          <a
            href="#apply"
            className="group relative inline-flex items-center justify-center overflow-hidden rounded-full border border-gold px-10 py-4 text-[0.72rem] font-light uppercase tracking-[0.28em] text-gold transition-colors duration-500 ease-out hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold/60 focus-visible:ring-offset-2 focus-visible:ring-offset-ink"
          >
            {/* Fill layer: sweeps up from transparent to solid gold on hover */}
            <span
              aria-hidden="true"
              className="absolute inset-0 -z-0 origin-bottom scale-y-0 bg-gold transition-transform duration-500 ease-[cubic-bezier(0.22,1,0.36,1)] group-hover:scale-y-100"
            />
            {/* Shimmer: a soft gold-light sweep across the button on hover */}
            <span
              aria-hidden="true"
              className="pointer-events-none absolute inset-0 -z-0 overflow-hidden"
            >
              <span className="absolute inset-y-0 left-0 w-1/3 -translate-x-[120%] skew-x-[-12deg] bg-gradient-to-r from-transparent via-white/40 to-transparent group-hover:animate-shimmer motion-reduce:group-hover:animate-none" />
            </span>
            <span className="relative z-10">Request an Invitation</span>
          </a>
        </motion.div>
      </motion.div>

      {/* ── Brand mark, quiet in the top-left ── */}
      <motion.div
        variants={fade}
        initial="hidden"
        animate="show"
        className="pointer-events-none absolute left-6 top-6 z-10 sm:left-10 sm:top-9"
      >
        <span className="font-display text-sm tracking-[0.24em] text-cream/80">
          {BRAND}
        </span>
      </motion.div>

      {/* ── Faint animated film grain over the whole background ── */}
      <GrainOverlay reduce={reduce} />
    </section>
  )
}

/**
 * A tiling SVG noise texture rendered as a fixed overlay. The texture drifts
 * on a slow loop (via the `grain` keyframes) unless reduced motion is set, in
 * which case it holds still at a low, static opacity.
 */
function GrainOverlay({ reduce }) {
  const noise =
    "data:image/svg+xml;utf8," +
    encodeURIComponent(
      `<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'>
        <filter id='n'>
          <feTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/>
          <feColorMatrix type='saturate' values='0'/>
        </filter>
        <rect width='100%' height='100%' filter='url(%23n)'/>
      </svg>`
    )

  return (
    <div
      aria-hidden="true"
      className={`pointer-events-none absolute inset-[-150%] z-20 opacity-[0.05] mix-blend-soft-light ${
        reduce ? '' : 'animate-grain'
      }`}
      style={{
        backgroundImage: `url("${noise}")`,
        backgroundRepeat: 'repeat',
      }}
    />
  )
}
