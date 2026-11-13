# Projet scraping : consignes pour Claude Code

Outil de scraping (récupération automatique d'informations sur des sites web) destiné à être utilisé par les autres agents et projets de Quentin dans `E:\BOT`. Démarré le 10/11/2026. Les règles communes (ton, `TODO.md`, git, hygiène, sous-agents) sont dans le CLAUDE.md global.

## Le projet
- En ligne : dépôt **public** https://github.com/Theorible1/scraping (publié le 10/11/2026 avec l'accord de Quentin, tout le projet). Outil partagé entre le PC perso et le PC du bureau via GitHub.
- Document de référence : `docs/CAHIER_DES_CHARGES.md` (périmètre et technologie). `README.md` : présentation et mode d'emploi pour les autres agents.
- `scraper.bat` : point d'entrée, c'est ce que les agents appellent. `src\scraper.py` : tout le code de l'outil. `tests\test_scraper.py` : tests hors ligne (sites simulés).
- `requirements.txt`, `.venv\` (Python isolé du projet, hors git), `.gitignore` (secrets, `.venv`, résultats). `outils\`, `import\`, `_archives\` : vides.

## Règles propres au projet
- Les choix de fond (sites visés, données récupérées, format) appartiennent à Quentin : proposer, argumenter, le laisser trancher.
- Scraping responsable : respecter les conditions d'utilisation et le `robots.txt` des sites, aller doucement (pause entre deux requêtes), pas de contournement de connexion, de paywall ou de captcha, pas de collecte de données personnelles de particuliers.
- Secrets (identifiants, clés) uniquement dans `.env`, jamais affichés ni commités.
- L'outil doit rester simple à appeler par un autre agent : une interface stable et documentée dans `README.md`. L'interface (options, champs JSON, codes d'erreur) est utilisée par d'autres agents : ne pas la casser ; toute évolution doit rester compatible et être reportée dans `README.md`.
- Dépôt **public** : avant chaque commit, vérifier la liste (aucun secret, aucune donnée perso, rien d'inattendu). Tout ce qui est dans git est public.
- Depuis le 10/11/2026 (demande de Quentin, deux PC) : chaque commit est poussé aussitôt (`git push`), sans attendre. Une modification commitée mais pas poussée n'est pas terminée (l'autre PC ne la verra pas). Après le push, entrée dans `MISE_A_JOUR.md` du dossier BOT (outil partagé avec le bureau).
- Les commits utilisent l'e-mail anonyme GitHub (`97162976+Theorible1@users.noreply.github.com`, réglé dans la config git locale) : ne jamais remettre un vrai e-mail.
- Lancement des tests et vérification : pour tout changement visible, regarder le résultat réel (fichier produit, sortie lue).
- Chaque consigne de sous-agent commence par : « Lis d'abord `<dossier BOT>\Outils\scraping\SOUS_AGENT.md` en entier et respecte-le. » (dossier BOT : `E:\BOT` au PC perso, `C:\Quentin\SCRIPT` au bureau) Tout interdit ajouté ici est reporté dans `SOUS_AGENT.md`.

## Technique
- Python 3.14 installé, Git 2.56. Technologie : Python (`.venv` du projet), httpx, trafilatura (articles), markdownify (wikis). Toujours utiliser `.venv\Scripts\python.exe`.
- Lancement : `.\scraper.bat <adresse> [--format markdown|json|texte] [--sortie fichier]`.
- Tests : `.\.venv\Scripts\python.exe -m pytest -q tests` (hors ligne).
