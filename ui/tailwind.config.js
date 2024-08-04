/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: { 
      colors: {
      'accent': 'blue-500'
      },
    },
  },
  plugins: [
    require('tailwind-scrollbar'),
  ],
}

