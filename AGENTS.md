# Kr8tig Website — Agent Richtlijnen

## Projectoverzicht

Dit is de website van **Kr8tig**, een zorgorganisatie in Weert (Limburg) die jongeren begeleidt via arbeidsmatige dagbesteding en interne/ambulante begeleiding. De website presenteert de organisatie, haar afdelingen, het team en contactinformatie aan verwijzers, bezoekers en potentiële deelnemers.

- **Doel**: Informatieve bedrijfswebsite voor een zorginstelling
- **Doelgroep**: Verwijzers (gemeenten, zorginstellingen), bezoekers, potentiële deelnemers en hun omgeving
- **Taal**: Alle content is in het **Nederlands**
- **Hosting**: Ubuntu VPS (`45.10.16.142`) met Nginx & Let's Encrypt SSL (`https://kr8tig.nl`)

## Tech Stack

| Technologie       | Versie / Details                          |
| ----------------- | ----------------------------------------- |
| **Build tool**    | Vite 8.x (`vite-plugin-html-inject`)      |
| **CSS framework** | Tailwind CSS 4.x (via `@tailwindcss/vite` plugin) |
| **PostCSS**       | autoprefixer + postcss                    |
| **Fonts**         | Plus Jakarta Sans, Outfit, Inter (Google Fonts) |
| **Hosting**       | Ubuntu VPS met Nginx (`/var/www/kr8tig`)  |
| **Module type**   | ES Modules (`"type": "module"`)           |

## Projectstructuur

```
websitenew/
├── index.html              # Homepage
├── afdelingen.html         # Overzicht van alle afdelingen
├── bakkerij.html           # Afdeling: Bakkerij
├── beauty-salon.html       # Afdeling: Schoonheidssalon Pr8tig
├── creatief.html           # Afdeling: Creatief
├── fietsenmaker.html       # Afdeling: Fietsenmaker
├── horeca.html             # Afdeling: Horeca
├── ict-multimedia.html     # Afdeling: ICT & Multimedia
├── techniek.html           # Afdeling: Techniek
├── verwijzers.html         # Informatie voor verwijzers + intake-formulier
├── over-ons.html           # Over Kr8tig
├── team.html               # Het team
├── contact.html            # Contactpagina
├── src/
│   ├── components/         # Herbruikbare HTML componenten
│   │   ├── head-common.html # Centrale head-tags (meta, fonts, favicons, stylesheet link)
│   │   ├── header.html     # Centrale navigatiebalk & mobiel menu
│   │   └── footer.html     # Centrale footer
│   ├── main.js             # Gedeelde JavaScript (navigatie, scroll, formulier)
│   └── style.css           # Hoofd-stylesheet (Tailwind + custom CSS)
├── assets/
│   ├── logo.png            # Kr8tig logo
│   ├── banners/            # Hero banner afbeeldingen
│   │   ├── banner.jpg
│   │   └── banner.png
│   ├── keurmerken/         # Keurmerk/certificering logo's
│   │   ├── keurmerk 1.jpg
│   │   ├── keurmerk 2.png
│   │   └── keurmerk 3.png
│   ├── personeel/          # Teamfoto's per medewerker (en initialen-avatars)
│   └── afdelingen/         # Afdelingsspecifieke afbeeldingen (geselecteerd/gecomprimeerd)
├── scripts/                # Python scripts en fonts
│   ├── compress_images.py  # Script voor afbeeldingencompressie (in prebuild)
│   ├── generate_initial.py # Script om initialen-avatars te genereren
│   └── fonts/
│       └── Outfit-Bold.ttf # Font gebruikt door generate_initial.py
├── teksten/                # Markdown bronbestanden met paginateksten
│   ├── afdelingen.md
│   ├── bakkerij.md
│   ├── Beauty.md
│   ├── horeca.md
│   ├── fietsenwerkplaats.md
│   ├── techniek.md
│   └── Multimedia-ICT.md
├── public/
│   ├── favicon.svg
│   └── icons.svg
├── vite.config.js          # Vite configuratie met multi-page input
└── package.json
```

## Design Systeem & Stijlregels

### Kleuren

- **Primary**: `#791b5c` (diep paars/magenta — Kr8tig huisstijlkleur)
- **Primary Light**: `#9c2878`
- **Secondary**: `#333333`
- **Achtergrond**: `#fafafa` (lichtgrijs)
- **Tekst**: `#0f172a` (donker slate)

### Typografie

- **Body**: `Plus Jakarta Sans` (fallback: Inter, system-ui)
- **Headings**: `Outfit` (fallback: Inter, system-ui)
- Headings gebruiken `letter-spacing: -0.02em` voor een strakke look

### Design Patronen

- **Glassmorphism** navigatiebalk met `backdrop-blur` en semi-transparante achtergronden
- **Scroll-afhankelijke header**: transparant op hero, wit/ondoorzichtig na scrollen
- **Subpage-variant**: subpagina's zonder hero krijgen direct een witte navigatiebalk
- **Scroll reveal animaties** via Intersection Observer (`.reveal-hidden` → `.reveal-visible`)
- **Hover effecten** op kaarten: subtiele lift (`-translate-y-2`), kleurovergang, schaduw
- **Ambient glows**: Radial gradient pseudo-elementen op `body` als achtergrond-accenten

### CSS Architectuur

De hoofd-stylesheet (`style.css` in de root) combineert:

1. Google Fonts import
2. `@import "tailwindcss"` (Tailwind v4 syntax)
3. `@theme` blok voor custom design tokens (kleuren, fonts)
4. Custom CSS classes voor animaties, navigatie, en pagina-specifieke stijlen

Alle custom styling staat in `src/style.css`.

## JavaScript Architectuur

Alle pagina's laden `src/main.js` als ES module. Dit bestand bevat:

1. **Navbar scroll logic**: Header class-toggling op basis van scroll-positie
2. **Subpage detection**: Herkent pagina's zonder hero-sectie voor alternatieve nav-styling
3. **Mobile menu toggle**: Hamburger menu open/dicht met body scroll-lock
4. **Scroll reveal**: Intersection Observer voor fade-in animaties
5. **Intake formulier**: `mailto:` handler voor het verwijzers-formulier

## Conventies & Regels

### Algemeen

- **Taal**: Alle UI-tekst, labels, knoppen en content moeten in het **Nederlands** zijn
- **Multi-page app**: Dit is géén SPA — elke pagina is een apart HTML-bestand met gedeelde head, navigatie en footer
- **Centrale componenten**: Staan in `src/components/` en worden via Vite HTML injection geladen:
  - `src/components/head-common.html`: Centrale `<head>` tags (meta charset/viewport, Google Fonts, favicons, stylesheet link). Geladen via `<load src="./src/components/head-common.html" />` binnen `<head>`.
  - `src/components/header.html`: Centrale navigatiebalk & mobiel menu, geladen via `<load src="./src/components/header.html" />`.
  - `src/components/footer.html`: Centrale footer, geladen via `<load src="./src/components/footer.html" />`.
- Bij aanpassingen aan meta tags, favicons, fonts, navigatie of footer: **wijzig uitsluitend het betreffende component-bestand in `src/components/`**

### HTML

- Gebruik `lang="nl"` op het `<html>` element
- Elke pagina heeft een eigen `<title>` en importeert `./src/components/head-common.html` via `<load src="..." />`
- Elke pagina importeert `./src/main.js` via `<script type="module">`
- Semantische HTML5-elementen: `<header>`, `<section>`, `<footer>`, `<nav>`
- Pagina's met een full-screen hero-sectie gebruiken class `relative h-screen`
- Subpagina's zonder hero gebruiken een `pt-32` spacer na de header

### CSS / Tailwind

- Gebruik Tailwind v4 utility classes in HTML
- Custom stijlen toevoegen in `src/style.css`
- Tailwind theme tokens staan in het `@theme` blok in `src/style.css`
- Gebruik de bestaande `--color-primary` en `--color-primary-light` variabelen
- Behoud de bestaande animatie-classes: `animate-fade-in-up`, `reveal-hidden`, `reveal-visible`

### Afbeeldingen

- Sla afbeeldingen op in `assets/`
- Teamfoto's in `assets/personeel/`
- Afdelingsspecifieke afbeeldingen in `assets/afdelingen/`
- Gebruik relatieve paden: `./assets/...`
- **Let op grote bestandsgroottes** — veel foto's zijn 10+ MB. Optimaliseer nieuwe afbeeldingen. In `scripts/` staat `compress_images.py` om afbeeldingen te verkleinen (max. 1200px) en te comprimeren. Dit script wordt automatisch uitgevoerd vóór de build.
- **Initialen-afbeeldingen genereren (Avatars)**: Als een medewerker geen foto heeft, kan een initialen-avatar worden gegenereerd met het script `scripts/generate_initial.py`.
  - Gebruik het commando:
    ```bash
    py scripts/generate_initial.py -i <INITIALEN> -o assets/personeel/<Naam>.png --start-color "<HEX_START>" --end-color "<HEX_END>"
    ```
  - **Kleurtheorie & Gradients**: Zorg ervoor dat de gekozen kleuren (start- en end-color) harmonieus bij elkaar passen (kleurtheorie) en voldoende contrast hebben (vermijd kleuren die te dicht bij elkaar liggen, zodat het niet op één egale kleur lijkt). Stem de verloopkleuren af op de betreffende afdeling:
    - *Techniek*: Oranje gradients (bijv. `#f97316` naar `#c2410c`)
    - *Bakkerij*: Amber/geel-oranje gradients (bijv. `#fbbf24` naar `#b45309`)
    - *Horeca*: Rose/rood gradients (bijv. `#fb7185` naar `#be123c`)
    - *ICT & Multimedia*: Blauw gradients (bijv. `#60a5fa` naar `#1d4ed8`)
    - *Beauty / Kapsalon*: Roze/magenta gradients (bijv. `#fda4af` naar `#9d174d`)
    - *Creatief*: Paars/violet gradients (bijv. `#c084fc` naar `#701a75`)
    - *Algemeen / Begeleiding*: Kr8tig plum gradients (bijv. `#fda4af` naar `#791b5c`)

### Content

- Bronteksten voor afdelingspagina's staan als Markdown in `teksten/`
- Raadpleeg deze bestanden bij het aanpassen van paginateksten
- Houd de warme, persoonlijke tone of voice aan die past bij een zorgorganisatie

### Vacaturebeheer ("Werken bij Kr8tig")

De pagina `werken-bij.html` toont actieve vacatures of een lege status als er geen openstaande vacatures zijn.

- **Actieve vacatures tonen**:
  - Voeg vacature-kaarten toe in de div met `id="active-vacancies-section"`.
  - Zorg ervoor dat `id="active-vacancies-section"` **geen** `hidden` klasse heeft.
  - Zorg ervoor dat `id="no-vacancies-section"` (de lege status) **wel** de `hidden` klasse heeft.
- **Geen openstaande vacatures (Lege status)**:
  - Zorg ervoor dat `id="active-vacancies-section"` de `hidden` klasse heeft.
  - Zorg ervoor dat `id="no-vacancies-section"` **geen** `hidden` klasse heeft.
- **Ontwerp van vacatures**:
  - Gebruik interactieve accordeon-kaarten met de klasse `vacancy-card`.
  - De header-knop moet de klasse `vacancy-header` hebben.
  - De details-container moet de klassen `vacancy-details hidden border-t border-slate-200/60 p-6 sm:p-8 bg-white/50` hebben.
  - De details worden automatisch in- en uitgeklapt door de click listeners in `src/main.js`.
- **Geen open sollicitaties**:
  - Er is geen algemene open sollicitatie-optie of CTA meer op de pagina. Richt je uitsluitend op specifieke actieve vacatures of de lege status.

## Build & Deployment

De website draait op een Ubuntu VPS met Nginx.

### Lokale Ontwikkeling

```bash
# Ontwikkelserver starten (Windows PowerShell: npm.cmd)
npm run dev

# Productie-build genereren en lokaal testen
npm run build
npm run preview
```

### Wijzigingen Live Zetten op de VPS

Na het pushen van wijzigingen naar GitHub (`git push origin main`), log in op de VPS via SSH (`ssh root@45.10.16.142`) en voer uit:

```bash
cd /var/www/source && bash deploy.sh
```

*(Of via npm op de server: `cd /var/www/source && npm run deploy`). Dit script haalt de nieuwste code op, bouwt de website en kopieert de bestanden direct naar `/var/www/kr8tig/`.*

### Vite Build Configuratie

Alle HTML-pagina's zijn als **multi-page input** geconfigureerd in `vite.config.js`. Bij het toevoegen van een nieuwe pagina:

1. Maak het HTML-bestand aan in de root
2. Voeg een entry toe aan `build.rollupOptions.input` in `vite.config.js`
3. Voeg de pagina toe aan de navigatie in **alle** HTML-bestanden

## Git & Samenwerkings-Workflow

Als AI-agent werk je nauw samen met de gebruiker en eventueel andere ontwikkelaars. Volg daarom strikt deze Git workflow:

### 1. Altijd eerst Pullen (Start of Session)
Voordat je begint met het analyseren van code of het maken van wijzigingen bij de allereerste gebruikersvraag:
*   Haal **altijd** eerst de nieuwste wijzigingen op van GitHub om merge conflicten te voorkomen:
    ```bash
    git pull origin main
    ```

### 2. Branching Strategie
*   **Kleine/Directe wijzigingen:** (Bijvoorbeeld: tekstuele wijzigingen, kleine CSS tweaks, bugfixes). Deze mogen direct op de `main` branch worden uitgevoerd.
*   **Grote/Architecturale wijzigingen:** (Bijvoorbeeld: structuurwijzigingen, nieuwe grote functionaliteiten of ingrijpende refactors).
    1.  Maak een feature branch aan: `git checkout -b feature/naam-van-wijziging`.
    2.  Voer de taken uit en commit lokaal.
    3.  Controleer de build (`npm run build`).
    4.  Samenvoegen: Schakel terug naar `main` (`git checkout main`), doe een pull (`git pull origin main`), merge de branch (`git merge feature/naam-van-wijziging`) en push het resultaat (`git push origin main`).

### 3. Commits & Pushen
*   **Commit Berichten:** Gebruik duidelijke, beschrijvende commit-berichten (bij voorkeur Conventional Commits zoals `feat: ...`, `fix: ...`, `refactor: ...`).
*   **Bestanden toevoegen:** Stage alle actieve wijzigingen (`git add .`), maar let op dat tijdelijke bestanden en build-bestanden (zoals `dist/`) uitgesloten blijven via `.gitignore`.
*   **Pushen:** Push je wijzigingen na afronding direct naar GitHub (`git push origin main`), zodat de code direct beschikbaar is voor andere computers en ontwikkelaars.

## Contactgegevens (voor content referentie)

- **Organisatie**: Kr8tig
- **Adres**: Parallelweg 169, 6001 HM Weert (locatie: Perron 8)
  - *Let op*: Het officiële post-/hoofdadres en de locatie van bepaalde afdelingen (Beauty, Techniek, ICT) en de footer-verwijzingen is **Parallelweg 169**.
  - In lopende teksten en bij specifieke ingangen (centrale hal van Perron 8, Bakkerij Broodnodig, de Horeca en de Fietsenwerkplaats) wordt de ingang **Parallelweg 168** gebruikt. Wijzig deze nummers niet zomaar in elkaar, dit is opzettelijk zo verdeeld.
- **E-mail**: info@kr8tig.nl
- **Socials**: Instagram (@kr8tig.nl), LinkedIn (kr8tig), Facebook (kr8tig.nl)
