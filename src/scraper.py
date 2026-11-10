"""Outil de scraping commun aux agents de E:\\BOT.

Usage en ligne de commande (voir README.md) :
    scraper.bat <adresse> [<adresse> ...] [--format markdown|json|texte] [--sortie fichier]

Usage depuis Python (avec le Python du .venv de ce projet) :
    from scraper import recuperer
    resultat = recuperer("https://exemple.fr/article")
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from urllib.parse import unquote, urlparse
from urllib.robotparser import RobotFileParser

import httpx
import lxml.html
import trafilatura
from markdownify import markdownify

VERSION = "0.1.0"
USER_AGENT = f"BOT-scraping/{VERSION} (outil perso, usage modere)"
DELAI_ENTRE_REQUETES = 2.0  # secondes entre deux pages d'un meme site
TIMEOUT = 20.0
TAILLE_MAX = 10 * 1024 * 1024  # 10 Mo, au-dela on refuse

_robots_cache: dict[str, RobotFileParser | None] = {}
_derniere_requete: dict[str, float] = {}


class ErreurScraping(Exception):
    """Erreur lisible renvoyee a l'agent appelant."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def _verifier_adresse(url: str) -> str:
    url = url.strip()
    if not urlparse(url).scheme:
        url = "https://" + url
    parties = urlparse(url)
    if parties.scheme not in ("http", "https") or not parties.netloc:
        raise ErreurScraping("adresse_invalide", f"Adresse invalide : {url}")
    return url


def _robots_autorise(client: httpx.Client, url: str) -> bool:
    parties = urlparse(url)
    racine = f"{parties.scheme}://{parties.netloc}"
    if racine not in _robots_cache:
        parseur: RobotFileParser | None = RobotFileParser()
        try:
            rep = client.get(racine + "/robots.txt")
            if rep.status_code == 200:
                parseur.parse(rep.text.splitlines())
            elif _est_protection_anti_robot(rep):
                parseur = None  # robots.txt illisible : la page dira elle-meme qu'elle est protegee
            elif rep.status_code in (401, 403):
                parseur.disallow_all = True
            else:
                parseur = None  # pas de robots.txt : tout est permis
        except httpx.HTTPError:
            parseur = None
        _robots_cache[racine] = parseur
    parseur = _robots_cache[racine]
    return True if parseur is None else parseur.can_fetch(USER_AGENT, url)


def _est_protection_anti_robot(rep: httpx.Response) -> bool:
    if rep.status_code not in (403, 429, 503):
        return False
    if rep.headers.get("cf-mitigated") == "challenge":
        return True
    debut = rep.text[:3000]
    return "Just a moment" in debut or "challenge-platform" in debut


def _attendre_politesse(url: str) -> None:
    site = urlparse(url).netloc
    derniere = _derniere_requete.get(site)
    if derniere is not None:
        reste = DELAI_ENTRE_REQUETES - (time.monotonic() - derniere)
        if reste > 0:
            time.sleep(reste)
    _derniere_requete[site] = time.monotonic()


def _telecharger(client: httpx.Client, url: str) -> tuple[str, str]:
    """Telecharge une page HTML. Verifie le type AVANT de tout telecharger. Renvoie (html, url_finale)."""
    _attendre_politesse(url)
    try:
        with client.stream("GET", url) as rep:
            if rep.status_code >= 400:
                rep.read()
                _verifier_statut(rep)
            type_contenu = rep.headers.get("content-type", "")
            if "html" not in type_contenu and "xml" not in type_contenu:
                raise ErreurScraping(
                    "pas_une_page_web", f"Ce n'est pas une page web (type : {type_contenu or 'inconnu'})."
                )
            if int(rep.headers.get("content-length") or 0) > TAILLE_MAX:
                raise ErreurScraping("page_trop_grosse", "Page trop volumineuse (plus de 10 Mo).")
            morceaux, total = [], 0
            for morceau in rep.iter_bytes():
                total += len(morceau)
                if total > TAILLE_MAX:
                    raise ErreurScraping("page_trop_grosse", "Page trop volumineuse (plus de 10 Mo).")
                morceaux.append(morceau)
            contenu = b"".join(morceaux)
            encodage = rep.charset_encoding or "utf-8"
            try:
                html = contenu.decode(encodage, errors="replace")
            except LookupError:
                html = contenu.decode("utf-8", errors="replace")
            return html, str(rep.url)
    except httpx.TimeoutException:
        raise ErreurScraping("delai_depasse", f"Le site ne repond pas en {TIMEOUT:.0f} s.")
    except httpx.HTTPError as e:
        raise ErreurScraping("connexion_impossible", f"Connexion impossible : {e}")


def _verifier_statut(rep: httpx.Response) -> None:
    if _est_protection_anti_robot(rep):
        raise ErreurScraping(
            "protection_anti_robot",
            "Le site est protege contre les robots (verification type Cloudflare). "
            "L'outil ne contourne pas ces protections volontairement.",
        )
    if rep.status_code in (401, 403):
        raise ErreurScraping(
            "acces_refuse",
            f"Le site refuse l'acces (code {rep.status_code}) : connexion requise ou robots bloques.",
        )
    if rep.status_code == 404:
        raise ErreurScraping("page_introuvable", "Page introuvable (404).")
    if rep.status_code == 429:
        raise ErreurScraping("trop_de_requetes", "Le site demande de ralentir (429). Reessayer plus tard.")
    if rep.status_code >= 400:
        raise ErreurScraping("erreur_site", f"Erreur du site (code {rep.status_code}).")


_A_RETIRER_WIKI = (
    "script, style, img, figure, .thumb, .gallery, .wikia-gallery, #toc, .toc, .navbox, .mw-editsection, "
    "sup.reference, .mw-references-wrap, ol.references, .noprint, .mw-empty-elt, "
    ".bandeau-container, .ambox, .metadata"
)


def _retirer_titres_vides(texte: str) -> str:
    """Retire les titres de section qui ne sont suivis d'aucun contenu (ex. sections de references videes)."""
    lignes = texte.split("\n")
    gardees: list[str] = []
    for i, ligne in enumerate(lignes):
        m = re.match(r"^(#{1,6}) ", ligne)
        if m:
            suite = next((l for l in lignes[i + 1:] if l.strip()), None)
            m2 = re.match(r"^(#{1,6}) ", suite) if suite else None
            if suite is None or (m2 and len(m2.group(1)) <= len(m.group(1))):
                continue
        gardees.append(ligne)
    return "\n".join(gardees)


def _wiki_en_markdown(fragment: str) -> str:
    """Convertit le HTML renvoye par l'API d'un wiki en Markdown propre (titres de sections conserves)."""
    if not fragment.strip():
        return ""
    racine = lxml.html.fragment_fromstring(fragment, create_parent="div")
    for el in racine.cssselect(_A_RETIRER_WIKI):
        el.drop_tree()
    for h in racine.xpath(".//h1|.//h2|.//h3|.//h4|.//h5|.//h6"):
        texte = " ".join(h.text_content().split())
        for enfant in list(h):
            h.remove(enfant)
        h.text = texte
    html = lxml.html.tostring(racine, encoding="unicode")
    texte = markdownify(html, heading_style="ATX", strip=["a"], bullets="-")
    texte = _retirer_titres_vides(texte)
    texte = re.sub(r"\n{3,}", "\n\n", texte)
    return texte.strip()


def _via_api_wiki(client: httpx.Client, url: str) -> dict | None:
    """Pour les wikis MediaWiki (Fandom, Wikipedia...) : passe par l'API officielle prevue pour les programmes.

    Renvoie None si l'adresse n'est pas un wiki ou si l'API ne repond pas : on retombe alors sur la page normale.
    """
    parties = urlparse(url)
    if not parties.path.startswith("/wiki/") or len(parties.path) <= 6:
        return None
    titre_page = unquote(parties.path[6:])
    racine = f"{parties.scheme}://{parties.netloc}"
    params = {
        "action": "parse",
        "page": titre_page,
        "prop": "text|displaytitle",
        "format": "json",
        "formatversion": "2",
        "redirects": "1",
        "disableeditsection": "1",
        "disabletoc": "1",
        "maxlag": "5",
    }
    for chemin in ("/api.php", "/w/api.php"):
        _attendre_politesse(url)
        try:
            rep = client.get(racine + chemin, params=params)
        except httpx.HTTPError:
            continue
        if rep.status_code != 200 or "json" not in rep.headers.get("content-type", ""):
            continue
        donnees = rep.json()
        if "error" in donnees:
            if donnees["error"].get("code") == "missingtitle":
                raise ErreurScraping("page_introuvable", f"Page de wiki introuvable : {titre_page}")
            continue
        parse = donnees.get("parse", {})
        return {
            "texte": _wiki_en_markdown(parse.get("text", "")),
            "url_finale": f"{racine}/wiki/{parse.get('title', titre_page).replace(' ', '_')}",
            "titre": parse.get("title"),
            "site": parties.netloc,
        }
    return None


def recuperer(url: str, client: httpx.Client | None = None, respecter_robots: bool = True) -> dict:
    """Recupere une page et renvoie son contenu principal nettoye.

    Renvoie un dict : ok, url, url_finale, titre, auteur, date, site, description, texte (Markdown), nb_mots.
    En cas d'echec : ok=False, url, erreur (code), message.
    """
    proprietaire = client is None
    if client is None:
        client = httpx.Client(
            headers={"User-Agent": USER_AGENT, "Accept-Language": "fr,en;q=0.8"},
            timeout=TIMEOUT,
            follow_redirects=True,
        )
    try:
        url = _verifier_adresse(url)
        wiki = _via_api_wiki(client, url)
        if wiki is not None:
            texte, url_finale, methode = wiki["texte"], wiki["url_finale"], "api_wiki"
            titre, site, auteur, date, description = wiki["titre"], wiki["site"], None, None, None
        else:
            if respecter_robots and not _robots_autorise(client, url):
                raise ErreurScraping("interdit_par_robots", "Le fichier robots.txt du site interdit cette page.")
            html, url_finale = _telecharger(client, url)
            methode = "page"
            texte = trafilatura.extract(
                html,
                url=url_finale,
                output_format="markdown",
                include_tables=True,
                include_formatting=True,
                include_links=False,
                include_comments=False,
                favor_recall=True,
            )
            meta = trafilatura.extract_metadata(
                html, default_url=url_finale, extensive=False,
                date_config={"original_date": True, "extensive_search": False, "url": url_finale},
            )
            titre = getattr(meta, "title", None)
            site = getattr(meta, "sitename", None)
            auteur = getattr(meta, "author", None)
            date = getattr(meta, "date", None)
            description = getattr(meta, "description", None)

        if not texte or not texte.strip():
            raise ErreurScraping(
                "contenu_vide",
                "Aucun texte trouve. La page est peut-etre construite en JavaScript ou vide.",
            )
        return {
            "ok": True,
            "url": url,
            "url_finale": url_finale,
            "methode": methode,
            "titre": titre,
            "auteur": auteur,
            "date": date,
            "site": site,
            "description": description,
            "texte": texte.strip(),
            "nb_mots": len(texte.split()),
        }
    except ErreurScraping as e:
        return {"ok": False, "url": url, "erreur": e.code, "message": e.message}
    finally:
        if proprietaire:
            client.close()


def _en_markdown(r: dict) -> str:
    if not r["ok"]:
        return f"# ERREUR : {r['url']}\n\n- code : {r['erreur']}\n- message : {r['message']}\n"
    lignes = [f"# {r['titre'] or r['url_finale']}", ""]
    lignes.append(f"- source : {r['url_finale']}")
    for cle in ("site", "auteur", "date"):
        if r.get(cle):
            lignes.append(f"- {cle} : {r[cle]}")
    lignes.append(f"- mots : {r['nb_mots']}")
    lignes += ["", "---", "", r["texte"], ""]
    return "\n".join(lignes)


def main(argv: list[str] | None = None) -> int:
    parseur = argparse.ArgumentParser(
        prog="scraper", description="Recupere le contenu principal de pages web (texte propre)."
    )
    parseur.add_argument("adresses", nargs="+", help="Une ou plusieurs adresses de pages.")
    parseur.add_argument("--format", choices=["markdown", "json", "texte"], default="markdown")
    parseur.add_argument("--sortie", help="Fichier ou ecrire le resultat (sinon : ecran).")
    parseur.add_argument("--ignorer-robots", action="store_true", help=argparse.SUPPRESS)
    args = parseur.parse_args(argv)

    with httpx.Client(
        headers={"User-Agent": USER_AGENT, "Accept-Language": "fr,en;q=0.8"},
        timeout=TIMEOUT,
        follow_redirects=True,
    ) as client:
        resultats = [recuperer(a, client, not args.ignorer_robots) for a in args.adresses]

    if args.format == "json":
        contenu = json.dumps(resultats if len(resultats) > 1 else resultats[0], ensure_ascii=False, indent=2)
    elif args.format == "texte":
        contenu = "\n\n".join(r["texte"] if r["ok"] else f"ERREUR {r['erreur']} : {r['message']}" for r in resultats)
    else:
        contenu = "\n\n".join(_en_markdown(r) for r in resultats)

    if args.sortie:
        with open(args.sortie, "w", encoding="utf-8") as f:
            f.write(contenu)
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(contenu)

    return 0 if all(r["ok"] for r in resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
