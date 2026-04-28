import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    tailwindcss(),
  ],
  build: {
    rollupOptions: {
      input: {
        main: 'index.html',
        afdelingen: 'afdelingen.html',
        verwijzers: 'verwijzers.html',
        over_ons: 'over-ons.html',
        team: 'team.html',
        contact: 'contact.html'
      }
    }
  }
})
