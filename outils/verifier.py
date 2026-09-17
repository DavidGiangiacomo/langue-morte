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
  6. la fenêtre de fin attend qu'on ait lu la tablette du dernier signe, se ferme,
     et ne couvre pas les outils hors jeu
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
 16. la Parole III : `lire` après `copier`, les trois effets, `scribe` composable et compté
     dans l'arbre
 17. la Modalité : la branche s'ouvre sur le signe le plus fréquent du corpus, `il-faut`
     porte l'atelier et non la grammaire, et les 816 attestations passent en français
 18. `zéro` : composé de deux branches et de deux actes, il ne s'obtient qu'à la grille,
     n'avance pas l'arbre, et rend lisibles les onze zéros du corpus
 19. `les-lecteurs` : dernier signe de l'acte III, il n'ouvre aucune recette tant que
     ⟨nous⟩ n'est pas au lexique, ne multiplie rien, et laisse la tablette 18 à 80 %
 20. une partie finie quand l'arbre était plus petit reprend au lieu de rouvrir sur la fin
 21. l'ambiguïté : un signe ambigu propose ses deux lectures au même prix et au même
     effet, la fausse repeint tout le corpus et ses composés, la prime de 25 % ne se
     lit nulle part, la dette court sans s'afficher, et les ruptures d'AMB-4 se rendent
     bien dans le texte
 22. le doute : il est le même pour les deux lectures d'un signe, il se fige à la décision
     et non au regard, la rupture distributionnelle du §7.4 se lit en infobulle, et la
     révision repeint le corpus sans jamais dire si l'on avait raison
 23. la contradiction : elle se solde à l'ouverture du doute, le passage qui refuse ne bouge
     pas avec les signes mal lus, aucune progression n'est perdue (R2), et la révision la
     lève sans la réarmer
 24. `faux` : il allume les lignes où la lecture ne se construit pas — la LIGNE et jamais le
     jeton — et n'allume rien pour les quatre signes sans rupture ni pour une paire réparante
 25. les trois builds : ce que chacun n'a pas — la boucle tourne sans chronomètre, « recommencer »
     marche sans le bouton de la barre, et le sélecteur de vitesse se journalise là où il reste

Prérequis : pip install playwright && playwright install chromium
"""
import json
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
# 6 s et non 4 : au tout premier lancement, navigateur froid, le rendu des 3 838 signes
# est monté à 4,30 s pour 1,50 s à chaque lancement suivant. Un seuil qui échoue une
# fois sur dix pour une raison qui n'est pas dans le code apprend à ignorer les échecs.
RENDU_MAX_S = 6.0

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

        # Le dénominateur du compteur de lexique EST la taille de l'arbre. Le figer dans
        # ces tests les fait échouer à chaque lot de glyphes sans que rien soit cassé —
        # la leçon du garde-fou de durée de `balayage.py`, ici en petit.
        ngl = page.evaluate("() => NGL")

        print("\nchargement")
        verifier(not erreurs, f"aucune erreur JS ({erreurs[:2] if erreurs else ''})")
        verifier(duree < RENDU_MAX_S, f"rendu en {duree:.2f}s (< {RENDU_MAX_S}s)")

        signes = page.eval_on_selector_all("#corpus .tok:not(.sep)", "e => e.length")
        verifier(signes == SIGNES_ATTENDUS, f"{signes} signes rendus (attendu {SIGNES_ATTENDUS})")

        tablettes = page.eval_on_selector_all(".tablet:not([hidden])", "e => e.length")
        verifier(tablettes == 4, f"{tablettes} tablettes dégagées au départ (attendu 4)")

        # Le dégagement : quatre tablettes tant qu'on ne lit rien, les trente au dernier
        # signe de l'arbre, et jamais un pas en arrière. `REV_R` règle la forme de la courbe
        # entre les deux (14/09/2026) ; ces trois bornes-là ne se règlent pas — la première
        # est le gabarit de l'acte I, la dernière est le corpus entier.
        courbe = page.evaluate("""() => { const vrai = S_.gl.slice();
            const suite = []; S_.gl.length = 0; suite.push(revCount());
            for(const g of GL.filter(x => !x.sec)){ S_.gl.push(g.id); suite.push(revCount()); }
            S_.gl.length = 0; S_.gl.push(...vrai); return suite; }""")
        verifier(courbe[0] == 4 and courbe[-1] == 30,
                 f"quatre tablettes à zéro signe, trente au dernier : {courbe[0]} → {courbe[-1]}")
        verifier(all(y >= x for x, y in zip(courbe, courbe[1:])) and max(courbe) <= 30,
                 f"et la courbe ne recule jamais : {courbe}")

        def acheter_carte(trancher="j"):
            """Achète la première carte payable du lexique et rend son identifiant. Un signe
            ambigu n'est pas acheté au clic : il ouvre ses deux lectures (AMB-1), et c'est le
            second clic qui paie. `trancher` dit laquelle prendre — juste par défaut, pour
            que tout ce qui était vrai avant ce lot le reste."""
            carte = page.query_selector("#lex .gcard.afford")
            if not carte:
                return None
            gl = carte.get_attribute("data-gl")
            carte.click()
            page.wait_for_timeout(120)
            if page.query_selector("#amb:not([hidden])"):
                i = page.evaluate("(t) => ambOrdre.indexOf(t)", trancher)
                page.query_selector(f'#amb-choix [data-amb="{i}"]').click()
                page.wait_for_timeout(120)
            return gl

        print("\néchelle de la numération")
        for mot, attendu in ECHELLE:
            page.evaluate("(m) => { const g = GL.find(x => x.mot === m); S_.C += g.cost; }", mot)
            page.wait_for_timeout(120)
            acheter_carte()
            page.wait_for_timeout(180)
            lus = sorted({int(t) for t in page.eval_on_selector_all(
                "#corpus .tok.num", "e => e.map(x => x.textContent.replace(/\\D/g, ''))") if t})
            verifier(attendu(lus), f"après « {mot} » : {lus[:12]}{' …' if len(lus) > 12 else ''}")

        print("\ninfobulles")

        # acheter de quoi avoir des mots traduits (les 5 glyphes de nombre n'en donnent aucun)
        page.evaluate("() => { S_.C = 9999; }")
        page.wait_for_timeout(120)
        for _ in range(3):
            acheter_carte()
            page.wait_for_timeout(120)

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
        verifier(len(frq()) == 5, f"un comptage par tête de branche : {frq()}")
        # La Modalité entre par le signe le plus fréquent du corpus : 290 attestations,
        # dont aucune lisible jusque-là. C'est l'arbitrage que la Table met sous les yeux.
        verifier(page.evaluate("() => freqGlyphe('la')") == 290,
                 "« ne-pas », tête de la Modalité (290)")
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
        verifier(set(rec) == {"anna", "urtem", "nurnur", "imme", "tabsar", "enla", "lan"},
                 f"sept recettes ouvertes aujourd'hui : {sorted(rec)}")
        # la Parole III les a ouvertes d'elle-même, sans qu'aucune liste soit tenue (règle 15)
        verifier(rec.get("imme") == ["im", "sar"] and rec.get("tabsar") == ["tab", "sar"],
                 "scribe = dire + graver, archive = tablette + graver")
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
        verifier(page.text_content("#lexr").strip() == f"3 / {ngl}", f"le lexique affiche « 3 / {ngl} »")
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

        print("\nla Parole III : lire, scribe, archive")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        ordre = page.evaluate("() => GL.filter(g => g.br === 'parole').map(g => g.id)")
        verifier(ordre == ["im", "sar", "kal", "shen", "imme", "tabsar", "shenu"],
                 f"posés dans la branche après « copier » : {ordre}")
        classe = lambda i: page.evaluate("i => $('lex').querySelector('[data-gl=\"'+i+'\"]').className", i)
        page.evaluate("() => { S_.C = 99999; ['im','sar'].forEach(acheterGl); }")
        page.wait_for_timeout(150)
        verifier("locked" in classe("shen"), "« lire » reste fermé tant que « copier » manque")
        page.evaluate("() => acheterGl('kal')")
        page.wait_for_timeout(150)
        verifier("locked" not in classe("shen") and "locked" in classe("imme"),
                 "« copier » ouvre « lire », et lui seul")
        r = page.evaluate("""() => { const g0 = M.gram(); acheterGl('shen');
            const c0 = M.cop(), a0 = M.ate(); acheterGl('imme');
            const t0 = M.tabl(); acheterGl('tabsar');
            return [M.gram()/g0, M.cop()/c0, M.ate()/a0, M.tabl()/t0].map(x => Math.round(x*100)/100); }""")
        verifier(r == [1.5, 1.5, 1.5, 1.5],
                 f"+50 % grammaire, copiste, atelier, table : {r}")
        page.wait_for_timeout(250)
        # les deux signes étaient dans le texte depuis la première seconde : l'achat ne fait
        # que les rendre lisibles, et partout — y compris dans les tablettes pas encore dégagées
        lus = page.eval_on_selector_all("#corpus .tok[data-w=imme]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'scribe').length]")
        verifier(lus[0] == 65 and lus[1] == 65, f"les signatures se lisent : {lus[1]} « scribe » sur {lus[0]}")
        lus = page.eval_on_selector_all("#corpus .tok[data-w=shen]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'lire').length]")
        verifier(lus[0] == 92 and lus[1] == 92, f"« lire » partout : {lus[1]} sur {lus[0]}")

        # Glyphe d'arbre composable : posé en avance, il avance la partie — contrairement au
        # grenier, secret, qui n'ajoute qu'au savoir.
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 99999; ['im','sar','nur'].forEach(acheterGl);
            S_.C = 700; S_.H = 100000; const n = nArbre();
            return [composer('im','sar'), nArbre() - n, has('imme'), has('kal')]; }""")
        page.wait_for_timeout(250)
        verifier(r == ["acquis", 1, True, False],
                 f"dire + graver donne le scribe avant « copier », et compte dans l'arbre : {r}")
        verifier(page.text_content("#lexr").strip() == f"4 / {ngl}", f"le lexique affiche « 4 / {ngl} »")
        verifier("done" in classe("imme") and "locked" in classe("tabsar"),
                 "sa carte est cochée, sans ouvrir « archive » par-dessus « copier »")

        print("\nla Modalité : ne-pas, si, peut-être, il-faut, faux, sinon")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        ordre = page.evaluate("() => GL.filter(g => g.br === 'modalite').map(g => g.id)")
        verifier(ordre == ["la", "en", "mik", "dun", "lash", "enla"],
                 f"six signes, du plus fréquent au dernier mot du protocole : {ordre}")
        page.evaluate("() => { S_.C = 99999; }")
        page.wait_for_timeout(150)
        verifier("locked" in classe("en"), "« si » reste fermé tant que « ne-pas » manque")
        # Le bonus va à l'atelier, pas à la grammaire : « il-faut copier » est une consigne de
        # copie, et la Modalité ne doit pas raccourcir l'acte qu'elle allonge (cf. economie.js).
        r = page.evaluate("""() => { ['la','en','mik'].forEach(acheterGl);
            const a0 = M.ate(), g0 = M.gram(); acheterGl('dun');
            return [M.ate()/a0, M.gram()/g0]; }""")
        verifier(r == [1.5, 1], f"« il-faut » : +50 % à l'atelier, rien à la grammaire : {r}")
        # `copier` avec eux : la consigne du protocole est « il-faut copier », et sans son
        # verbe la ligne ne se lit pas jusqu'au bout.
        page.evaluate("() => { ['enla','kal'].forEach(acheterGl); }")
        page.wait_for_timeout(300)
        lus = page.evaluate("""() => ['la','en','dun','enla'].map(id =>
            [...document.querySelectorAll('#corpus .tok[data-w='+id+']')]
              .filter(x => x.textContent.trim() === byId[id].mot).length)""")
        verifier(lus == [290, 239, 156, 131],
                 f"les {sum(lus)} attestations passent en français : {lus}")
        # Le protocole de copie, en entier : « il-faut copier · si ne-pas · sinon ». La ligne
        # s'arrête là, et ce qui vient après « sinon » n'est écrit nulle part (règle 5).
        ligne = page.evaluate("""() => { const tb = document.querySelector('.tablet[data-tb="8"]');
            return [...tb.children].map(l => [...l.children].map(t => t.textContent.trim()).join(' '))
                                   .find(t => t.startsWith('il-faut copier')); }""")
        verifier(ligne == "il-faut copier · si ne-pas · sinon",
                 f"le protocole se lit jusqu'à son dernier mot : {ligne!r}")

        print("\nzéro : le composé de deux branches et de deux actes")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        nuls = lambda: page.eval_on_selector_all(
            "#corpus .tok[data-n='0']", "e => e.filter(x => x.textContent.trim() === '0').length")
        page.evaluate("""() => { S_.C = 99999;
            ['an','anna','hem','sela','meku','mille','nur'].forEach(acheterGl); }""")
        page.wait_for_timeout(300)
        verifier(nuls() == 0, "toute la numération acquise ne rend pas un seul zéro lisible")
        verifier(page.evaluate("() => GL.find(g => g.id === 'lan').sec") is True,
                 "aucune branche ne l'offre : il ne s'obtient qu'à la grille")
        r = page.evaluate("() => { S_.C = 500; S_.H = 99999; return composer('la','an'); }")
        verifier(r == "refus", "et il ne se pose pas sans savoir lire « ne-pas »")
        page.evaluate("() => { S_.C = 99999; acheterGl('la'); S_.C = 500; }")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => { const c = S_.C, n = nArbre(), su = SU.size;
            const issue = composer('la','an');
            return [issue, c - S_.C, nArbre() - n, SU.size - su]; }""")
        page.wait_for_timeout(300)
        verifier(r[0] == "acquis" and r[1] == 120,
                 f"ne-pas + un donne le zéro, à son coût en certitude : {r[:2]}")
        verifier(r[2] == 0, "et n'avance pas l'arbre : c'est du savoir, pas de la progression")
        # Règle 3 : la numération s'acquiert signe par signe. Le zéro n'ouvre que le zéro.
        verifier(r[3] == 0, "il n'ouvre aucun autre rang de numération")
        verifier(nuls() == 11, f"les {nuls()} zéros du corpus passent en chiffres")
        # docs/corpus.md §5 : la tablette 29 est un registre de zéros, et elle reste un seul
        # signe répété pendant presque toute la partie. C'est ce qui rend sa lecture brutale.
        z29 = page.eval_on_selector_all(".tablet[data-tb='29'] .tok[data-n='0']", "e => e.length")
        verifier(z29 == 9, f"la tablette 29 en portait {z29} depuis la première seconde")

        print("\nles-lecteurs : le nom, et ce qu'il laisse à lire")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("() => { S_.C = 9e6; GL.filter(g => !g.sec && g.id !== 'shenu')"
                      "                      .forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(300)
        # Règle 15 : une recette n'existe que si sa cible et ses deux parties sont au lexique.
        # ⟨les-lecteurs⟩ se dessine ⟨lire⟩ sur ⟨nous⟩, et ⟨nous⟩ appartient à l'acte IV — la
        # grille ne doit donc pas l'offrir, même une fois tout l'arbre acquis.
        r = page.evaluate("""() => [COMP.shenu, RECETTES.shenu === undefined,
                                    recetteDe('shen','nash') === undefined,
                                    byId.nash === undefined]""")
        verifier(r == [["shen", "nash"], True, True, True],
                 f"le nom se dessine sur un signe qui n'est pas au lexique, et n'ouvre aucune recette : {r}")
        # Aucun effet chiffré, et c'est mesuré : dernier achat de l'arbre, il serait payé à la
        # seconde où la partie s'arrête. Cinq variantes d'effet donnent la même durée simulée.
        r = page.evaluate("""() => { const av = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            acheterGl('shenu');
            const ap = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            return [av.every((v, i) => v === ap[i]), S_.done, $('end').hidden, [...finLire]]; }""")
        page.wait_for_timeout(400)
        verifier(r[0] is True, "il ne multiplie rien : aucun instrument ne bouge à l'achat")
        verifier(r[1] is True and r[3] == [18],
                 f"il ferme l'arbre, et la seule tablette qu'il ouvre est la 18 : {r[1:]}")
        verifier(page.text_content("#lexr").strip() == f"{ngl} / {ngl}", f"le lexique affiche « {ngl} / {ngl} »")
        lus = page.eval_on_selector_all("#corpus .tok[data-w=shenu]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'les-lecteurs').length]")
        verifier(lus == [3, 3], f"ses trois attestations passent en français : {lus}")
        # Ce que l'achat NE donne pas : la tablette 18 s'arrête à ⟨nous⟩, qui se tient seul
        # juste devant le nom, sur la même ligne. C'est la porte de l'acte IV, et elle est
        # dans le texte (docs/backlog-1.0.md, PAR-2 et VOIX-1).
        reste = page.eval_on_selector_all(".tablet[data-tb='18'] .tok.g",
                                          "e => e.map(x => x.dataset.w)")
        verifier(sorted(reste) == ["nash", "nash", "nash", "nash", "nm4"],
                 f"et la tablette 18 s'arrête sur « nous », quatre fois, plus un nom propre : {reste}")
        pct = page.evaluate("() => Math.round(100 * pctTablette(TBN[18]))")
        verifier(pct == 80, f"soit {pct} % de la tablette, contre 68 avant l'achat")

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
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("() => { S_.C = 9e6; GL.forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(400)
        # Elle ne s'ouvre plus au clic : le dernier signe de l'arbre est celui qui rend
        # lisible la tablette 18, et un écran de statistiques posé par-dessus la couvrirait
        # avant qu'on l'ait lue. Elle attend d'être allé voir (finRegarder(), economie.js).
        verifier(page.get_attribute("#end", "hidden") is not None,
                 "elle ne couvre pas la tablette que le dernier signe vient d'ouvrir")
        page.evaluate("() => { finArmee -= 7000; versTablette(1); }")
        page.wait_for_timeout(900)
        verifier(page.get_attribute("#end", "hidden") is not None,
                 "ni ne vient sur une tablette qui n'a rien à voir")
        page.evaluate("() => versTablette(18)")
        page.wait_for_timeout(900)
        verifier(page.get_attribute("#end", "hidden") is None,
                 "elle vient une fois la tablette 18 sous les yeux")
        # Le garde-fou : un joueur qui n'y va pas doit quand même avoir une fin. Le corpus
        # est rangé dans l'ordre du temps à ce stade — remonter de la 18 à la 1 est un long
        # défilement, et `tabletteVisible()` ne change qu'une fois qu'il a abouti.
        page.evaluate("() => { $('end').hidden = true; finLire = new Set([18]);"
                      "        versTablette(1); }")
        page.wait_for_timeout(1600)
        page.evaluate("() => { finArmee = performance.now() - 7000; }")
        page.wait_for_timeout(500)
        verifier(page.get_attribute("#end", "hidden") is not None, "sinon elle patiente")
        page.evaluate("() => { finArmee = performance.now() - 95000; }")
        page.wait_for_timeout(400)
        verifier(page.get_attribute("#end", "hidden") is None,
                 "mais elle finit par venir, lecture ou pas")
        # `showEnd()` désarme : sans ça la carte reviendrait sur celui qui la ferme.
        verifier(page.evaluate("() => finArmee") == 0, "et elle se désarme en s'ouvrant")
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
        # En dernier, parce qu'il vide la partie : « réinitialiser » ne recharge pas la page,
        # et une carte armée survivrait à la remise à zéro pour s'ouvrir sur la partie neuve —
        # le défaut qu'avait `SU` avant PT4, avec ses 229 nombres encore lisibles.
        page.evaluate("() => { finArmee = performance.now() - 95000; finLire = new Set();"
                      "        $('reset').click(); }")
        page.wait_for_timeout(500)
        verifier(page.get_attribute("#end", "hidden") is not None
                 and page.evaluate("() => finArmee") == 0,
                 "« réinitialiser » la désarme : une partie neuve ne s'ouvre pas sur la fin")

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

        # ---- les quatre trous ouverts par le dépouillement de PT10 ----
        # Quatre questions du backlog étaient posées à un instrument qui ne les mesurait pas :
        # la révision n'était pas enveloppée du tout, le degré de doute n'était pas écrit, une
        # paire juste impayable se lisait comme un coup de sonde au hasard, et le chrono gelait
        # à la fin. Ce qui suit tient les quatre réponses.
        def journal():
            return [tuple(l.split("\t")[2:4])
                    for l in page.evaluate("() => tracesTSV()").split("\n")
                    if l and not l.startswith("#") and not l.startswith("temps\t")]

        def neuf():
            page.evaluate("() => $('reset').click()")
            page.wait_for_timeout(200)
            page.evaluate("() => { TR.length = 0; S_.t = 0; prochainEtat = 0; }")

        # le doute à l'achat (MOD-2) : écrit sur un signe ambigu, tu sur tous les autres
        neuf()
        page.evaluate("() => { S_.C = 9999; acheterGl('an'); acheterGl('tem', 'f'); }")
        ach = dict((d.split(" ")[0], d) for g, d in journal() if g == "acheterGl")
        verifier("· doute " in ach.get("tem", "") and "✗" in ach.get("tem", ""),
                 f"la lecture ET le doute à l'achat : « {ach.get('tem', '—')} »")
        verifier("· doute " not in ach.get("an", "x"),
                 "un signe non ambigu n'a pas de doute à écrire")

        # la révision (CONTR-2) : le signe, la lecture quittée, le prix, le doute avant → après
        page.evaluate("""() => { S_.C = 99999; acheterGl('mik');
                                 S_.conc['tem'] = 1;      // le signe est travaillé entre les deux
                                 S_.C = 99999; reviser('tem', 'j'); }""")
        rev = [d for g, d in journal() if g == "reviser"]
        verifier(len(rev) == 1, f"la révision est journalisée ({len(rev)} ligne)")
        verifier(len(rev) == 1 and "poussière ✗ → grain" in rev[0],
                 "elle dit la lecture quittée et la lecture prise")
        dts = rev[0].split("doute ")[-1].split(" → ") if rev else []
        verifier(len(dts) == 2 and int(dts[1]) < int(dts[0]),
                 f"le doute avant → après, et le travail le fait baisser : {' → '.join(dts)}")

        # la composition : trois issues, et non deux (le ✓ porte sur la PAIRE)
        neuf()
        page.evaluate("() => { S_.C = 99999; ['nur','ur','tem','im','sar'].forEach(g => acheterGl(g));"
                      "        S_.H = 1e6; }")
        page.evaluate("() => { S_.C = 0; composer('im', 'sar'); }")     # juste, mais 600 C
        page.evaluate("() => composer('ur', 'im')")                     # fausse : au carnet
        page.evaluate("() => { S_.C = 99999; composer('ur', 'tem'); }")  # juste et payée
        com = [d for g, d in journal() if g == "composer"]
        verifier(com == ["im + sar ✓ imme · impayable (600 C)",
                         "ur + im ✗ carnet",
                         "ur + tem ✓ urtem"],
                 f"trois issues de composition distinctes : {com}")

        # la fin : datée au dernier signe de l'arbre, sans attendre la carte (FIN-1)
        neuf()
        page.evaluate("() => { S_.C = 9e6; GL.filter(g => !g.sec).forEach(g => acheterGl(g.id)); }")
        j = journal()
        verifier([g for g, _ in j].count("finjeu") == 1 and j[-1][0] == "finjeu",
                 "« finjeu » suit le dernier signe de l'arbre, et une seule fois")
        verifier(not any(g == "fin" for g, _ in j),
                 "la carte n'est pas encore venue : c'est bien deux instants séparés")
        # et le chrono continue pendant la fenêtre de lecture, que `tick` n'alimente plus
        t0 = page.evaluate("() => TR[TR.length - 1][0]")
        page.wait_for_timeout(1300)
        page.evaluate("() => { S_.O = 1e6; formuler(); }")
        t1 = page.evaluate("() => TR[TR.length - 1][0]")
        verifier(t1 - t0 >= 1, f"après la fin, le journal date encore les actions ({t0} → {t1})")

        # ---- trancher à l'achat : AMB-1, AMB-2, AMB-3 ----
        # Onze signes supportent deux lectures ; neuf sont dans l'arbre des actes I-III. Ce
        # que ces vérifications tiennent, c'est surtout ce que le jeu NE dit PAS : rien, à
        # aucun endroit, ne distingue la lecture juste de la fausse avant `peut-être`.
        print("\ntrancher à l'achat : les deux lectures")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("() => [Object.keys(AMB).length, Object.keys(AMB).filter(k => byId[k]).length]")
        verifier(r == [11, 9], f"onze lectures fausses écrites, neuf dans l'arbre d'aujourd'hui : {r}")

        page.evaluate("() => { S_.C = 99999; ['an','anna','im'].forEach(acheterGl); }")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { const c = S_.C; ambOuvrir('tem');
            const b = [...$('amb-choix').querySelectorAll('[data-amb]')].map(x => x.textContent);
            return [$('amb').hidden, has('tem'), c === S_.C, b.sort()]; }""")
        verifier(r[:3] == [False, False, True] and r[3] == ["grain", "poussière"],
                 f"un signe ambigu n'est pas acheté au clic : il propose ses deux lectures — {r[3]}")
        # La fenêtre ne porte qu'une chose de plus que la carte du lexique : le second mot.
        r = page.evaluate("""() => [$('amb-eff').textContent, byId.tem.eff,
                                    $('amb-cost').textContent, String(byId.tem.cost)]""")
        verifier(r[0] == r[1] and r[2] == r[3],
                 f"même effet et même prix pour les deux : « {r[0]} » à {r[2]} C")
        r = page.evaluate("""() => { const c = S_.C; ambFermer();
            return [$('amb').hidden, has('tem'), c === S_.C]; }""")
        verifier(r == [True, False, True], f"revenir laisse le signe à acheter, sans rien coûter : {r}")
        # L'ordre des deux lectures est tiré au sort : la juste toujours à gauche se retiendrait
        # en une partie, et la seconde n'aurait plus rien à trancher (règle 14, par analogie).
        ordres = {page.evaluate("() => { ambOuvrir('tem'); ambFermer(); return ambOrdre.join(''); }")
                  for _ in range(40)}
        verifier(ordres == {"jf", "fj"}, f"et leur ordre n'est pas fixe : {sorted(ordres)}")

        print("\nle mot faux, partout")
        page.evaluate("() => { S_.C = 99999; acheterGl('tem','f'); }")
        page.wait_for_timeout(300)
        r = page.eval_on_selector_all("#corpus .tok[data-w=tem]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'poussière').length]")
        verifier(r == [315, 315], f"les {r[0]} attestations passent au mot faux, blocs générés compris : {r}")
        verifier(page.evaluate("() => $('lex').querySelector('[data-gl=tem] .ttl').textContent")
                 == "poussière", "le lexique porte le mot faux")
        verifier("poussière" in page.text_content("#log"), "et la ligne de journal est la sienne")
        verifier(page.evaluate("() => { const t = [...document.querySelectorAll('#corpus .tok[data-w=tem]')][0];"
                               "  return tipHTML(t).includes('poussière'); }") is True,
                 "l'infobulle aussi")
        # La dette (AMB-3) : de 1 à 3 points selon les attestations, invisible partout.
        verifier(page.evaluate("() => dette()") == 3,
                 "trois points de dette pour un signe attesté 315 fois")
        vu = page.evaluate("() => document.querySelector('.shell').innerText")
        verifier("dette" not in vu.lower(), "et rien à l'écran ne la nomme")

        print("\nla prime est silencieuse, et elle ne porte que sur ce qui multiplie")
        r = page.evaluate("""() => { S_.gl = ['tem']; S_.lect = {};
            const j = [M.cop(), M.ate()]; S_.lect = {tem:'f'};
            const f = [M.cop(), M.ate()];
            return [j, f, f.map((v, i) => +(v / j[i]).toFixed(4))]; }""")
        verifier(r[0] == [1.3, 1.3] and r[1] == [1.375, 1.375],
                 f"+30 % devient +37,5 % — la prime porte sur le bonus, pas sur l'instrument : {r[1]}")
        # Quatre des neuf signes ambigus de l'acte III ne multiplient rien : mal les lire ne
        # paie pas, et on ne leur invente pas un effet pour porter la prime.
        r = page.evaluate("""() => ['ur','nur','pat','la'].map(g => { S_.gl = [g];
            const cle = ['cop','ate','tabl','con','gram','click'];
            S_.lect = {}; const j = cle.map(k => M[k]());
            S_.lect = {[g]:'f'}; return cle.every((k, i) => M[k]() === j[i]); })""")
        verifier(r == [True] * 4, f"maison, année, avant, ne-pas ne multiplient rien, juste ou faux : {r}")
        # Et elle ne se lit nulle part : la carte du lexique annonce le même effet dans les
        # deux cas. Un « +37,5 % » à l'achat serait l'oracle que le design interdit.
        r = page.evaluate("""() => { S_.gl = []; S_.lect = {}; S_.C = 99999; acheterGl('im');
            acheterGl('kish','f'); paintLex();
            return $('lex').querySelector('[data-gl=kish] .eff').textContent; }""")
        verifier(r == "+30 % à la table de fréquences",
                 f"la carte annonce toujours l'effet de la lecture juste : « {r} »")

        print("\nle composé se salit par ses parties")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 9e5; ['an','anna','nur'].forEach(g => acheterGl(g));
            const out = {};
            const pose = (u, t) => { S_.gl = S_.gl.filter(g => g !== 'ur' && g !== 'tem' && g !== 'urtem');
                delete S_.lect.ur; delete S_.lect.tem;
                acheterGl('ur', u); acheterGl('tem', t); acheterGl('urtem');
                return [motDe('urtem'), logDe('urtem').slice(0, 12)]; };
            out.jj = pose('j','j'); out.fj = pose('f','j');
            out.jf = pose('j','f'); out.ff = pose('f','f');
            return out; }""")
        page.wait_for_timeout(200)
        verifier([r["jj"][0], r["fj"][0], r["jf"][0], r["ff"][0]]
                 == ["grenier", "caveau", "poussier", "ossuaire"],
                 f"grenier · caveau · poussier · ossuaire, selon les parties mal lues")
        verifier(r["ff"][1].startswith("L’ossuaire"),
                 f"et la ligne de journal suit le composé, pas ses parties : « {r['ff'][1]}… »")
        # Règle 14 : la grille ne renseigne jamais. Un joueur qui lit ⟨ne-pas⟩ « fin » et à qui
        # elle répond « zéro » vient d'apprendre qu'il s'est trompé.
        r = page.evaluate("""() => { S_.C = 9e5; S_.H = 9e5; acheterGl('la','f');
            const z = composer('la','an'); paintComp();
            return [z, motDe('lan'), motDe('enla'), $('comp-choix')
                .querySelector('[data-pion=la]').title]; }""")
        verifier(r == ["acquis", "fin-un", "à la fin", "fin"],
                 f"⟨fin⟩ posé sur ⟨un⟩ donne « fin-un », et la grille ne dit rien de plus : {r}")

        print("\nl'indice est dans le texte : les ruptures d'AMB-4")

        def ligne(tb, i):
            """Une ligne du corpus telle qu'elle se lit : un mot par jeton déchiffré, le
            nom du signe entre chevrons pour les autres. `textContent` seul recolle les
            jetons — « maison1 · poussière20 » — et ne dit rien de ce qu'on voit."""
            return page.evaluate(
                "([t, i]) => [...[...document.querySelectorAll('#corpus .tablet')]"
                "  .find(x => +x.dataset.tb === t).querySelectorAll('.ln')[i]"
                "  .querySelectorAll('.tok')]"
                "  .map(x => x.textContent.trim() || '⟨' + (x.dataset.w || x.dataset.n) + '⟩')"
                "  .join(' ')", [tb, i])

        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        # §7.3 : une rupture de paire réparante ne se vérifie qu'en tenant l'AUTRE signe à sa
        # lecture juste. Sinon l'assertion échoue alors que le jeu fait ce qui a été décidé.
        page.evaluate("""() => { S_.C = 9e5; ['an','anna','hem','sela'].forEach(acheterGl);
            acheterGl('ur','j'); acheterGl('tem','f'); }""")
        page.wait_for_timeout(300)
        verifier(ligne(5, 3).startswith("maison 1 · poussière 20"),
                 f"tablette 5 : « {ligne(5, 3)[:34]} » — on ne distribue pas vingt mesures de poussière")
        page.evaluate("() => { S_.lect.tem = 'j'; S_.lect.ur = 'f'; paintCorpus(null); }")
        page.wait_for_timeout(250)
        verifier(ligne(5, 3).startswith("tombe 1 · grain 20"),
                 f"et par l'autre bout : « {ligne(5, 3)[:34]} » — ni de grain aux tombes")
        # La paire réparante, elle, passe : c'est la décision du 14/09/2026, pas un défaut.
        page.evaluate("() => { S_.lect.tem = 'f'; paintCorpus(null); }")
        page.wait_for_timeout(250)
        verifier(ligne(5, 3).startswith("tombe 1 · poussière 20"),
                 f"les deux fausses ensemble se tiennent, et le jeu laisse passer : « {ligne(5, 3)[:36]} »")
        # `ne-pas` → « fin » casse sur `sinon`, qui est ⟨si⟩⟨ne-pas⟩ : 131 fois sur la même ligne.
        page.evaluate("() => { S_.C = 9e5; ['im','sar','kal','nur','pat','zur'].forEach(g => acheterGl(g));"
                      "  acheterGl('la','f'); acheterGl('en'); acheterGl('enla'); }")
        page.wait_for_timeout(300)
        verifier(ligne(5, 4).endswith("si fin · à la fin"),
                 f"tablette 5 : « {ligne(5, 4)[-24:]} » — deux signes, presque le même mot")
        # `avant` → « dessous » casse tablette 15, lignes 3 et 4, qui se suivent.
        page.evaluate("() => { S_.C = 9e5; acheterGl('kish'); acheterGl('nurnur');"
                      "  S_.lect.pat = 'f'; paintCorpus(null); }")
        page.wait_for_timeout(300)
        verifier(ligne(15, 3) == "siècle 1 · après" and ligne(15, 4).startswith("dessous · siècle 1"),
                 f"tablette 15 : « {ligne(15, 3)} » puis « {ligne(15, 4)} » — un siècle n'a pas de dessous")
        # `graver` → « couper », dernière ligne du corpus et rupture la plus tardive du lot.
        page.evaluate("() => { S_.lect.sar = 'f'; paintCorpus(null); }")
        page.wait_for_timeout(250)
        verifier("couper" in ligne(30, 6) and ligne(30, 6).count("couper") == 2,
                 f"tablette 30 : « {ligne(30, 6)} » — quelqu'un coupe un nom propre")

        print("\nla lecture tranchée tient")
        # La dette ne se sauvegarde pas : elle se DÉDUIT des lectures, qui se sauvegardent.
        # Tenue en solde, elle dérivait dès qu'une révision ne passait pas par le bon chemin,
        # et un solde faux sur un chiffre que personne n'affiche ne se verrait jamais.
        r = page.evaluate("""() => { const av = JSON.stringify(S_.lect);
            sauver(); const p = JSON.parse(localStorage.getItem(KEY));
            return [JSON.stringify(p.lect) === av, p.dette === undefined, dette() > 0]; }""")
        verifier(r == [True, True, True], f"les lectures passent à la sauvegarde, la dette s'en déduit : {r}")
        r = page.evaluate("() => { $('reset').click(); return [JSON.stringify(S_.lect), dette()]; }")
        verifier(r == ["{}", 0], f"et « réinitialiser » les remet à zéro : {r}")

        # ---- le doute et la révision : MOD-2, CONTR-2, CONTR-3 ----
        # Ce que ces vérifications tiennent est surtout négatif, comme pour AMB-1 : le degré
        # de doute ne doit jamais dépendre de la lecture retenue, sinon c'est un oracle.
        print("\npeut-être : le doute se chiffre")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        verifier(page.get_attribute("#pdoute", "hidden") is not None,
                 "avant lui, le panneau du doute n'existe pas")
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier("doute" not in vu and "peut-être" not in vu,
                 "et rien à l'écran ne laisse entendre qu'une lecture puisse être autre chose")
        r = page.evaluate("""() => { const g = byId.mik;
            return [g.br, g.cost, GL.filter(x => x.br === 'modalite').map(x => x.id)]; }""")
        verifier(r[:2] == ["modalite", 450] and r[2] == ["la","en","mik","dun","lash","enla"],
                 f"450 C, entre « si » et « il-faut » : {r}")
        r = page.evaluate("""() => { S_.C = 9e5; const av = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram()];
            ['la','en'].forEach(acheterGl); acheterGl('mik');
            const ap = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram()];
            return av.every((v, i) => v === ap[i]); }""")
        page.wait_for_timeout(300)
        verifier(r is True, f"il ne multiplie rien : {r}")
        verifier(page.get_attribute("#pdoute", "hidden") is None, "et il ouvre le panneau du doute")
        lus = page.eval_on_selector_all("#corpus .tok[data-w=mik]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'peut-être').length]")
        verifier(lus == [10, 10], f"ses dix attestations passent en français : {lus}")

        print("\nle doute se fige à la décision, pas au regard")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        # Deux signes ambigus achetés au même instant, donc sur le même corpus dégagé : l'un
        # concordé AVANT de trancher, l'autre après. Seul le premier doit en profiter.
        r = page.evaluate("""() => { S_.C = 9e5;
            ['an','anna','hem','sela','meku','im','tab','gan','kal','mille','nur'].forEach(acheterGl);
            concChoisir('tem'); concFermer();          // on regarde ⟨grain⟩ avant de trancher
            acheterGl('tem','j'); acheterGl('ur','j'); // ⟨maison⟩ est tranché à l'aveugle
            const avant = [douteDe('tem'), douteDe('ur')];
            concChoisir('ur'); concFermer();           // ... et regardé APRÈS
            return [avant, [douteDe('tem'), douteDe('ur')]]; }""")
        page.wait_for_timeout(250)
        verifier(r[0][0] < r[0][1],
                 f"concorder avant de trancher fait tomber le doute : {r[0][0]} contre {r[0][1]}")
        verifier(r[1] == r[0],
                 f"concorder après ne le bouge pas : {r[1]} — on ne dé-aveugle pas une décision prise")
        # Le chiffre ne dépend pas de la lecture : c'est ce qui l'autorise à être affiché.
        # Au même instant, sur le même état : seule la lecture change. Recalculer plus tard
        # donnerait un autre chiffre pour une autre raison — le corpus a continué de sortir.
        r = page.evaluate("""() => { const lu = S_.lect.ur;
            S_.lect.ur = 'j'; const a = douteCalc('ur');
            S_.lect.ur = 'f'; const b = douteCalc('ur');
            S_.lect.ur = lu; return [a, b]; }""")
        verifier(r[0] == r[1],
                 f"et il est le même pour les deux lectures : {r} — il dit l'aveuglement, pas l'erreur")
        # Un signe acquis avant ce lot n'a aucun relevé : le jeu ne prétend pas savoir.
        r = page.evaluate("() => { delete S_.dte.ur; return douteDe('ur'); }")
        verifier(r == 100, f"sans relevé de décision, le doute est entier : {r}")

        print("\nla rupture distributionnelle (docs/corpus.md §7.4)")
        r = page.evaluate("""() => ['nur','esh','tem','ur','la','sar'].map(id =>
            Math.round(100*partCadre(id)))""")
        verifier(r[0] == 100 and r[1] == 0,
                 f"⟨année⟩ 100 % en cadre de nombre, ⟨nuit⟩ 0 % : {r[:2]} — et rien ne le commente")
        verifier(r == [100, 0, 98, 100, 0, 2],
                 f"le même fait pour les autres, identique aux deux lectures : {r}")
        # L'infobulle ne la porte qu'après `peut-être` : avant, ce chiffre n'existe pas.
        r = page.evaluate("""() => { const t = document.querySelector('#corpus .tok[data-w=nur]');
            const sans = tipHTML(t).includes('cadre de nombre');
            S_.C = 9e5; ['pat','zur','nurnur','esh','nurhal','la','en'].forEach(acheterGl);
            acheterGl('mik');
            return [sans, tipHTML(t).includes('cadre de nombre')]; }""")
        page.wait_for_timeout(250)
        verifier(r == [False, True], f"l'infobulle ne la porte qu'après « peut-être » : {r}")

        print("\nrouvrir une lecture")
        r = page.evaluate("""() => { S_.C = 9e5; S_.lect.tem = 'f'; paintCorpus(null);
            const c0 = S_.C, d0 = douteDe('tem'), r0 = S_.rev;
            const ok = reviser('tem','j');
            return [ok, c0 - S_.C, revCost(), S_.rev - r0, motDe('tem'), d0, douteDe('tem')]; }""")
        page.wait_for_timeout(300)
        verifier(r[0] is True and r[1] == 240 and r[3] == 1,
                 f"elle coûte 240 C la première fois : {r[:4]}")
        verifier(r[2] == 384, f"et la suivante 384 — le prix croît par révision, jamais par signe : {r[2]}")
        verifier(r[4] == "grain", f"le corpus repasse au mot choisi : {r[4]}")
        mots = page.eval_on_selector_all("#corpus .tok[data-w=tem]",
            "e => e.filter(x => x.textContent.trim() === 'grain').length")
        verifier(mots == 315, f"partout, et d'un coup : {mots} attestations")
        # Ce que la révision NE dit PAS. C'est tout le lot : elle repeint, elle ne juge pas.
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier(not any(m in vu for m in ("erreur", "correct", "juste !", "mauvaise lecture")),
                 "et elle ne dit jamais si l'on avait raison")
        # La dette suit, et reste invisible : retirée quand on quitte une lecture fausse,
        # reposée quand on y retombe.
        r = page.evaluate("""() => { const d0 = dette();
            reviser('tem','f'); const d1 = dette();
            reviser('tem','j'); return [d0, d1 - d0, dette()]; }""")
        page.wait_for_timeout(250)
        verifier(r[1] == 3 and r[2] == r[0],
                 f"la dette se repose et se retire avec la lecture : {r}")
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier("dette" not in vu, "sans jamais s'afficher")

        print("\nle coût du brute-force (CONTR-3)")
        r = page.evaluate("""() => { S_.rev = 0; const c = [];
            for(let i = 0; i < 9; i++){ c.push(revCost()); S_.rev++; }
            return [c[0], c[8], c.reduce((a, b) => a + b, 0)]; }""")
        # 4 550 C est ce qu'il reste à dépenser en signes après `peut-être` (outils/sim.py).
        verifier(r[2] > 5 * 4550,
                 f"balayer les neuf coûte {r[2]} C, près de six fois ce qui reste à dépenser ({r[0]} → {r[1]})")
        r = page.evaluate("() => { S_.rev = 0; let c = 0; for(let i=0;i<3;i++){ c += revCost(); S_.rev++; } return c; }")
        verifier(r < 4550 / 3, f"trois révisions choisies en coûtent {r} — lire reste moins cher que chercher")
        page.evaluate("() => { S_.rev = 0; }")

        # ---- la contradiction : CONTR-1 ----
        # R2 du backlog : on ne perd que du débit, jamais de la progression. Et règle 18 :
        # le passage qui refuse ne doit désigner aucun signe, sinon c'est un oracle.
        print("\nla contradiction : un passage refuse de se résoudre")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        socle = """S_.C = 9e5; S_.H = 9e5; S_.b.gram = 10; S_.b.con = 20;
            ['an','anna','hem','sela','meku','im','tab','gan','kal','mille','nur','pat','zur',
             'nurnur','esh','nurhal','la','en'].forEach(acheterGl);"""
        # Toute la dette qu'on veut, tant que `peut-être` n'est pas là : rien ne se déclenche.
        r = page.evaluate("() => { " + socle + """
            acheterGl('tem','f'); acheterGl('ur','f'); acheterGl('kish','f');
            acheterGl('sar','f'); acheterGl('shen','f');
            return [dette(), S_.contr, contrDiv()]; }""")
        page.wait_for_timeout(300)
        verifier(r == [9, 0, 1], f"avant « peut-être », aucune dette ne déclenche rien : {r}")
        verifier(page.get_attribute("#doute-etat", "hidden") is not None, "et rien ne l'annonce")
        r = page.evaluate("() => { acheterGl('mik'); return [dette(), S_.contr, contrDiv()]; }")
        page.wait_for_timeout(350)
        verifier(r == [9, 1, 2], f"« peut-être » solde les lectures faites : {r}")
        # Ce qui se perd, et ce qui ne se perd pas — mesuré sur la contradiction SEULE, en la
        # basculant. Comparer avant et après l'achat de `mik` ne mesurerait pas la sanction :
        # ce signe-là ajoute un glyphe et dix attestations, et bouge tous ces compteurs pour
        # une raison qui n'est pas elle.
        etat = lambda: page.evaluate("""() => { paintCorpus(null); paintLex(); return [
            Math.round(1000*pctTablette(TBN[17])), mesures().sig, mesures().lig,
            $('lexr').textContent]; }""")
        arme = etat()
        page.evaluate("() => { S_.contr = 0; }")
        libre = etat()
        page.evaluate("() => { S_.contr = 1; paintCorpus(null); }")
        page.wait_for_timeout(200)
        verifier(arme == libre,
                 f"aucune progression n'est perdue, seulement du débit (R2) : {arme}")
        # Le débit affiché dit la vérité : moitié moins.
        r = page.evaluate("""() => { const c = S_.b.con*CON_P*M.con() + S_.b.gram*GRAM_P*gramMul()*M.gram();
            const t = $('rt-C').textContent;
            S_.contr = 0; const t0 = (paintRes(), $('rt-C').textContent);
            S_.contr = 1; paintRes();
            return [t, t0]; }""")
        verifier(r[0] != r[1], f"le débit de Certitude affiché est moitié moindre : {r[0]} contre {r[1]}")
        # Le passage. Fixe, et il ne désigne rien.
        ligne = lambda i: page.evaluate("""(i) => [...[...document.querySelectorAll('.tablet')]
            .find(x => +x.dataset.tb === 17).children[i].querySelectorAll('.tok')]
            .map(t => t.textContent.trim() || '⟨⟩').join(' ')""", i)
        marques = lambda: page.eval_on_selector_all(".tablet[data-tb='17'] .tok.refus", "e => e.length")
        verifier("⟨⟩" in ligne(4) and marques() == 3,
                 f"tablette 17 ligne 4 revient aux signes : « {ligne(4)} », {marques()} jetons marqués")
        verifier("⟨⟩" not in ligne(3),
                 f"et la ligne d'à côté se lit toujours : « {ligne(3)} »")
        # Le même passage quelles que soient les lectures fausses : le choisir d'après l'erreur
        # la désignerait (règle 18).
        r = page.evaluate("""() => { const lu = JSON.parse(JSON.stringify(S_.lect));
            for(const k in S_.lect) S_.lect[k] = 'j';
            S_.lect.nur = 'f'; S_.lect.pat = 'f'; S_.lect.la = 'f';
            paintCorpus(null);
            const n = document.querySelectorAll('.tablet[data-tb="17"] .tok.refus').length;
            const ailleurs = document.querySelectorAll('.tok.refus').length;
            S_.lect = lu; paintCorpus(null);
            return [n, ailleurs]; }""")
        page.wait_for_timeout(250)
        verifier(r == [3, 3], f"le passage ne bouge pas avec les signes mal lus : {r}")
        vu = page.evaluate("() => $('doute-etat').textContent")
        verifier("divisée par deux" in vu and not any(m in vu for m in
                 ("grain", "poussière", "maison", "eau", "année")),
                 f"l'état est affiché sans ambiguïté, et ne nomme aucun signe : « {vu[:58]}… »")

        print("\nla révision dénoue, et ne réarme pas")
        # Une révision qui ne suffit pas ne lève rien — et ne le dit pas non plus.
        r = page.evaluate("() => { reviser('kish','j'); return [dette(), S_.contr]; }")
        page.wait_for_timeout(250)
        verifier(r == [8, 1], f"une révision qui ne descend pas sous le seuil ne lève rien : {r}")
        verifier(marques() == 3, "le passage refuse toujours")
        # Celle qui suffit lève tout, et c'est le « bonus rétroactif » du design doc §8 —
        # payé en dette effacée, donc sans rien annoncer.
        r = page.evaluate("""() => { reviser('tem','j'); reviser('ur','j');
            return [dette(), S_.contr, contrDiv()]; }""")
        page.wait_for_timeout(350)
        verifier(r == [2, 0, 1], f"sous le seuil, la contradiction se lève : {r}")
        verifier(marques() == 0 and "⟨⟩" not in ligne(4),
                 f"et le passage se résout : « {ligne(4)} »")
        # Levée, elle ne se réarme pas : il n'y a plus de franchissement d'acte dans le
        # prototype, et on ne ballotte pas le joueur sur un chiffre qu'il ne voit pas.
        r = page.evaluate("""() => { reviser('tem','f'); reviser('ur','f'); reviser('kish','f');
            return [dette(), S_.contr]; }""")
        page.wait_for_timeout(250)
        verifier(r[0] > 5 and r[1] == 0,
                 f"et ne se réarme pas, même si la dette remonte : {r}")
        # Rien, nulle part, ne dit si une révision était juste.
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier(not any(m in vu for m in ("dette", "erreur", "correct", "mauvaise lecture")),
                 "et rien à l'écran ne nomme la dette ni ne juge une lecture")

        # ---- `faux` : où le texte ne tient pas (MOD-3) ----
        # Le premier lot où le jeu dit quelque chose — et il ne dit toujours pas QUOI est
        # faux, il montre OÙ ça ne se construit pas. Le §11 du design doc l'exige : la
        # relecture de fin surlignera les erreurs « y compris celles jamais détectées », donc
        # `faux` n'a pas donné le corrigé.
        print("\nfaux : les passages qui ne se construisent pas")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { const g = byId.lash; return [g.br, g.cost]; }""")
        verifier(r == ["modalite", 700], f"700 C, entre « il-faut » et « sinon » : {r}")
        rompues = lambda: page.evaluate("""() => [...document.querySelectorAll('.ln.rompu')]
            .map(l => l.closest('.tablet').dataset.tb + ':' + [...l.parentNode.children].indexOf(l))""")
        # Tout l'arbre sauf `faux` : les ruptures sont dans le texte, rien ne les allume.
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.id !== 'lash' && g.id !== 'shenu')
              .forEach(g => acheterGl(g.id, 'f')); }""")
        page.wait_for_timeout(400)
        verifier(rompues() == [], "avant lui, aucune ligne n'est allumée — même toutes lectures fausses")
        r = page.evaluate("""() => { const av = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram()];
            acheterGl('lash');
            return av.every((v, i) => v === [M.cop(), M.ate(), M.tabl(), M.con(), M.gram()][i]); }""")
        page.wait_for_timeout(400)
        verifier(r is True, "il ne multiplie rien")
        lus = page.eval_on_selector_all("#corpus .tok[data-w=lash]",
            "e => [e.length, e.filter(x => x.textContent.trim() === 'faux').length]")
        verifier(lus == [16, 16], f"ses seize attestations passent en français : {lus}")
        # La tablette 26 : la dernière scribe marque comme fausses les tablettes qui espéraient.
        # Le joueur vient de faire le même geste sur son propre corpus. Lu ici en lectures
        # justes — le socle ci-dessus a tout acheté faux pour vérifier que rien ne s'allume.
        l26 = page.evaluate("""() => { S_.lect = {}; paintCorpus(null);
            const tb = [...document.querySelectorAll('.tablet')]
            .find(x => +x.dataset.tb === 26);
            return [27, 28, 29].map(i => [...tb.children[i].querySelectorAll('.tok')]
              .map(t => t.textContent.trim() || '⟨⟩').join(' ')); }""")
        verifier(l26[2] == "peut-être eau · faux",
                 f"la tablette 26 annule l'espoir quatre-vingt-dix-sept ans plus tard : {l26}")

        print("\nce qui s'allume, et surtout ce qui ne s'allume pas")
        pose = lambda lect: page.evaluate("""(lect) => { S_.lect = {};
            for(const k in lect) S_.lect[k] = lect[k]; paintCorpus(null); }""", lect) or rompues()
        verifier(pose({'tem': 'f'}) == ["5:3"],
                 "⟨grain⟩ seul allume la tablette 5 : on ne distribue pas vingt mesures de poussière")
        verifier(pose({'ur': 'f'}) == ["5:3"], "⟨maison⟩ seul allume la même ligne, par l'autre bout")
        # Le §7.3, rendu mécanique : deux erreurs bien choisies ne trahissent rien.
        verifier(pose({'tem': 'f', 'ur': 'f'}) == [],
                 "LES DEUX n'allument rien — la paire réparante se tient, et le texte ne trahit rien")
        # Le §7.4 : les erreurs que le design doc §11 appelle « jamais détectées ».
        verifier(pose({'kish': 'f', 'nur': 'f', 'shen': 'f', 'dun': 'f'}) == [],
                 "⟨eau⟩, ⟨année⟩, ⟨lire⟩ et ⟨il-faut⟩ n'allument rien : ils ne cassent nulle part")
        verifier(pose({'la': 'f'}) == ["5:4"], "⟨ne-pas⟩ allume « si fin · à la fin »")
        verifier(pose({'pat': 'f'}) == ["15:4"], "⟨avant⟩ allume « dessous · siècle 1 »")
        verifier(pose({'sar': 'f'}) == ["30:6"], "⟨graver⟩ allume « je couper ⟨N6⟩ »")
        # Et la mesure qui résume le lot.
        tout = pose({k: 'f' for k in ("tem","ur","kish","sar","shen","nur","pat","dun","la")})
        verifier(tout == ["5:4", "15:4", "30:6"],
                 f"tout faux n'allume que trois lignes sur cinq : se tromper partout cache deux erreurs — {tout}")

        print("\nil montre où, jamais quoi")
        # C'est la LIGNE qui s'allume : marquer le jeton nommerait le signe fautif.
        r = page.evaluate("""() => { S_.lect = {tem:'f'}; paintCorpus(null);
            const ln = [...document.querySelectorAll('.ln.rompu')][0];
            return [ln.querySelectorAll('.tok').length,
                    ln.querySelectorAll('.tok.rompu, .tok.faux').length,
                    [...ln.querySelectorAll('.tok')].filter(t => byId[t.dataset.w] && AMB[t.dataset.w]).length]; }""")
        page.wait_for_timeout(250)
        verifier(r[1] == 0 and r[2] >= 2,
                 f"la ligne porte la marque, aucun jeton — et {r[2]} signes ambigus y figurent : {r}")
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier("poussière" in vu and "rupture" not in vu and "erreur" not in vu,
                 "et rien à l'écran ne nomme un signe fautif")
        n = page.evaluate("() => $('doute-rupt').textContent")
        verifier("Un passage ne se construit pas — il est allumé" in n,
                 f"le panneau compte les passages sans dire lesquels : « {n} »")
        # Réviser éteint la ligne — et c'est la seule confirmation que le joueur obtiendra.
        r = page.evaluate("() => { S_.C = 9e6; reviser('tem','j'); return 1; }") and rompues()
        page.wait_for_timeout(300)
        verifier(r == [], f"réviser l'éteint : {r or 'plus aucune ligne'}")

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
        verifier(vieille.text_content("#lexr").strip() == f"5 / {ngl}", "le lexique compte cinq signes")
        r = vieille.evaluate("""() => { S_.C = 9999; acheterGl('nur'); S_.H = 99999;
            const i = composer('tem','im'); sauver();
            const p = JSON.parse(localStorage.getItem('langue-morte-actes-i-iii'));
            return [i, p.carnet, p.comp]; }""")
        verifier(r == ["rate", ["tem+im"], 1], f"et la composition s'y enregistre : {r}")
        ctx.close()

        # ---- une partie finie quand l'arbre était plus petit ----
        # Elle est `done` à vingt glyphes ; l'arbre en compte davantage. Rouvrir sur l'écran
        # de fin, `tick` arrêté, serait le cul-de-sac qui a déjà coûté un changement de clé.
        print("\nune partie finie à vingt glyphes reprend")
        vingt = ["an", "anna", "hem", "sela", "meku", "mille", "tem", "ur", "tab", "kish", "gan",
                 "im", "sar", "kal", "nur", "pat", "zur", "nurnur", "esh", "nurhal"]
        finie = ('{"O":1e9,"H":5e4,"C":40,"rec":30,"clicks":900,'
                 '"b":{"cop":60,"tab":56,"con":39,"ate":36,"gram":18},'
                 '"gl":%s,"t":4400,"done":true}' % json.dumps(vingt))
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-actes-i-iii', %r)" % finie)
        vieille = ctx.new_page()
        casses = []
        vieille.on("pageerror", lambda e: casses.append(str(e)))
        vieille.goto(PAGE.resolve().as_uri())
        vieille.wait_for_timeout(700)
        verifier(not casses, f"aucune erreur au chargement : {casses[:1] or '—'}")
        etat = vieille.evaluate("() => [S_.done, $('end').hidden, S_.gl.length]")
        verifier(etat == [False, True, 20], f"pas d'écran de fin, la partie continue : {etat}")
        verifier(vieille.text_content("#lexr").strip() == f"20 / {ngl}", f"le lexique affiche « 20 / {ngl} »")
        verifier("locked" not in vieille.evaluate(
                     "() => $('lex').querySelector('[data-gl=shen]').className"),
                 "et « lire » attend d'être acheté")
        ctx.close()

        # ---- les trois builds (LIV-2) ----
        # `python build.py` sort trois pages du même `src/`. Ce qui se vérifie ici n'est pas
        # qu'elles existent, c'est que **retirer un bouton ne casse rien d'autre** : les
        # liaisons de jeu.js et la boucle de rendu supposaient toutes les deux que la barre
        # hors jeu était là, et une seule ligne qui la suppose empêche tout le reste du
        # fichier de s'exécuter — `requestAnimationFrame` compris.
        print("\nles trois builds")

        # Le sélecteur de vitesse laisse enfin une trace. C'est la seule commande capable de
        # fausser toute la timeline d'un playtest, et rien ne la voyait — pas même le contrôle
        # de `outils/depouiller.py`, qui rejoue le modèle sur ces mêmes secondes de jeu.
        page.evaluate("() => { TR.length = 0; vitesse(1); }")
        page.evaluate("() => document.querySelector('[data-spd=\"3\"]').click()")
        page.evaluate("() => document.querySelector('[data-spd=\"3\"]').click()")
        page.evaluate("() => document.querySelector('[data-spd=\"1\"]').click()")
        vit = [tuple(l.split("\t")[2:4])
               for l in page.evaluate("() => tracesTSV()").split("\n")
               if "\tvitesse\t" in l]
        verifier(vit == [("vitesse", "×3"), ("vitesse", "×1")],
                 f"le sélecteur de vitesse se journalise, sans doublon : {vit}")
        entete = [l for l in page.evaluate("() => tracesTSV()").split("\n") if l.startswith("# build")]
        verifier(len(entete) == 1 and "dev" in entete[0] and f"{ngl} glyphes" in entete[0],
                 f"le journal dit de quel build il sort : « {entete[0] if entete else '—'} »")
        page.evaluate("() => vitesse(1)")

        for nom, attendu in (("playtest", True), ("public", False)):
            page2 = nav.new_page(viewport={"width": 1440, "height": 900})
            casses = []
            page2.on("pageerror", lambda e: casses.append(str(e)))
            page2.goto((RACINE / "dist" / f"{nom}.html").resolve().as_uri())
            page2.wait_for_timeout(900)
            print(f"\n  — {nom}.html")
            verifier(not casses, f"aucune erreur JS ({casses[:1] or '—'})")
            # Le corpus est rendu et la partie tourne : c'est le chrono absent qui aurait
            # arrêté la boucle à la première frame, et rien ne l'aurait dit.
            signes2 = page2.eval_on_selector_all("#corpus .tok:not(.sep)", "e => e.length")
            verifier(signes2 == SIGNES_ATTENDUS, f"{signes2} signes rendus")
            t0 = page2.evaluate("() => S_.t")
            page2.wait_for_timeout(500)
            verifier(page2.evaluate("() => S_.t") > t0, "la boucle tourne (le temps de jeu avance)")
            # Ni sélecteur de vitesse ni « réinitialiser » : c'est tout l'objet des deux builds.
            verifier(page2.eval_on_selector_all("[data-spd]", "e => e.length") == 0,
                     "pas de sélecteur de vitesse")
            verifier(page2.evaluate("() => !$('reset')"), "pas de « réinitialiser »")
            # « recommencer » de la carte de fin se déléguait au bouton de la barre.
            page2.evaluate("() => { S_.C = 9999; acheterGl('an'); $('again').click(); }")
            page2.wait_for_timeout(200)
            verifier(page2.evaluate("() => S_.gl.length") == 0,
                     "« recommencer » marche sans le bouton de la barre")
            verifier(page2.evaluate("() => typeof TR") == ("object" if attendu else "undefined"),
                     "le journal d'actions est là" if attendu else "pas de journal d'actions")
            if attendu:
                verifier(page2.evaluate("() => !!$('tr-dl') && !!$('tr-cp')"),
                         "les deux boutons d'export restent")
                ent = [l for l in page2.evaluate("() => tracesTSV()").split("\n") if l.startswith("# build")]
                verifier(len(ent) == 1 and nom in ent[0], f"le journal s'estampille : « {ent[0]} »")
                verifier([g for g, d in [tuple(l.split("\t")[2:4])
                                         for l in page2.evaluate("() => tracesTSV()").split("\n")
                                         if "\tacheterGl\t" in l or "\treset\t" in l]] == ["acheterGl", "reset"],
                         "et il journalise l'achat puis la coupure, dans cet ordre")
            else:
                verifier(page2.eval_on_selector_all(".devbar", "e => e.length") == 0,
                         "plus de barre hors jeu du tout")
                verifier(page2.evaluate("() => !$('chrono')"), "ni de chronomètre")
            page2.close()

        nav.close()

    print("\n" + ("TOUT PASSE" if not echecs else f"{len(echecs)} ÉCHEC(S)"))
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
