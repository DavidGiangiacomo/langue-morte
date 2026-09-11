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
  7. le relevé se fait dans le corpus ; le gisement s'épuise et se tarife à la 1re visite
  8. le recoupement se fait dans le corpus : deux passages d'un même signe
  9. la datation : une tablette se date quand on sait lire sa date, et pas avant
 10. le rangement chronologique range l'affichage sans rien dégager de neuf
 11. la Grammaire s'ouvre à « année » et croît avec le lexique
 12. la nuit : 40 % du débit hors ligne, plafonnée, consommée une seule fois
 13. la concordance : le corpus se replie sur les attestations d'un signe, et la crue
     se lit alors de 14 à 0
 14. la composition : la grille s'ouvre à « année », l'ordre compte, l'échec ne coûte
     jamais de Certitude, et un composé secret n'avance pas la progression de l'arbre
 15. une partie commencée avant une mécanique neuve se rouvre sans rien perdre

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

SIGNES_ATTENDUS = 3838          # cf. sortie de outils/corpus.py
RENDU_MAX_S = 4.0

# glyphe acheté -> ensemble exact des nombres du corpus qui doivent devenir lisibles
ECHELLE = [
    ("un",   lambda ns: ns == [1]),
    ("deux", lambda ns: ns == [1, 2, 3, 4]),
    ("cinq", lambda ns: set(ns) >= set(range(1, 10)) and 50 in ns and 10 not in ns),
    ("dix",  lambda ns: set(ns) >= set(range(1, 100)) and 100 not in ns),
    ("cent", lambda ns: 212 in ns and 756 in ns and 1200 not in ns),
    ("mille", lambda ns: 1200 in ns),
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
        verifier(page.evaluate("() => GIS_TOTAL") == 399, "gisement du corpus : 399 relevés")
        ouvert = page.evaluate(
            "() => { let n = 0; for (let i = 0; i < revCount(); i++) n += gisReste(TB[i].t); return n; }")
        verifier(ouvert == 13, f"13 relevés ouverts au départ ({ouvert})")
        # Le tarif se fige à la première visite, pas au dégagement : le figer au dégagement
        # laissait à 1 occurrence, pour toute la partie, les tablettes qu'on atteint tôt.
        verifier(page.evaluate("() => Object.keys(S_.prix).length") == 0,
                 "dégager une tablette ne la tarife pas")
        marq = page.evaluate("""() => { const c = $('rail').children, n = revCount();
            let m = 0; for (let i = 0; i < n; i++) if (c[i].classList.contains('lue')) m++;
            return [m, n]; }""")
        verifier(marq[0] == 0,
                 f"et aucune des {marq[1]} tablettes du départ n'est marquée lue ({marq[0]})")
        page.evaluate("() => { S_.b.cop = 500; S_.rel = {}; S_.prix = {}; S_.O = 0; }")
        page.wait_for_timeout(120)
        tar = page.evaluate("""() => {
            const t = TB[0].t;
            relever(t, 0); const a = S_.prix[t];
            S_.b.cop = 5000;                       // le débit décuple entre les deux relevés
            relever(t, 1);
            return [Math.round(a), Math.round(S_.prix[t]), Math.round(tarifRel())]; }""")
        verifier(tar[0] == 601, f"la première visite tarife au débit du moment ({tar[0]})")
        verifier(tar[0] == tar[1], "et le tarif ne bouge plus ensuite")
        verifier(tar[2] > tar[1] * 5,
                 f"même quand le débit a décuplé (il vaudrait {tar[2]} aujourd'hui)")
        mk = page.evaluate("""() => { peindreGisement(); const c = $('rail').children;
            return [c[0].classList.contains('lue'), c[1].classList.contains('lue'),
                    titreCell(TB[0].t), titreCell(TB[1].t)]; }""")
        verifier(mk[0] is True and mk[1] is False,
                 "le premier relevé marque sa tablette comme lue, et elle seule")
        verifier("intacte :" in mk[3] and "si tu l'ouvres maintenant" in mk[3],
                 "l'infobulle d'une intacte chiffre le tarif du moment")
        verifier("occ. par relevé" in mk[2] and "intacte" not in mk[2],
                 "celle d'une tablette travaillée donne son tarif acquis")
        # le tarif d'une intacte suit la production : figé dans l'attribut, il serait faux
        suit = page.evaluate("""() => { const a = titreCell(TB[1].t);
            S_.b.cop *= 4; return [a, titreCell(TB[1].t)]; }""")
        verifier(suit[0] != suit[1], "et il suit la production, au lieu d'être figé")
        page.hover('#rail .rcell:nth-child(2)')
        page.wait_for_timeout(120)
        verifier("intacte :" in page.eval_on_selector("#rail .rcell:nth-child(2)",
                                                      "e => e.title"),
                 "le survol l'écrit sur la cellule")
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
        # les deux bouts de l'échelle ne se cumulent pas : éteinte, elle n'est pas en plus assombrie
        cl = page.evaluate("() => $('rail').children[0].className")
        verifier("lue" not in cl, "et cesse d'être seulement marquée lue")
        verifier("épuisée" in page.evaluate("() => titreCell(TB[0].t)"),
                 "son infobulle le dit")
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
        verifier(len(frq()) == 4, f"un comptage par tête de branche : {frq()}")
        # le piège : compter les mots seuls donnerait 8 à « un » et 0 à « cinq », alors que
        # leur signe est partout DANS les nombres. Ce serait dire que la branche la plus
        # rentable du jeu est la plus pauvre.
        verifier(page.evaluate("() => freqGlyphe('an')") == 1661, "« un » compte ses chiffres (1 661)")
        verifier(page.evaluate("() => freqGlyphe('hem')") == 543, "« cinq » compte ses chiffres (543)")
        verifier(page.evaluate("() => freqGlyphe('tem')") == 315, "« grain », mot seul (315)")

        print("\nacte III : la datation, puis le rangement")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        datees = lambda: page.evaluate("() => TB.filter(tb => datee(tb.t)).length")
        ordreBarre = lambda: page.eval_on_selector_all("#rail .rcell", "e => e.map(x => +x.dataset.go)")
        ordreTexte = lambda: page.eval_on_selector_all("#corpus .tablet", "e => e.map(x => +x.dataset.tb)")
        sortie = page.evaluate("() => ORDRE")
        verifier(datees() == 0, "aucune tablette datée au départ")

        # les cinq glyphes de nombre ne datent rien : la date est là, illisible faute du mot
        page.evaluate("""() => { S_.C = 9999;
            ['an','anna','hem','sela','meku'].forEach(acheterGl); }""")
        page.wait_for_timeout(250)
        verifier(datees() == 0, "savoir lire les nombres ne suffit pas à dater")
        page.evaluate("() => { S_.C = 9999; acheterGl('nur'); }")
        page.wait_for_timeout(250)
        verifier(datees() == 28, f"« année » date 28 tablettes ({datees()})")
        verifier(page.evaluate("""() => document.querySelector('#rail .rcell[data-go="1"] .ry').textContent"""
                              ) == "9", "la barre porte l'année de la tablette 1")
        verifier(ordreBarre() == sortie and ordreTexte() == sortie,
                 "dater ne range pas : l'ordre reste celui de la sortie de terre")

        vues = lambda: page.eval_on_selector_all("#corpus .tablet:not([hidden])", "e => e.map(x => +x.dataset.tb)")
        page.evaluate("() => { S_.C = 9999; acheterGl('pat'); }")
        page.wait_for_timeout(250)
        verifier(ordreBarre() != sortie and ordreTexte() == sortie,
                 "« avant » range la barre, et elle seule")
        page.evaluate("() => { S_.C = 9999; acheterGl('zur'); }")
        page.wait_for_timeout(250)
        verifier(ordreTexte() != sortie, "« après » range le texte")
        # le corpus se numérote lui-même dans l'ordre du temps — c'est ce que le rangement
        # démontre, et personne ne le dit au joueur
        verifier(ordreTexte()[:28] == sorted(ordreTexte()[:28]),
                 "les 28 tablettes datées se rangent dans l'ordre de leur numéro")
        verifier(ordreTexte()[-2:] == [29, 30], "les deux non datées ferment la marche")
        # le dégagement suit la sortie de terre, le rangement l'affichage : les deux ne
        # doivent jamais se confondre, sinon ranger dégagerait des tablettes d'avance
        verifier(sorted(vues()) == sorted(sortie[:len(vues())]),
                 f"les {len(vues())} dégagées restent les premières sorties de terre")
        annees = page.evaluate("""() => [...document.querySelectorAll('#corpus .tablet')]
            .filter(e => datee(+e.dataset.tb) && !ANNEE[+e.dataset.tb].fin)
            .map(e => ANNEE[+e.dataset.tb].n)""")
        verifier(annees == sorted(annees), "les années lues à l'écran ne reculent jamais")
        page.evaluate("() => { S_.C = 9999; ['nurnur','esh','nurhal'].forEach(acheterGl); }")
        page.wait_for_timeout(250)
        verifier(datees() == 30, "« dernière-année » date les deux dernières")

        print("\nla Grammaire")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        ouverte = lambda: page.evaluate("() => INS.find(i => i.k === 'gram').unlock()")
        verifier(not ouverte(), "fermée tant qu'on n'a pas « année »")
        page.evaluate("() => { S_.C = 9999; acheterGl('nur'); }")
        page.wait_for_timeout(200)
        verifier(ouverte(), "ouverte par « année »")
        # son rendement dépend du lexique, et c'est la seule qui ait cette propriété
        r1 = page.evaluate("() => GRAM_P * gramMul() * M.gram()")
        page.evaluate("() => { S_.C = 9999; ['an','anna','hem'].forEach(acheterGl); }")
        page.wait_for_timeout(200)
        r2 = page.evaluate("() => GRAM_P * gramMul() * M.gram()")
        verifier(r2 > r1 * 1.5, f"trois signes de plus la font passer de {r1:.4f} à {r2:.4f} cert./s")

        print("\nla composition : poser un signe sur un autre")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        verifier(page.get_attribute("#pcomp", "hidden") is not None,
                 "pas de grille tant qu'on n'a pas « année »")
        # Les recettes sont dérivées de COMP, dont les valeurs sont des clés de TRACÉ : elles
        # ne valent comme règle du jeu qu'une fois traduites en glyphes, et filtrées sur ceux
        # qui existent. `selanna` (vingt) reste dessinable mais a été retiré du lexique.
        rec = page.evaluate("() => RECETTES")
        verifier(set(rec) == {"anna", "urtem", "nurnur"},
                 f"trois recettes ouvertes aujourd'hui : {sorted(rec)}")
        verifier("selanna" not in rec, "« vingt » n'est proposé par aucune recette")
        verifier("nurhal" not in rec,
                 "« dernière-année » non plus : `finir` n'est pas encore un glyphe")

        page.evaluate("() => { S_.C = 9999; ['nur','ur','tem'].forEach(acheterGl); S_.C = 500; }")
        page.wait_for_timeout(250)
        verifier(page.get_attribute("#pcomp", "hidden") is None, "« année » ouvre la grille")
        vus = page.eval_on_selector_all("#comp-choix .pion:not([hidden])", "e => e.length")
        verifier(vus == 3, f"on ne peut poser que ce qu'on sait lire : {vus} signes")

        # L'ordre compte : ⟨grenier⟩ porte la maison à gauche et le grain à droite, et le
        # corpus le montre depuis la première seconde. Le mauvais sens ne donne rien.
        page.evaluate("() => { S_.H = 100000; }")
        page.wait_for_timeout(120)
        base_h = page.evaluate("() => compCost()")
        r = page.evaluate("""() => { const c = S_.C, h = S_.H;
            const issue = composer('tem', 'ur');
            return [issue, c - S_.C, h - S_.H, S_.carnet.slice(), has('urtem')]; }""")
        verifier(r[0] == "rate" and r[4] is False, "grain + maison ne donne rien")
        verifier(r[1] == 0, "et ne coûte AUCUNE certitude — jamais (R3)")
        verifier(r[2] == base_h, f"seulement des hypothèses : {r[2]}")
        verifier(r[3] == ["tem+ur"], f"la paire entre au carnet : {r[3]}")

        r = page.evaluate("""() => { const h = S_.H, n = S_.comp;
            const issue = composer('tem', 'ur');
            return [issue, h - S_.H, S_.comp - n]; }""")
        verifier(r == ["refus", 0, 0], "la même paire retentée ne coûte plus rien")

        page.wait_for_timeout(150)
        verifier(page.get_attribute("#carnet", "hidden") is None,
                 "le carnet apparaît après la première tentative")
        c2 = page.evaluate("() => compCost()")
        verifier(c2 > base_h,
                 f"la tentative suivante coûte plus cher : {c2} contre {base_h}")

        # Le bon sens, lui, acquiert le composé au coût normal en Certitude.
        avant_rev = page.eval_on_selector_all("#corpus .tablet:not([hidden])", "e => e.length")
        r = page.evaluate("""() => { const c = S_.C, h = S_.H, n = nArbre();
            const issue = composer('ur', 'tem');
            return [issue, c - S_.C, h - S_.H, nArbre() - n, has('urtem')]; }""")
        page.wait_for_timeout(280)
        verifier(r[0] == "acquis" and r[4] is True, "maison + grain donne le grenier")
        verifier(r[1] == 60 and r[2] == 0,
                 f"au coût normal en certitude ({r[1]} C), sans toucher aux hypothèses")
        # Ce qui suit protège une économie réglée sur neuf playtests : un composé secret
        # s'ajoute à ce que le joueur SAIT, jamais à ce que l'arbre a rendu.
        verifier(r[3] == 0, "le compte de l'arbre ne bouge pas")
        verifier(page.text_content("#lexr").strip() == "3 / 20", "le lexique affiche « 3 / 20 »")
        apres_rev = page.eval_on_selector_all("#corpus .tablet:not([hidden])", "e => e.length")
        verifier(apres_rev == avant_rev, "et aucune tablette n'est dégagée en composant")

        lus = page.eval_on_selector_all("#corpus .tok[data-w=urtem]",
                                        "e => e.filter(x => x.textContent.trim() === 'grenier').length")
        verifier(lus == 24, f"les {lus} attestations du grenier passent en français")
        verifier(page.get_attribute("#lexsec", "hidden") is None,
                 "le bloc « Composés » du lexique s'ouvre")
        verifier(page.evaluate("() => $('lex').querySelector('[data-gl=urtem]').disabled") is True,
                 "et sa carte ne s'achète pas : on ne l'achète pas, on l'a posée")

        r = page.evaluate("""() => [composer('ur','tem'), composer('kish','tem'),
                                    composer('nur','nur')]""")
        verifier(r[0] == "refus", "le grenier ne se recompose pas")
        verifier(r[1] == "refus", "un signe qu'on ne sait pas lire ne se pose pas")
        verifier(r[2] == "acquis", "année + année donne le siècle, sans passer par la branche")

        print("\nla concordance : rassembler les attestations d'un signe")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        verifier(page.get_attribute("#a-con", "hidden") is not None,
                 "pas de bouton sans Concordance")
        page.evaluate("() => { S_.b.con = 1; }")
        page.wait_for_timeout(120)
        verifier(page.get_attribute("#a-con", "hidden") is None,
                 "la première Concordance le fait apparaître")
        # tout le corpus, puis la seule colonne de l'eau
        page.evaluate("() => { S_.C = 9999; GL.forEach(g => acheterGl(g.id)); $('end').hidden = true; }")
        page.wait_for_timeout(300)
        lignes = lambda: page.eval_on_selector_all(
            "#corpus .tablet:not([hidden]):not(.vide) .ln:not(.off)", "e => e.length")
        avant = lignes()
        verifier(avant == 705, f"corpus entier : {avant} lignes")
        page.evaluate("() => concChoisir('kish')")
        page.wait_for_timeout(250)
        apres = lignes()
        verifier(apres < avant / 6, f"replié sur « eau » : {apres} lignes ({avant} avant)")
        # chaque tablette gardée montre sa première ligne, celle qui la date : sans elle la
        # colonne n'aurait plus de dates, et c'est du texte ancien, pas un en-tête ajouté
        dates = page.evaluate("""() => [...document.querySelectorAll('#corpus .tablet:not([hidden]):not(.vide)')]
            .map(e => { const l = e.querySelector('.ln'); return l && !l.classList.contains('off'); })""")
        verifier(all(dates) and len(dates) > 15,
                 f"les {len(dates)} tablettes retenues gardent leur ligne de date")
        # la série, dans l'ordre du temps : c'est tout le propos de l'acte III
        eaux = page.evaluate("""() => [...document.querySelectorAll('#corpus .tablet:not([hidden]):not(.vide)')]
            .map(e => { const tb = TBN[+e.dataset.tb];
              for (const l of tb.l) { const m = l.match(/^kish %(\\d+)$/); if (m) return +m[1]; }
              return null; }).filter(v => v !== null)""")
        verifier(eaux[0] == 14 and eaux[len(eaux) - 1] == 0,
                 f"la crue se lit de {eaux[0]} à {eaux[len(eaux)-1]} en {len(eaux)} relevés")
        verifier(sum(1 for i in range(1, len(eaux)) if eaux[i] > eaux[i - 1]) <= 4,
                 "elle descend, avec le bruit des bonnes années")
        # un nombre n'est pas un signe, et fermer rend le corpus entier
        page.evaluate("() => concChoisir(undefined)")
        page.wait_for_timeout(120)
        verifier(lignes() == apres, "un nombre ne se concorde pas")
        page.evaluate("() => concFermer()")
        page.wait_for_timeout(200)
        verifier(lignes() == avant, "fermer rend le corpus entier")

        print("\nla nuit : ce que le corpus produit sans le joueur")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("() => { S_.b.cop = 100; S_.O = 0; S_.ts = Date.now() - 3600 * 1000; }")
        verifier(page.evaluate("() => veillee()") == 0, "sans « nuit », l'absence ne produit rien")
        page.evaluate("() => { S_.C = 9999; acheterGl('esh'); }")
        page.wait_for_timeout(200)
        # une heure d'absence à 40 % du débit = 1 440 s de production, soit 144 000 pour
        # cent copistes sans aucun bonus
        nuit = page.evaluate("""() => { S_.O = 0; S_.t = 300; S_.ts = Date.now() - 3600 * 1000;
            const g = veillee(); return [Math.round(g), Math.round(S_.t)]; }""")
        verifier(abs(nuit[0] - 144000) < 2000, f"une heure d'absence rend 40 % du débit ({nuit[0]})")
        verifier(nuit[1] == 300, "et le chronomètre ne bouge pas : c'est du temps de lecture")
        plafond = page.evaluate("""() => { S_.O = 0; S_.ts = Date.now() - 20 * 3600 * 1000;
            return Math.round(veillee()); }""")
        verifier(abs(plafond - 4 * 144000) < 8000, f"vingt heures ne rendent que quatre ({plafond})")
        verifier(page.evaluate("() => veillee()") == 0, "et l'instant d'après, plus rien")
        # remettre les cent copistes à zéro : ils rendraient inabordable le Copiste que
        # la section suivante achète pour vérifier le journal d'actions
        page.evaluate("() => { S_.b.cop = 0; }")

        print("\nfenêtre de fin")
        page.evaluate("() => { S_.C = 9999; GL.forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(200)
        verifier(page.get_attribute("#end", "hidden") is None,
                 "elle s'ouvre au vingtième signe")
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

        # ---- une sauvegarde d'avant la mécanique neuve doit se rouvrir ----
        # La clé a déjà changé une fois, et toutes les parties en cours ont été perdues. Un
        # champ neuf est censé se migrer tout seul (`Object.assign(fresh(), p)`) ; ce test le
        # vérifie au lieu de le supposer. L'injection passe par un contexte neuf : recharger
        # l'onglet ferait sauvegarder la page courante par-dessus, via `pagehide`.
        print("\nune partie d'avant la composition se rouvre")
        ancienne = ('{"O":5000,"H":300,"C":120,"rec":9,"clicks":40,'
                    '"b":{"cop":12,"tab":8,"con":3,"ate":1,"gram":0},'
                    '"gl":["an","anna","tem","ur","im"],"t":900,"done":false,'
                    '"rel":{"1":[0,1]},"prix":{"1":7}}')
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-actes-i-iii', %r)" % ancienne)
        vieille = ctx.new_page()
        casses = []
        vieille.on("pageerror", lambda e: casses.append(str(e)))
        vieille.goto(PAGE.resolve().as_uri())
        vieille.wait_for_timeout(700)
        verifier(not casses, f"aucune erreur au chargement : {casses[:1] or '—'}")
        etat = vieille.evaluate("() => [S_.gl.length, Math.round(S_.C), S_.rec, S_.b.cop]")
        verifier(etat == [5, 120, 9, 12], f"la partie est reprise telle quelle : {etat}")
        neufs = vieille.evaluate("() => [Array.isArray(S_.carnet), S_.carnet.length, S_.comp]")
        verifier(neufs == [True, 0, 0], f"les champs neufs arrivent vides : {neufs}")
        verifier(vieille.text_content("#lexr").strip() == "5 / 20", "le lexique compte cinq signes")
        r = vieille.evaluate("""() => { S_.C = 9999; acheterGl('nur'); S_.H = 99999;
            const i = composer('tem','im'); sauver();
            const p = JSON.parse(localStorage.getItem('langue-morte-actes-i-iii'));
            return [i, p.carnet, p.comp]; }""")
        verifier(r == ["rate", ["tem+im"], 1], f"et la composition s'y enregistre : {r}")
        ctx.close()

        nav.close()

    print("\n" + ("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)"))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
