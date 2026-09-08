# Nette URL's in Nginx

Open op de VPS de Nginx-siteconfiguratie die het `server`-blok voor `kr8tig.nl` bevat. Voeg de inhoud van `clean-urls.conf` toe binnen dat blok. Vervang daarbij een bestaande algemene `location /` door de versie uit dit bestand, zodat er maar één `location /` overblijft.

Controleer en laad Nginx daarna opnieuw:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

De website kan vervolgens intern nog steeds losse HTML-bestanden uit `dist/` gebruiken, terwijl bezoekers `/afdelingen` zien. Oude adressen als `/afdelingen.html` sturen permanent door naar `/afdelingen`.
