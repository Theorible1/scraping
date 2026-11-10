# Statut : scraping

## Fait (10/11/2026)
- Structure du projet et fichiers de contexte.
- Version 0.1.0 de l'outil : `scraper.bat` + `src/scraper.py`.
  - Articles et blogs : texte principal en Markdown, titre, date, auteur, site.
  - Wikis MediaWiki via l'API officielle, titres de sections gardés, sommaire / bandeaux / références retirés.
  - Respect du robots.txt, pause de 2 s entre deux pages d'un même site, identification honnête.
  - Erreurs claires avec codes stables ; fichiers non HTML refusés sans téléchargement.
- Mode d'emploi pour les agents dans `README.md`.

## Vérifié
- 11 tests hors ligne : tous passent.
- Essais réels (10/11/2026) :
  - `finalfantasy.fandom.com/wiki/Job_system` : ok, 8 046 mots, sections présentes, méthode api_wiki.
  - `fr.wikipedia.org/wiki/Web_scraping` : ok, bandeau d'avertissement retiré.
  - Article `blog.python.org` : ok, date juste (26/10/2026).
  - Fichier `.exe` : refusé en ~1 s sans téléchargement. 404, domaine inexistant, page Cloudflare : bons codes d'erreur.

## Pas testé
- Utilisation réelle par un autre agent d'un autre projet.
- Sites d'actu français à gros trafic (pubs, cookies, paywall).

## Reste à faire
- Faire essayer l'outil par un agent d'un autre projet.
- Sites avec connexion.
- Pages construites en JavaScript.

## Questions ouvertes
- Quels sites avec connexion, et quel compte ?
- Quels sites d'actu / blogs Quentin lit vraiment (pour tester dessus) ?
