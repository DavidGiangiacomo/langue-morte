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

from sim import P, run

# Une combinaison est jouée aux trois cadences et notée sur son pire cas : un réglage qui
# ne tient qu'à 40 clics/minute ne tient pas.
CADENCES = (5, 15, 40)
GRILLE = dict(rec_r=(1.26, 1.30, 1.35), con_b=(350, 400, 450), cop_b=(10, 15))

# Garde-fous. Durée et écart viennent de PT9 : 66 min 49 mesurées, 71 à 77 simulées par
# l'acheteur recalé. Le plafond par tranche est la règle 2 du CLAUDE.md.
DUREE = (71.0, 77.0)
ECART_MAX = 6.0
I6_MAX = 30.0
NT = 6                  # tranches retenues : 0-10′ à 50-60′, au-delà tout est à zéro


def i6_tranches(s):
    """I6 par tranche de dix minutes. None quand la tranche produit moins d'une demi-
    certitude : le ratio n'y mesure rien. C'est le cas de 0-10′ tant qu'aucune Concordance
    n'est posée — 22 certitudes de recoupement contre 0 d'instrument font 100 %, ce qui
    donne la date du premier achat et rien sur l'équilibrage."""
    return [None if r + i < 0.5 else 100.0 * r / (r + i)
            for r, i in zip(s['tr_rec'][:NT], s['tr_ins'][:NT])]


def essai(variante):
    """Une combinaison, jouée aux trois cadences, réduite à ses pires mesures."""
    durees, ecarts, con1, trs = [], [], [], []
    for cpm in CADENCES:
        tt, marks, _, s = run({**P, **variante}, cpm)
        durees.append(tt)
        ecarts.append(max((marks[i][1] - marks[i - 1][1] for i in range(1, len(marks))),
                          default=0.0))
        con1.append(s['premier'].get('con'))
        trs.append(i6_tranches(s))
    pire = [max((t[i] for t in trs if t[i] is not None), default=None) for i in range(NT)]
    return dict(
        d0=min(durees), d1=max(durees), ecart=max(ecarts),
        con1=max((c for c in con1 if c is not None), default=None),
        tr=pire,
        rythme=DUREE[0] <= min(durees) and max(durees) <= DUREE[1] and max(ecarts) <= ECART_MAX,
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
    lignes.sort(key=lambda x: (not (x[1]['rythme'] and x[1]['i6']),
                               max((t for t in x[1]['tr'][1:] if t is not None), default=0.0)))

    entete = ' '.join(f"{k.split('_')[0]:>4}" for k in cles)
    tranches = ' '.join(f"{i*10:>2}-{i*10+10}′" for i in range(NT))
    print(f"{entete} | durée (min) | écart | 1re Conc. | {tranches} | verdict")
    print('-' * (len(entete) + len(tranches) + 46))

    for v, r in lignes:
        vals = ' '.join(f"{v[k]:>4}" for k in cles)
        con1 = '  —  ' if r['con1'] is None else f"{r['con1']:4.1f}′"
        verdict = ('rythme ' if r['rythme'] else '       ') + ('I6' if r['i6'] else '  ')
        print(f"{vals} | {r['d0']:5.1f}–{r['d1']:5.1f} | {r['ecart']:5.1f} | "
              f"{con1:>9} | {' '.join(pct(t) for t in r['tr'])} | {verdict}")

    retenues = [v for v, r in lignes if r['rythme'] and r['i6']]
    print(f"\n{len(retenues)} combinaison(s) sur {len(lignes)} passent les garde-fous "
          f"(durée {DUREE[0]:.0f}–{DUREE[1]:.0f} min, écart ≤ {ECART_MAX:.0f} min, "
          f"tranches ≥ 10′ ≤ {I6_MAX:.0f} %).")
    print("La tranche 0-10′ est affichée mais ne compte pas : voir i6_tranches().")
