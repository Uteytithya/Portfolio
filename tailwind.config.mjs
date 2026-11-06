/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      // Mirrors the tokens in src/styles/global.css. Kept in step by hand:
      // the CSS variables are the source of truth, these are the Tailwind
      // utilities that need the same values at build time.
      colors: {
        void: '#0b0c0e',
        'steel-deep': '#0f1113',
        steel: '#15181c',
        'steel-raised': '#1d2127',
        bone: '#e6e8ea',
        ash: '#a6adb5',
        'ash-faint': '#878d96',
        volt: '#e8dc55',
        'volt-ink': '#8f8620',
        signal: '#4dd8e8',
        alert: '#ff4d3d'
      },
      fontFamily: {
        // One family carries the site. The old display-en / display-ja serif
        // entries pointed at Playfair Display and Noto Serif JP, neither of
        // which was still loaded.
        sans: ['"Zen Kaku Gothic New"', 'sans-serif'],
        display: ['Oxanium', '"Zen Kaku Gothic New"', 'sans-serif'],
        mono: ['ui-monospace', '"SF Mono"', 'Menlo', 'Consolas', 'monospace']
      },
      maxWidth: {
        site: '1200px'
      }
    }
  },
  plugins: []
};
