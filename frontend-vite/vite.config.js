import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // 原有的端口: 5173
    // 修改為5位數冷門端口: 15173
    port: 15173,
    proxy: {
      '/api': {
        // 原有的端口: 8000
        // 修改為5位數冷門端口: 18000
        target: 'http://localhost:18000',
        changeOrigin: true
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
