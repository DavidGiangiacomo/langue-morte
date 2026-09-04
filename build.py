#!/usr/bin/env python3
"""
Assemble les sources de src/ en deux fichiers monolithiques dans dist/ :

  dist/langue-morte.html   page complète et autonome — à ouvrir directement
  dist/artefact.html       même contenu sans <!doctype>/<html>/<head>/<body>,
                           format attendu par l'outil Artifact de Claude

Le jeu se joue aussi directement depuis src/index.html sans rien construire :
le build ne sert qu'à produire un fichier unique à distribuer.

Usage :  python build.py
"""
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).parent
SRC, DIST = RACINE / "src", RACINE / "dist"

# L'ordre compte : les scripts partagent la portée globale et se lisent de haut en bas.
SCRIPTS = ["signes.js", "lexique.js", "corpus.js", "economie.js", "rendu.js", "jeu.js"]

RESET = (
    "<style>html{color-scheme:dark}body{margin:0}img{max-width:100%}"
    "[hidden]{display:none!important}</style>"
)


def lire(nom: str) -> str:
    chemin = SRC / nom
    if not chemin.exists():
        sys.exit(f"manquant : {chemin}")
    return chemin.read_text(encoding="utf-8")


def main() -> None:
    index = lire("index.html")

    markup = re.search(r"<body>\s*(.*?)\s*<script src=", index, re.S)
    if not markup:
        sys.exit("index.html : markup introuvable entre <body> et le premier <script>")
    markup = markup.group(1)

    polices = "\n".join(l for l in index.splitlines() if l.startswith("<link rel="))
    style = lire("style.css").rstrip()
    js = "\n\n".join(lire(n) for n in SCRIPTS)

    corps = (
        f"<title>La langue morte</title>\n{polices}\n"
        f"<style>\n{style}\n</style>\n\n{markup}\n\n<script>\n{js}\n</script>\n"
    )

    DIST.mkdir(exist_ok=True)
    (DIST / "artefact.html").write_text(corps, encoding="utf-8")
    (DIST / "langue-morte.html").write_text(
        "<!doctype html>\n<html lang=\"fr\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        f"{RESET}\n"
        f"<title>La langue morte</title>\n{polices}\n"
        f"<style>\n{style}\n</style>\n</head>\n<body>\n{markup}\n\n"
        f"<script>\n{js}\n</script>\n</body>\n</html>\n",
        encoding="utf-8",
    )

    for nom in ("langue-morte.html", "artefact.html"):
        print(f"dist/{nom} — {(DIST / nom).stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
