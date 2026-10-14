import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// The browser only ever calls relative /api/... URLs. Vite forwards them to the backend,
// so there is no hardcoded host/port and no CORS problem in development.
const backend = process.env.VITE_BACKEND_URL || 'http://127.0.0.1:9000'

export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: Number(process.env.VITE_PORT) || 5300,
    proxy: {
      '/api': { target: backend, changeOrigin: true },
    },
  },
})
