import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
server: {
    host: true,
    port: 5173,
    allowedHosts: ['cau-evo2.shennong.cc']  // 添加允许的域名
  },
  preview: {
    host: true,
    port: 5173,
    allowedHosts: ['cau-evo2.shennong.cc'],  // preview模式也需要
    strictPort: true
  }
})
