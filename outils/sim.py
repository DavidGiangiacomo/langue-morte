#!/usr/bin/env python3
"""
Simulateur d'économie — « La langue morte », actes I à III.
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
import sys


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
      ('meku','nombre',33), ('mille','nombre',110),
      ('tem','matiere',3), ('ur','matiere',6), ('tab','matiere',14), ('kish','matiere',22),
      ('gan','matiere',40),
      ('im','parole',8), ('sar','parole',27), ('kal','parole',48),
      ('nur','temps',60), ('pat','temps',130), ('zur','temps',190), ('nurnur','temps',260),
      ('esh','temps',360), ('nurhal','temps',500)]

# ---- constantes économiques ----------------------------------------------
P = dict(
    cop_b=15,   cop_r=1.12, cop_p=1.0,                 # Copiste          : +1 occ./s
    tab_b=100,  tab_r=1.15, tab_c=1.0,  tab_p=0.6,     # Table de fréq.   : -1 occ./s -> +0,6 hyp./s
    con_b=450,  con_r=1.18, con_c=0.5,  con_p=0.0039,  # Concordance      : -0,5 hyp./s -> +0,0039 cert./s
    ate_b=1800, ate_r=1.15, ate_p=25.0,                # Atelier de copie : +25 occ./s
    gram_b=12000, gram_r=1.20, gram_c=3.0,             # Grammaire (acte III) : -3 hyp./s ...
    gram_p=0.0012, gram_g=1.16,                        # ... -> gram_p x gram_g^lexique cert./s
    rec_o=12, rec_h=3, rec_r=1.18,                     # Recouper : coût de base et croissance
    rec_div=5, rec_max=3,                              # Recouper : gain = min(rec_max, 1 + lexique//rec_div)
    hyp_c=3,                                           # Formuler : 3 occ. -> 1 hyp.
    duree_att=45,                                      # durée attendue, pour l'essai du thésauriseur
    click_share=1.20,                                  # Relevé neuf = (1 + K x débit) x mult.
    click_floor=1.0,                                   # Relevé sur gisement épuisé : le plancher seul
    gis_div=10,                                        # Gisement d'une tablette = jetons / gis_div
    rev_base=4,                                        # tablettes dégagées au départ
    ate_socle=30,                                      # Copistes avant d'épargner pour l'Atelier (PT9 : 22 au premier, 35 à la 14e min)
)

BR = {}
for g in GL:
    BR.setdefault(g[1], []).append(g)


def run(P, cpm=15, cap_min=600, garde=0.0):
    """cpm = clics manuels par minute. `garde` = fraction de la partie pendant laquelle
    le joueur s'interdit de relever, pour tarifer ses tablettes au débit maximal —
    c'est le pire cas contre lequel il faut se prémunir. Retourne (durée, jalons, ...)."""
    O = H = C = 0.0
    b = {'cop': 0, 'tab': 0, 'con': 0, 'ate': 0, 'gram': 0}
    gl, rec, t, dt = set(), 0, 0.0, 0.1
    marks, c_rec, c_con = [], 0.0, 0.0
    # I6 par tranche de dix minutes : PT7 s'est posé à 31,2 % sur la partie entière en
    # cachant un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes.
    # La moyenne d'une partie ne dit rien de la partie ; les tranches, si.
    tr_rec, tr_ins = [0.0]*12, [0.0]*12
    o_main = o_pass = gis_use = 0.0
    has = lambda x: x in gl
    GIS = [-(-n // P['gis_div']) for n in TOKENS]   # gisement : jetons / gis_div
    reste = list(GIS)                               # ce qu'il reste à relever, par tablette
    prix = [None] * len(GIS)                        # tarif figé au premier relevé
    # tablettes dégagées : 4 au départ, les 30 au dernier glyphe (cf. revCount() dans rendu.js)
    nrev = lambda: min(len(GIS), P['rev_base']
                       + round(len(gl) * (len(GIS) - P['rev_base']) / len(GL)))
    ouvert = 0
    mcop   = lambda: (1.3 if has('tem')  else 1) * (2 if has('kal') else 1)
    mate   = lambda: mcop() * (1.3 if has('mille') else 1) * (1.5 if has('nurhal') else 1)
    mtab   = lambda: (1.3 if has('kish') else 1) * (2 if has('kal') else 1)
    mcon   = lambda: (1.5 if has('sar')  else 1) * (2 if has('kal') else 1)
    mgram  = lambda: (1.5 if has('nurnur') else 1) * (2 if has('kal') else 1)
    gramp  = lambda: P['gram_p'] * (P['gram_g'] ** len(gl)) * mgram()
    mclick = lambda: (1.25 if has('anna') else 1) * (1.5 if has('tab') else 1) * (2 if has('kal') else 1)
    obrut  = lambda: b['cop'] * P['cop_p'] * mcop() + b['ate'] * P['ate_p'] * mate()
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
        ouvert = nrev()
        # Le joueur travaille les tablettes dans l'ordre où elles sortent de terre, et le
        # tarif de chacune se fige au premier relevé qu'il y fait. `garde` retarde tout :
        # les tablettes sont alors tarifées au débit de la fin.
        nc = (cpm / 60.0) * dt
        neuves_ok = t >= garde * 60 * P['duree_att']
        gain = 0.0
        while nc > 1e-12:
            # d'abord ce qui est déjà tarifé ; une tablette neuve ne s'ouvre qu'ensuite —
            # et le thésauriseur s'en abstient jusqu'à `garde`, pour les tarifer au maximum
            i = next((k for k in range(ouvert) if reste[k] > 0 and prix[k] is not None), None)
            if i is None and neuves_ok:
                i = next((k for k in range(ouvert) if reste[k] > 0), None)
                if i is not None: prix[i] = tarif()  # première visite : on tarife
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
            C += g; c_con += g; tr_ins[min(11, int(t // 600))] += g
        w = b['gram'] * P['gram_c'] * dt
        if w > 0:
            c = min(w, H); fr = c / w; H -= c
            g = b['gram'] * gramp() * fr * dt
            C += g; c_con += g; tr_ins[min(11, int(t // 600))] += g

        # achats d'instruments : garder la chaîne alimentée avant de l'allonger
        for _ in range(60):
            netO = obrut() - b['tab'] * P['tab_c']
            netH = b['tab'] * P['tab_p'] * mtab() - b['con'] * P['con_c'] - b['gram'] * P['gram_c']
            k = None
            # La Grammaire passe avant la Concordance dès qu'elle est ouverte : elle rend
            # plus par occurrence dépensée, et surtout elle boit les hypothèses que la
            # chaîne laissait s'entasser.
            # Producteur : celui qui rend le plus par occurrence dépensée — et quand c'est
            # l'Atelier, on ÉPARGNE pour lui au lieu d'acheter ce qui est payable tout de
            # suite. L'acheteur d'avant prenait ce qui passait sous sa main : premier Atelier
            # à la 24e minute, 84 Copistes en fin de partie, et vingt pour cent de trop sur
            # la durée simulée, deux playtests de suite (PT8, PT9). Le joueur réel prend son
            # premier Atelier à la dixième minute, sur un socle d'une vingtaine de Copistes,
            # et n'achète plus un Copiste passé la 33e.
            eff_cop = cost('cop') / (P['cop_p'] * mcop())
            eff_ate = cost('ate') / (P['ate_p'] * mate())
            prod = 'ate' if b['cop'] >= P['ate_socle'] and eff_ate <= eff_cop else 'cop'
            epargne = prod == 'ate' and O < cost('ate')
            if has('nur') and netH >= P['gram_c'] and O >= cost('gram'):     k = 'gram'
            elif epargne:                                                    break
            elif netH >= P['con_c'] and O >= cost('con'):                    k = 'con'
            elif netO >= P['tab_c'] and O >= cost('tab') and b['cop'] > 0:   k = 'tab'
            elif O >= cost(prod):                                            k = prod
            if k is None: break
            O -= cost(k); b[k] += 1

        # recoupement manuel tant qu'il reste franchement rentable
        rc = reccost()
        while O >= rc[0] * 4 and H >= rc[1] * 4 and rc[0] < O * 0.25:
            O -= rc[0]; H -= rc[1]
            C += recgain(); c_rec += recgain(); rec += 1
            tr_rec[min(11, int(t // 600))] += recgain()
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
                                  tr_rec=tr_rec, tr_ins=tr_ins,
                                  gis_tot=sum(-(-n // P['gis_div']) for n in TOKENS))


if __name__ == '__main__':
    # force l'encodage des sorties pour ne pas dépendre de la machine (windows utilise cp1252 par défaut)
    # certains caractères comme U+2032 qui est utilisé ici vont faire planter l'exécution en voulant faire l'affichage
    sys.stdout.reconfigure(encoding='utf-8')
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
        tr = []
        for i in range(12):
            r, ins = s['tr_rec'][i], s['tr_ins'][i]
            if r + ins < 0.5: continue
            tr.append(f"{i*10}-{i*10+10}′ {100*r/(r+ins):.0f} %")
        print("     I6 par tranche : " + " · ".join(tr))
