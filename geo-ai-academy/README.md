# Geo AI Academy — Dark Luxury Hero

A full-viewport hero section for a premium digital-education brand. Editorial,
restrained, high-end — luxury fashion magazine, not tech startup.

**Stack:** React 18 · Tailwind CSS 3 · Framer Motion 11 · Vite

## Run it

```bash
cd geo-ai-academy
npm install
npm run dev      # http://localhost:5173
```

```bash
npm run build    # production bundle → dist/
npm run preview  # serve the build locally
```

## Design

| Token        | Value     | Use                                   |
| ------------ | --------- | ------------------------------------- |
| `bg` (ink)   | `#080808` | near-black background                 |
| `gold`       | `#D4AF37` | accent — emphasis only, used sparingly |
| `cream`      | `#F5F3EE` | warm text                             |

**Typography** — Playfair Display (headline), Cormorant Garamond italic
(subheadline), Montserrat light (body/labels). Loaded from Google Fonts in
`index.html`.

## Motion

All Framer Motion, all reduced-motion aware (`useReducedMotion` + a CSS
fallback in `src/index.css`):

- **Headline** — words fade + rise in, staggered 0.1s each on load.
- **Gold glow** — slow radial pulse behind the headline, 4s loop.
- **CTA** — transparent pill with a gold border that fills gold on hover, plus
  a soft gold shimmer that sweeps across.
- **Grain** — a faint animated film-noise texture over the whole background.

With `prefers-reduced-motion: reduce`, staggering and travel are removed
(content simply fades in), the glow holds a steady opacity, and the grain sits
still.

## Where to edit

Everything lives in `src/components/Hero.jsx`:

- `BRAND` — the brand name.
- `HEADLINE` — words per line; set `gold: true` on the one word to emphasise.
- The eyebrow, subheadline, and CTA copy/`href` are inline in the JSX.
