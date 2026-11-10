# scraping

Outil qui va lire une page web et rend son **contenu principal en texte propre** (Markdown), sans menus, pubs ni pieds de page. Fait pour être appelé par les autres agents et projets de `E:\BOT`.

Version 0.1.0 (10/11/2026). Code source : https://github.com/Theorible1/scraping

## Pour un agent : comment s'en servir

### En ligne de commande (méthode recommandée, marche depuis n'importe quel projet)
```powershell
& E:\BOT\Outils\scraping\scraper.bat "https://site.fr/article"
```
Options :
| Option | Effet |
|---|---|
| plusieurs adresses à la suite | les traite une par une (pause de 2 s entre deux pages du même site) |
| `--format markdown` | (par défaut) en-tête avec titre, source, date + texte |
| `--format json` | données structurées, idéal pour un programme (voir champs plus bas) |
| `--format texte` | juste le texte |
| `--sortie fichier.md` | écrit dans un fichier au lieu de l'écran |

Code de retour : `0` si toutes les pages ont réussi, `1` si au moins une a échoué.

### Depuis Python (seulement avec le Python du projet scraping)
```python
import sys; sys.path.insert(0, r"E:\BOT\Outils\scraping\src")
from scraper import recuperer
r = recuperer("https://site.fr/article")
```
Attention : il faut que les bibliothèques soient installées dans le Python utilisé. Si le projet appelant a son propre `.venv`, passer plutôt par la ligne de commande.

### Champs du résultat (format json)
| Champ | Contenu |
|---|---|
| `ok` | `true` / `false` |
| `url`, `url_finale` | adresse demandée, adresse réelle après redirection |
| `methode` | `page` (page lue normalement) ou `api_wiki` (wiki lu via son API officielle) |
| `titre`, `auteur`, `date`, `site`, `description` | métadonnées si trouvées, sinon `null` |
| `texte` | contenu principal en Markdown |
| `nb_mots` | taille approximative |
| `erreur`, `message` | si `ok` = `false` : code d'erreur et explication |

### Codes d'erreur
| Code | Signification |
|---|---|
| `adresse_invalide` | adresse mal formée |
| `connexion_impossible`, `delai_depasse` | site injoignable ou trop lent (20 s) |
| `page_introuvable` | 404 ou page de wiki inexistante |
| `acces_refuse` | 401/403 : connexion requise |
| `protection_anti_robot` | site protégé (type Cloudflare) : **pas contourné, volontairement** |
| `interdit_par_robots` | le `robots.txt` du site interdit cette page |
| `trop_de_requetes` | le site demande de ralentir (429) |
| `pas_une_page_web`, `page_trop_grosse` | fichier (PDF, exe...) ou page > 10 Mo, refusé sans le télécharger |
| `contenu_vide` | aucun texte trouvé (souvent une page construite en JavaScript) |
| `erreur_site` | autre erreur du site |

## Ce qui marche aujourd'hui
- Articles, blogs, pages d'info classiques.
- Wikis MediaWiki (Fandom, Wikipédia...) : passage automatique par l'API officielle, même quand la page est protégée par Cloudflare. Titres de sections conservés.

## Limites connues
- Pas encore de pages nécessitant une connexion.
- Pas de pages construites entièrement en JavaScript.

## Installation (déjà faite sur ce PC)
```powershell
cd E:\BOT\Outils\scraping
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Tests
```powershell
.\.venv\Scripts\python.exe -m pytest -q tests
```
Hors ligne, les sites sont simulés.
