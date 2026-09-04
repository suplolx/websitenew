#!/bin/bash
set -e

echo "🚀 Website updaten op de VPS..."

# Ga naar de source directory
cd /var/www/source

# Haal de nieuwste wijzigingen op
echo "📥 Wijzigingen ophalen van GitHub..."
git pull origin main

# Voer build uit
echo "🔨 Productie-build genereren..."
npm run build

# Kopieer de gebouwde bestanden naar de webserver-map
echo "📁 Bestanden kopiëren naar /var/www/kr8tig/..."
cp -r dist/* /var/www/kr8tig/

echo "✅ Klaar! De website staat live op https://kr8tig.nl"
