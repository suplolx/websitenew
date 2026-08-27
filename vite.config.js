import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import fs from 'fs'
import path from 'path'

function htmlInjectPlugin() {
  return {
    name: 'custom-html-inject',
    enforce: 'pre',
    transformIndexHtml(html) {
      const loadRegex = /<load\s+src=["']([^"']+)["']\s*\/?>/gi;
      return html.replace(loadRegex, (match, srcPath) => {
        const filePath = path.resolve(srcPath);
        if (fs.existsSync(filePath)) {
          return fs.readFileSync(filePath, 'utf-8');
        }
        console.warn(`[htmlInjectPlugin] File not found: ${filePath}`);
        return match;
      });
    },
    handleHotUpdate({ file, server }) {
      if (file.includes('src' + path.sep + 'components') || file.includes('src/components')) {
        server.ws.send({ type: 'full-reload' });
      }
    }
  }
}

export default defineConfig({
  plugins: [
    tailwindcss(),
    htmlInjectPlugin(),
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
        werken_bij: 'werken-bij.html',
        kapsalon: 'kapsalon.html'
      }
    }
  }
})
