/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        washi: '#F7F3EB',
        'washi-warm': '#FBF8F1',
        'sumi-charcoal': '#1E1D1C',
        'sumi-ink': '#2B2928',
        stone: '#57524c',
        indigo: '#223A5E',
        vermilion: '#C73E3A',
        gold: '#C9A96E',
        matcha: '#7A8B5E'
      },
      fontFamily: {
        'display-en': ['"Playfair Display"', 'serif'],
        'body-en': ['"Zen Kaku Gothic New"', 'sans-serif'],
        'display-ja': ['"Noto Serif JP"', 'serif'],
        'body-ja': ['"Zen Kaku Gothic New"', 'sans-serif']
      },
      maxWidth: {
        site: '1200px'
      }
    }
  },
  plugins: []
};
