import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // Vendor chunks - separate large dependencies
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'framer-motion': ['framer-motion'],
          'markdown': ['react-markdown', 'remark-gfm'],
        },
      },
    },
    // Increase chunk size warning limit to 600kb (current size)
    chunkSizeWarningLimit: 600,
  },
})
