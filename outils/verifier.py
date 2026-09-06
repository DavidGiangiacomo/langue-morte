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
  6. la fenêtre de fin se ferme, et ne couvre pas les outils hors jeu

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

        print("\nréinitialisation")
        page.evaluate("() => { S_.C = 9999; GL.forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(150)
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(250)
        # la table de numération doit repartir vide : sinon on rejoue une partie « neuve »
        # avec les nombres de la précédente encore lisibles à l'écran
        verifier(page.evaluate("() => SU.size") == 0, "les signes de numération sont oubliés")
        verifier(page.eval_on_selector_all("#corpus .tok.num", "e => e.length") == 0,
                 "plus aucun nombre en chiffres")
        verifier(page.evaluate("() => mesures().sig") == 0, "la jauge repart de 0 %")

        print("\ncomptage d'occurrences dans le lexique")
        frq = lambda: page.eval_on_selector_all("#lex .frq", "e => e.map(x => x.textContent)")
        page.evaluate("() => { S_.C = 9999; S_.b.tab = 0; }")
        page.wait_for_timeout(200)
        verifier(frq() == [], "rien sans Table de fréquences")
        page.evaluate("() => { S_.b.tab = 1; }")
        page.wait_for_timeout(200)
        verifier(frq() == [], "rien sans « deux » : le nombre serait illisible")
        page.evaluate("() => { acheterGl('an'); acheterGl('anna'); }")
        page.wait_for_timeout(250)
        verifier(len(frq()) == 3, f"un comptage par tête de branche : {frq()}")
        # le piège : compter les mots seuls donnerait 8 à « un » et 0 à « cinq », alors que
        # leur signe est partout DANS les nombres. Ce serait dire que la branche la plus
        # rentable du jeu est la plus pauvre.
        verifier(page.evaluate("() => freqGlyphe('an')") == 1668, "« un » compte ses chiffres (1 668)")
        verifier(page.evaluate("() => freqGlyphe('hem')") == 544, "« cinq » compte ses chiffres (544)")
        verifier(page.evaluate("() => freqGlyphe('tem')") == 315, "« grain », mot seul (315)")

        print("\nfenêtre de fin")
        page.evaluate("() => { S_.C = 9999; GL.forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(200)
        verifier(page.get_attribute("#end", "hidden") is None,
                 "elle s'ouvre au treizième signe")
        # relevé en PT5 : la partie finie, l'overlay couvrait le journal d'actions —
        # inatteignable au moment précis où il faut l'exporter
        verifier(page.evaluate("""() => {
                     const r = document.querySelector('#tr-cp').getBoundingClientRect();
                     const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
                     return !!e && e.id === 'tr-cp'; }"""),
                 "le bouton « copier » reste cliquable par-dessus")
        for fermeture, action in (("« revenir au corpus »", lambda: page.click("#fermer")),
                                  ("échap", lambda: page.keyboard.press("Escape")),
                                  ("un clic sur le fond", lambda: page.mouse.click(12, 500))):
            page.evaluate("() => { $('end').hidden = false; }")
            page.wait_for_timeout(120)
            action()
            page.wait_for_timeout(120)
            verifier(page.get_attribute("#end", "hidden") is not None, f"{fermeture} la ferme")
        # le corpus derrière est figé sur la partie terminée, pas remis à zéro
        verifier(page.evaluate("() => mesures().sig") > 50, "le corpus reste déchiffré derrière")

        print("\njournal d'actions (hors jeu)")
        page.evaluate("() => { TR.length = 0; prochainEtat = 0; }")
        for _ in range(3):
            page.click("#a-rel")
        page.click("#corpus .tok:not(.sep)")
        page.evaluate("() => { S_.O = 0; formuler(); }")                    # doit être ignoré
        page.evaluate("() => { S_.O = 500; S_.H = 20; formuler(); recouper(); acheterIns('cop'); }")
        page.evaluate("() => { versTablette(2); versTablette(2); }")        # doublon ignoré
        page.evaluate("() => { for (let i = 0; i < 30; i++) { S_.t += 3; tick(0.001); } }")
        lignes = [l for l in page.evaluate("() => tracesTSV()").split("\n")
                  if l and not l.startswith("#")]
        genres = [l.split("\t")[2] for l in lignes[1:]]
        etats = [float(l.split("\t")[1]) for l in lignes[1:] if l.split("\t")[2] == "etat"]
        verifier(lignes[0].split("\t") == ["temps", "t_s", "genre", "détail"], "en-tête TSV")
        verifier(sum(1 for l in lignes if l.endswith("\tbouton")) == 3, "3 relevés au bouton")
        verifier(sum(1 for l in lignes if l.endswith("\tcorpus")) == 1, "1 relevé dans le corpus")
        verifier(genres.count("formuler") == 1, "l'action sans effet n'est pas journalisée")
        verifier(genres.count("recouper") == 1 and genres.count("acheterIns") == 1,
                 "recoupement et instrument journalisés")
        verifier(genres.count("tablette") == 1, "navigation dédoublonnée")
        verifier(len(etats) >= 3 and all(etats[i] - etats[i - 1] >= 25 for i in range(1, len(etats))),
                 f"{len(etats)} relevés d'état espacés de ~30 s")

        nav.close()

    print("\n" + ("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)"))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
