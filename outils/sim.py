#!/usr/bin/env python3
"""
Simulateur d'économie — « La langue morte », MVP actes I-II.
Rejoue la boucle du prototype avec un acheteur heuristique et une cadence
de clic paramétrable, pour vérifier le rythme sans avoir à jouer 40 minutes.

Usage :  python3 sim.py
Modifier P (constantes) et GL (coûts des glyphes) pour tester une variante.

Le relevé manuel n'est plus un débit : il puise dans le gisement d'une tablette, fini,
qui se débloque au rythme du dégagement. C'est ce qui l'empêche à la fois d'être décoratif
(PT5 : 0,6 % des occurrences) et de redevenir la colonne vertébrale (PT1 : 3 853 clics).
"""
import json
import math
import pathlib
import re

# ---- le corpus, lu à la source : ce simulateur a déjà divergé du jeu une fois -----------
_src = (pathlib.Path(__file__).parent.parent / 'src' / 'corpus.js').read_text(encoding='utf-8')
_corpus = json.loads(re.search(r'const CORPUS=(\[.*?\]);\n', _src, re.S).group(1))
_ordre = json.loads(re.search(r'const ORDRE = (\[.*?\]);', _src, re.S).group(1))
_jetons = {tb['t']: sum(1 for l in tb['l'] for tk in l.split(' ') if tk != '·') for tb in _corpus}
# ORDRE, et non l'ordre du fichier : les tablettes sortent de terre dans cet ordre-là, et
# les deux divergent dès la cinquième. C'est lui qui décide du gisement ouvert à un instant.
TOKENS = [_jetons[n] for n in _ordre]

# ---- lexique : (id, branche, coût en Certitude) ---------------------------
GL = [('an','nombre',2), ('anna','nombre',5), ('hem','nombre',11), ('sela','nombre',18),
      ('meku','nombre',33),
      ('tem','matiere',3), ('ur','matiere',6), ('tab','matiere',14), ('kish','matiere',22),
      ('gan','matiere',40),
      ('im','parole',8), ('sar','parole',27), ('kal','parole',48)]

# ---- constantes économiques ----------------------------------------------
P = dict(
    cop_b=15,   cop_r=1.12, cop_p=1.0,                 # Copiste          : +1 occ./s
    tab_b=100,  tab_r=1.15, tab_c=1.0,  tab_p=0.6,     # Table de fréq.   : -1 occ./s -> +0,6 hyp./s
    con_b=450,  con_r=1.18, con_c=0.5,  con_p=0.0039,  # Concordance      : -0,5 hyp./s -> +0,0039 cert./s
    ate_b=1800, ate_r=1.15, ate_p=25.0,                # Atelier de copie : +25 occ./s
    rec_o=12, rec_h=3, rec_r=1.18,                     # Recouper : coût de base et croissance
    rec_div=5, rec_max=3,                              # Recouper : gain = min(rec_max, 1 + lexique//rec_div)
    hyp_c=3,                                           # Formuler : 3 occ. -> 1 hyp.
    click_share=1.20,                                  # Relevé neuf = (1 + K x débit) x mult.
    click_floor=1.0,                                   # Relevé sur gisement épuisé : le plancher seul
    gis_div=10,                                        # Gisement d'une tablette = jetons / gis_div
    rev_base=4,                                        # tablettes dégagées au départ
)

BR = {}
for g in GL:
    BR.setdefault(g[1], []).append(g)


def run(P, cpm=15, cap_min=600):
    """cpm = clics manuels par minute. Retourne (durée_min, jalons, bâtiments, stats)."""
    O = H = C = 0.0
    b = {'cop': 0, 'tab': 0, 'con': 0, 'ate': 0}
    gl, rec, t, dt = set(), 0, 0.0, 0.1
    marks, c_rec, c_con = [], 0.0, 0.0
    o_main = o_pass = gis_use = 0.0
    has = lambda x: x in gl
    GIS = [-(-n // P['gis_div']) for n in TOKENS]   # gisement : jetons / gis_div
    reste = list(GIS)                               # ce qu'il reste à relever, par tablette
    prix = [0.0] * len(GIS)                         # tarif verrouillé au dégagement
    # tablettes dégagées : 4 au départ, les 30 au dernier glyphe (cf. revCount() dans rendu.js)
    nrev = lambda: min(len(GIS), P['rev_base']
                       + round(len(gl) * (len(GIS) - P['rev_base']) / len(GL)))
    ouvert = 0
    mcop   = lambda: (1.3 if has('tem')  else 1) * (2 if has('kal') else 1)
    mtab   = lambda: (1.3 if has('kish') else 1) * (2 if has('kal') else 1)
    mcon   = lambda: (1.5 if has('sar')  else 1) * (2 if has('kal') else 1)
    mclick = lambda: (1.25 if has('anna') else 1) * (1.5 if has('tab') else 1) * (2 if has('kal') else 1)
    obrut  = lambda: (b['cop'] * P['cop_p'] + b['ate'] * P['ate_p']) * mcop()
    # Un relevé ne vaut plein tarif que sur du terrain neuf. Le gisement épuisé rend le
    # plancher, jamais zéro : à t=0 le débit est nul, les deux se valent, et l'ouverture
    # reste possible à la main comme aujourd'hui.
    tarif  = lambda: (1 + P['click_share'] * obrut()) * mclick()
    plancher = lambda: P['click_floor'] * mclick()
    cost   = lambda k: math.ceil(P[k + '_b'] * P[k + '_r'] ** b[k])

    def reccost():
        m = (P['rec_r'] ** rec) * (0.75 if has('gan') else 1)
        return math.ceil(P['rec_o'] * m), math.ceil(P['rec_h'] * m)

    recgain = lambda: min(P['rec_max'], 1 + len(gl) // P['rec_div'])

    def avail():                       # premier glyphe non acquis de chaque branche
        out = []
        for lst in BR.values():
            for g in lst:
                if g[0] not in gl:
                    out.append(g); break
        return out

    while len(gl) < len(GL) and t < 60 * cap_min:
        t += dt
        o_pass += obrut() * dt
        # une tablette qui sort de terre voit son gisement tarifé au débit du moment
        while ouvert < nrev():
            prix[ouvert] = tarif(); ouvert += 1
        # le joueur le plus gourmand vide d'abord la tablette la mieux payée
        nc = (cpm / 60.0) * dt
        gain = 0.0
        while nc > 1e-12:
            i = max((k for k in range(ouvert) if reste[k] > 0),
                    key=lambda k: prix[k], default=None)
            if i is None: break
            n = min(nc, reste[i])
            reste[i] -= n; gis_use += n; gain += prix[i] * n; nc -= n
        gain += plancher() * nc                     # gisement épuisé : le plancher, jamais zéro
        o_main += gain
        O += obrut() * dt + gain
        w = b['tab'] * P['tab_c'] * dt
        if w > 0:
            c = min(w, O); fr = c / w; O -= c
            H += b['tab'] * P['tab_p'] * mtab() * fr * dt
        w = b['con'] * P['con_c'] * dt
        if w > 0:
            c = min(w, H); fr = c / w; H -= c
            g = b['con'] * P['con_p'] * mcon() * fr * dt
            C += g; c_con += g

        # achats d'instruments : garder la chaîne alimentée avant de l'allonger
        for _ in range(60):
            netO = obrut() - b['tab'] * P['tab_c']
            netH = b['tab'] * P['tab_p'] * mtab() - b['con'] * P['con_c']
            k = None
            if netH >= P['con_c'] and O >= cost('con'):                      k = 'con'
            elif netO >= P['tab_c'] and O >= cost('tab') and b['cop'] > 0:   k = 'tab'
            elif O >= cost('ate') and (b['con'] > 0 or O >= P['ate_b'] * 1.5): k = 'ate'
            elif O >= cost('cop'):                                           k = 'cop'
            if k is None: break
            O -= cost(k); b[k] += 1

        # recoupement manuel tant qu'il reste franchement rentable
        rc = reccost()
        while O >= rc[0] * 4 and H >= rc[1] * 4 and rc[0] < O * 0.25:
            O -= rc[0]; H -= rc[1]
            C += recgain(); c_rec += recgain(); rec += 1
            rc = reccost()

        # achat de glyphes : le moins cher disponible d'abord
        while True:
            a = [g for g in avail() if C >= g[2]]
            if not a: break
            a.sort(key=lambda g: g[2]); g = a[0]
            C -= g[2]; gl.add(g[0]); marks.append((g[0], t / 60))

    return t / 60, marks, b, dict(rec=rec, c_rec=c_rec, c_con=c_con,
                                  obrut=obrut(), cs=b['con'] * P['con_p'] * mcon(),
                                  o_main=o_main, o_pass=o_pass, gis_use=gis_use,
                                  gis_tot=sum(-(-n // P['gis_div']) for n in TOKENS))


if __name__ == '__main__':
    for cpm in (5, 15, 40):
        tt, marks, b, s = run(P, cpm)
        gaps = [marks[i][1] - marks[i - 1][1] for i in range(1, len(marks))] or [0]
        share = 100 * s['c_rec'] / max(1e-9, s['c_rec'] + s['c_con'])
        main = 100 * s['o_main'] / max(1e-9, s['o_main'] + s['o_pass'])
        print(f"--- {cpm:>2} clics/min : {tt:5.1f} min · écart max {max(gaps):4.1f} min · "
              f"{s['rec']:>3} recoup. ({share:.0f} % de la Certitude) · "
              f"{s['obrut']:.0f} occ./s · {s['cs']:.3f} cert./s")
        print(f"     relevés {s['gis_use']:.0f}/{s['gis_tot']} du gisement · "
              f"la main fournit {main:.1f} % des occurrences")
        print("     " + ", ".join(f"{n} {m:.0f}′" for n, m in marks))
        print(f"     bâtiments {b}")
