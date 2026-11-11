import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    // PWA (parte do Rodrigo): instalação, ícone neutro e funcionamento offline.
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'Elo',
        short_name: 'Elo', // nome que aparece na tela inicial: nunca o nome da doença
        description: 'Seu cuidado, dia a dia',
        lang: 'pt-BR',
        display: 'standalone',
        theme_color: '#5B2A86',
        background_color: '#F6F3FA',
        icons: [
          // TODO (Rodrigo): gerar public/icons/elo-192.png e public/icons/elo-512.png
          // { src: '/icons/elo-192.png', sizes: '192x192', type: 'image/png' },
          // { src: '/icons/elo-512.png', sizes: '512x512', type: 'image/png' },
        ],
      },
    }),
  ],
})
