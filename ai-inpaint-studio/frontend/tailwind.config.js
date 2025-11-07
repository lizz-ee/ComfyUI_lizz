/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // VSCode-inspired dark theme
        'bg-primary': '#1e1e1e',
        'bg-secondary': '#252526',
        'bg-tertiary': '#2d2d30',
        'border': '#3e3e42',
        'text-primary': '#cccccc',
        'text-secondary': '#858585',
        'accent': '#007acc',
        'accent-hover': '#005a9e',
        'success': '#4ec9b0',
        'error': '#f48771',
        'warning': '#cca700',
      },
    },
  },
  plugins: [],
}
