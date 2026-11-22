import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath, URL } from "node:url";

// En développement, le serveur Vite relaie les requêtes vers l'API locale.
const api = process.env.VITE_API_PROXY ?? "http://127.0.0.1:8000";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
  server: {
    port: 5173,
    proxy: {
      "/api": api,
      "/health": api,
      "/version": api,
    },
  },
  // Ne pas livrer de carte de sources dans le bundle de production.
  build: { sourcemap: false, chunkSizeWarningLimit: 900 },
});
