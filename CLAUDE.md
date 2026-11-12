# Projet scraping : consignes permanentes pour Claude Code

Outil de scraping (récupération automatique d'informations sur des sites web) destiné à être utilisé par les autres agents et projets de Quentin dans `E:\BOT`. Démarré le 10/11/2026. Le périmètre et la technologie se précisent dans `docs/CAHIER_DES_CHARGES.md`.

L'utilisateur (Quentin) parle français et n'est pas technicien : réponses en **français**, consignes courtes, **une action à la fois**, noms exacts des menus et boutons. Ton de pote (tutoiement, un peu d'humour ok), rigueur intacte. Il veut de l'autonomie : ne pas poser de question à chaque étape, mais demander avant toute action irréversible. Quand il doit remplacer un fichier, lui donner le fichier **complet**.

## Au début de chaque session
0. **Se mettre à jour** : `& E:\BOT\synchroniser.bat` (l'outil est partagé entre le PC perso et le PC du bureau via GitHub). Traiter toute ligne `[!!]` avant de travailler.
1. Lire `REPRISE_SESSION.md` et `TODO.md`.
2. Seulement si besoin : `STATUT.md`, `docs/DECISIONS.md`, `docs/ARBORESCENCE.md`, `docs/CAHIER_DES_CHARGES.md`.
3. Si un document contredit l'état réel des fichiers, l'état réel prime : le signaler.

## À la fin de chaque étape
1. Lancer les tests ; pour tout changement visible, regarder le résultat réel (fichier produit, sortie lue).
2. Mettre à jour `STATUT.md`.
3. Nouvelle décision : une ligne datée dans `docs/DECISIONS.md`.
4. Nouveau dossier ou fichier important : mettre à jour `docs/ARBORESCENCE.md`.
5. Étape validée : sauvegarde git (`git add -A` puis `git commit -m "<ce qui a été fait, en français>"`). Étape validée = un commit avec un message en français.
6. **Publier en ligne** : `git push`, tout de suite. Une modification commitée mais pas poussée n'est pas terminée (l'autre PC ne la verra pas).

## À la fin de chaque session (« on s'arrête », « fin de session »)
- Réécrire `REPRISE_SESSION.md` (une page max, date du jour).

## Hygiène de session
- Appliquer la section « hygiène de session » de `E:\BOT\A_LIRE_AVANT_TOUT_PROJET.md` : surveiller la taille du contexte, rappeler à Quentin `/compact` (avant une pause) et `/clear` (changement de sujet).
- Si le contexte devient trop lourd : tout mettre à jour (REPRISE_SESSION, STATUT, DECISIONS, ARBORESCENCE, mémoire), puis proposer un prompt de redémarrage à coller dans une nouvelle conversation.
- Quentin apprend à le faire seul : expliquer en une phrase pourquoi c'est le moment, et lui signaler après coup s'il aurait dû faire `/clear` ou `/compact` plus tôt (sans reproche). Voir « Apprendre à Quentin quand faire `/clear` ou `/compact` » dans le A_LIRE.

## Modèle et sous-agents
- Conversation principale sur Opus 5.5. Appliquer la section « choix du modèle et délégation aux sous-agents » de `E:\BOT\A_LIRE_AVANT_TOUT_PROJET.md` : fragmenter la demande, faire soi-même ce qui est petit ou lié à la discussion, confier les étapes longues et séparables à un sous-agent `haiku` ou `sonnet` (tableau de référence du A_LIRE), vérifier son retour, dire à Quentin ce qui a été délégué et à quel modèle.
- Jamais de sous-agent Fable (seul Quentin choisit Fable, à la main). Deux sous-agents en même temps au maximum. Toujours écrire le paramètre `model`.
- Chaque consigne de sous-agent commence par : « Lis d'abord `<chemin du projet>\SOUS_AGENT.md` en entier et respecte-le. » Tout interdit ajouté ici est reporté dans `SOUS_AGENT.md`.
- Aucune action irréversible ou vers l'extérieur (commit, push, mise en ligne, suppression) n'est déléguée.

## Règles absolues
- Rien n'est « fait » sans valeur attendue ET valeur lue. Dire ce qui est fait / testé / pas testé.
- Ne rien supprimer sans accord explicite : ce qui ne sert plus va dans `_archives/`.
- Les choix de fond (sites visés, données récupérées, format) appartiennent à Quentin : proposer, argumenter, le laisser trancher.
- Pas de tiret long dans les textes produits.
- Scraping responsable : respecter les conditions d'utilisation et le `robots.txt` des sites, aller doucement (pause entre deux requêtes), pas de contournement de connexion, de paywall ou de captcha, pas de collecte de données personnelles de particuliers.
- Secrets (identifiants, clés) uniquement dans `.env`, jamais affichés ni commités.
- L'outil doit rester simple à appeler par un autre agent : une interface stable et documentée dans `README.md`.

## Technique
- Windows 10, PowerShell 5.1 (pas de `&&`), VS Code + Claude Code.
- Python 3.14 installé. Git 2.56 (si `git` n'est pas reconnu : `& "C:\Program Files\Git\cmd\git.exe"`). Dépôt **public** en ligne : https://github.com/Theorible1/scraping (publié le 10/11/2026 avec l'accord de Quentin, tout le projet). Depuis le 10/11/2026 (demande de Quentin, deux PC) : chaque commit est poussé aussitôt (`git push`), sans attendre. Les commits utilisent l'e-mail anonyme GitHub (`97162976+Theorible1@users.noreply.github.com`, réglé dans la config git locale) : ne jamais remettre un vrai e-mail. Tout ce qui est dans git est public : jamais de secret ni de donnée perso.
- Technologie : Python (`.venv` du projet), httpx, trafilatura (articles), markdownify (wikis). Toujours utiliser `.venv\Scripts\python.exe`.
- Lancement : `.\scraper.bat <adresse> [--format markdown|json|texte] [--sortie fichier]`.
- Tests : `.\.venv\Scripts\python.exe -m pytest -q tests` (hors ligne).
- L'interface (options, champs JSON, codes d'erreur) est utilisée par d'autres agents : ne pas la casser ; toute évolution doit rester compatible et être reportée dans `README.md`.

## Liste des tâches
- `TODO.md` est la liste des tâches du projet, toujours à jour : la lire en début de session avec `REPRISE_SESSION.md`, la mettre à jour à la fin de chaque étape, en fin de session et avant `/clear`. Une tâche n'est cochée que vérifiée. Règles et modèle : section « liste des tâches `TODO.md` » de `E:\BOT\A_LIRE_AVANT_TOUT_PROJET.md`.
