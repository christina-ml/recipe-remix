/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        crust: "#FBF6EE",
        char: "#2B2320",
        spice: "#B8842A",
        sage: "#4F6B4C",
        rust: "#9C4A3A",
        line: "#E4DAC8",
      },
      fontFamily: {
        display: ["'Fraunces'", "serif"],
        body: ["'Inter'", "sans-serif"],
      },
    },
  },
  plugins: [],
}
