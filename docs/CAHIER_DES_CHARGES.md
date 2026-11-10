# Cahier des charges : scraping

## But
Un outil commun qui récupère des informations sur le web et les rend propres et structurées, pour les autres agents et projets de `E:\BOT`.

## Utilisateurs
- Les agents Claude des autres projets.
- Quentin, ponctuellement.

## Pages visées (réponses de Quentin, 10/11/2026)
- N'importe quelle page, en priorité articles d'actu et blogs.
- Wikis (premier test : `https://finalfantasy.fandom.com/wiki/Job_system`).
- Certains sites demandent une connexion : à traiter dans une étape suivante.

## Fonctions
- À la demande : un agent donne une ou plusieurs adresses, l'outil répond tout de suite. (Pas d'automatique pour l'instant.)
- Sortie Markdown (défaut), JSON ou texte, à l'écran ou dans un fichier.
- Messages d'erreur clairs avec un code stable (voir README).
- Wikis MediaWiki lus via leur API officielle.

## Plus tard (non fait)
- Sites avec connexion (compte de Quentin).
- Pages construites en JavaScript (navigateur automatisé).
- Cache, suivi des liens, extraction de données précises (prix, tableaux).

## Hors périmètre
- Contourner une connexion, un paywall, un captcha ou une protection anti-robot.
- Collecter des données personnelles de particuliers.
- Ignorer les conditions d'utilisation ou le `robots.txt` d'un site.
