# Arborescence : scraping

```
scraping\
├── scraper.bat          Point d'entrée : c'est ce que les agents appellent
├── requirements.txt     Bibliothèques Python à installer
├── CLAUDE.md            Consignes permanentes pour Claude
├── REPRISE_SESSION.md   Où on en est (une page)
├── STATUT.md            Fait / vérifié / reste à faire
├── README.md            Présentation + mode d'emploi pour les autres agents
├── .gitignore           Fichiers exclus de git (secrets, .venv, résultats)
├── .venv\               Python isolé du projet (non sauvegardé dans git)
├── docs\
│   ├── ARBORESCENCE.md      Ce fichier
│   ├── DECISIONS.md         Historique des décisions
│   ├── IDEES.md             Idées non validées
│   └── CAHIER_DES_CHARGES.md  But, utilisateurs, fonctions, hors périmètre
├── src\
│   └── scraper.py       Tout le code de l'outil
├── tests\
│   └── test_scraper.py  Tests hors ligne (sites simulés)
├── outils\              Petits scripts utiles (vide)
├── import\              Matériel brut déposé par Quentin (vide)
└── _archives\           Anciennes versions (vide)
```
