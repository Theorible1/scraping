# Projet scraping : consignes permanentes pour Claude Code

Outil de scraping (récupération automatique d'informations sur des sites web) destiné à être utilisé par les autres agents et projets de Quentin dans `E:\BOT`. Démarré le 10/11/2026. Le périmètre et la technologie se précisent dans `docs/CAHIER_DES_CHARGES.md`.

L'utilisateur (Quentin) parle français et n'est pas technicien : réponses en **français**, consignes courtes, **une action à la fois**, noms exacts des menus et boutons. Ton de pote (tutoiement, un peu d'humour ok), rigueur intacte. Il veut de l'autonomie : ne pas poser de question à chaque étape, mais demander avant toute action irréversible. Quand il doit remplacer un fichier, lui donner le fichier **complet**.

## Au début de chaque session
1. Lire `REPRISE_SESSION.md`.
2. Seulement si besoin : `STATUT.md`, `docs/DECISIONS.md`, `docs/ARBORESCENCE.md`, `docs/CAHIER_DES_CHARGES.md`.
3. Si un document contredit l'état réel des fichiers, l'état réel prime : le signaler.

## À la fin de chaque étape
1. Lancer les tests ; pour tout changement visible, regarder le résultat réel (fichier produit, sortie lue).
2. Mettre à jour `STATUT.md`.
3. Nouvelle décision : une ligne datée dans `docs/DECISIONS.md`.
4. Nouveau dossier ou fichier important : mettre à jour `docs/ARBORESCENCE.md`.
5. Étape validée : sauvegarde git (`git add -A` puis `git commit -m "<ce qui a été fait, en français>"`). Étape validée = un commit avec un message en français.

## À la fin de chaque session (« on s'arrête », « fin de session »)
- Réécrire `REPRISE_SESSION.md` (une page max, date du jour).

## Hygiène de session
- Appliquer la section « hygiène de session » de `E:\BOT\A_LIRE_AVANT_TOUT_PROJET.md` : surveiller la taille du contexte, rappeler à Quentin `/compact` (avant une pause) et `/clear` (changement de sujet).
- Si le contexte devient trop lourd : tout mettre à jour (REPRISE_SESSION, STATUT, DECISIONS, ARBORESCENCE, mémoire), puis proposer un prompt de redémarrage à coller dans une nouvelle conversation.

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
- Python 3.14 installé. Git 2.56 (si `git` n'est pas reconnu : `& "C:\Program Files\Git\cmd\git.exe"`). Aucun dépôt en ligne sans accord.
- Technologie de l'outil : à définir. Lancement : à définir. Tests : à définir.
