#!/usr/bin/env python3
"""
Assemble les sources de src/ en fichiers monolithiques dans dist/ :

  dist/langue-morte.html   page complète et autonome — à ouvrir directement
  dist/artefact.html       même contenu sans <!doctype>/<html>/<head>/<body>,
                           format attendu par l'outil Artifact de Claude
  dist/playtest.html       le journal d'actions, sans le sélecteur de vitesse ni
                           « réinitialiser » : ce qu'on met devant un joueur qu'on ne
                           regarde pas jouer, et ce que GitHub Pages déploie
  dist/public.html         ni barre hors jeu, ni traces.js (LIV-2)

Le jeu se joue aussi directement depuis src/index.html sans rien construire :
le build ne sert qu'à produire un fichier unique à distribuer.

Les quatre sortent du même passage et non d'un drapeau : une variante qu'il faut penser à
demander est une variante qu'on oublie de reconstruire — et c'est celle-là qui part en ligne.

Usage :  python build.py
"""
import datetime
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).parent
SRC, DIST = RACINE / "src", RACINE / "dist"

# L'ordre compte : les scripts partagent la portée globale et se lisent de haut en bas.
SCRIPTS = ["signes.js", "lexique.js", "corpus.js", "economie.js", "rendu.js", "traces.js", "jeu.js"]

# Ce que chaque variante garde de la barre « hors jeu », et si elle emporte le journal
# d'actions. Les blocs sont marqués dans src/index.html, jamais listés ici : ajouter un
# bouton hors jeu ne doit pas demander de toucher au build.
#   `garde` : les blocs `<!--#nom-->…<!--/#nom-->`, présents dans la source, que la variante
#             conserve — tous les autres sont retirés.
#   `ouvre` : les blocs `<!--+nom … -->`, endormis en commentaire, que la variante ouvre.
#             Sans eux, src/index.html — qui se joue tel quel — afficherait l'étiquette des
#             deux builds à la fois.
VARIANTES = {
    "dev":      {"garde": {"horsjeu", "dev"}, "ouvre": set(),        "traces": True},
    "playtest": {"garde": {"horsjeu"},        "ouvre": {"playtest"}, "traces": True},
    "public":   {"garde": set(),              "ouvre": set(),        "traces": False},
}

BLOC = re.compile(r"<!--#(\w+)-->(.*?)<!--/#\1-->", re.S)
OUVRE = re.compile(r"<!--\+(\w+)\s(.*?)\s*-->", re.S)
# Retirer un bloc laisse sa ligne d'indentation derrière lui. La source n'a aucune ligne
# faite d'espaces seuls (vérifié) : celles-là sont donc toutes des cicatrices de découpe,
# alors qu'une ligne vraiment vide sépare deux sections et se garde.
CICATRICES = re.compile(r"^[ \t]+$\n?", re.M)
VIDES = re.compile(r"\n{3,}")

RESET = (
    "<style>html{color-scheme:dark}body{margin:0}img{max-width:100%}"
    "[hidden]{display:none!important}</style>"
)


def lire(nom: str) -> str:
    chemin = SRC / nom
    if not chemin.exists():
        sys.exit(f"manquant : {chemin}")
    return chemin.read_text(encoding="utf-8")


def variante(markup: str, v: dict) -> str:
    """Retire de `markup` ce que la variante ne garde pas, ouvre ce qu'elle réclame."""
    def passe(txt: str) -> str:
        txt = BLOC.sub(lambda m: passe(m.group(2)) if m.group(1) in v["garde"] else "", txt)
        return OUVRE.sub(lambda m: m.group(2) if m.group(1) in v["ouvre"] else "", txt)
    return VIDES.sub("\n\n", CICATRICES.sub("", passe(markup))).strip()


def scripts(nom: str, v: dict) -> str:
    """Les sources JS de la variante, le journal d'actions estampillé de son build."""
    js = []
    for s in SCRIPTS:
        if s == "traces.js":
            if not v["traces"]:
                continue
            # Le journal doit dire de quel build il sort : sans ça un TSV qui revient trois
            # semaines plus tard ne dit pas contre quels réglages il a été joué.
            texte, ancre = lire(s), "let BUILD = 'src';"
            if ancre not in texte:
                sys.exit(f"{s} : « {ancre} » introuvable — l'estampille de build ne se pose plus")
            jour = datetime.date.today().isoformat()
            js.append(texte.replace(ancre, f"let BUILD = '{nom} · {jour}';", 1))
        else:
            js.append(lire(s))
    return "\n\n".join(js)


def main() -> None:
    index = lire("index.html")

    markup = re.search(r"<body>\s*(.*?)\s*<script src=", index, re.S)
    if not markup:
        sys.exit("index.html : markup introuvable entre <body> et le premier <script>")
    markup = markup.group(1)

    polices = "\n".join(l for l in index.splitlines() if l.startswith("<link rel="))
    style = lire("style.css").rstrip()

    DIST.mkdir(exist_ok=True)
    for nom, v in VARIANTES.items():
        corps, js = variante(markup, v), scripts(nom, v)
        page = (
            f"<title>La langue morte</title>\n{polices}\n"
            f"<style>\n{style}\n</style>\n\n{corps}\n\n<script>\n{js}\n</script>\n"
        )
        # `artefact.html` n'a pas de variante : c'est la page de développement, sans l'enveloppe
        # que l'outil Artifact fournit lui-même.
        if nom == "dev":
            (DIST / "artefact.html").write_text(page, encoding="utf-8")
        fichier = {"dev": "langue-morte.html"}.get(nom, nom + ".html")
        (DIST / fichier).write_text(
            "<!doctype html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            f"{RESET}\n"
            f"<title>La langue morte</title>\n{polices}\n"
            f"<style>\n{style}\n</style>\n</head>\n<body>\n{corps}\n\n"
            f"<script>\n{js}\n</script>\n</body>\n</html>\n",
            encoding="utf-8",
        )

    for nom in ("langue-morte.html", "artefact.html", "playtest.html", "public.html"):
        print(f"dist/{nom} — {(DIST / nom).stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
