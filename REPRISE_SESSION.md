# Reprise de session : scraping

**Date : 10/11/2026**

## Où on en est
Version 0.1.0 fonctionnelle : `scraper.bat <adresse>` rend le texte propre d'une page (articles, blogs, wikis via API). 11 tests passent, essais réels ok (voir STATUT.md). Mode d'emploi pour les agents dans README.md.

## Prochaine étape
Au choix de Quentin :
1. Tester sur les sites d'actu / blogs qu'il lit vraiment.
2. Gérer les sites avec connexion (lui demander lesquels).
3. Pages construites en JavaScript.

## Décisions récentes
- Python + httpx + trafilatura + markdownify ; sortie Markdown par défaut.
- Wikis via API officielle (Fandom bloque la page normale par Cloudflare).
- Aucun contournement de protection anti-robot.

## Pièges
- Lancer Python via `.venv\Scripts\python.exe`, pas le Python global.
- trafilatura jette les titres des wikis : c'est pour ça que les wikis passent par markdownify.
