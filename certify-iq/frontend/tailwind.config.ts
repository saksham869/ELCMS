import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: {
          base: "#030712",
          raised: "#0d1117",
          overlay: "#161b22",
          border: "#21262d",
          muted: "#30363d",
        },
        text: {
          primary: "#f0f6fc",
          secondary: "#8b949e",
          muted: "#6e7681",
          link: "#58a6ff",
        },
        accent: {
          blue: "#1f6feb",
          "blue-hover": "#388bfd",
          green: "#238636",
          "green-bright": "#3fb950",
          amber: "#9e6a03",
          "amber-bright": "#d29922",
          red: "#da3633",
          "red-bright": "#f85149",
          purple: "#6e40c9",
          "purple-bright": "#a371f7",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "Consolas", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;