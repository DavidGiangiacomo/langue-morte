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
  6. les deux fins : le dernier signe ouvre « achever » et « interrompre » au lexique comme à
     la grille, l'effacement attend qu'on ait lu sa tablette, ne laisse que « relire » et
     « recommencer » et pas un chiffre, une partie interrompue ne reprend pas, et rien ne
     couvre les outils hors jeu ; la relecture rend le texte entier et marque chaque faute
     sur son jeton — restée, corrigée, d'un Élève —, et ce qui n'a jamais été trouvé
 31. le Lecteur : ouvert par ⟨semence⟩, un signe pour nom et aucune ligne d'effet, il lit le
     corpus seul — une tablette par minute et par Lecteur, marquée dans la barre et dans le
     texte —, verse à la question suivante, ne lit pas la nuit, s'arrête à trente, et son nom
     se lit avec ⟨devenir-lecture⟩
 32. le Corpus jumeau : ouvert par ⟨nous⟩, acheté une seule fois, il rend à chaque tablette la
     moitié de son gisement, tarifée au premier relevé sur la copie ; l'original passe
     d'abord, la barre et le texte le montrent, et le journal d'actions dit quel gisement a
     payé
 33. I2 : au million, une fois l'acte IV ouvert, les zéros des nombres du joueur s'écrivent
     en ⟨zéro⟩ — compteurs et coûts, pas avant ⟨nous⟩, pas sous le million —, ⟨zéro⟩ posé à
     la grille rend la notation compacte, et le journal d'actions date la première fois
 34. la sanction aux actes IV et V (ECO-3) : la contradiction ne divise plus que par 1,25 une
     fois l'acte IV ouvert, les Élèves n'y rendent plus leur bonus mais tranchent toujours,
     et le bandeau comme la ligne de l'instrument disent l'un et l'autre sans nommer un signe
 35. la coupure entre deux séances (PT11) : rouvrir une partie laisse au journal d'actions une
     ligne `reprise` qui dit l'absence à l'horloge — avant ⟨nuit⟩, rien d'autre ne la marquait
  7. le relevé se fait dans le corpus ; le gisement s'épuise et se tarife à la 1re visite
  8. le recoupement se fait dans le corpus : deux passages d'un même signe
  9. la datation : une tablette se date quand on sait lire sa date, et pas avant
 10. le rangement chronologique range l'affichage sans rien dégager de neuf
 11. la Grammaire s'ouvre à « année » et croît avec le lexique
 12. la nuit : 40 % du débit hors ligne, plafonnée, consommée une seule fois
 13. la concordance : le corpus se replie sur les attestations d'un signe, et la crue
     se lit alors de 14 à 0
 14. la composition : la grille s'ouvre à « année », l'ordre compte, l'échec ne coûte
     jamais de Certitude, et un composé secret n'avance pas la progression de l'arbre —
     puis ce que le panneau dit de LUI-MÊME : la palette porte son nom, un emplacement plein
     dit ce que le clic y fait, et les deux refus rendent le même texte, qui n'affirme rien
 15. une partie commencée avant une mécanique neuve se rouvre sans rien perdre
 16. la Parole III : `lire` après `copier`, les trois effets, `scribe` composable et compté
     dans l'arbre
 17. la Modalité : la branche s'ouvre sur le signe le plus fréquent du corpus, `il-faut`
     porte l'atelier et non la grammaire, et les 816 attestations passent en français
 18. `zéro` : composé de deux branches et de deux actes, il ne s'obtient qu'à la grille,
     n'avance pas l'arbre, et rend lisibles les onze zéros du corpus
 19. `les-lecteurs` : dernier signe de l'acte III, il ne se compose qu'une fois ⟨nous⟩ acquis,
     ne multiplie rien, ne ferme plus l'arbre, et laisse la tablette 18 à 80 %
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
 26. l'Élève : il s'ouvre à la première Grammaire, multiplie les cinq instruments et pas le
     relevé, tranche les signes ambigus à la place du joueur avec un taux d'erreur qui croît
     avec leur nombre — et ce taux ne se lit nulle part
 27. la sauvegarde survit aux actes : une partie écrite sous l'ancienne clé déménage, numérotée,
     sans perdre sa nuit ni un instrument qu'elle n'avait pas ; la version se compte sur les
     migrations ; et une sauvegarde que le jeu ne sait pas lire — plus récente, ou dont la
     migration casse — ne se charge pas et ne s'écrase pas
 28. la Personne : six signes sans multiplicateur, ⟨nous⟩ achève la tablette 18, ⟨toi⟩ replie
     le corpus sur ce qui s'adressait au lecteur, deux composés se posent à la grille et
     ⟨nous-fûmes⟩ attend ⟨finir⟩, ⟨moi-absent⟩ n'a aucune attestation,
     le dernier mot du corpus met le récit au passé — sauf ce qui s'adresse à ⟨toi⟩ —, et la
     contradiction se solde de nouveau en entrant dans l'acte IV
 29. les Questions : la Certitude s'arrête à 9 999, ce qui déborde fait des questions à partir
     de ⟨toi⟩ et jamais la nuit, chaque réponse finit une ligne gravée et s'écrit avec les
     lectures du joueur, le silence ne coûte rien, rien ne se pose sans question en main, et
     le doute n'en sait rien
 30. la Fin : sept signes au plafond, trois offerts par une réponse, ⟨devenir-lecture⟩ en
     dernier et composable tôt, les ruptures de ⟨semence⟩ et ⟨devenir⟩, « notre-fin · ne-pas »
     qui ne se tranche pas, et l'entrée dans l'acte V qui solde la contradiction

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
    # Même parade que `sim.py` et `balayage.py`. Ici le défaut ne se voyait qu'une fois la
    # sortie redirigée : la console sait afficher le → de la cinquième assertion, un fichier
    # ou un tube en cp1252 non, et la suite mourait là avec 311 contrôles non joués.
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
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
        verifier(len(frq()) == len(page.evaluate("() => BR")), f"un comptage par tête de branche : {frq()}")
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
        # La Personne (VOIX-1) en a ouvert trois de plus d'elle-même : ⟨toi-qui⟩, ⟨moi-absent⟩,
        # et ⟨les-lecteurs⟩, dont la seconde moitié ⟨nous⟩ est enfin au lexique. La Fin
        # (GRAINE-1) six : ses quatre composés, et deux d'avant qui attendaient ⟨finir⟩.
        verifier(set(rec) == {"anna", "urtem", "nurnur", "imme", "tabsar", "enla", "lan",
                              "taru", "mula", "shenu", "nurhal", "nashal",
                              "halan", "halnash", "meshke", "shenke"},
                 f"seize recettes ouvertes aujourd'hui : {sorted(rec)}")
        # la Parole III les a ouvertes d'elle-même, sans qu'aucune liste soit tenue (règle 15)
        verifier(rec.get("imme") == ["im", "sar"] and rec.get("tabsar") == ["tab", "sar"],
                 "scribe = dire + graver, archive = tablette + graver")
        verifier("selanna" not in rec, "« vingt » n'est proposé par aucune recette")
        verifier(rec.get("nurhal") == ["nur", "hal"],
                 "« dernière-année » se pose depuis que ⟨finir⟩ est un glyphe, sans liste à tenir (règle 15)")

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

        # ---- ce que le panneau dit de LUI-MÊME (COMP-6) ----
        # La grille ne renseigne jamais sur le corpus (règle 14) ; ça ne l'autorisait pas à se
        # taire sur ses propres règles, ni à les dire faux. Trois endroits le faisaient, et
        # PT10 a buté sur les trois.
        print("\nle panneau de composition dit vrai sur lui-même")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("() => { S_.C = 9999; ['nur','ur','tem'].forEach(acheterGl); }")
        page.wait_for_timeout(250)
        # 1. La palette ne montrait que les signes acquis et ne le disait que dans son
        #    aria-label — le seul endroit qu'un joueur voyant ne lit pas.
        ch = page.text_content("#pcomp .palette .ch").strip()
        verifier(ch == "Ce que je sais lire", f"la palette porte son nom à l'écran : « {ch} »")
        verifier(page.evaluate("() => $('comp-choix').getAttribute('aria-label')")
                 .startswith(ch), "et l'aria-label dit exactement la même chose")
        # Nommer la liste ne la remplit pas : ce qu'elle cache reste caché (règle 14), et le
        # carnet, lui, n'annonce toujours pas qu'on peut se tromper avant que ça arrive.
        vus = page.eval_on_selector_all("#comp-choix .pion:not([hidden])", "e => e.length")
        verifier(vus == 3, f"aucun pion de plus n'apparaît : {vus}")
        verifier(page.get_attribute("#carnet", "hidden") is not None,
                 "et le carnet n'est toujours pas là avant la première tentative")

        # 2. Un emplacement plein annonçait « poser un signe » alors que le clic l'enlève.
        page.evaluate("() => compPoser('ur')")
        page.wait_for_timeout(150)
        titres = page.evaluate("() => [...$('pcomp').querySelectorAll('.slot')].map(s => s.title)")
        verifier(titres == ["retirer ce signe", "poser un second signe"],
                 f"un emplacement dit ce que le clic y fait : {titres}")
        page.evaluate("() => compVider()")

        # 3. La ligne de refus disait « ces deux signes ne se rencontrent nulle part » — faux
        #    dès que la paire existe, et c'était le cas de CINQ des six tentatives de PT10. Les
        #    deux refus doivent rester le même texte (règle 14 : distinguer, c'est renseigner)
        #    et ce texte ne doit plus rien affirmer du corpus.
        page.evaluate("() => { S_.C = 10; S_.H = 100000; }")   # 10 C, le grenier en coûte 60
        lu = lambda: page.evaluate("() => $('log').querySelector('p:last-child').textContent")
        juste = page.evaluate("""() => { const h = S_.H, i = composer('ur','tem');
            return [i, h - S_.H, S_.carnet.slice(), has('urtem')]; }""")
        m_juste = lu()
        rate = page.evaluate("""() => { const h = S_.H, i = composer('tem','ur');
            return [i, h - S_.H, S_.carnet.slice()]; }""")
        m_rate = lu()
        verifier(juste[0] == "rate" and juste[3] is False,
                 "une paire juste qu'on ne peut pas payer échoue comme une autre")
        verifier(m_juste == m_rate, f"et rend le MÊME texte qu'une paire fausse : « {m_juste} »")
        verifier("nulle part" not in m_juste and "rencontrent" not in m_juste,
                 "qui n'affirme plus que les deux signes ne se rencontrent nulle part")
        verifier(juste[1] == rate[1], f"pour le même prix en hypothèses : {juste[1]}")
        # Ce que l'écran distingue quand même, et qu'on laisse (voir le commentaire de
        # `composer`) : le carnet, le prix de la suivante, et la paire retentable.
        verifier(juste[2] == [] and rate[2] == ["tem+ur"],
                 f"seul le carnet les sépare, et c'est assumé : {juste[2]} contre {rate[2]}")

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
        page.evaluate("() => { S_.C = 9e6; GL.filter(g => !g.sec && g.id !== 'shenu' && !['personne', 'fin'].includes(g.br))"
                      "                      .forEach(g => acheterGl(g.id)); }")
        page.wait_for_timeout(300)
        # Règle 15 : une recette n'existe que si sa cible et ses deux parties sont au lexique.
        # ⟨les-lecteurs⟩ se dessine ⟨lire⟩ sur ⟨nous⟩ ; depuis que ⟨nous⟩ y est (VOIX-1), la
        # recette existe — mais la palette ne montre que les signes acquis, et ⟨nous⟩ ne l'est
        # pas tant qu'on n'a pas ouvert l'acte IV.
        r = page.evaluate("""() => [COMP.shenu, RECETTES.shenu, has('nash')]""")
        verifier(r == [["shen", "nash"], ["shen", "nash"], False],
                 f"le nom se dessine ⟨lire⟩ sur ⟨nous⟩, et ne se pose qu'une fois ⟨nous⟩ acquis : {r}")
        # Aucun effet chiffré. Il était le dernier achat de l'arbre ; il ne l'est plus, et la
        # question s'est mesurée : un ×1,5 à la grammaire raccourcirait l'acte IV de six à huit
        # minutes, les trois autres instruments ne déplacent presque rien (docs/journal.md).
        r = page.evaluate("""() => { const av = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            acheterGl('shenu');
            const ap = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            return [av.every((v, i) => v === ap[i]), S_.done, [...touchees]]; }""")
        page.wait_for_timeout(400)
        verifier(r[0] is True, "il ne multiplie rien : aucun instrument ne bouge à l'achat")
        verifier(r[1] is False and r[2] == [18],
                 f"il ne ferme plus l'arbre, et la seule tablette qu'il touche est la 18 : {r[1:]}")
        verifier(page.text_content("#lexr").strip() == f"{ngl - 13} / {ngl}",
                 f"le lexique affiche « {ngl - 13} / {ngl} » : la Personne et la Fin restent à lire")
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
        # ⟨toi⟩ est dans l'arbre depuis VOIX-1, et son achat replie le corpus sur ce qui
        # s'adresse au lecteur (VOIX-2) : on le referme pour partir du corpus entier.
        page.evaluate("() => { S_.C = 9e6; GL.forEach(g => acheterGl(g.id)); finDesarmer();"
                      "        concFermer(); }")
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

        print("\nles deux fins : la fenêtre")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        # Les durées de l'effacement sont des secondes d'horloge et des choix de mise en scène
        # (FIN_EFF, rendu.js) : on les raccourcit pour le test, le fondu de 2,4 s reste.
        presque = """() => { FIN_EFF.interface = 0.6; FIN_EFF.lecture = 0.6; FIN_EFF.texte = 0.6;
            S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.id !== 'shenke').forEach(g => acheterGl(g.id, 'j'));
            concFermer(); S_.C = 9e6; }"""
        fin = lambda: page.evaluate("() => document.body.classList.contains('fin')")
        page.evaluate(presque)
        page.wait_for_timeout(300)
        page.evaluate("() => $('lex').querySelector('[data-gl=shenke]').click()")
        page.wait_for_timeout(150)
        r = page.evaluate("() => [$('fins').hidden, has('shenke'), S_.done]")
        verifier(r == [False, False, False],
                 f"le dernier signe ne s'achète pas d'un clic : il ouvre les deux fins ({r})")
        # Aucune n'est la bonne (design doc §11) : même habit, et la fenêtre dit sa règle —
        # sans elle, « le laisser non lu » se lirait « pas maintenant ».
        r = page.evaluate("""() => [[...$('fins-choix').children].map(b => b.className),
                                    $('fins').innerText.toLowerCase()]""")
        verifier(len(set(r[0])) == 1 and "partie s’arrête" in r[1],
                 f"même habit pour les deux, et la partie s'arrête dans les deux cas : {r[0]}")
        ordres = page.evaluate("""() => { const o = new Set();
            for (let i = 0; i < 30; i++) { finsFermer(); finsOuvrir('shenke');
              o.add($('fins-choix').firstElementChild.dataset.fin); }
            return [...o].sort(); }""")
        verifier(ordres == ["achever", "interrompre"],
                 f"la place de gauche n'est à aucune des deux : l'ordre se tire au sort ({ordres})")
        for fermeture, action in (("« revenir au corpus »", lambda: page.click("#fins-annuler")),
                                  ("échap", lambda: page.keyboard.press("Escape"))):
            action()
            page.wait_for_timeout(120)
            verifier(page.evaluate("() => [$('fins').hidden, has('shenke'), S_.done]") == [True, False, False],
                     f"{fermeture} la referme sans rien décider")
            page.evaluate("() => finsOuvrir('shenke')")
        # Interrompre n'est pas le repli de qui ne peut pas payer : sans les moyens d'achever,
        # ni fenêtre ni interruption.
        r = page.evaluate("""() => { finsFermer(); const c = S_.C; S_.C = 9000;
            finsOuvrir('shenke'); interrompre('shenke'); const r = [$('fins').hidden, S_.done];
            S_.C = c; return r; }""")
        verifier(r == [True, False], f"sans les 9 999 C, ni fenêtre ni interruption : {r}")

        print("\nles deux fins : achever")
        # Trois secondes de texte seul, pour avoir le temps de voir l'interface partie et le
        # texte encore là.
        page.evaluate("() => { FIN_EFF.lecture = 3; finsOuvrir('shenke'); $('fins-choix').querySelector('[data-fin=achever]').click(); }")
        page.wait_for_timeout(300)
        r = page.evaluate("() => [has('shenke'), S_.done, S_.fin, [...finLire]]")
        verifier(r == [True, True, "achevee", [27]], f"achever le lit, et la partie s'arrête : {r}")
        # L'effacement attend qu'on ait lu la tablette que le dernier signe vient d'ouvrir
        # (règle 16) : ⟨devenir-lecture⟩ n'a qu'une attestation, sur la 27.
        verifier(not fin(), "l'interface ne s'efface pas sur la tablette qu'il vient d'ouvrir")
        clics = page.evaluate("""() => { const c = S_.clicks;
            elCorpus.querySelector('.tablet:not([hidden]) .tok:not(.sep)').click(); return [c, S_.clicks]; }""")
        verifier(clics[0] == clics[1], "le corpus se lit et ne se travaille plus : un clic ne relève rien")
        page.evaluate("() => { finArmee -= 7000; versTablette(1); }")
        page.wait_for_timeout(900)
        verifier(not fin(), "ni sur une tablette qui n'a rien à voir")
        page.evaluate("() => versTablette(27)")
        page.wait_for_timeout(900)
        verifier(fin(), "il commence une fois la tablette 27 sous les yeux")
        verifier(page.evaluate("() => finArmee") == 0, "et se désarme en commençant")
        page.wait_for_timeout(3500)
        # « plus de compteurs, plus d'instruments, juste le texte » (design doc §11)
        r = page.evaluate("""() => [[...document.querySelectorAll('.panel, .masthead h1, .masthead .sub')]
              .filter(e => e !== elCorpus.parentElement && getComputedStyle(e).visibility !== 'hidden')
              .map(e => e.id || e.className),
            getComputedStyle(elCorpus).visibility, getComputedStyle(elCorpus.parentElement).backgroundColor]""")
        verifier(r == [[], "visible", "rgba(0, 0, 0, 0)"],
                 f"l'interface est partie, cadre compris, et le texte reste : {r}")
        # relevé en PT5 : la partie finie, l'écran couvrait le journal d'actions —
        # inatteignable au moment précis où il faut l'exporter
        verifier(page.evaluate("""() => {
                     const r = document.querySelector('#tr-cp').getBoundingClientRect();
                     const e = document.elementFromPoint(r.x + r.width / 2, r.y + r.height / 2);
                     return !!e && e.id === 'tr-cp'; }"""),
                 "le bouton « copier » reste là, et cliquable")
        page.wait_for_timeout(6000)
        r = page.evaluate("""() => [getComputedStyle(elCorpus).visibility, $('apres').hidden,
                                    $('again').textContent.trim(), S_.efface]""")
        verifier(r == ["hidden", False, "recommencer", True],
                 f"puis le texte s'efface aussi, et il ne reste que « recommencer » : {r}")
        # Plus de carte de statistiques : « signes déchiffrés 87 % » était un score. Et rien
        # n'annonce ce que les actes suivants révèlent — l'écran de fin est lu avant
        # l'entretien de playtest.
        r = page.evaluate("""() => [...document.querySelectorAll('body *')]
            .filter(e => !e.closest('.devbar') && e.children.length === 0 && e.offsetParent !== null
                         && getComputedStyle(e).visibility !== 'hidden' && e.textContent.trim())
            .map(e => e.textContent.trim())""")
        verifier(r == ["relire", "recommencer"], f"ni chiffre ni phrase — « relire », parce qu'on a achevé : {r}")
        # Une partie achevée se rouvre achevée, sur la page vide.
        sauve = page.evaluate("() => { sauver(); return localStorage.getItem(KEY); }")
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r)" % sauve)
        autre = ctx.new_page()
        casses = []
        autre.on("pageerror", lambda e: casses.append(str(e)))
        autre.goto(PAGE.resolve().as_uri())
        autre.wait_for_timeout(600)
        r = autre.evaluate("""() => [S_.done, S_.fin, document.body.className.split(' ').sort().join(' '),
                                     $('apres').hidden, getComputedStyle(elCorpus).visibility]""")
        verifier(not casses and r == [True, "achevee", "fin fin-sec fin-texte", False, "hidden"],
                 f"rechargée, elle rouvre sur la page vide, sans refaire l'effacement : {r} {casses[:1]}")
        ctx.close()
        page.evaluate("() => $('again').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => [S_.gl.length, S_.fin, document.body.className, $('apres').hidden,
            getComputedStyle($('lex').closest('.panel')).visibility, elCorpus.parentElement.style.transform]""")
        verifier(r == [0, None, "", True, "visible", ""],
                 f"« recommencer » défait tout : interface, texte, glissement : {r}")

        print("\nles deux fins : interrompre")
        page.evaluate(presque)
        page.wait_for_timeout(300)
        r = page.evaluate("""() => { TR.length = 0;
            $('lex').querySelector('[data-gl=shenke]').click();
            $('fins-choix').querySelector('[data-fin=interrompre]').click();
            return [has('shenke'), S_.done, S_.fin, nArbre() === NGL - 1, finArmee,
                    TR.map(e => e[1]).filter(k => k !== 'etat')]; }""")
        verifier(r[:5] == [False, True, "interrompue", True, 0],
                 f"interrompre laisse le signe non lu, et la partie s'arrête là : {r[:5]}")
        verifier(r[5] == ["finsOuvrir", "interrompre", "finjeu"],
                 f"le journal d'actions dit la fenêtre, le choix, et l'arrêt : {r[5]}")
        # L'interface met quatorze secondes à s'en aller : la carte du signe laissé et la grille
        # restent sous la main pendant ce temps, et aucune ne doit le rendre.
        r = page.evaluate("""() => { $('lex').querySelector('[data-gl=shenke]').click();
            const f = $('fins').hidden; acheterGl('shenke'); const c = composer('shen', 'ke');
            return [f, c, has('shenke'), S_.fin]; }""")
        verifier(r[0] is True and r[2:] == [False, "interrompue"],
                 f"ni le lexique, ni la grille, ni un achat direct ne rendent le signe laissé : {r}")
        t0 = page.evaluate("() => S_.t")
        page.wait_for_timeout(3600)
        r = page.evaluate("""() => [S_.t, getComputedStyle($('lex').closest('.panel')).visibility,
            getComputedStyle(elCorpus).visibility, document.body.classList.contains('fin-texte'),
            $('apres').hidden]""")
        verifier(r == [t0, "hidden", "visible", False, False],
                 f"l'interface s'en va, le corpus reste figé, et le texte ne s'efface pas : {r}")
        r = page.evaluate("() => { relire(); return [$('relire').hidden, relecture]; }")
        verifier(r == [True, False], f"et pas de relecture : elle est celle d'un livre lu jusqu'au bout : {r}")
        # « Le jeu se ferme sur le corpus figé, et ne propose pas de reprendre » : rechargée,
        # elle reste interrompue, alors que l'arbre a un signe de plus qu'elle — c'est ce que
        # la règle de réouverture ne doit pas confondre avec un arbre qui a grandi.
        sauve = page.evaluate("() => { sauver(); return localStorage.getItem(KEY); }")
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r)" % sauve)
        autre = ctx.new_page()
        casses = []
        autre.on("pageerror", lambda e: casses.append(str(e)))
        autre.goto(PAGE.resolve().as_uri())
        autre.wait_for_timeout(600)
        r = autre.evaluate("""() => [S_.done, S_.fin, nArbre() === NGL - 1, document.body.classList.contains('fin'),
                                     getComputedStyle(elCorpus).visibility, $('apres').hidden]""")
        verifier(not casses and r == [True, "interrompue", True, True, "visible", False],
                 f"rechargée, elle reste interrompue : pas de reprise : {r} {casses[:1]}")
        ctx.close()

        print("\nles deux fins : par la grille, sur un autre signe, et sans aller voir")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate(presque)
        page.wait_for_timeout(300)
        # La grille ne passe pas par le lexique, et ⟨devenir-lecture⟩ est ⟨lire⟩ sur ⟨devenir⟩ :
        # posé là quand il est le dernier, il ouvre les deux fins aussi.
        # Le bouton ne s'active qu'à la frame suivante, comme sous la main du joueur.
        page.evaluate("() => { compSel[0] = 'shen'; compSel[1] = 'ke'; }")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => { const c = S_.comp, h = S_.H; $('a-comp').click();
            return [$('fins').hidden, has('shenke'), S_.comp - c, S_.H - h, compSel.join('')]; }""")
        verifier(r == [False, False, 0, 0, ""],
                 f"poser le dernier signe à la grille ouvre les deux fins, sans rien compter ni coûter : {r}")
        r = page.evaluate("""() => { const c = S_.comp;
            $('fins-choix').querySelector('[data-fin=achever]').click();
            return [has('shenke'), S_.done, S_.fin, S_.comp - c]; }""")
        verifier(r == [True, True, "achevee", 1], f"et achever le pose, tentative comptée : {r}")
        # Le garde-fou : un joueur qui ne va pas voir doit quand même avoir une fin. Le corpus
        # est rangé dans l'ordre du temps à ce stade — remonter à la 1 est un long défilement,
        # et `tabletteVisible()` ne change qu'une fois qu'il a abouti.
        page.evaluate("() => versTablette(1)")
        page.wait_for_timeout(1600)
        page.evaluate("() => { finArmee = performance.now() - 7000; }")
        page.wait_for_timeout(500)
        verifier(not fin(), "sinon l'effacement patiente")
        page.evaluate("() => { finArmee = performance.now() - 95000; }")
        page.wait_for_timeout(400)
        verifier(fin(), "mais il finit par venir, lecture ou pas")
        # « recommencer » ne recharge pas la page : un effacement armé ou en cours sur la partie
        # d'avant viendrait vider la partie neuve — le défaut qu'avait `SU` avant PT4.
        page.evaluate("() => { $('reset').click(); }")
        page.evaluate("() => { finArmee = performance.now() - 95000; finLire = new Set(); $('reset').click(); }")
        page.wait_for_timeout(4500)
        r = page.evaluate("() => [document.body.className, finArmee, $('apres').hidden, getComputedStyle(elCorpus).visibility]")
        verifier(r == ["", 0, True, "visible"],
                 f"« réinitialiser » désarme et défait : une partie neuve ne s'ouvre pas sur la fin : {r}")
        # Un dernier signe ambigu : les deux fins d'abord, puis les deux lectures. Qui a
        # composé ⟨devenir-lecture⟩ tôt finit sur un autre mot (règle 25).
        page.evaluate("""() => { FIN_EFF.interface = 0.6; FIN_EFF.lecture = 0.6; FIN_EFF.texte = 0.6;
            S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.id !== 'tem').forEach(g => acheterGl(g.id, 'j'));
            concFermer(); S_.C = 9e6; }""")
        page.wait_for_timeout(300)
        r = page.evaluate("""() => { $('lex').querySelector('[data-gl=tem]').click();
            const f = $('fins').hidden;
            $('fins-choix').querySelector('[data-fin=achever]').click();
            return [f, $('amb').hidden, has('tem'), S_.done]; }""")
        verifier(r == [False, False, False, False],
                 f"⟨grain⟩ laissé pour la fin : les deux fins, puis ses deux lectures : {r}")
        r = page.evaluate("""() => { $('amb-choix').querySelector('[data-amb]').click();
            return [has('tem'), S_.done, S_.fin, ['j', 'f'].includes(S_.lect.tem)]; }""")
        verifier(r == [True, True, "achevee", True], f"et la lecture tranchée l'achève : {r}")

        # ---- la relecture (FIN-3) ----
        # Une partie qui s'est trompée de toutes les façons que la relecture distingue : ⟨grain⟩,
        # ⟨maison⟩ et ⟨ne-pas⟩ mal lus par le joueur et jamais corrigés — ⟨maison⟩ avec
        # ⟨grain⟩, c'est la paire réparante, que rien n'a jamais trahie —, ⟨avant⟩ mal lu par
        # un Élève, ⟨eau⟩ mal lu puis révisé, ⟨grenier⟩ et le zéro jamais posés.
        print("\nla relecture (FIN-3)")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("""() => { TR.length = 0; FIN_EFF.interface = 0.3; FIN_EFF.lecture = 0.3; FIN_EFF.texte = 0.3;
            S_.C = 9e6; S_.H = 9e6;
            const lu = {tem: 'f', ur: 'f', kish: 'f', la: 'f'};
            GL.filter(g => !g.sec && !['shenke', 'pat'].includes(g.id)).forEach(g => acheterGl(g.id, lu[g.id] || 'j'));
            S_.b.elv = 1; acheterGl('pat', 'f', true); S_.b.elv = 0;
            reviser('kish', 'j'); concFermer(); S_.C = 9e6;
            finsOuvrir('shenke'); $('fins-choix').querySelector('[data-fin=achever]').click();
            finArmee = performance.now() - 95000; }""")
        page.wait_for_timeout(300)
        verifier(page.evaluate("() => $('apres').hidden"), "rien à relire tant que l'effacement n'est pas allé au bout")
        page.wait_for_timeout(6000)
        r = page.evaluate("() => [$('relire').hidden, S_.fautes, S_.lusEleve, S_.contr]")
        verifier(r[0] is False and r[1] == {"tem": "moi", "ur": "moi", "kish": "moi", "la": "moi", "pat": "eleve"}
                 and r[2] == {"pat": True},
                 f"« relire » s'offre ; la partie a retenu chaque faute et qui l'a faite, révisée comprise : {r}")
        page.click("#relire")
        page.wait_for_timeout(400)
        r = page.evaluate("""() => [relecture, document.body.classList.contains('relire'),
            document.body.classList.contains('fin-texte'), getComputedStyle(elCorpus).visibility,
            [...elCorpus.querySelectorAll('.tablet')].filter(e => e.hidden).length,
            [...elCorpus.querySelectorAll('.tok.g')].filter(e => !/^nm/.test(e.dataset.w)).length,
            elCorpus.querySelectorAll('[data-n]:not(.num)').length]""")
        verifier(r == [True, True, False, "visible", 0, 0, 0],
                 f"le texte revient, entier : trente tablettes, plus un signe illisible hors les noms propres : {r}")
        marques = lambda w: page.evaluate("""w => [...new Set([...elCorpus.querySelectorAll('[data-w="' + w + '"]')]
            .map(e => e.className.replace('tok w', '').trim() + ' | ' + e.textContent + ' | ' + (e.dataset.avant || '')))]""", w)
        mots = page.evaluate("() => ({tem: AMB.tem.mot, ur: AMB.ur.mot, pat: AMB.pat.mot, kish: AMB.kish.mot})")
        verifier(marques("tem") == [f"malu | grain | j’avais lu « {mots['tem']} »"]
                 and marques("ur") == [f"malu | maison | j’avais lu « {mots['ur']} »"],
                 f"la paire réparante est avouée, jeton par jeton, avec le mot juste : {marques('tem') + marques('ur')}")
        verifier(marques("pat") == [f"malu | avant | un élève avait lu « {mots['pat']} »"],
                 f"ce qu'un Élève avait lu se dit à lui : {marques('pat')}")
        verifier(marques("kish") == [f"corrige | eau | j’avais lu « {mots['kish']} », puis corrigé"],
                 f"la faute corrigée reste à part : {marques('kish')}")
        r = page.evaluate("""() => { const e = elCorpus.querySelector('[data-w="enla"]');
            return [e.className, e.textContent, e.dataset.avant, byId.enla.mot, motDe('enla')]; }""")
        verifier(r[0] == "tok w malu" and r[1] == r[3] and r[2] == f"j’avais lu « {r[4]} »",
                 f"le composé que sa partie salissait aussi : {r[:3]}")
        r = page.evaluate("""() => [...new Set([...elCorpus.querySelectorAll('[data-w="urtem"], [data-n="0"]')]
            .map(e => e.className + ' | ' + e.textContent + ' | ' + e.dataset.avant))]""")
        verifier(r == ["tok w jamais | grenier | jamais trouvé", "tok num jamais | 0 | jamais trouvé"],
                 f"⟨grenier⟩ et le zéro, jamais posés, se lisent et le disent : {r}")
        # ⟨graver⟩ s'écrit aussi « gravé » sous le verrou du passé : deux mots, aucune marque.
        verifier(all(m.startswith(" | ") and m.endswith(" | ") for m in marques("sar")),
                 f"une lecture juste ne porte rien : {marques('sar')}")
        r = page.evaluate("""() => [S_.contr, elCorpus.querySelectorAll('.tok.refus, .ln.rompu').length]""")
        verifier(r == [1, 0], f"ni le passage qui refuse, ni les lignes de `faux` : le texte juste se construit partout : {r}")
        # Le survol dit ce qu'on avait lu, et rien sur les autres jetons.
        el = page.query_selector("#corpus [data-w='tem']")
        el.scroll_into_view_if_needed()
        b = el.bounding_box()
        page.mouse.move(b["x"] + 3, b["y"] + 3)
        page.wait_for_timeout(150)
        r = page.evaluate("() => [$('tip').hidden, $('tip').textContent]")
        verifier(r[0] is False and mots["tem"] in r[1], f"le survol d'une faute dit le mot lu : {r}")
        el = page.query_selector("#corpus [data-w='sar']")
        el.scroll_into_view_if_needed()
        b = el.bounding_box()
        page.mouse.move(b["x"] + 3, b["y"] + 3)
        page.wait_for_timeout(150)
        verifier(page.evaluate("() => $('tip').hidden"), "et rien sur une lecture juste")
        # Aucun score : la légende nomme ses trois marques, et ne compte rien.
        r = page.evaluate("""() => [...$('apres').querySelectorAll('*')]
            .filter(e => e.children.length === 0 && e.offsetParent !== null).map(e => e.textContent.trim())""")
        verifier(r == ["mal lu", "mal lu, puis corrigé", "jamais trouvé", "recommencer"],
                 f"la légende nomme, ne compte pas : {r}")
        r = page.evaluate("() => TR.filter(e => e[1] === 'relire').map(e => e[2])")
        verifier(len(r) == 1 and "mal lus" in r[0], f"le journal d'actions date la relecture et compte ce qu'elle avoue : {r}")
        # Rechargée pendant la relecture, la partie rouvre sur la page vide : on rouvre le livre
        # d'un clic, rien ne se perd.
        sauve = page.evaluate("() => { sauver(); return localStorage.getItem(KEY); }")
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r)" % sauve)
        autre = ctx.new_page()
        casses = []
        autre.on("pageerror", lambda e: casses.append(str(e)))
        autre.goto(PAGE.resolve().as_uri())
        autre.wait_for_timeout(600)
        r = autre.evaluate("() => { const a = [$('relire').hidden, relecture]; relire(); return [...a, relecture, elCorpus.querySelectorAll('.tok.malu').length > 0]; }")
        verifier(not casses and r == [False, False, True, True], f"rechargée, elle se relit encore : {r} {casses[:1]}")
        ctx.close()
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(300)
        r = page.evaluate("""() => [relecture, document.body.className, $('legende').hidden,
            elCorpus.querySelectorAll('[data-avant], .tok.malu, .tok.jamais').length,
            elCorpus.querySelectorAll('.tok.w').length]""")
        verifier(r == [False, "", True, 0, 0], f"« recommencer » referme le livre : plus une marque, plus un mot lu : {r}")

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

        # la fin : datée au dernier signe de l'arbre, sans attendre l'effacement (FIN-1)
        neuf()
        page.evaluate("() => { S_.C = 9e6; GL.filter(g => !g.sec).forEach(g => acheterGl(g.id)); }")
        # Sans les lignes `zeros` (I2) : une Certitude à neuf millions, que le jeu plafonne à
        # 9 999, s'écrit avec leurs zéros à la frame suivante — ce n'est pas une action.
        j = [e for e in journal() if e[0] != "zeros"]
        verifier([g for g, _ in j].count("finjeu") == 1 and j[-1][0] == "finjeu",
                 "« finjeu » suit le dernier signe de l'arbre, et une seule fois")
        verifier(not any(g == "fin" for g, _ in j),
                 "l'effacement n'a pas commencé : c'est bien deux instants séparés")
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
        verifier(r == [11, 11], f"onze lectures fausses écrites, toutes dans l'arbre depuis la Fin : {r}")

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
        # Levée, elle ne se réarme pas d'elle-même : on ne ballotte pas le joueur sur un
        # chiffre qu'il ne voit pas. Seul le franchissement d'acte suivant la re-solde.
        r = page.evaluate("""() => { reviser('tem','f'); reviser('ur','f'); reviser('kish','f');
            return [dette(), S_.contr]; }""")
        page.wait_for_timeout(250)
        verifier(r[0] > 5 and r[1] == 0,
                 f"et ne se réarme pas, même si la dette remonte : {r}")
        r = page.evaluate("() => { S_.C = 9e5; acheterGl('nash'); return [dette() > 5, S_.contr]; }")
        page.wait_for_timeout(250)
        verifier(r == [True, 1], f"jusqu'au franchissement suivant — l'entrée dans l'acte IV : {r}")

        # ---- la sanction aux actes IV et V (ECO-3) ----
        # Le ÷2 doublait tout ce qui restait une fois les prix au plafond ; il ne divise plus que
        # par 1,25. Et les Élèves attendent : sans ça, sept Élèves qui lisent tout faux
        # finissaient avant le joueur sans Élève (règle 21).
        print("\nla sanction aux actes IV et V")
        r = page.evaluate("""() => { paintDoute(); return [contrDiv(), $('doute-etat').textContent]; }""")
        verifier(r[0] == 1.25 and "réduite d’un cinquième" in r[1] and "par deux" not in r[1]
                 and "élèves" not in r[1],
                 f"une fois l'acte IV ouvert, la Certitude ne perd plus qu'un cinquième, et le bandeau le dit : {r}")
        r = page.evaluate("""() => { S_.b.elv = 3; const arme = [elvMul(), M.gram()];
            paintDoute(); paintInstr();
            const ds = $('instr').querySelector('[data-ins=elv] .ds').textContent, bn = $('doute-etat').textContent;
            S_.contr = 0; const libre = [elvMul(), M.gram()]; paintInstr();
            const ds0 = $('instr').querySelector('[data-ins=elv] .ds').textContent;
            S_.contr = 1; return [arme, libre, ds, ds0, bn, elvTranche()]; }""")
        verifier(r[0][0] == 1 and abs(r[1][0] - 1.15) < 1e-9 and abs(r[1][1] / r[0][1] - 1.15) < 1e-9,
                 f"tant qu'elle court, les Élèves ne rendent plus rien — et le rendent levée : {r[0]} / {r[1]}")
        verifier("suspendu" in r[2] and "déchiffre seul" in r[2] and "+5 % aux autres" in r[3] and r[5] is True,
                 f"leur ligne le dit, et ils tranchent toujours à l'achat : « {r[2]} »")
        verifier("élèves attendent" in r[4] and not any(m in r[4] for m in ("grain", "maison", "avant", "lire", "faux")),
                 f"le bandeau nomme l'attente, ni un signe ni un coupable : « {r[4]} »")
        page.evaluate("() => { S_.b.elv = 0; }")
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
        # champ neuf est censé se migrer tout seul (`fusionner()`) ; ce test le vérifie au lieu
        # de le supposer. La partie est posée sous la clé d'avant LIV-3 : c'est là que toutes
        # celles d'avant la composition ont été écrites. L'injection passe par un contexte
        # neuf : recharger l'onglet ferait sauvegarder la page courante par-dessus, via
        # `pagehide`.
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
        # Un instrument neuf est un champ de `S_.b`, pas de premier niveau : sans son zéro,
        # `elvMul()` rend NaN et toute la production avec lui.
        neufs = vieille.evaluate("() => [S_.b.elv, M.cop() > 0]")
        verifier(neufs == [0, True], f"et l'instrument neuf arrive à zéro, sans rien casser : {neufs}")
        verifier(vieille.text_content("#lexr").strip() == f"5 / {ngl}", "le lexique compte cinq signes")
        r = vieille.evaluate("""() => { S_.C = 9999; acheterGl('nur'); S_.H = 99999;
            const i = composer('tem','im'); sauver();
            const p = JSON.parse(localStorage.getItem(KEY));
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
        etat = vieille.evaluate("() => [S_.done, S_.fin, document.body.classList.contains('fin'), S_.gl.length]")
        verifier(etat == [False, None, False, 20], f"pas de fin, la partie continue : {etat}")
        verifier(vieille.text_content("#lexr").strip() == f"20 / {ngl}", f"le lexique affiche « 20 / {ngl} »")
        verifier("locked" not in vieille.evaluate(
                     "() => $('lex').querySelector('[data-gl=shen]').className"),
                 "et « lire » attend d'être acheté")
        ctx.close()
        # La même, finie sur l'arbre entier d'aujourd'hui avant les deux fins : il n'y avait
        # qu'une façon de finir, donc elle est achevée (migration 1 → 2, FIN-2), et elle rouvre
        # sur la page vide — pas sur une partie qui court, ni sur un corpus figé.
        arbre = page.evaluate("() => GL.filter(g => !g.sec).map(g => g.id)")
        finie = ('{"O":1e9,"H":5e4,"C":40,"rec":30,"clicks":900,"b":{"cop":60},'
                 '"gl":%s,"t":9000,"done":true}' % json.dumps(arbre))
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r)" % finie)
        vieille = ctx.new_page()
        casses = []
        vieille.on("pageerror", lambda e: casses.append(str(e)))
        vieille.goto(PAGE.resolve().as_uri())
        vieille.wait_for_timeout(700)
        etat = vieille.evaluate("""() => [S_.done, S_.fin, S_.efface, document.body.classList.contains('fin-texte'),
                                          $('apres').hidden]""")
        verifier(not casses and etat == [True, "achevee", True, True, False],
                 f"finie sur l'arbre entier avant les deux fins : achevée, sur la page vide : {etat} {casses[:1]}")
        ctx.close()

        # ---- l'Élève (ELV-1, ELV-2) ----
        # Le premier instrument ambivalent : il multiplie ce que rendent les cinq autres, et
        # dès qu'il y en a un, ce n'est plus le joueur qui tranche un signe ambigu. Ce qui se
        # vérifie ici est surtout ce qu'il ne fait PAS : il ne touche pas la main, il n'achète
        # rien à la place du joueur, et rien à l'écran ne chiffre ce qu'il rate.
        print("\nl'Élève : il multiplie tout")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        # Huit boutons pour neuf instruments : l'Œil est le relevé, et il se fait dans le corpus.
        # Le Corpus jumeau (VOIX-4) et le Lecteur (GRAINE-2) viennent après l'Élève.
        verifier(page.eval_on_selector_all("#instr .ins", "e => e.map(b => b.dataset.ins)")[-3:] == ["elv", "jum", "lec"]
                 and page.eval_on_selector_all("#instr .ins", "e => e.length") == 8,
                 "l'Élève est au panneau, après la Grammaire")
        elv = lambda: page.evaluate("() => INS.find(i => i.k === 'elv').unlock()")
        page.evaluate("() => { S_.C = 9e6; acheterGl('nur', 'j'); }")
        verifier(not elv(), "« année » ouvre la Grammaire, pas l'Élève")
        page.evaluate("() => { S_.b.gram = 1; }")
        verifier(elv(), "c'est la première Grammaire qui l'ouvre")
        r = page.evaluate("""() => { const i = INS.find(x => x.k === 'elv'), a = insCost(i);
            const av = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            S_.O = 1e9; acheterIns('elv'); const b = insCost(i); acheterIns('elv');
            const ap = [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            return [a, b, S_.b.elv, ap.map((v, k) => Math.round(1000 * v / av[k]) / 1000)]; }""")
        verifier(r[:3] == [20000, 36000, 2], f"20 000 occurrences, puis ×1,8 : {r[:3]}")
        verifier(r[3] == [1.1, 1.1, 1.1, 1.1, 1.1, 1],
                 f"deux Élèves : +10 % aux cinq instruments, rien au relevé : {r[3]}")
        r = page.evaluate("""() => [0, 1, 2, 7].map(n => { S_.b.elv = n;
            return Math.round(100 * elvErr()); })""")
        verifier(r == [0, 15, 28, 68], f"le taux d'erreur croît avec leur nombre : {r} %")

        print("\nl'Élève : il tranche à ma place")
        ouverte = lambda: page.evaluate("() => !$('amb').hidden")
        clic = lambda g: (page.wait_for_timeout(120),
                          page.evaluate("g => $('lex').querySelector('[data-gl=' + g + ']').click()", g),
                          page.wait_for_timeout(120))
        # Sans Élève, rien ne change : le signe ambigu ouvre ses deux lectures et n'est pas payé.
        page.evaluate("() => { S_.b.elv = 0; }")
        clic("pat")
        verifier(ouverte() and not page.evaluate("() => has('pat')"),
                 "sans Élève, « avant » ouvre ses deux lectures")
        page.evaluate("() => ambFermer()")
        # Avec un seul, le clic paie et la fenêtre ne vient pas. Le dé est tenu : c'est le
        # seul hasard du jeu qui décide de quelque chose, et un test ne se joue pas aux dés.
        # Le journal ne garde que deux lignes, et le dégagement d'une tablette peut s'y glisser
        # derrière : on relève donc tout ce qui s'y écrit pendant le clic.
        page.evaluate("""() => { S_.b.elv = 1; S_.C = 500; TR.length = 0; window._rnd = Math.random; Math.random = () => 0;
            window._logs = []; window._push = pushLog; pushLog = x => { _logs.push(x); _push(x); }; }""")
        clic("pat")
        r = page.evaluate("() => [has('pat'), S_.lect.pat, S_.dte.pat, S_.C, dette(), motDe('pat')]")
        verifier(not ouverte() and r[0], "avec un Élève, le clic paie et la fenêtre ne vient pas")
        verifier(r[3] == 370, f"le signe se paie toujours en Certitude, au même prix : {r[3]}")
        verifier(r[1] == "f" and r[5] == "dessous" and r[4] == 2,
                 f"son erreur est une lecture — le mot, et la dette qui s'en déduit : {r[1:2] + r[4:]}")
        vu = page.evaluate("() => { pushLog = _push; return _logs; }")
        verifier(len(vu) >= 2 and "élève" in vu[0] and vu[1].startswith("Dessous"),
                 f"le journal dit qui a lu, puis ce qui a été lu : {[x[:30] for x in vu]}")
        ligne = [l.split("\t")[3] for l in page.evaluate("() => tracesTSV()").split("\n") if "\tacheterGl\t" in l]
        verifier(len(ligne) == 1 and ligne[0].endswith("· doute 100 · élève 1") and "✗" in ligne[0],
                 f"et le journal d'actions aussi, pour le dépouillement : « {ligne[0] if ligne else '—'} »")
        # Le doute vaut cent pour les deux lectures : le joueur n'a rien tranché, et un chiffre
        # qui suivrait le taux d'erreur serait un oracle (règle 18).
        page.evaluate("() => { S_.b.elv = 7; S_.C = 500; Math.random = () => 0.99; }")
        clic("zur"); clic("la")
        r = page.evaluate("() => [has('la'), S_.lect.la, S_.dte.la, S_.dte.pat, S_.dte.zur === undefined]")
        verifier(r == [True, "j", 100, 100, True],
                 f"lu juste ou lu faux, à un Élève ou à sept, le doute est le même : {r}")
        page.evaluate("() => { Math.random = window._rnd; }")
        # Rien ne chiffre l'erreur, et rien ne la juge : elle se découvre dans le texte.
        page.evaluate("() => { acheterGl('an'); acheterGl('tem', 'j'); acheterGl('ur', 'j'); acheterGl('im'); }")
        page.wait_for_timeout(200)
        ds = page.evaluate("() => $('instr').querySelector('[data-ins=elv] .ds').innerText")
        verifier("déchiffre seul" in ds and "+5 % aux autres" in ds, f"sa ligne dit les deux moitiés : « {ds} »")
        vu = page.evaluate("() => document.querySelector('.shell').innerText.toLowerCase()")
        verifier(not any(m in vu for m in ("erreur", "se trompe", "68 %", "15 %", "dette")),
                 "et ne chiffre que la première — le taux d'erreur n'est nulle part à l'écran")
        # Un composé posé à la grille n'offre aucun choix, Élève ou pas : la lecture juste, et
        # le doute du joueur. Et la révision reste la sienne — elle rouvre les deux lectures.
        page.evaluate("() => { S_.C = 9e6; S_.H = 9e6; S_.b.elv = 3; acheterGl('mik'); }")
        page.wait_for_timeout(150)
        page.evaluate("() => $('doutes').querySelector('[data-dou=pat]').click()")
        verifier(ouverte(), "la révision d'un signe lu par l'Élève rouvre les deux lectures")
        r = page.evaluate("() => { ambFermer(); reviser('pat', 'j'); return [S_.lect.pat, S_.dte.pat < 100, dette()]; }")
        verifier(r == ["j", True, 0], f"et c'est alors le joueur qui tranche, avec son propre doute : {r}")

        # ---- la sauvegarde survit aux actes (LIV-3) ----
        # La clé ne change plus : la version est dans la sauvegarde, et elle se migre. Une
        # partie écrite sous l'ancienne clé déménage — sans y perdre sa nuit, que `ts` mesure,
        # ni un instrument qu'elle n'avait pas encore. Un instrument absent de `b` arrivait à
        # zéro par une liste recopiée à la main dans le chargement ; oubliée au lot suivant,
        # il serait arrivé à `undefined`, et son prix à NaN. La sauvegarde n'en porte ici
        # qu'un seul : tous les autres doivent arriver à zéro, ceux d'aujourd'hui comme ceux
        # des actes IV et V, sans qu'aucune ligne de ce test ait à les nommer.
        print("\nla sauvegarde survit aux actes")
        nuitee = ('{"O":5000,"H":300,"C":120,"rec":9,"clicks":40,"b":{"cop":12},'
                  '"gl":%s,"t":3000,"done":false}' % json.dumps(vingt))
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-actes-i-iii', "
                            "JSON.stringify(Object.assign(%s, {ts: Date.now() - 2*3600e3})))" % nuitee)
        vieille = ctx.new_page()
        casses = []
        vieille.on("pageerror", lambda e: casses.append(str(e)))
        vieille.goto(PAGE.resolve().as_uri())
        vieille.wait_for_timeout(700)
        verifier(not casses, f"aucune erreur au chargement : {casses[:1] or '—'}")
        r = vieille.evaluate("""() => { const p = JSON.parse(localStorage.getItem(KEY) || 'null');
            return [S_.gl.length, Math.round(S_.C), S_.b.cop,
                    localStorage.getItem('langue-morte-actes-i-iii'),
                    p && p.v, p && p.gl.length, versionSauvegarde()]; }""")
        verifier(r[:3] == [20, 120, 12] and r[3] is None and r[4] == r[6] and r[5] == 20,
                 f"la partie d'avant déménage sous la nouvelle clé, numérotée, et quitte l'ancienne : {r}")
        verifier(vieille.evaluate("() => nuitPassee") > 0,
                 "elle n'y perd pas sa nuit : deux heures hors ligne, rattrapées au retour")
        r = vieille.evaluate("""() => [Object.keys(fresh().b).filter(k => S_.b[k] !== (k === 'cop' ? 12 : 0)),
                                       INS.filter(i => !Number.isFinite(insCost(i))).map(i => i.k)]""")
        verifier(r == [[], []], f"chaque instrument qu'elle ne connaissait pas arrive à zéro, aucun prix à NaN : {r}")

        # La chaîne elle-même. On pose une migration de plus, le temps du test : la version se
        # compte sur la liste, une sauvegarde sans numéro part de la version 1 et les traverse
        # toutes, et une sauvegarde déjà à jour ne repasse par rien.
        r = vieille.evaluate("""() => { const v = versionSauvegarde();
            MIGRATIONS.push(p => { p.essai = (p.essai || 0) + 1; });
            const r = [versionSauvegarde() - v, migrer({b:{}}).v - v, migrer({b:{}}).essai || 0,
                       migrer({v: v, b:{}}).essai || 0, migrer({v: v + 1, b:{}}).essai || 0];
            MIGRATIONS.pop(); return r; }""")
        verifier(r == [1, 1, 1, 1, 0], f"une migration ajoutée fait la version, et ne passe qu'une fois : {r}")
        # La première écrite pour de bon (FIN-2) : une partie finie avant les deux fins
        # l'avait été par le dernier signe de l'arbre, il n'y avait pas d'autre façon.
        r = vieille.evaluate("() => [versionSauvegarde(), migrer({b:{}, done:true}), migrer({b:{}, done:false}).fin]")
        verifier(r[0] == 2 and r[1]["fin"] == "achevee" and r[1]["efface"] is True and r[2] is None,
                 f"version 2 : une partie finie avant les deux fins est achevée, une partie en cours n'est rien : {r}")
        # Une migration qui casse est un défaut du jeu, pas de la partie : la sauvegarde reste
        # telle quelle pour le jeu corrigé, et rien ne s'écrit par-dessus en attendant.
        r = vieille.evaluate("""() => { sauver(); const avant = localStorage.getItem(KEY);
            MIGRATIONS.push(() => { throw new Error('cassée'); });
            const lue = charger(), garde = sauvegardeIntouchable;
            S_.C += 1000; sauver(); const apres = localStorage.getItem(KEY);
            MIGRATIONS.pop(); sauvegardeIntouchable = false; S_.C -= 1000;
            return [lue, garde, apres === avant]; }""")
        verifier(r == [None, True, True], f"une migration qui casse ne charge rien et n'écrase rien : {r}")
        ctx.close()

        # Une sauvegarde écrite par un jeu PLUS RÉCENT — un déploiement défait, un vieux
        # fichier rouvert dans le navigateur où l'on joue le neuf. Ce jeu-ci ne sait pas ce que
        # ses champs veulent dire : il joue une partie neuve, et ni la sauvegarde des quatre
        # secondes ni « recommencer » ne touchent à l'autre.
        future = ('{"v":999,"O":7,"H":0,"C":40,"rec":0,"clicks":3,"b":{"cop":2},'
                  '"gl":["an","anna"],"t":120,"done":false,"inconnu":{"x":1}}')
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r)" % future)
        vieille = ctx.new_page()
        casses = []
        vieille.on("pageerror", lambda e: casses.append(str(e)))
        vieille.goto(PAGE.resolve().as_uri())
        vieille.wait_for_timeout(700)
        verifier(not casses, f"aucune erreur au chargement : {casses[:1] or '—'}")
        r = vieille.evaluate("() => [KEY, S_.gl.length, sauvegardeIntouchable]")
        verifier(r == ["langue-morte-partie", 0, True],
                 f"une sauvegarde d'une version plus récente ne se charge pas : {r}")
        t0 = vieille.evaluate("() => S_.t")
        vieille.wait_for_timeout(400)
        verifier(vieille.evaluate("() => S_.t") > t0, "la partie neuve se joue quand même")
        r = vieille.evaluate("""() => { S_.C = 9999; acheterGl('an'); sauver(); const a = localStorage.getItem(KEY);
            recommencer(); return [a, localStorage.getItem(KEY)]; }""")
        verifier(r == [future, future], "et ni la sauvegarde ni « recommencer » ne l'écrasent")
        ctx.close()

        # ---- la Personne (VOIX-1) ----
        # Six signes, et la porte que l'acte III laissait dans le texte : ⟨nous⟩, seul devant
        # le nom ⟨les-lecteurs⟩. Aucun multiplicateur — la branche donne de la lecture, comme
        # la Modalité — et des prix mesurés contre un plafond (I1 : quatre chiffres).
        print("\nla Personne : qui parle")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("() => GL.filter(g => g.br === 'personne').map(g => [g.id, g.cost])")
        verifier([x[0] for x in r] == ["nash", "mu", "ta", "taru", "mula", "nashal"]
                 and all(a[1] < b[1] for a, b in zip(r, r[1:])) and r[-1][1] < 10000,
                 f"six signes, ⟨nous⟩ en tête, à prix croissants sous le plafond d'I1 : {r}")
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br)).forEach(g => acheterGl(g.id)); }""")
        page.wait_for_timeout(300)
        r = page.evaluate("""() => { const m = () => [M.cop(), M.ate(), M.tabl(), M.con(), M.gram(), M.click()];
            const av = m(); acheterGl('nash'); const ap = m();
            return [av.every((v, i) => v === ap[i]), S_.done, [...touchees].includes(18)]; }""")
        page.wait_for_timeout(300)
        verifier(r == [True, False, True], f"⟨nous⟩ ne multiplie rien, et rouvre la tablette 18 : {r}")
        reste = page.eval_on_selector_all(".tablet[data-tb='18'] .tok.g", "e => e.map(x => x.dataset.w)")
        verifier(reste == ["nm4"], f"qui se lit entière, nom propre à part : {reste}")
        # Règle 15 : deux composés se posent dès qu'on a leur première moitié ; le troisième
        # est ⟨nous⟩ sur ⟨finir⟩, de l'acte V, et ne se pose qu'une fois ⟨finir⟩ lu.
        r = page.evaluate("() => [RECETTES.taru, RECETTES.mula, RECETTES.nashal, has('hal')]")
        verifier(r == [["ta", "en"], ["mu", "la"], ["nash", "hal"], False],
                 f"⟨toi-qui⟩ est ⟨toi⟩ sur ⟨si⟩, ⟨moi-absent⟩ ⟨je⟩ sur ⟨ne-pas⟩, ⟨nous-fûmes⟩ attend ⟨finir⟩ : {r}")
        r = page.evaluate("""() => { acheterGl('mu'); acheterGl('ta'); const n = nArbre();
            const r = composer('ta', 'en');
            return [r, has('taru'), nArbre() - n]; }""")
        page.wait_for_timeout(250)
        verifier(r == ["acquis", True, 1], f"posé à la grille, ⟨toi-qui⟩ compte dans l'arbre (règle 13) : {r}")
        # VOIX-2 : l'achat de ⟨toi⟩ a replié le corpus, une fois, sur ce qui s'adressait au
        # lecteur — les lignes qui portent ⟨toi⟩, ⟨toi-qui⟩ ou ⟨lire⟩. Rien d'ajouté au texte.
        r = page.evaluate("""() => { const vis = [...elCorpus.querySelectorAll('.tablet')]
                .filter(t => !t.hidden && !t.classList.contains('vide'));
            const lignes = vis.flatMap(t => [...t.children].slice(1).filter(l => !l.classList.contains('off')));
            const porte = l => ADRESSE.some(id => l.querySelector('[data-w="'+id+'"]'));
            return [concToi, lignes.length === concN, lignes.every(porte),
                    lignes.filter(l => !l.querySelector('[data-w="ta"],[data-w="taru"]')).length > 20,
                    $('a-con').hidden, $('a-con').textContent.startsWith('à toi'), S_.conc.shen || 0]; }""")
        verifier(r == [True, True, True, True, False, True, 0],
                 f"⟨toi⟩ replie le corpus sur ce qui s'adressait au lecteur, ⟨lire⟩ compris, sans compter comme une concordance : {r}")
        page.keyboard.press("Escape")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => [concToi, elCorpus.classList.contains('filtre'),
            TR.some(x => x[1] === 'adresser'), TR.some(x => x[1] === 'concFermer' && x[2] === '@toi')]""")
        verifier(r == [False, False, True, True],
                 f"échap rend le corpus entier, et le journal d'actions date l'ouverture et la sortie : {r}")
        # ⟨moi-absent⟩ : aucune attestation, et sa lecture suit ⟨ne-pas⟩ (docs/corpus.md §7.2).
        r = page.evaluate("""() => { const n = freqGlyphe('mula'); const j = [motDe('mula'), logDe('mula')];
            S_.lect.la = 'f'; const f = [motDe('mula'), logDe('mula')]; S_.lect.la = 'j';
            const pivot = 'Ils avaient un mot pour ça, et aucune tablette ne l’emploie';
            return [n, j[0], f[0], j[1].includes(pivot) && f[1].includes(pivot),
                    f[1].includes('ne pas')]; }""")
        verifier(r == [0, "moi-absent", "moi-mort", True, False],
                 f"⟨moi-absent⟩ : zéro attestation, « moi-mort » sous ⟨ne-pas⟩ mal lu, la même ligne autour : {r}")
        # ⟨nous-fûmes⟩ : une attestation, le dernier mot du corpus. Il fermait l'arbre jusqu'à
        # la Fin ; c'est désormais ⟨devenir-lecture⟩ qui le ferme (GRAINE-1).
        verifier(page.evaluate("() => [...document.querySelectorAll('#corpus .tok')].some(x => x.textContent.trim() === 'il-fallait')") is False,
                 "avant ⟨nous-fûmes⟩, rien n'est au passé")
        r = page.evaluate("""() => { acheterGl('mula'); acheterGl('nashal');
            const tb = document.querySelector('.tablet[data-tb="30"]');
            return [freqGlyphe('nashal'), S_.done, nArbre() === NGL - 7,
                    tb.lastElementChild.textContent.trim()]; }""")
        page.wait_for_timeout(300)
        verifier(r == [1, False, True, "nous-fûmes"],
                 f"⟨nous-fûmes⟩ rend lisible le dernier mot du corpus, et laisse la Fin à lire : {r}")
        # Le verrou du passé : le récit se relit au passé, y compris ce qui est déjà lu — sauf
        # ce qui s'adresse à ⟨toi⟩. La couche de traduction change ; le texte, jamais.
        textes = lambda: page.evaluate("""() => [...document.querySelectorAll('#corpus .ln')]
            .map(ln => [...ln.querySelectorAll('.tok')].map(x => x.textContent.trim()).join(' '))""")
        tx = textes()
        verifier(page.evaluate("() => document.querySelectorAll('#corpus [data-t]').length") == 275,
                 "deux cent soixante-quinze jetons portent le temps, marqués une fois pour toutes")
        verifier("je gravé · toi lire" in tx and "il-faut toi" in tx
                 and sum("· nous · il-fallait" in l for l in tx) == 30,
                 "« je gravé · toi lire », « il-faut toi » intact, et trente « après · nous · il-fallait »")
        verifier(not any("il-fallait copié" in l or "toi lu" in l or "il-faut copier" in l for l in tx),
                 "le verbe qui suit « il-fallait » garde son infinitif, et le lecteur reste au présent")
        r = page.evaluate("""() => [GL.filter(g => ['sar','kal','shen','dun'].includes(g.id)).map(g => motDe(g.id)),
            (S_.lect.dun = 'f', S_.lect.shen = 'f', paintCorpus(null),
             [...document.querySelectorAll('#corpus .tok[data-t]')].map(x => x.textContent.trim())
               .filter(m => m === 'on pouvait' || m === 'compté').length > 0)]""")
        page.evaluate("() => { S_.lect.dun = 'j'; S_.lect.shen = 'j'; paintCorpus(null); }")
        verifier(r == [["graver", "copier", "lire", "il-faut"], True],
                 f"le lexique garde l'infinitif, et le verrou suit la lecture retenue (« on pouvait », « compté ») : {r}")
        # Le franchissement d'acte (règle 19, cas général) : une dette de 5 à l'ouverture du
        # doute passe ; ⟨il-faut⟩ mal lu ensuite la porte à 7 sans que rien ne la solde ; la
        # première Personne la solde.
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br) && g.id !== 'dun')
              .forEach(g => acheterGl(g.id, ['tem', 'pat'].includes(g.id) ? 'f' : 'j'));
            const doute = [dette(), S_.contr]; acheterGl('dun', 'f');
            const ilFaut = [dette(), S_.contr]; acheterGl('nash');
            const entree = S_.contr; acheterGl('mu');
            return [doute, ilFaut, entree, S_.contr]; }""")
        page.wait_for_timeout(300)
        verifier(r == [[5, 0], [7, 0], 1, 1],
                 f"ce qu'on a tranché après le doute se solde en entrant dans l'acte IV : {r}")
        # Et pas avant le doute : sans ⟨peut-être⟩, aucun franchissement ne solde rien.
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br) && g.id !== 'mik')
              .forEach(g => acheterGl(g.id, 'f'));
            acheterGl('nash'); return [dette() > 5, S_.contr]; }""")
        verifier(r == [True, 0], f"sans le doute ouvert, entrer dans l'acte IV ne solde rien : {r}")

        # ---- les Questions (VOIX-3) ----
        # La Certitude s'arrête à 9 999 et, à partir de ⟨toi⟩, ce qui déborde remplit des
        # questions. Une question est une condition — ⟨si⟩ et des signes qu'on sait lire — et
        # la réponse est ce que le corpus a gravé après, jamais un mot écrit pour l'occasion.
        # Les instruments sont remis à zéro entre deux contrôles : sans production, rien ne
        # déborde par surprise entre deux lectures de l'état.
        print("\nles Questions : demander au texte")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br)).forEach(g => acheterGl(g.id, 'j'));
            S_.C = 9990; S_.H = 9e6; S_.b.con = 400; S_.b.gram = 40; }""")
        page.wait_for_timeout(600)
        r = page.evaluate("() => [S_.C, S_.qf, S_.qn, $('pquest').hidden]")
        verifier(r == [9999, 0, 0, True],
                 f"la Certitude s'arrête à 9 999, et avant ⟨toi⟩ le surplus se perd, panneau fermé : {r}")
        page.evaluate("() => { S_.C = 9e6; acheterGl('nash'); acheterGl('mu'); acheterGl('ta'); concFermer(); S_.C = 9999; S_.qf = 0; S_.qn = 0; }")
        page.wait_for_timeout(500)
        r = page.evaluate("() => [S_.C, S_.qf > 0, S_.qn, $('pquest').hidden]")
        verifier(r == [9999, True, 0, False], f"à partir de ⟨toi⟩, ce qui déborde remplit une question : {r}")
        page.evaluate("() => { S_.qf = Q_COUT - 10; }")
        page.wait_for_timeout(500)
        r = page.evaluate("() => { const r = [S_.C, S_.qn, questionsEnMain(), S_.qf < Q_COUT]; S_.b.con = 0; S_.b.gram = 0; return r; }")
        verifier(r == [9999, 1, 1, True], f"4 000 de surplus font une question, et la Certitude ne bouge plus : {r}")
        r = page.evaluate("""() => { S_.C = 5000; S_.b.con = 400; S_.b.gram = 40; S_.qf = 100;
            S_.ts = Date.now() - 2*3600*1000; veillee();
            const r = [S_.C, S_.qn, S_.qf]; S_.b.con = 0; S_.b.gram = 0; S_.C = 9999; return r; }""")
        verifier(r == [9999, 1, 100], f"la nuit remplit la Certitude jusqu'au plafond, jamais une question : {r}")
        # R8 : la table des réponses est lue dans le corpus. Chaque réponse finit une ligne
        # gravée, et chaque ligne porte ⟨si⟩ suivi de la condition.
        r = page.evaluate("""() => { let ok = true, n = 0;
            for(const [cle, rep] of Object.entries(QUESTIONS)) for(const e of rep) for(const [t, l] of e.lignes){
              const ln = CORPUS.find(x => x.t === t).l[l]; n++;
              const sansNb = ln.split(' ').filter(x => x.charCodeAt(0) !== 37).join(' ');
              ok = ok && (e.suite ? ln.endsWith(e.suite) : sansNb.endsWith('en ' + cle))
                      && sansNb.includes('en ' + cle);
            }
            return [Object.keys(QUESTIONS).length, ok, n, QUESTIONS['ta shen'][0].suite, QUESTIONS['ta shen'][0].lignes]; }""")
        verifier(r[0] == 15 and r[1] and r[3] == "nash la hal" and r[4] == [[24, 3]],
                 f"quinze conditions, et chaque réponse est la fin d'une ligne gravée — « si toi lire · nous ne-pas finir » : {r[:2] + r[3:]}")
        r = page.evaluate("""() => [document.querySelectorAll('#q-choix .pion:not([hidden])').length, S_.gl.length]""")
        verifier(r[0] == r[1], f"la palette ne montre que les signes acquis (règle 14) : {r}")
        dte0 = page.evaluate("() => JSON.stringify([S_.conc, S_.recs, S_.dte])")
        page.evaluate("() => { qPoser('ta'); qPoser('shen'); }")
        page.wait_for_timeout(150)
        page.click("#a-quest")
        page.wait_for_timeout(250)
        r = page.evaluate("""() => { const l = [...document.querySelectorAll('.ln.repondu')];
            const s = document.querySelector('.qrep.vu .qsuite');
            return [S_.qa, questionsEnMain(), l.length, l.map(x => x.closest('.tablet').dataset.tb),
                    !!s && s.textContent.includes('nous') && s.textContent.includes('ne-pas'),
                    !!s && !!s.querySelector('svg'), qSel.length]; }""")
        verifier(r == [["ta shen"], 0, 1, ["24"], True, True, 0],
                 f"« si toi lire » : la réponse coûte une question, s'écrit avec mes mots, ⟨finir⟩ en signe, et sa ligne s'allume : {r}")
        verifier(page.evaluate("() => JSON.stringify([S_.conc, S_.recs, S_.dte])") == dte0,
                 "poser une question ne touche pas au degré de doute (règle 18)")
        r = page.evaluate("() => [questionner(['kal']), questionner(['mu', 'nash']), S_.qa.length, LOGS.includes('Le texte ne dit rien.')]")
        verifier(r == ["refus", "refus", 1, False],
                 f"sans question en main, rien ne se pose — gravé ou non, pour ne pas dire lesquelles le sont : {r}")
        page.evaluate("() => { S_.qn += 2; }")
        r = page.evaluate("""() => [questionner(['mu', 'nash']), questionsEnMain(), LOGS[LOGS.length-1],
            questionner(['mu', 'nash'])]""")
        page.wait_for_timeout(150)
        verifier(r == ["silence", 2, "Le texte ne dit rien.", "refus"],
                 f"une condition gravée nulle part : « Le texte ne dit rien. », rien de dépensé, et elle ne se repose pas : {r}")
        r = page.evaluate("""() => { const r = questionner(['shen']); const rep = QUESTIONS['shen'];
            return [r, rep.map(e => [e.suite, e.lignes.length])]; }""")
        page.wait_for_timeout(150)
        rendu = page.evaluate("""() => [...document.querySelectorAll('.qrep')].find(b => b.dataset.q === 'shen')
            .querySelector('.qsuites').textContent""")
        verifier(r == ["reponse", [["", 58], ["ke", 1]]] and rendu.endswith("rien après ×58"),
                 f"« si lire » : « devenir » une fois, et cinquante-huit fois rien — ce qui est gravé d'abord : {r} · « {rendu} »")
        r = page.evaluate("""() => { const o = ouvertsParReponse();
            return [o.has('hal'), o.has('ke'), GL.filter(g => g.rep).map(g => g.id)]; }""")
        verifier(r == [True, True, ["hal", "ke", "meshke"]],
                 f"les réponses portent ⟨finir⟩ et ⟨devenir⟩, deux des trois mots que seule une réponse offre : {r}")
        page.evaluate("() => { S_.lect.la = 'f'; }")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => { const b = [...document.querySelectorAll('.qrep')].find(x => x.dataset.q === 'ta shen');
            const t = b.querySelector('.qsuite').textContent; S_.lect.la = 'j'; return [t.includes('fin'), t.includes('ne-pas'), QUESTIONS['ta shen'][0].suite]; }""")
        verifier(r == [True, False, "nash la hal"],
                 f"la réponse suit la lecture du joueur, jamais la vérité — ⟨ne-pas⟩ lu « fin » s'y lit « fin » : {r}")
        page.keyboard.press("Escape")
        page.wait_for_timeout(100)
        verifier(page.evaluate("() => [qVue, document.querySelectorAll('.ln.repondu').length]") == [None, 0],
                 "échap éteint les lignes de la réponse")
        page.evaluate("() => { S_.qn = Q_MAX - 1; S_.qf = Q_COUT - 1; S_.C = 9999; S_.b.con = 400; S_.b.gram = 40; }")
        page.wait_for_timeout(500)
        page.evaluate("() => { S_.b.con = 0; S_.b.gram = 0; }")
        r = page.evaluate("() => [S_.qn, S_.qf, $('q-regle').textContent, $('q-jauge-w').hidden]")
        verifier(r == [12, 0, "Douze questions : il n’en viendra plus.", True],
                 f"douze questions sur la partie, et le panneau le dit : {r}")
        r = page.evaluate("""() => { const av = gramMul(); S_.gl.push('mesh', 'hal');
            const ap = gramMul(), n = nArbre(); S_.gl.splice(-2, 2);
            return [GL.filter(g => !g.sec && (ACTE[g.br]||0) < 5).length, av === ap, n - nGrammaire()]; }""")
        verifier(r == [36, True, 2], f"la Grammaire gèle aux mots de la fin : trente-six signes la font croître, ⟨semence⟩ et ⟨finir⟩ non : {r}")
        r = page.evaluate("() => TR.filter(x => x[1] === 'questionner').map(x => x[2])")
        verifier(r == ["ta shen (toi lire) → 1 suite", "mu nash (je nous) · silence", "shen (lire) → 2 suites"],
                 f"le journal d'actions date chaque question, ce qu'elle demandait et si le texte a répondu : {r}")
        page.evaluate("() => { qMontrer('shen'); qPoser('kal'); $('reset').click(); }")
        page.wait_for_timeout(200)
        r = page.evaluate("() => [document.querySelectorAll('.ln.repondu').length, qSel.length, S_.qa.length, $('pquest').hidden]")
        verifier(r == [0, 0, 0, True], f"recommencer efface les questions et éteint leurs lignes : {r}")

        # ---- la Fin (GRAINE-1) ----
        # Sept signes au plafond, sans multiplicateur. Trois ne s'offrent qu'une fois qu'une
        # réponse les a portés, le dernier qu'une fois tout le reste lu — et la grille, elle,
        # donne un composé dès qu'on en a les parties. ⟨semence⟩ et ⟨devenir⟩ sont ambigus : leurs
        # ruptures, écrites d'avance, s'allument enfin (AMB-4).
        print("\nla Fin : lire la fin dans leur langue")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => [GL.filter(g => g.br === 'fin').map(g => [g.id, g.cost, !!g.rep, !!g.dernier]),
            NGL]""")
        verifier([x[0] for x in r[0]] == ["mesh", "hal", "halan", "ke", "halnash", "meshke", "shenke"]
                 and all(x[1] == 9999 for x in r[0])
                 and [x[0] for x in r[0] if x[2]] == ["hal", "ke", "meshke"]
                 and [x[0] for x in r[0] if x[3]] == ["shenke"] and r[1] == 43,
                 f"sept signes au plafond, trois ouverts par une réponse, ⟨devenir-lecture⟩ en dernier, quarante-trois à l'arbre : {r[:2]}")
        # ⟨sinon⟩ est laissé de côté : un signe d'ailleurs encore à lire, pour voir le dernier
        # attendre.
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.br !== 'fin' && g.id !== 'enla').forEach(g => acheterGl(g.id, 'j'));
            concFermer(); acheterGl('mesh', 'j'); S_.C = 9e6; }""")
        page.wait_for_timeout(300)
        carte = lambda g: page.evaluate("""g => { const b = $('lex').querySelector('[data-gl=' + g + ']');
            return [b.className, b.disabled, b.querySelector('.eff').textContent]; }""", g)
        r = carte("hal")
        verifier(r == ["gcard attend", True, "le texte le donnera à qui l’interroge"],
                 f"⟨finir⟩ en tête de chaîne n'est pas offert, et la carte dit sa règle sans dire quoi demander : {r}")
        page.evaluate("() => { S_.qn = 1; questionner(['ta', 'shen']); }")
        page.wait_for_timeout(200)
        r = carte("hal")
        verifier(r[0] == "gcard afford" and r[1] is False,
                 f"« si toi lire » a porté ⟨finir⟩ : il s'offre, au prix de tous les autres : {r}")
        page.evaluate("() => $('lex').querySelector('[data-gl=hal]').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("() => [has('hal'), S_.done, $('amb').hidden]")
        verifier(r == [True, False, True], f"et s'achète d'un clic, sans lecture à trancher : {r}")
        # La grille ne passe pas par le lexique : ⟨germer⟩ est ⟨semence⟩ sur ⟨devenir⟩, et qui le
        # voit fait l'économie de sa question.
        r = page.evaluate("""() => { acheterGl('ke', 'j'); const o = ouvertsParReponse().has('meshke');
            const c = composer('mesh', 'ke'); return [o, c, has('meshke'), S_.done]; }""")
        page.wait_for_timeout(200)
        verifier(r == [False, "acquis", True, False],
                 f"⟨germer⟩ posé à la grille sans que rien l'ait ouvert : {r}")
        page.evaluate("() => { acheterGl('halan'); acheterGl('halnash'); }")
        page.wait_for_timeout(200)
        r = carte("shenke")
        verifier(r[0] == "gcard attend" and r[2] == "il vient quand tout le reste est lu",
                 f"en tête de la Fin, ⟨devenir-lecture⟩ attend que tout le reste soit lu — ⟨sinon⟩ ne l'est pas : {r}")
        page.evaluate("() => { acheterGl('enla'); }")
        page.wait_for_timeout(200)
        r = carte("shenke")
        verifier(r[0] == "gcard afford", f"et s'offre quand c'est fait : {r}")
        r = page.evaluate("""() => { acheterGl('shenke');
            return [S_.done, [...finLire], nArbre() === NGL, logDe('shenke').startsWith('Devenir-lecture')]; }""")
        page.wait_for_timeout(300)
        verifier(r == [True, [27], True, True],
                 f"son achat ferme la partie, et la carte attend la tablette 27, sa seule attestation (règle 16) : {r}")
        # Composé tôt, il « grille la révélation de vitesse » (design doc §6) — et ne ferme rien.
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.br !== 'fin').forEach(g => acheterGl(g.id, 'j'));
            acheterGl('ke', 'j'); const c = composer('shen', 'ke');
            return [c, has('shenke'), S_.done, nArbre() === NGL - 5]; }""")
        page.wait_for_timeout(200)
        verifier(r == ["acquis", True, False, True],
                 f"⟨devenir-lecture⟩ composé tôt compte dans l'arbre et ne ferme pas la partie : {r}")
        # Le verrou du passé s'applique aux mots de la Fin, verbes et composés faux compris.
        ligne = lambda t, l: page.evaluate("""([t, l]) => [...document.querySelector('.tablet[data-tb="' + t + '"]').children[l]
            .querySelectorAll('.tok')].map(x => x.textContent.trim()).join(' ')""", [t, l])
        page.evaluate("() => { acheterGl('hal'); acheterGl('mesh', 'f'); acheterGl('meshke'); paintCorpus(null); }")
        page.wait_for_timeout(200)
        r = [ligne(24, 3), ligne(22, 19), ligne(22, 18)]
        verifier(r == ["si toi lire · nous ne-pas fini", "si tablette · né", "si enfant · ne-pas né"],
                 f"au passé, sauf ce qui s'adresse à ⟨toi⟩ ; ⟨germer⟩ salit par ⟨semence⟩ lu « enfant » : {r}")
        # AMB-4 : les deux ruptures de l'acte V, sur le texte rendu. Celle de ⟨semence⟩ se lit
        # l'autre moitié de sa paire réparante tenue juste (docs/corpus.md §7.3).
        page.evaluate("() => { acheterGl('lash'); paintCorpus(null); }")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => [ruptureLignes().map(x => x.gl), document.querySelector('.tablet[data-tb="22"]').children[18].classList.contains('rompu'),
            document.querySelectorAll('#corpus .tok.rompu').length]""")
        verifier(r == [["mesh"], True, 0],
                 f"« si enfant · ne-pas né » s'allume — la ligne, jamais le jeton (règle 20) : {r}")
        page.evaluate("() => { S_.lect.mesh = 'j'; S_.lect.ke = 'f'; numCache.length = 0; paintCorpus(null); }")
        page.wait_for_timeout(150)
        r = [ligne(17, 6), page.evaluate("() => ruptureLignes().map(x => x.gl)")]
        # Sous le verrou du passé, la ligne passe au passé avec le reste du récit — et ne se
        # construit pas davantage.
        verifier(r == ["il-fallait tablette · porté lu", ["ke"]],
                 f"⟨devenir⟩ lu « porter » : « il-fallait tablette · porté lu » ne se construit pas, et s'allume : {r}")
        page.evaluate("() => { S_.lect.mesh = 'f'; paintCorpus(null); }")
        page.wait_for_timeout(150)
        r = page.evaluate("() => ruptureLignes().map(x => x.gl)")
        verifier(r == ["ke"], f"la paire réparante ⟨semence⟩ + ⟨devenir⟩ éteint la ligne de ⟨semence⟩, pas celle de ⟨devenir⟩ : {r}")
        page.evaluate("() => { S_.lect.mesh = 'j'; S_.lect.ke = 'j'; paintCorpus(null); }")
        # « notre-fin · ne-pas » ne se tranche jamais : ni le corpus ni la ligne de journal ne
        # choisissent, et aucun texte ne présuppose une lecture qu'on n'a pas faite (règle 17).
        page.evaluate("() => { acheterGl('halnash'); paintCorpus(null); }")
        page.wait_for_timeout(150)
        lg = page.evaluate("() => [logDe('halnash'), AMB.mesh.log, byId.nashal.log]")
        verifier(ligne(30, 7) == "notre-fin · ne-pas" and not any(m in lg[0] for m in ("non", "pas notre", "sens")),
                 f"« notre-fin · ne-pas » : la ligne de journal ne tranche pas : « {lg[0]} »")
        verifier("tombe" not in lg[1] and "ne sais pas encore lire" not in lg[2],
                 "aucune ligne écrite d'avance ne présuppose une lecture : ni « tombes » sous ⟨semence⟩, ni ⟨finir⟩ illisible sous ⟨nous-fûmes⟩")
        # Le premier signe de la Fin franchit l'acte V : la contradiction s'y solde de nouveau.
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { S_.C = 9e6;
            GL.filter(g => !g.sec && g.br !== 'fin')
              .forEach(g => acheterGl(g.id, ['tem', 'pat'].includes(g.id) ? 'f' : 'j'));
            const iv = [dette(), S_.contr]; acheterGl('mesh', 'f');
            return [iv, dette(), S_.contr]; }""")
        page.wait_for_timeout(200)
        verifier(r == [[5, 0], 6, 1],
                 f"⟨semence⟩ mal lu en entrant dans l'acte V fait passer la dette à six, et la contradiction s'arme : {r}")

        # ---- le Lecteur (GRAINE-2) ----
        # « Acheté avant qu'on sache ce que c'est. On découvre à l'acte V que ce n'est pas un
        # instrument : c'est le corpus qui a commencé à lire » (design doc §5). Ce qui se
        # vérifie surtout, c'est ce qu'il ne dit pas : ni nom français, ni ligne d'effet.
        print("\nle Lecteur : le corpus a commencé à lire")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && g.br !== 'fin').forEach(g => acheterGl(g.id, 'j')); concFermer(); }""")
        page.wait_for_timeout(200)
        lecteur = lambda: page.evaluate("""() => { const b = $('instr').querySelector('[data-ins=lec]');
            return [b.className, b.disabled, b.querySelector('.nn').textContent, b.querySelector('.ds').textContent,
                    !!b.querySelector('.nn svg')]; }""")
        r = lecteur()
        verifier(r[0] == "ins locked" and r[1] is True, f"fermé jusqu'à ⟨semence⟩, l'acte IV entier lu : {r[:2]}")
        page.evaluate("() => { acheterGl('mesh', 'j'); S_.O = 2e6; S_.C = 9999; S_.qf = 0; S_.qn = 0; }")
        page.wait_for_timeout(200)
        r = lecteur()
        verifier(r == ["ins afford", False, "", "", True],
                 f"⟨semence⟩ l'ouvre : un signe pour nom, pas un mot, et aucune ligne d'effet — ⟨dire⟩ est pourtant lu : {r}")
        page.evaluate("() => $('instr').querySelector('[data-ins=lec]').click()")
        page.wait_for_timeout(150)
        r = page.evaluate("() => [S_.b.lec, S_.O, insCost(INS.find(i => i.k === 'lec'))]")
        verifier(r == [1, 1500000, 1000000], f"il se paie en occurrences, comme les huit autres : {r}")
        # Il lit seul : une tablette par minute et par Lecteur, et chaque tablette lue verse
        # 300 à la question suivante. Pas de nuit : `tick` ne tourne pas hors ligne.
        r = page.evaluate("""() => { const q0 = S_.qf; tick(90);
            return [S_.tete, S_.qf - q0, [...$('rail').querySelectorAll('.parcourue')].map(c => c.dataset.go),
                    [...elCorpus.querySelectorAll('.tablet.parcourue')].map(e => e.dataset.tb)]; }""")
        page.wait_for_timeout(200)
        verifier(abs(r[0] - 1.5) < 0.05 and r[1] == 300,
                 f"une tablette par minute, et chacune verse à la question suivante : {r[:2]}")
        r = page.evaluate("""() => [[...$('rail').querySelectorAll('.parcourue')].map(c => c.dataset.go),
            [...elCorpus.querySelectorAll('.tablet.parcourue')].map(e => e.dataset.tb),
            (() => { const l = elCorpus.querySelector('.ln.lecteur'); return l && [l.closest('.tablet').dataset.tb,
               [...l.parentElement.children].indexOf(l)]; })()]""")
        verifier(r[0] == ["1"] and r[1] == ["1"] and r[2] is not None and r[2][0] == "2",
                 f"on le voit faire : la tablette 1 marquée, une ligne de la 2 qui s'éclaire : {r}")
        r = page.evaluate("""() => { S_.b.lec = 3; const t0 = S_.tete; tick(60); const v = S_.tete - t0;
            const n = S_.qn, f = S_.qf; S_.ts = Date.now() - 3600e3; veillee();
            return [v, S_.tete === t0 + v, n, f]; }""")
        verifier(abs(r[0] - 3) < 1e-6 and r[1] is True,
                 f"trois Lecteurs lisent trois fois plus vite, et la nuit ne lit rien : {r[:2]}")
        # Sans aucun instrument qui produise : ce qui remplit la question, c'est lui seul.
        r = page.evaluate("""() => { S_.qn = 0; S_.qf = 0; const k = Math.floor(S_.tete); tick(3600);
            const a = [S_.tete, S_.qn * Q_COUT + S_.qf, (30 - k) * LEC_Q]; tick(600);
            return [...a, S_.tete, S_.qn * Q_COUT + S_.qf]; }""")
        verifier(r[0] == 30 and r[1] == r[2] and r[3] == 30 and r[4] == r[1],
                 f"trente tablettes, chacune versée une fois, et il s'arrête : {r}")
        verifier(page.evaluate("() => TR.filter(e => e[1] === 'lireCorpus').length") >= 3,
                 "le journal d'actions date chaque tablette qu'il finit")
        # La révélation par le texte : son nom est ⟨devenir-lecture⟩, qu'on lit quand on le sait,
        # avec le mot qu'on lit (règle 17) — et c'est la ligne de la tablette 27 que l'effacement
        # attend, « tablette · devenir-lecture ».
        nom = lambda: page.evaluate("() => $('instr').querySelector('[data-ins=lec] .nn').textContent")
        page.evaluate("() => { S_.lect.shen = 'f'; acheterGl('shenke'); }")
        page.wait_for_timeout(150)
        r = [nom(), page.evaluate("() => motDe('shenke')")]
        page.evaluate("() => { S_.lect.shen = 'j'; }")
        page.wait_for_timeout(150)
        r.append(nom())
        verifier(r[2] == "devenir-lecture" and r[0] == r[1] and r[0] != r[2],
                 f"son nom se lit avec le dernier signe — et avec la lecture qu'on en a : {r}")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)

        # ---- le Corpus jumeau (VOIX-4) ----
        # « Une deuxième inscription est trouvée » : une copie, pas un bilingue. Chaque tablette
        # regagne la moitié de son gisement, avec son propre tarif, figé au premier relevé sur
        # la copie (règle 9) ; l'original passe d'abord, et il n'y en a qu'une.
        print("\nle Corpus jumeau : une deuxième inscription")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br)).forEach(g => acheterGl(g.id, 'j'));
            concFermer(); S_.O = 0; S_.b.cop = 100; }""")
        page.wait_for_timeout(200)
        jumeau = lambda: page.evaluate("""() => { const b = $('instr').querySelector('[data-ins=jum]');
            return [b.classList.contains('locked'), b.disabled, b.querySelector('.nn').textContent,
                    b.querySelector('.ds').textContent, b.querySelector('.cs').textContent.trim(),
                    b.querySelectorAll('.sg svg').length]; }""")
        verifier(jumeau()[0] is True, "fermé tant que l'acte IV n'est pas ouvert")
        page.evaluate("() => { acheterGl('nash'); }")
        page.wait_for_timeout(200)
        r = jumeau()
        verifier(r[0] is False and r[2] == "Corpus jumeau" and "copie" in r[3] and r[5] == 2,
                 f"⟨nous⟩ l'ouvre : deux tablettes pour signe, et sa ligne dit ce qu'il est : {r}")
        # Une tablette dont l'original est vidé : le plancher, jusqu'à ce que la copie soit là.
        r = page.evaluate("""() => { for (let j = 0; j < GISEMENT[1]; j++) relever(1, j);
            const ou = relever(1, 0); S_.O = 400000; acheterIns('jum'); const o1 = S_.O;
            acheterIns('jum'); return [ou, S_.b.jum, o1, S_.O, LOGS.some(l => l.startsWith('Une deuxième inscription'))]; }""")
        verifier(r[0] == "plancher" and r[1] == 1 and r[2] == 100000 and r[3] == 100000 and r[4] is True,
                 f"l'original vidé rend le plancher ; la copie se paie une fois, en occurrences, et se dit : {r}")
        page.wait_for_timeout(150)
        r = jumeau()
        verifier(r[1] is True and r[4] == "", f"et ne se rachète pas : {r}")
        r = page.evaluate("""() => { const o = S_.O, tarif = tarifRel(), ou = relever(1, 0), gain = S_.O - o;
            const o2 = S_.O, ou2 = relever(1, 0);
            return [ou, Math.abs(gain - tarif) < 1e-6, gain > M.click(), Math.abs(S_.prixJ[1] - gain) < 1e-6, ou2, Math.abs(S_.O - o2 - M.click()) < 1e-6]; }""")
        verifier(r == ["copie", True, True, True, "plancher", True],
                 f"le premier relevé sur la copie fige son tarif au débit du moment, un jeton n'y vaut qu'une fois : {r}")
        r = page.evaluate("""() => { const vus = [];
            for (let j = 1; j < GIS_COPIE[1]; j++) vus.push(relever(1, j));
            const fini = LOGS.some(l => l === 'Tablette 1 : plus rien à en tirer.');
            return [vus.every(v => v === 'copie'), (S_.relJ[1] || []).length === GIS_COPIE[1], fini,
                    relever(1, GIS_COPIE[1]), gisReste(1), relever(2, 0)]; }""")
        verifier(r == [True, True, True, "plancher", 0, "neuf"],
                 f"la moitié du gisement, puis plus rien — et l'original passe toujours d'abord : {r}")
        # La barre et le texte le disent : une tablette vidée se rallume, un jeton relevé deux
        # fois porte une marque plus forte.
        r = page.evaluate("""() => { for (let j = 0; j < GISEMENT[3]; j++) relever(3, j);
            const t = titreCell(3); paintRail();
            const c = $('rail').querySelector('[data-go="3"]');
            return [t.includes('copie intacte'), t.includes('/' + (GISEMENT[3] + GIS_COPIE[3])), c.classList.contains('sec')]; }""")
        verifier(r == [True, True, False], f"la tablette vidée se rallume, et son infobulle dit la copie : {r}")
        page.evaluate("() => versTablette(3)")
        page.wait_for_timeout(600)
        page.evaluate("() => elCorpus.querySelector('.tablet[data-tb=\"3\"] .tok[data-j=\"0\"]').click()")
        page.wait_for_timeout(150)
        r = page.evaluate("""() => [elCorpus.querySelector('.tablet[data-tb="3"] .tok[data-j="0"]').className,
            TR.filter(e => e[1] === 'relever').slice(-1)[0][2]]""")
        verifier("rel2" in r[0] and r[1] == "tablette 3 · copie",
                 f"relevé une seconde fois, le jeton le montre, et le journal d'actions dit lequel a payé : {r}")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)

        # ---- I2 : perdre la lisibilité de ses propres nombres (VOIX-5) ----
        # Au million, une fois l'acte IV ouvert, trois chiffres restent au joueur et les zéros
        # qui suivent sont les leurs, dessinés comme ⟨zéro⟩. ⟨zéro⟩, posé à la grille, rend la
        # notation compacte de ⟨cent⟩.
        print("\nI2 : les zéros sont les leurs")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("""() => { S_.C = 9e6; S_.H = 9e6;
            GL.filter(g => !g.sec && !['personne', 'fin'].includes(g.br)).forEach(g => acheterGl(g.id, 'j'));
            concFermer(); S_.O = 2345678; S_.H = 0; S_.C = 0; }""")
        page.wait_for_timeout(200)
        compteur = lambda: page.evaluate("""() => { const v = $('vl-O');
            return [v.textContent, v.querySelectorAll('.zeros svg').length]; }""")
        r = compteur()
        verifier(r == ["2,35 M", 0], f"avant ⟨nous⟩, le million s'écrit encore en ⟨cent⟩ : {r}")
        page.evaluate("() => { S_.C = 9999; acheterGl('nash'); S_.C = 0; S_.O = 2345678; }")
        page.wait_for_timeout(200)
        r = compteur()
        verifier(r == ["234", 4], f"l'acte IV ouvert, trois chiffres sont les miens et quatre zéros les leurs : {r}")
        r = page.evaluate("""() => { const z = $('vl-O').querySelector('.zeros svg');
            return z && z.outerHTML === new DOMParser().parseFromString(sv('lan'), 'text/html').body.firstChild.outerHTML; }""")
        verifier(r is True, "et ces zéros sont le tracé de ⟨zéro⟩, ⟨ne-pas⟩ sur ⟨un⟩")
        # Tronqué et non arrondi, comme `big()` tronque avant de replier : un nombre à moi ne
        # s'affiche jamais plus grand qu'il n'est.
        r = page.evaluate("""() => [1000000, 1050000, 1200000, 1999999, 999000, 500000, 123456789].map(n => {
            const d = document.createElement('span'); d.innerHTML = big(n);
            return [d.textContent, d.querySelectorAll('.zeros svg').length]; })""")
        verifier(r == [["1", 6], ["105", 4], ["12", 5], ["199", 4], ["999,0 k", 0], ["500,0 k", 0], ["123", 6]],
                 f"un zéro de queue n'est jamais un chiffre à moi, et rien ne change sous le million : {r}")
        # Les coûts passent par la même porte que les compteurs : le prix d'un Élève au million.
        page.evaluate("() => { S_.b.gram = 1; S_.b.elv = 7; }")
        page.wait_for_timeout(200)
        r = page.evaluate("""() => { const c = $('instr').querySelector('[data-ins=elv] .cs');
            return [c.textContent, c.querySelectorAll('.zeros svg').length, insCost(INS.find(i => i.k === 'elv'))]; }""")
        verifier(r[0] == "122" and r[1] == 4 and r[2] == 1224441,
                 f"un coût au million aussi : {r}")
        r = page.evaluate("() => tracesTSV()").split("\n")
        r = [l for l in r[max(i for i, l in enumerate(r) if "\treset\t" in l):] if "\tzeros\t" in l]
        verifier(len(r) == 1 and r[0].split("\t")[3].replace("\u202f", " ") == "2 345 678",
                 f"le journal d'actions date la première fois, une seule : {[l.split(chr(9))[2:] for l in r]}")
        # Un composé secret n'ouvre pas l'acte IV : il ne franchit rien (règle 13).
        r = page.evaluate("() => { S_.gl = S_.gl.filter(x => x !== 'nash'); return acteIV(); }")
        verifier(r is False, "un composé secret ne compte pas pour l'acte IV")
        page.evaluate("() => { S_.gl.push('nash'); }")
        # ⟨zéro⟩ les rend : la notation compacte revient, compteurs et coûts.
        r = page.evaluate("() => { S_.C = 9999; S_.H = 9999; return [composer('la', 'an'), has('lan'), byId.lan.eff]; }")
        verifier(r[0] == "acquis" and r[1] is True and "grands nombres" in r[2],
                 f"⟨zéro⟩ se pose à la grille, et sa ligne dit ce qu'il rend : {r}")
        page.evaluate("() => { S_.O = 2345678; }")
        page.wait_for_timeout(200)
        r = compteur() + [page.evaluate("() => $('instr').querySelector('[data-ins=elv] .cs').textContent")]
        verifier(r == ["2,35 M", 0, "1,22 M"], f"et mes nombres se relisent : {r}")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)

        # ---- la coupure entre deux séances (PT11) ----
        # PT11 se joue en deux fois au plus. Avant ⟨nuit⟩, rouvrir une partie ne laissait
        # aucune trace : la partie attend, `veillee` ne journalise que ce qu'elle crédite, et le
        # chrono est du temps de jeu. Deux séances se lisaient comme une seule.
        print("\nla coupure entre deux séances")
        page.evaluate("() => $('reset').click()")
        page.wait_for_timeout(200)
        page.evaluate("() => { S_.C = 99; acheterGl('an'); sauver(); sauverTraces(); }")
        sauve = page.evaluate("() => { const s = JSON.parse(localStorage.getItem(KEY)); s.ts = Date.now() - 95*60000; return JSON.stringify(s); }")
        traces = page.evaluate("() => localStorage.getItem('langue-morte-traces-v1')")
        ctx = nav.new_context()
        ctx.add_init_script("localStorage.setItem('langue-morte-partie', %r); localStorage.setItem('langue-morte-traces-v1', %r);"
                            % (sauve, traces))
        autre = ctx.new_page()
        autre.goto(PAGE.resolve().as_uri())
        autre.wait_for_timeout(600)
        r = autre.evaluate("""() => { const t = TR.filter(e => e[1] !== 'etat');
            return [t.slice(-1)[0][1], t.slice(-1)[0][2], TR.some(e => e[1] === 'veillee'), has('an')]; }""")
        verifier(r[0] == "reprise" and r[1].startswith("95 min") and r[2] is False and r[3] is True,
                 f"rouvrir la partie laisse une ligne « reprise » qui dit l'absence, même avant ⟨nuit⟩ : {r}")
        ctx.close()
        r = page.evaluate("() => TR.filter(e => e[1] === 'reprise').length")
        verifier(r == 0, f"et une partie jamais rouverte n'en a aucune : {r}")

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
