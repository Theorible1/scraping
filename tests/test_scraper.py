"""Tests hors ligne : les sites sont simules, aucun acces internet."""

import json
import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import scraper  # noqa: E402

ARTICLE = """<html><head><title>Mon article</title>
<meta name="author" content="Alice"><meta property="article:published_time" content="2026-11-01"></head>
<body><nav>Menu Accueil Contact</nav><article><h1>Mon article</h1>
<p>Premier paragraphe assez long pour etre considere comme du vrai contenu par l'extracteur de texte.</p>
<h2>Une section</h2><p>Deuxieme paragraphe, lui aussi suffisamment long pour etre garde dans le resultat final.</p>
</article><footer>Mentions legales</footer></body></html>"""

WIKI_JSON = {
    "parse": {
        "title": "Job system",
        "text": '<div class="mw-parser-output"><div id="toc">Sommaire</div>'
        "<p>Intro du <b>systeme</b>.</p>"
        '<h2><span class="mw-headline"><a href="/wiki/X">Apparitions</a></span></h2>'
        "<p>Texte de section.</p><h2>Citations</h2></div>",
    }
}


@pytest.fixture(autouse=True)
def sans_delai(monkeypatch):
    monkeypatch.setattr(scraper, "DELAI_ENTRE_REQUETES", 0)
    scraper._robots_cache.clear()
    scraper._derniere_requete.clear()


def client_simule(gestion):
    return httpx.Client(transport=httpx.MockTransport(gestion), follow_redirects=True)


def test_article_normal():
    def gestion(req):
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, html=ARTICLE)

    r = scraper.recuperer("https://blog.exemple/article", client_simule(gestion))
    assert r["ok"], r
    assert r["methode"] == "page"
    assert "Premier paragraphe" in r["texte"]
    assert "Une section" in r["texte"]
    assert "Mentions legales" not in r["texte"]


def test_adresse_sans_https_est_completee():
    def gestion(req):
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, html=ARTICLE)

    r = scraper.recuperer("blog.exemple/article", client_simule(gestion))
    assert r["ok"] and r["url"] == "https://blog.exemple/article"


def test_adresse_invalide():
    r = scraper.recuperer("ftp://truc", client_simule(lambda req: httpx.Response(200)))
    assert not r["ok"] and r["erreur"] == "adresse_invalide"


def test_wiki_passe_par_api_et_garde_les_titres():
    def gestion(req):
        assert req.url.path == "/api.php", "une page wiki doit passer par l'API, pas par la page"
        return httpx.Response(200, json=WIKI_JSON)

    r = scraper.recuperer("https://jeu.fandom.com/wiki/Job_system", client_simule(gestion))
    assert r["ok"], r
    assert r["methode"] == "api_wiki"
    assert r["titre"] == "Job system"
    assert "## Apparitions" in r["texte"]
    assert "**systeme**" in r["texte"]
    assert "Sommaire" not in r["texte"]
    assert "Citations" not in r["texte"]  # titre vide retire


def test_wiki_page_introuvable():
    def gestion(req):
        return httpx.Response(200, json={"error": {"code": "missingtitle"}})

    r = scraper.recuperer("https://jeu.fandom.com/wiki/Rien", client_simule(gestion))
    assert not r["ok"] and r["erreur"] == "page_introuvable"


def test_protection_anti_robot_signalee():
    def gestion(req):
        return httpx.Response(403, headers={"cf-mitigated": "challenge"}, html="<title>Just a moment...</title>")

    r = scraper.recuperer("https://protege.exemple/page", client_simule(gestion))
    assert not r["ok"] and r["erreur"] == "protection_anti_robot"


def test_robots_txt_respecte():
    def gestion(req):
        if req.url.path == "/robots.txt":
            return httpx.Response(200, text="User-agent: *\nDisallow: /prive/")
        return httpx.Response(200, html=ARTICLE)

    c = client_simule(gestion)
    assert scraper.recuperer("https://site.exemple/prive/page", c)["erreur"] == "interdit_par_robots"
    assert scraper.recuperer("https://site.exemple/public/page", c)["ok"]


def test_fichier_non_html_refuse_sans_tout_telecharger():
    lus = []

    def flux():
        for _ in range(1000):
            lus.append(1)
            yield b"x" * 1024

    def gestion(req):
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, headers={"content-type": "application/octet-stream"}, content=flux())

    r = scraper.recuperer("https://site.exemple/gros.exe", client_simule(gestion))
    assert r["erreur"] == "pas_une_page_web"
    assert len(lus) == 0


def test_erreurs_http():
    codes = {"/a": 404, "/b": 429, "/c": 500, "/d": 401}

    def gestion(req):
        if req.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(codes[req.url.path], html="<p>non</p>")

    c = client_simule(gestion)
    attendu = {"/a": "page_introuvable", "/b": "trop_de_requetes", "/c": "erreur_site", "/d": "acces_refuse"}
    for chemin, code in attendu.items():
        assert scraper.recuperer(f"https://site.exemple{chemin}", c)["erreur"] == code


def test_retirer_titres_vides():
    texte = "# T\n\nintro\n\n## Vide\n\n## Plein\n\ncontenu\n\n### Fin"
    assert scraper._retirer_titres_vides(texte) == "# T\n\nintro\n\n\n## Plein\n\ncontenu\n"


def test_ligne_de_commande_json(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(scraper, "recuperer", lambda url, client=None, respecter_robots=True: {
        "ok": True, "url": url, "url_finale": url, "methode": "page", "titre": "T", "auteur": None,
        "date": None, "site": None, "description": None, "texte": "bonjour", "nb_mots": 1})
    sortie = tmp_path / "r.json"
    code = scraper.main(["https://x.exemple", "--format", "json", "--sortie", str(sortie)])
    assert code == 0
    assert json.loads(sortie.read_text(encoding="utf-8"))["texte"] == "bonjour"
