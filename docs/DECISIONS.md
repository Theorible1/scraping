# Décisions : scraping

On n'efface jamais, on ajoute.

| Date | Décision | Pourquoi |
|---|---|---|
| 10/11/2026 | Structure créée selon A_LIRE_AVANT_TOUT_PROJET.md | Mêmes règles que les autres projets de E:\BOT |
| 10/11/2026 | Nom du dossier : `scraping` (minuscules) | Demande de Quentin, pas d'accent ni d'espace |
| 10/11/2026 | Déclenchement à la demande uniquement | Choix de Quentin, le plus simple pour démarrer |
| 10/11/2026 | Python + httpx (téléchargement) + trafilatura (extraction d'articles) + markdownify (wikis) | Python déjà utilisé (bot-courses) ; trafilatura est la référence pour isoler le texte principal d'un article |
| 10/11/2026 | Sortie Markdown par défaut, JSON en option | Le Markdown est le format que les agents lisent le mieux ; le JSON pour les programmes |
| 10/11/2026 | Interface principale : `scraper.bat` en ligne de commande | Utilisable par n'importe quel agent sans partager d'environnement Python |
| 10/11/2026 | Wikis MediaWiki lus via l'API officielle (`api.php`) | Fandom bloque la page normale par Cloudflare ; l'API est prévue pour les programmes, c'est la voie légitime. Elle ne passe pas par le contrôle robots.txt (règle des robots d'indexation), mais respecte les usages de l'API (identification, pause, maxlag) |
| 10/11/2026 | Pas de contournement des protections anti-robot | Respect des sites, risque de blocage ; erreur claire `protection_anti_robot` à la place |
| 10/11/2026 | Connexion aux sites reportée à une étape suivante | Faire d'abord marcher les pages publiques |
| 10/11/2026 | Projet déplacé dans `E:\BOT\Outils\scraping` | Demande de Quentin : regrouper les outils mis à disposition des agents dans `E:\BOT\Outils` |
