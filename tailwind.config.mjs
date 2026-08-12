/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      colors: {
        // Legacy palette (kept for compatibility during transition)
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
        // Ligazon coalition palette
        ink: {
          950: "#0C1F16",
          900: "#163528",
          800: "#1F4636",
          700: "#2D5C48",
          600: "#426E58",
        },
        paper: {
          50: "#FBF7EE",
          100: "#F5EDDE",
          200: "#ECE0C9",
          300: "#DBC9A6",
        },
        clay: {
          50: "#FBEFE9",
          100: "#F4D4C5",
          200: "#E8A98F",
          300: "#D5764F",
          500: "#B5491C",
          600: "#993D17",
          700: "#7A2F11",
        },
        saffron: {
          50: "#FAF1DA",
          100: "#F4DFA8",
          200: "#ECC972",
          300: "#E3BC5A",
          500: "#D4A23E",
          600: "#B0832B",
          700: "#836018",
        },
        moss: {
          50: "#E6EFE9",
          100: "#BDD5C5",
          300: "#5C8A72",
          400: "#3A6B52",
          500: "#1E4A37",
          600: "#173A2B",
          700: "#0F2C1F",
        },
        maroon: {
          50: "#F7E5E8",
          100: "#ECC3CB",
          200: "#C68490",
          300: "#A85365",
          400: "#8E2E3C",
          500: "#7A2632",
          700: "#4F1820",
        },
        gold: {
          400: "#D8A93B",
          500: "#B0832B",
          600: "#8C6720",
          700: "#6B4E18",
        },
      },
      fontFamily: {
        display: ["Newsreader", "Iowan Old Style", "Georgia", "Times New Roman", "serif"],
        ui: ["Space Grotesk", "Geist", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        body: ["Newsreader", "Iowan Old Style", "Georgia", "Times New Roman", "serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "Menlo", "monospace"],
      },
    },
  },
  plugins: [],
};
