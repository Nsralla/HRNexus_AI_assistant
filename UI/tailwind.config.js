/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#0A0A0A',
        accent: '#4A7DFF',
        neutral: '#F5F5F7',
        'card-white': '#FFFFFF',
      },
      fontFamily: {
        'sf-pro': ['SF Pro Display', 'Inter', 'system-ui', 'sans-serif'],
        'inter': ['Inter', 'system-ui', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '1rem',
      },
      boxShadow: {
        'soft': '0 4px 24px rgba(0, 0, 0, 0.06)',
        'hover': '0 8px 32px rgba(0, 0, 0, 0.12)',
      },
    },
  },
  plugins: [],
}
