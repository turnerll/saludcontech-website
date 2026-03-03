/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      colors: {
        purple: {
          DEFAULT: "#6B5CE7",
          50: "#F5F3FF",
          100: "#EDE9FE",
          200: "#DDD6FE",
          300: "#C4B5FD",
          400: "#A78BFA",
          500: "#6B5CE7",
          600: "#5B4BD3",
          700: "#4C3DBF",
          800: "#3D2FA0",
          900: "#2E2280",
        },
        navy: {
          DEFAULT: "#1A1A2E",
          50: "#F0F0F4",
          100: "#E1E1E9",
          700: "#2A2A44",
          800: "#222238",
          900: "#1A1A2E",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
      },
    },
  },
  plugins: [],
};
