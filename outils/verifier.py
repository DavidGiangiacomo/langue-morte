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
  7. le relevé se fait dans le corpus, et le gisement d'une tablette s'épuise
  8. le recoupement se fait dans le corpus : deux passages d'un même signe

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

        print("\nle relevé, acte de lecture")
        verifier(page.evaluate("() => GIS_TOTAL") == 398, "gisement du corpus : 398 relevés")
        ouvert = page.evaluate(
            "() => { let n = 0; for (let i = 0; i < revCount(); i++) n += gisReste(TB[i].t); return n; }")
        verifier(ouvert == 13, f"13 relevés ouverts au départ ({ouvert})")
        # le tarif est figé au dégagement : sinon la stratégie optimale est de ne rien
        # relever pendant quarante minutes puis de tout vider au débit maximal
        page.evaluate("() => { S_.b.cop = 500; paintCorpus(null); }")
        page.wait_for_timeout(120)
        verifier(page.evaluate("() => S_.prix[TB[0].t]") == 1,
                 "le tarif d'une tablette dégagée ne bouge plus")
        gains = page.evaluate("""() => {
            const t = TB[0].t; S_.rel = {}; S_.prix[t] = 100; S_.O = 0;
            relever(t, 0); const a = S_.O; relever(t, 0); return [a, S_.O - a]; }""")
        verifier(gains == [100, 1], f"un jeton neuf paie {gains[0]}, le repassage {gains[1]}")
        # épuisé, le gisement rend le plancher et jamais zéro : sinon l'ouverture se
        # verrouille, les 4 tablettes du départ n'offrant que 13 relevés pour un Copiste à 15
        epuise = page.evaluate("""() => {
            const t = TB[0].t; S_.rel = {}; S_.prix[t] = 100; S_.O = 0;
            for (let j = 0; j < GISEMENT[t] + 5; j++) relever(t, j);
            return [gisReste(t), S_.O, GISEMENT[t]]; }""")
        verifier(epuise[0] == 0, "le gisement d'une tablette s'épuise")
        verifier("plus rien à en tirer" in page.eval_on_selector("#log", "e => e.textContent"),
                 "et le journal le dit")
        verifier(epuise[1] == 100 * epuise[2] + 5, "puis rend le plancher, jamais zéro")
        page.evaluate("() => { S_.b.cop = 0; S_.rel = {}; S_.O = 0; paintCorpus(null); }")
        page.wait_for_timeout(120)
        page.click("#corpus .tok:not(.sep)")
        page.wait_for_timeout(120)
        verifier(page.eval_on_selector_all("#corpus .tok.rel", "e => e.length") == 1,
                 "le jeton relevé reste marqué")
        page.evaluate("() => paintCorpus(null)")
        page.wait_for_timeout(120)
        verifier(page.eval_on_selector_all("#corpus .tok.rel", "e => e.length") == 1,
                 "et le reste après un repeint complet")
        page.evaluate("""() => { const t = TB[0].t; S_.rel = {}; S_.rel[t] = [];
            for (let j = 0; j < GISEMENT[t]; j++) S_.rel[t].push(j); paintCorpus(null); }""")
        page.wait_for_timeout(120)
        verifier(page.evaluate("() => $('rail').children[0].classList.contains('sec')"),
                 "la tablette épuisée s'éteint dans la barre")
        page.evaluate("() => { S_.rel = {}; paintCorpus(null); }")

        print("\nle recoupement, dans le texte")
        page.evaluate("() => { S_.O = 500; S_.H = 50; S_.C = 0; S_.rec = 0; recArmer(false); }")
        page.wait_for_timeout(140)
        page.click("#a-rec")
        page.wait_for_timeout(140)
        verifier(page.evaluate("() => recArme") is True and page.evaluate("() => S_.rec") == 0,
                 "le bouton arme le corpus au lieu de recouper")
        # choisir un passage allume toutes les autres attestations du même signe
        page.evaluate("""() => { const e = document.querySelector('.tablet[data-tb="1"] [data-w="tem"]');
            recChoisir(1, +e.dataset.j, 'tem'); }""")
        page.wait_for_timeout(140)
        ec = page.evaluate("""() => [
            document.querySelectorAll('#corpus .tok.echo').length,
            document.querySelectorAll('.tablet[data-tb="1"] .tok.echo').length,
            document.querySelectorAll('#corpus .tok.pick').length,
            document.querySelectorAll('.tablet[hidden] .tok.echo').length]""")
        verifier(ec[0] > 0 and ec[2] == 1, f"{ec[0]} attestations allumées ailleurs, 1 passage retenu")
        verifier(ec[1] == 0, "aucune dans la tablette du passage : il en faut deux")
        verifier(ec[3] == 0, "aucune dans une tablette non dégagée")
        # deux passages d'une même tablette ne recoupent pas : ils déplacent le choix
        avant = page.evaluate("() => S_.rec")
        page.evaluate("""() => { const l = document.querySelectorAll('.tablet[data-tb="1"] [data-w="tem"]');
            recChoisir(1, +l[1].dataset.j, 'tem'); }""")
        page.wait_for_timeout(100)
        verifier(page.evaluate("() => S_.rec") == avant,
                 "deux passages d'une même tablette ne recoupent pas")
        res = page.evaluate("""() => {
            const a = document.querySelector('.tablet[data-tb="1"] [data-w="tem"]');
            recChoisir(1, +a.dataset.j, 'tem');
            const o = S_.O, h = S_.H, c = S_.C, r = S_.rec;
            const b = document.querySelector('.tablet[data-tb="2"] [data-w="tem"]');
            recChoisir(2, +b.dataset.j, 'tem');
            return [S_.rec - r, S_.C - c, o - S_.O, h - S_.H, recArme, recSel.tb]; }""")
        verifier(res[0] == 1 and res[1] == 1, f"deux tablettes différentes : +{res[1]} certitude")
        verifier(res[2] == 12 and res[3] == 3, f"coût inchangé : {res[2]} occ. + {res[3]} hyp.")
        verifier(res[4] is True and res[5] == 2,
                 "on reste armé, et le second passage devient le point d'appui")
        # on suit alors le signe de tablette en tablette, un clic par rapprochement
        suite = page.evaluate("""() => {
            const r = S_.rec;
            for (const t of [3, 4, 2]) {
                const e = document.querySelector('.tablet[data-tb="' + t + '"] [data-w="tem"]');
                if (e) recChoisir(t, +e.dataset.j, 'tem');
            }
            return S_.rec - r; }""")
        verifier(suite == 3, f"trois clics de suite = trois rapprochements ({suite})")
        # la barre désigne où chercher : sinon c'est une chasse au trésor dans 30 tablettes
        cib = page.evaluate("""() => {
            const c = [...document.querySelectorAll('.rcell.cible')].map(e => e.title);
            return [c.length, c.some(t => t.startsWith('tablette ' + recSel.tb + ' '))]; }""")
        verifier(cib[0] > 0, f"{cib[0]} tablettes désignées dans la barre")
        verifier(cib[1] is False, "sauf celle du passage retenu")
        # armé, le clic sert au recoupement et ne relève pas
        page.evaluate("() => { S_.rel = {}; S_.clicks = 0; }")
        page.click("#corpus .tablet:not([hidden]) .tok:not(.sep)")
        page.wait_for_timeout(140)
        verifier(page.evaluate("() => S_.clicks") == 0, "armé, le clic ne relève pas")
        page.evaluate("""() => { recSel = null;
            const e = document.querySelector('.tablet:not([hidden]) [data-n]');
            recChoisir(+e.closest('.tablet').dataset.tb, +e.dataset.j, e.dataset.w); }""")
        verifier(page.evaluate("() => recSel === null"), "un nombre n'est pas un signe : rien à recouper")
        # PT6 : armé sans les ressources, le bouton désactivé enfermait le joueur — il ne
        # pouvait plus ni désarmer ni relever, et rien ne disait qu'échap existait
        page.evaluate("() => { S_.O = 0; S_.H = 0; }")
        page.wait_for_timeout(140)
        verifier(page.evaluate("() => document.getElementById('a-rec').disabled") is False,
                 "armé sans ressources, le bouton reste cliquable")
        verifier("pas de quoi" in page.eval_on_selector("#a-rec .an", "e => e.textContent"),
                 "et il dit pourquoi")
        page.click("#a-rec")
        page.wait_for_timeout(140)
        verifier(page.evaluate("() => recArme") is False, "un clic désarme malgré tout")
        verifier(page.evaluate("() => document.getElementById('a-rec').disabled") is True,
                 "désarmé et sans ressources, il redevient inerte")
        page.evaluate("() => { S_.O = 500; S_.H = 50; recArmer(true); }")
        page.wait_for_timeout(140)
        page.keyboard.press("Escape")
        page.wait_for_timeout(140)
        verifier(page.evaluate("() => recArme") is False, "échap désarme")
        verifier(page.eval_on_selector_all("#corpus .tok.echo, #corpus .tok.pick", "e => e.length") == 0,
                 "et éteint les attestations")

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
        page.evaluate("() => { TR.length = 0; prochainEtat = 0; S_.t = 0; }")
        jetons = page.query_selector_all("#corpus .tablet:not([hidden]) .tok:not(.sep)")
        for el in jetons[:3]:
            el.click()
        page.evaluate("() => { S_.O = 0; formuler(); }")                    # doit être ignoré
        page.evaluate("() => { S_.O = 500; S_.H = 20; formuler(); recouper(); acheterIns('cop'); }")
        page.evaluate("() => { versTablette(2); versTablette(2); }")        # doublon ignoré
        page.evaluate("() => { for (let i = 0; i < 30; i++) { S_.t += 3; tick(0.001); } }")
        lignes = [l for l in page.evaluate("() => tracesTSV()").split("\n")
                  if l and not l.startswith("#")]
        genres = [l.split("\t")[2] for l in lignes[1:]]
        etats = [float(l.split("\t")[1]) for l in lignes[1:] if l.split("\t")[2] == "etat"]
        verifier(lignes[0].split("\t") == ["temps", "t_s", "genre", "détail"], "en-tête TSV")
        verifier(genres.count("relever") == 3, "3 relevés journalisés")
        verifier(all("tablette " in l.split("\t")[3] for l in lignes if "\trelever\t" in l),
                 "chaque relevé note sa tablette")
        verifier(genres.count("formuler") == 1, "l'action sans effet n'est pas journalisée")
        verifier(genres.count("recouper") == 1 and genres.count("acheterIns") == 1,
                 "recoupement et instrument journalisés")
        verifier(genres.count("tablette") == 1, "navigation dédoublonnée")
        # le premier relevé tombe au démarrage du journal ; c'est à partir du deuxième
        # que la cadence doit être régulière
        pas = [round(etats[i] - etats[i - 1]) for i in range(2, len(etats))]
        verifier(len(etats) >= 3 and all(p == 30 for p in pas),
                 f"{len(etats)} relevés d'état, cadence {set(pas) or '—'} s")

        nav.close()

    print("\n" + ("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)"))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
