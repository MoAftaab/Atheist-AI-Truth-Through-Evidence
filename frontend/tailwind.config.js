/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#000000',
          light: '#1a1a1a',
          dark: '#000000',
        },
      },
      fontFamily: {
        arabic: ['Noto Sans Arabic', 'Arial', 'sans-serif'],
        display: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'pattern-dots': 'radial-gradient(circle, #000 1px, transparent 1px)',
      },
      backgroundSize: {
        'pattern-size': '20px 20px',
      },
    },
  },
  plugins: [],
  darkMode: 'class',
}


