#!/usr/bin/env python3
"""
Balayage de constantes — « La langue morte », actes I à III.
Rejoue `sim.run` sur une grille de valeurs et ne rend qu'une ligne par combinaison,
pour choisir un réglage sans lire quatre cents lignes de journal.

Usage :  python outils/balayage.py
Modifier GRILLE pour balayer d'autres constantes de P.

L'économie n'est pas recopiée ici : elle est importée de `sim.py`, qui l'a déjà recopiée
une fois depuis `economie.js`. Un troisième exemplaire diverge le jour où on règle une
constante dans l'un et pas dans l'autre — et il répond alors avec assurance.
"""
import itertools
import sys

from sim import AMBIGUS, P, run

# Une combinaison est jouée aux trois cadences et notée sur son pire cas : un réglage qui
# ne tient qu'à 40 clics/minute ne tient pas.
CADENCES = (5, 15, 40)
# ... et aux deux lectures extrêmes, depuis AMB-1 : toutes justes, toutes fausses. La lecture
# fausse majore de 25 % le bonus des cinq signes ambigus qui en portent un, ce qui RACCOURCIT
# la partie de cinq minutes environ sans toucher aux autres garde-fous. Deux réglages entre
# lesquels seule la lecture tranche n'existent pas : c'est le même réglage, joué par deux
# joueurs qui n'ont pas lu la même chose, et il doit tenir pour les deux.
LECTURES = ((), AMBIGUS)
GRILLE = dict(rec_r=(1.26, 1.30, 1.35), con_b=(350, 400, 450), cop_b=(10, 15),
              rev_r=(1.0, 1.1, 1.25))

# Garde-fous. L'écart et le plafond par tranche sont des invariants — I4 et la règle 2 du
# CLAUDE.md — et ne bougent pas. La DURÉE, elle, n'en est pas un : elle vaut pour un lexique
# d'une taille donnée, et grandit à chaque lot de glyphes. Elle est restée à (71, 77), la
# mesure de PT9 à vingt glyphes, pendant que l'arbre passait à vingt-trois : au commit
# `da61b19`, ce balayage rejetait ses dix-huit combinaisons, y compris le réglage en place,
# et disait « 0 sur 18 » sans que rien ne soit cassé. Re-baser cette fenêtre fait partie de
# tout lot qui ajoute des signes.
# 29 glyphes (`peut-être` compris) : le réglage retenu mesure 90,5-93,7 min aux trois
# cadences toutes lectures justes, et 85,2-88,1 min toutes lectures fausses. La fenêtre
# couvre les deux, aux mêmes marges qu'aux lots précédents — trois minutes sous le plancher
# mesuré, deux au-dessus du plafond. Elle reste large depuis AMB-1, qui lui a ajouté la
# lecture comme variable, et trie d'autant moins : c'est assumé, et ce sont les trois autres
# garde-fous qui trient, aucun n'étant touché par la lecture (pire tranche 26 % juste contre
# 22 % faux, écart 5,2 contre 4,6, main 21,6 % contre 23,5 %).
DUREE = (82.0, 96.0)
ECART_MAX = 6.0
I6_MAX = 30.0
# La part manuelle des OCCURRENCES, entrée dans le tri le 14/09/2026 en même temps que
# `rev_r`. Aucune combinaison de la grille actuelle ne s'en approche (22 à 24 %), et c'est
# exprès : ce garde-fou est là pour la famille de courbes qui N'Y est pas. Le premier
# candidat au réglage du dégagement était « tout sortir de terre à 80 % de l'arbre » ; il
# gagnait deux points sur la pire tranche d'I6 et ramenait la main de 22,9 % à 12,4 %,
# parce qu'une tablette sortie tôt voit son tarif figé bas (règle 9). C'est le défaut de
# PT6, où la main était tombée à 0,1 % des occurrences — et aucun des garde-fous
# précédents ne le voyait passer. Le plancher est donc la borne utile ici ; le plafond de
# 40 % du CLAUDE.md, lui, porte sur la mesure RÉELLE d'un playtest (36,3 % en PT9 pour
# 22 % simulés), que ce simulateur n'atteint jamais.
MAIN_MIN = 15.0
NT = 6                  # tranches retenues : 0-10′ à 50-60′, au-delà tout est à zéro


def i6_tranches(s):
    """I6 par tranche de dix minutes. None quand la tranche produit moins d'une demi-
    certitude : le ratio n'y mesure rien. C'est le cas de 0-10′ tant qu'aucune Concordance
    n'est posée — 22 certitudes de recoupement contre 0 d'instrument font 100 %, ce qui
    donne la date du premier achat et rien sur l'équilibrage."""
    return [None if r + i < 0.5 else 100.0 * r / (r + i)
            for r, i in zip(s['tr_rec'][:NT], s['tr_ins'][:NT])]


def essai(variante):
    """Une combinaison, jouée aux trois cadences et aux deux lectures extrêmes, réduite à
    ses pires mesures."""
    durees, ecarts, con1, trs, mains = [], [], [], [], []
    for cpm, lect in itertools.product(CADENCES, LECTURES):
        tt, marks, _, s = run({**P, **variante}, cpm, faux=lect)
        durees.append(tt)
        ecarts.append(max((marks[i][1] - marks[i - 1][1] for i in range(1, len(marks))),
                          default=0.0))
        con1.append(s['premier'].get('con'))
        trs.append(i6_tranches(s))
        mains.append(100.0 * s['o_main'] / max(1e-9, s['o_main'] + s['o_pass']))
    pire = [max((t[i] for t in trs if t[i] is not None), default=None) for i in range(NT)]
    return dict(
        d0=min(durees), d1=max(durees), ecart=max(ecarts),
        con1=max((c for c in con1 if c is not None), default=None),
        tr=pire, main=min(mains),
        rythme=DUREE[0] <= min(durees) and max(durees) <= DUREE[1] and max(ecarts) <= ECART_MAX,
        # Règle 9 : le gisement, et non la cadence de clic, décide de ce que la main
        # rapporte. Un réglage qui la vide ne se rattrape pas ailleurs.
        main_ok=min(mains) >= MAIN_MIN,
        # L'ouverture est exclue du verdict, pas de l'affichage : elle est structurellement
        # au-dessus du plafond tant que la chaîne n'a pas rendu sa première Certitude.
        i6=all(v is None or v <= I6_MAX for v in pire[1:]),
    )


def pct(v):
    return ' —  ' if v is None else f"{v:3.0f} %"


if __name__ == '__main__':
    # Sans ça le script meurt sur une console cp1252 — le ′ des tranches suffit — après
    # avoir imprimé les premières lignes, ce qui a l'air d'une réussite partielle.
    sys.stdout.reconfigure(encoding='utf-8')

    cles = list(GRILLE)
    lignes = [(v, essai(v)) for v in
              (dict(zip(cles, val)) for val in itertools.product(*(GRILLE[k] for k in cles)))]
    # Les combinaisons retenues d'abord, puis la pire tranche hors ouverture : c'est elle
    # qui décide, l'ouverture ne discrimine rien.
    lignes.sort(key=lambda x: (not (x[1]['rythme'] and x[1]['i6'] and x[1]['main_ok']),
                               max((t for t in x[1]['tr'][1:] if t is not None), default=0.0)))

    entete = ' '.join(f"{k.split('_')[0]:>4}" for k in cles)
    tranches = ' '.join(f"{i*10:>2}-{i*10+10}′" for i in range(NT))
    print(f"{entete} | durée (min) | écart | 1re Conc. | main | {tranches} | verdict")
    print('-' * (len(entete) + len(tranches) + 53))

    for v, r in lignes:
        vals = ' '.join(f"{v[k]:>4}" for k in cles)
        con1 = '  —  ' if r['con1'] is None else f"{r['con1']:4.1f}′"
        verdict = (('rythme ' if r['rythme'] else '       ')
                   + ('I6 ' if r['i6'] else '   ') + ('main' if r['main_ok'] else '    '))
        print(f"{vals} | {r['d0']:5.1f}–{r['d1']:5.1f} | {r['ecart']:5.1f} | "
              f"{con1:>9} | {r['main']:3.0f} % | {' '.join(pct(t) for t in r['tr'])} | {verdict}")

    retenues = [v for v, r in lignes if r['rythme'] and r['i6'] and r['main_ok']]
    print(f"\n{len(retenues)} combinaison(s) sur {len(lignes)} passent les garde-fous "
          f"(durée {DUREE[0]:.0f}–{DUREE[1]:.0f} min, écart ≤ {ECART_MAX:.0f} min, "
          f"tranches ≥ 10′ ≤ {I6_MAX:.0f} %, main ≥ {MAIN_MIN:.0f} % des occurrences).")
    print("La tranche 0-10′ est affichée mais ne compte pas : voir i6_tranches().")
