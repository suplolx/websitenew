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
        contact: 'contact.html',
        bakkerij: 'bakkerij.html',
        beauty_salon: 'beauty-salon.html',
        creatief: 'creatief.html',
        horeca: 'horeca.html',
        ict_multimedia: 'ict-multimedia.html',
        techniek: 'techniek.html',
        fietsenmaker: 'fietsenmaker.html',
        werken_bij: 'werken-bij.html'
      }
    }
  }
})
