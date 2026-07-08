/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        ink: '#080808',      // near-black background
        gold: '#D4AF37',      // accent — used sparingly
        cream: '#F5F3EE',     // warm cream text
      },
      fontFamily: {
        display: ['"Playfair Display"', 'serif'],           // headings
        serifItalic: ['"Cormorant Garamond"', 'serif'],     // subheadings, italic
        sans: ['Montserrat', 'system-ui', 'sans-serif'],    // body
      },
      letterSpacing: {
        widest2: '0.35em',
      },
      keyframes: {
        // A faint, ever-shifting film grain
        grain: {
          '0%,100%': { transform: 'translate(0,0)' },
          '10%': { transform: 'translate(-5%,-10%)' },
          '20%': { transform: 'translate(-15%,5%)' },
          '30%': { transform: 'translate(7%,-25%)' },
          '40%': { transform: 'translate(-5%,25%)' },
          '50%': { transform: 'translate(-15%,10%)' },
          '60%': { transform: 'translate(15%,0%)' },
          '70%': { transform: 'translate(0%,15%)' },
          '80%': { transform: 'translate(3%,-10%)' },
          '90%': { transform: 'translate(-10%,10%)' },
        },
        // The gold shimmer sweep across the CTA on hover
        shimmer: {
          '0%': { transform: 'translateX(-120%) skewX(-12deg)' },
          '100%': { transform: 'translateX(220%) skewX(-12deg)' },
        },
      },
      animation: {
        grain: 'grain 8s steps(6) infinite',
        shimmer: 'shimmer 1.1s ease-out',
      },
    },
  },
  plugins: [],
}
