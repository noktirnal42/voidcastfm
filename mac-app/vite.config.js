import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

const PI_HOST = '192.168.1.25';
const PI_PORT = '8080';

export default defineConfig({
  plugins: [svelte()],
  base: './',
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: `http://${PI_HOST}:${PI_PORT}`,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        ws: true,
      },
      '/ws': {
        target: `ws://${PI_HOST}:${PI_PORT}`,
        ws: true,
      },
    },
  },
});
