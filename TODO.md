# scraping : à faire

## Où on en est (mis à jour le 13/11/2026)
- État : version 0.1.0 fonctionnelle (10/11/2026) : `scraper.bat <adresse>` rend le texte propre d'une page (articles, blogs, wikis via API). 11 tests hors ligne passent, essais réels ok (voir « Fait récemment »). Mode d'emploi pour les agents dans `README.md`. Projet déplacé dans `E:\BOT\Outils\scraping` le 10/11/2026.
- Prochaine étape : au choix de Quentin : tester sur les sites d'actu et blogs qu'il lit vraiment, gérer les sites avec connexion (lui demander lesquels), ou les pages construites en JavaScript.
- Points d'attention : lancer Python via `.venv\Scripts\python.exe`, pas le Python global. trafilatura jette les titres des wikis, d'où markdownify pour les wikis. Décisions : Python + httpx + trafilatura + markdownify, sortie Markdown par défaut ; wikis via l'API officielle (Fandom bloque la page normale par Cloudflare) ; aucun contournement de protection anti-robot. Pas encore testé : utilisation réelle par un autre agent, sites d'actu français à gros trafic (pubs, cookies, paywall).

## En cours
- Aucune tâche en cours (dernière session le 10/11/2026 : la suite est au choix de Quentin).

## À faire (par ordre de priorité)
- [ ] Faire essayer l'outil par un agent d'un autre projet et relever ce qui gêne (Claude, avec l'accord de Quentin sur le projet)
- [ ] Gérer les sites avec connexion (cadrer d'abord avec Quentin lesquels ; voir En attente)
- [ ] Gérer les pages construites en JavaScript

## En attente
- [ ] Sites avec connexion : attend de Quentin la liste des sites et le compte à utiliser
- [ ] Test sur les sites d'actu et blogs que Quentin lit : attend de Quentin la liste de ces sites (pas encore testé : gros trafic, pubs, cookies, paywall)

## Fait récemment
- [x] 10/11/2026 : version 0.1.0 de `scraper.bat` (vérifié : 11 tests hors ligne passent)
- [x] 10/11/2026 : wiki Fandom `Job_system` (vérifié : 8 046 mots, sections présentes, méthode api_wiki)
- [x] 10/11/2026 : `fr.wikipedia.org/wiki/Web_scraping` (vérifié : bandeau d'avertissement retiré)
- [x] 10/11/2026 : article `blog.python.org` (vérifié : date juste, 26/10/2026)
- [x] 10/11/2026 : fichier `.exe` refusé sans téléchargement (vérifié : refus en environ 1 s ; 404, domaine inexistant et page Cloudflare donnent les bons codes d'erreur)

Historique détaillé avant le 13/11/2026 : `_archives\refonte_2026-11-13\` (STATUT.md, REPRISE_SESSION.md, ARBORESCENCE.md).
