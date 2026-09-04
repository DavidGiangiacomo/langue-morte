#!/usr/bin/env python3
"""
Vérifications automatiques du prototype. À lancer après toute modification de src/.

  python build.py && python outils/verifier.py

Contrôle :
  1. aucune erreur JavaScript au chargement
  2. le corpus se rend entièrement (nombre de signes attendu)
  3. l'échelle de la numération : chaque glyphe de nombre ouvre exactement ce qu'il doit
  4. les infobulles répondent dans les quatre cas prévus
  5. le temps de rendu initial reste sous le seuil

Prérequis : pip install playwright && playwright install chromium
"""
import pathlib
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright manquant :  pip install playwright && playwright install chromium")

RACINE = pathlib.Path(__file__).parent.parent
PAGE = RACINE / "dist" / "langue-morte.html"

SIGNES_ATTENDUS = 3825          # cf. sortie de outils/corpus.py
RENDU_MAX_S = 4.0

# glyphe acheté -> ensemble exact des nombres du corpus qui doivent devenir lisibles
ECHELLE = [
    ("un",   lambda ns: ns == [1]),
    ("deux", lambda ns: ns == [1, 2, 3, 4]),
    ("cinq", lambda ns: set(ns) >= set(range(1, 10)) and 50 in ns and 10 not in ns),
    ("dix",  lambda ns: set(ns) >= set(range(1, 100)) and 100 not in ns),
    ("cent", lambda ns: 212 in ns and 756 in ns and 1200 not in ns),
]

echecs = []


def verifier(condition, message):
    if condition:
        print(f"  ok   {message}")
    else:
        print(f"  ÉCHEC {message}")
        echecs.append(message)


def main() -> None:
    if not PAGE.exists():
        sys.exit(f"{PAGE} absent — lancer d'abord : python build.py")

    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page(viewport={"width": 1440, "height": 900})
        erreurs = []
        page.on("pageerror", lambda e: erreurs.append(str(e)))
        page.on("console", lambda m: erreurs.append(m.text)
                if m.type == "error" and "net::" not in m.text else None)

        t0 = time.time()
        page.goto(PAGE.resolve().as_uri())
        page.wait_for_timeout(1200)
        duree = time.time() - t0

        print("\nchargement")
        verifier(not erreurs, f"aucune erreur JS ({erreurs[:2] if erreurs else ''})")
        verifier(duree < RENDU_MAX_S, f"rendu en {duree:.2f}s (< {RENDU_MAX_S}s)")

        signes = page.eval_on_selector_all("#corpus .tok:not(.sep)", "e => e.length")
        verifier(signes == SIGNES_ATTENDUS, f"{signes} signes rendus (attendu {SIGNES_ATTENDUS})")

        tablettes = page.eval_on_selector_all(".tablet:not([hidden])", "e => e.length")
        verifier(tablettes == 4, f"{tablettes} tablettes dégagées au départ (attendu 4)")

        print("\néchelle de la numération")
        for mot, attendu in ECHELLE:
            page.evaluate("(m) => { const g = GL.find(x => x.mot === m); S_.C += g.cost; }", mot)
            page.wait_for_timeout(120)
            carte = page.query_selector("#lex .gcard.afford")
            if carte:
                carte.click()
            page.wait_for_timeout(220)
            lus = sorted({int(t) for t in page.eval_on_selector_all(
                "#corpus .tok.num", "e => e.map(x => x.textContent.replace(/\\D/g, ''))") if t})
            verifier(attendu(lus), f"après « {mot} » : {lus[:12]}{' …' if len(lus) > 12 else ''}")

        print("\ninfobulles")

        # acheter de quoi avoir des mots traduits (les 5 glyphes de nombre n'en donnent aucun)
        page.evaluate("() => { S_.C = 9999; }")
        page.wait_for_timeout(120)
        for _ in range(3):
            carte = page.query_selector("#lex .gcard.afford")
            if carte:
                carte.click()
            page.wait_for_timeout(180)

        def bulle(selecteur):
            el = page.query_selector(selecteur)
            if not el:
                return None
            page.mouse.move(8, 400)          # sortir du corpus pour forcer un mousemove
            page.wait_for_timeout(60)
            el.hover()
            page.wait_for_timeout(160)
            if page.get_attribute("#tip", "hidden") is not None:
                return ""
            return page.eval_on_selector("#tip", "e => e.textContent")

        verifier(bool(bulle("#corpus .tok.w")), "mot traduit : le signe revient")
        verifier(bool(bulle("#corpus .tok.num")), "nombre traduit : les signes reviennent")
        page.evaluate("() => { S_.b.tab = 0; }")
        page.wait_for_timeout(100)
        verifier(bulle("#corpus .tok.g") == "", "signe inconnu sans Table de fréquences : rien")
        page.evaluate("() => { S_.b.tab = 1; }")
        page.wait_for_timeout(100)
        verifier("occurrence" in (bulle("#corpus .tok.g") or ""),
                 "signe inconnu avec Table de fréquences : le comptage")

        nav.close()

    print("\n" + ("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)"))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
