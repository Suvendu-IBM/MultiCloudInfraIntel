import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy all /api/* requests to the FastAPI backend during development.
      // The backend runs on port 8001; mcp_server.py runs on 8000.
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
})
