# scraping : consignes pour les sous-agents

Tu es un sous-agent lancé par la conversation principale de Claude Code pour une étape précise sur l'outil scraping. Lis ce fichier en entier avant de commencer. Il prime sur le `CLAUDE.md` du projet, qui s'adresse à la conversation principale : ses parties sur le début et la fin de session, la synchronisation, `REPRISE_SESSION.md`, `STATUT.md`, les commits et les push ne te concernent pas.

## Le projet en bref
- Outil commun qui lit une page web et rend son contenu principal en texte propre. D'autres agents l'appellent par `scraper.bat`.
- Python dans le `.venv` du projet (httpx, trafilatura, markdownify). Code dans `src\`, tests dans `tests\`, mode d'emploi dans `README.md`.
- Le dépôt GitHub est **public** : tout ce qui est écrit dans un fichier du projet peut finir visible de tous.

## Ce que tu ne fais jamais
1. **Git et extérieur.** Ni `git add`, ni `git commit`, ni `git push`, ni mise en ligne.
2. **Fichiers.** Ne rien supprimer ni déplacer. Ne modifier que les fichiers que ta consigne nomme. Si elle n'en nomme aucun, tu es en lecture seule.
3. **Secrets et données personnelles.** Ne jamais lire, afficher ni écrire un secret (`.env`, jeton, mot de passe). Aucune donnée personnelle, aucun vrai e-mail, aucun nom de personne dans un fichier.
4. **Requêtes vers des sites.** Aucune requête réelle vers un site web, sauf si ta consigne le demande. Dans ce cas : respecter `robots.txt` et les conditions du site, faire une pause entre deux requêtes, ne contourner ni connexion, ni paywall, ni captcha.
5. **Interface.** Ne pas changer les options, les champs JSON ni les codes d'erreur de l'outil : d'autres agents en dépendent.
6. **Périmètre.** Rester dans le dossier du projet. Ne pas lancer d'autre sous-agent.

Tu ne peux pas poser de question à Quentin. Si la consigne est ambiguë ou si tu es bloqué, arrête-toi et dis-le dans ton rapport plutôt que de deviner.

## Pour travailler
- Windows, PowerShell 5.1 (pas de `&&`).
- Python : toujours `.venv\Scripts\python.exe`.
- Tests (hors ligne) : `.\.venv\Scripts\python.exe -m pytest -q tests`.
- Textes en français, sans tiret long.

## Ton rapport
- Court : ce que tu as trouvé ou fait, avec les chemins et les numéros de ligne.
- Ce que tu as vérifié (commande lancée, résultat lu) et ce que tu n'as pas vérifié.
- Ce qui t'a bloqué ou surpris, et tout écart par rapport à la consigne.
- Pas de fichier recopié en entier.
- N'invente rien : « je n'ai pas trouvé » est une réponse valable.
