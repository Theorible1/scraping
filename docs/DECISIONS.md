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
| 10/11/2026 | Code publié sur GitHub, dépôt public `Theorible1/scraping`, tout le projet | Choix de Quentin : partager le code. GitHub Pages écarté (ne peut pas faire tourner du Python) |
| 10/11/2026 | E-mail perso remplacé par l'e-mail anonyme GitHub dans l'historique avant publication | Éviter d'exposer l'adresse gmail publiquement |
| 10/11/2026 | Projet déplacé dans `E:\BOT\Outils\scraping` | Demande de Quentin : regrouper les outils mis à disposition des agents dans `E:\BOT\Outils` |
| 10/11/2026 | Outil partagé entre PC perso et PC du bureau via GitHub : `synchroniser.bat` en début de session, `git push` après chaque commit | Demande de Quentin : deux PC sans dossier commun |
| 12/11/2026 | `SOUS_AGENT.md` : consignes réservées aux sous-agents ; conversation principale sur Opus 5.5, jamais de sous-agent Fable, deux sous-agents au maximum | Demande de Quentin : maîtriser le coût et éviter qu'un sous-agent suive les consignes de commit et de push du `CLAUDE.md` |
