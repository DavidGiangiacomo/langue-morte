#!/usr/bin/env python3
"""
Simulateur d'économie — « La langue morte », actes I à V.
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
# Le même compte, indexé par NUMÉRO de tablette : `depouiller.py` lit un journal
# d'actions où les relevés portent le numéro, pas le rang de sortie de terre.
JETONS = dict(_jetons)

# ---- lexique : (id, branche, coût en Certitude) ---------------------------
# Les prix de la Fin, dans l'ordre de sa chaîne. Tous au plafond, et c'est une mesure : à
# l'acte V le prix ne porte plus le rythme — les questions nées du surplus et le gel de la
# Grammaire le portent (VOIX-3). Au plafond, ⟨semence⟩ tombe après ⟨nous-fûmes⟩ et l'acte V
# vient entier après l'acte IV ; à 6 000, il se glissait entre ⟨toi-qui⟩ et ⟨moi-absent⟩ pour
# un dixième de minute de moyenne. Rampes de 4 000 ou 7 000 à 9 999 : les signes sans question
# tombent à 2,2-2,7 min, sous I4 avec Élèves.
FIN_PRIX = (9999,) * 7
GL = [('an','nombre',2), ('anna','nombre',5), ('hem','nombre',11), ('sela','nombre',18),
      ('meku','nombre',33), ('mille','nombre',110),
      ('tem','matiere',3), ('ur','matiere',6), ('tab','matiere',14), ('kish','matiere',22),
      ('gan','matiere',40),
      ('im','parole',8), ('sar','parole',27), ('kal','parole',48),
      ('shen','parole',300), ('imme','parole',600), ('tabsar','parole',900),
      # `les-lecteurs` ferme l'acte III, et il est le seul glyphe de l'arbre sans effet
      # chiffré par mesure et non par oubli : dernier achat, il est payé à la seconde où
      # la partie se termine. Concordance, table, grammaire, atelier ou rien — cinq
      # variantes, trois cadences, la même durée à la décimale près. Ce simulateur est
      # l'outil qui le montre, et c'est tout ce qu'il peut en dire.
      ('shenu','parole',1200),
      ('nur','temps',60), ('pat','temps',130), ('zur','temps',190), ('nurnur','temps',260),
      ('esh','temps',360), ('nurhal','temps',500),
      # Modalité (acte III). Seul `dun` (il-faut) a un effet chiffré, +50 % à l'atelier ; les
      # trois autres ne rendent que de la lecture — 816 attestations, un signe du corpus sur
      # cinq. Donner à `si` le troisième ×1,5 de la Grammaire RACCOURCIT
      # l'acte au lieu de l'allonger — mesuré 82,5 min contre 87,0, soit quatre signes de plus
      # pour une minute de jeu. Dans une économie exponentielle, un multiplicateur sur
      # l'instrument qui porte la Certitude paie plus que ce qu'il coûte.
      # `peut-être` (MOD-2) s'intercale entre `si` et `il-faut`, et son prix est une mesure :
      # à 900 ou 1 100 C il tombe deux minutes avant la fin du prototype et le doute n'a pas
      # le temps de servir ; à 450 il laisse quatorze minutes, soit trois ou quatre révisions
      # au coût croissant. Aucun multiplicateur, comme le reste de la branche.
      # `faux` (MOD-3) s'intercale entre `il-faut` et `sinon`, et son prix est une mesure lui
      # aussi : au bout de la branche il tombe deux minutes avant la fin, à 700 il en laisse
      # six — de quoi lire les lignes allumées et payer deux ou trois révisions. À ce rang,
      # les neuf signes ambigus sont tous tranchés avant lui.
      ('la','modalite',150), ('en','modalite',320), ('mik','modalite',450),
      ('dun','modalite',550), ('lash','modalite',700), ('enla','modalite',800),
      # Personne (acte IV, VOIX-1). Aucun multiplicateur : comme la Modalité, la branche
      # donne de la lecture — soixante-six attestations, dont quarante et une pour ⟨nous⟩.
      # Les prix sont une mesure, et ils butent sur un plafond : l'économie est exponentielle
      # (la Grammaire croît en 1,16^arbre), et la règle I1 interdit d'afficher plus de quatre
      # chiffres de Certitude. Au pas de la branche d'avant (1 300 à 3 000 C), les six signes
      # tombent toutes les 1,5 min ; il faut aller jusqu'à 9 500 pour qu'ils tombent toutes
      # les 2 à 4 min. Ce que ça laisse à l'acte V : rien sous le plafond — c'est ECO-3.
      ('nash','personne',1800), ('mu','personne',2800), ('ta','personne',4000),
      ('taru','personne',5500), ('mula','personne',7300), ('nashal','personne',9500),
      # La Fin (acte V, GRAINE-1). Sept signes, aucun multiplicateur — la Grammaire gèle à
      # leur entrée (VOIX-3), et ils donnent de la lecture. Trois ne s'offrent qu'une fois
      # qu'une réponse les a portés (`REP`), et le dernier ne s'offre qu'en dernier
      # (`DERNIER`) ; la grille, elle, les donne dès qu'on en a les parties. L'ordre alterne
      # les mots ouverts par une question et ceux qui ne demandent que leur prix : deux
      # questions de suite feraient deux longues attentes, deux prix de suite une rafale.
      ('mesh','fin',FIN_PRIX[0]), ('hal','fin',FIN_PRIX[1]), ('halan','fin',FIN_PRIX[2]),
      ('ke','fin',FIN_PRIX[3]), ('halnash','fin',FIN_PRIX[4]), ('meshke','fin',FIN_PRIX[5]),
      ('shenke','fin',FIN_PRIX[6]),
      # Composés secrets : offerts par aucune branche, ils ne s'obtiennent qu'à la grille de
      # composition. Ils comptent dans ce que le joueur SAIT, jamais dans ce que l'arbre a
      # rendu — d'où `ARBRE`, qui est le compte dont dépendent le dégagement des tablettes, la
      # Grammaire et la fin de partie. Confondre les deux ferait avancer le jeu en composant.
      ('urtem','matiere',60), ('lan','nombre',120)]
SECRETS = {'urtem', 'lan'}
# Les mots qu'une réponse ouvre (règle 24) et le dernier signe, offert quand tous les autres
# sont lus. Suivent `rep` et `dernier` dans lexique.js.
REP = {'hal', 'ke', 'meshke'}
DERNIER = 'shenke'
ARBRE = [g for g in GL if g[0] not in SECRETS]
# L'acte d'une branche, pour ses franchissements. Les branches des actes I à III n'en ont pas
# besoin : la contradiction ne se solde jamais avant `peut-être`, qui est de l'acte III.
# Suit `ACTE` dans lexique.js.
ACTE = {'personne': 4, 'fin': 5}

# ---- constantes économiques ----------------------------------------------
P = dict(
    cop_b=10,   cop_r=1.12, cop_p=1.0,                 # Copiste          : +1 occ./s
    tab_b=100,  tab_r=1.15, tab_c=1.0,  tab_p=0.6,     # Table de fréq.   : -1 occ./s -> +0,6 hyp./s
    con_b=450,  con_r=1.18, con_c=0.5,  con_p=0.0039,  # Concordance      : -0,5 hyp./s -> +0,0039 cert./s
    ate_b=1800, ate_r=1.15, ate_p=25.0,                # Atelier de copie : +25 occ./s
    gram_b=12000, gram_r=1.20, gram_c=3.0,             # Grammaire (acte III) : -3 hyp./s ...
    gram_p=0.0012, gram_g=1.16,                        # ... -> gram_p x gram_g^lexique cert./s
    rec_o=12, rec_h=3, rec_r=1.30,                     # Recouper : coût de base et croissance
    rec_div=5, rec_max=3,                              # Recouper : gain = min(rec_max, 1 + lexique//rec_div)
    hyp_c=3,                                           # Formuler : 3 occ. -> 1 hyp.
    duree_att=45,                                      # durée attendue, pour l'essai du thésauriseur
    click_share=1.20,                                  # Relevé neuf = (1 + K x débit) x mult.
    click_floor=1.0,                                   # Relevé sur gisement épuisé : le plancher seul
    gis_div=10,                                        # Gisement d'une tablette = jetons / gis_div
    rev_base=4,                                        # tablettes dégagées au départ
    # Dégagement : 4 + 26 x (signes/arbre)^rev_r. Cet exposant tire les DEUX garde-fous, et
    # dans le même sens — le ralentir fait monter ce que vaut la main (tarif figé à la
    # première visite, règle 9 : une tablette sortie tard est chère) ET fait baisser la pire
    # tranche d'I6. L'accélérer refait le défaut de PT6 : tout dégager à 80 % de l'arbre
    # ramène la part manuelle de 22,9 % à 12,4 % pour deux points d'I6 gagnés. Balayé le
    # 14/09/2026 ; c'est `balayage.py` qui le trie désormais.
    rev_r=1.1,                                         # courbe du dégagement (1,0 = linéaire)
    ate_socle=30,                                      # Copistes avant d'épargner pour l'Atelier (PT9 : 22 au premier, 35 à la 14e min)
    # La contradiction (CONTR-1) : à l'ouverture du doute, si la dette dépasse le seuil, la
    # Certitude est divisée par deux jusqu'à révision. Le seuil suit `CONTR_SEUIL` dans
    # economie.js. Ce simulateur n'a pas de modèle de lecture et ne révise donc JAMAIS : il
    # mesure le pire cas, celui du joueur qui encaisse jusqu'au bout.
    contr_s=5, contr_div=2.0,
    # L'Élève (ELV-1) : il ne produit rien, il multiplie ce que rendent les cinq autres —
    # +elv_p par Élève, linéaire, contre un prix géométrique. Ouvert par la première
    # Grammaire. Et il tranche à la place du joueur (ELV-2) : `elv_e` est le taux d'erreur
    # d'un Élève seul, et n Élèves se trompent 1 - (1 - elv_e)^n fois.
    # Balayé le 12/10/2026 sur elv_p x elv_b x elv_r. Aucune des 36 combinaisons ne déplace
    # la pire tranche d'I6 (26 %, à 20-30′ : l'Élève n'existe pas encore) ni l'écart max
    # (5,2 min) ; elles ne règlent que DE COMBIEN il raccourcit et COMBIEN on en empile.
    # elv_p : 0,05 fait gagner 6,8 min à qui en prend sept ; 0,08 en fait gagner onze, et
    # sept Élèves qui lisent tout faux finissent ALORS avant le joueur qui n'en a aucun — il
    # n'y a plus d'arbitrage. 0,15 pousse la main à 46 % des occurrences.
    # elv_b : à 60 000 le premier Élève arrive après ⟨avant⟩, et ses erreurs ne pèsent plus
    # que quatre points — sous le seuil de la contradiction, donc se tromper PAIE.
    # elv_r : seul levier sur leur nombre, comme toujours (la leçon de `REC_R`).
    elv_b=20000, elv_r=1.8, elv_p=0.05, elv_e=0.15,
    # Les Questions (VOIX-3) : la Certitude s'arrête à 9 999 (I1), et à partir de ⟨toi⟩ ce
    # qui déborde remplit une question — 4 000 chacune, douze sur la partie. Suit `C_MAX`,
    # `Q_COUT` et `Q_MAX` dans economie.js. Sans effet sur le rythme des actes I à IV,
    # l'acheteur dépensant avant d'atteindre le plafond ; c'est l'acte V qu'il réglera, quand
    # ECO-2 l'aura porté ici (docs/note-questions.md).
    c_max=9999, q_cout=4000, q_max=12,
    # Le Lecteur (GRAINE-2) : il ne produit rien. Une fois acheté, il lit le corpus tout seul,
    # une tablette par minute et par Lecteur, et chaque tablette lue remplit `lec_q` de la
    # question suivante — trente tablettes, 9 000 au plus, deux questions et quart. Ouvert par
    # ⟨semence⟩, payé en occurrences, et acheté en dernier : l'acheteur n'épargne jamais pour
    # lui. Suit `LEC_V`, `LEC_Q` et l'entrée `lec` d'`INS` dans economie.js. Mesuré le
    # 19/10/2026 : il raccourcit l'acte V de 2,6 min avec Élèves et de 4,0 sans, et le pire
    # trou sans Élève passe de 7,2 à 5,8 min — ce sont les attentes de question qu'il comble.
    lec_b=500000, lec_r=2.0, lec_v=1 / 60, lec_q=300,
    # Le Corpus jumeau (VOIX-4) : une copie du corpus retrouvée, un seul exemplaire, ouvert par
    # ⟨nous⟩ et payé en occurrences. Chaque tablette de la copie a la moitié du gisement de
    # l'original, et son propre tarif, figé au premier relevé qu'on y fait ; le relevé va à
    # l'original tant qu'il en reste. Suit `JUM_F` et l'entrée `jum` d'`INS` dans economie.js.
    # Mesuré le 19/10/2026 : la part de la main remonte à 26-33 % des occurrences avec Élèves
    # (26 à 5 clics par minute, 33 à 15 et 40) et à 26 % sans, sous le plafond de 40. Un
    # gisement entier (jum_f = 1) la poussait à 43 % à 15 clics par minute.
    jum_b=300000, jum_f=0.5,
)

BR = {}
for g in ARBRE:
    BR.setdefault(g[1], []).append(g)
BRANCHE = {g[0]: g[1] for g in GL}

# ---- les recettes, lues à la source elles aussi ---------------------------
# `compose` ne peut poser un signe que si le joueur en connaît les deux parties. Le
# simulateur l'ignorait tant que les composés mesurés (grenier, scribe) se faisaient de
# signes acquis dès l'acte I ; `sinon` = si + ne-pas est dans sa propre branche, derrière
# `si`, et un simulateur qui l'oublie mesure un raccourci qui n'existe pas.
_sig = (pathlib.Path(__file__).parent.parent / 'src' / 'signes.js').read_text(encoding='utf-8')
_alias = dict(re.findall(r"(\w+):'(\w+)'", re.search(r'const ALIAS = \{(.*?)\};', _sig, re.S).group(1)))
_trace = {v: k for k, v in _alias.items()}
_ids = {g[0] for g in GL}
RECETTES = {}
for cible, a, b in re.findall(r"(\w+):\['(\w+)','(\w+)'\]", re.search(r'const COMP = \{(.*?)\};', _sig, re.S).group(1)):
    a, b = _trace.get(a, a), _trace.get(b, b)
    if {cible, a, b} <= _ids:
        RECETTES[cible] = (a, b)


# Les onze lectures fausses (docs/corpus.md §7, AMB-1). La fausse majore le BONUS du signe
# de 25 %, jamais l'instrument : +30 % devient +37,5 %, pas +62,5 %. Neuf des onze signes
# sont dans l'arbre des actes I-III, mais CINQ seulement portent un multiplicateur — tem au
# copiste et à l'atelier, dun à l'atelier, kish à la table, sar à la concordance, shen à la
# grammaire. Les quatre autres ne rendent que de la lecture : mal les lire ne paie rien, et
# ce simulateur ne mesure donc que la prime des cinq.
AMB_R = 1.25
AMBIGUS = ('tem', 'ur', 'kish', 'sar', 'shen', 'nur', 'pat', 'dun', 'la', 'mesh', 'ke')

# ---- la dette et la contradiction (AMB-3, CONTR-1) ------------------------
# Les poids se déduisent des attestations comme dans le jeu : 315 occurrences pèsent 3,
# quatre en pèsent 1. Recopier une table à la main les ferait diverger au premier signe
# ajouté.
_freq = {}
for _tb in _corpus:
    for _l in _tb['l']:
        for _tk in _l.split(' '):
            if _tk != '·' and not _tk.startswith('%'):
                _freq[_tk] = _freq.get(_tk, 0) + 1
DETTE = {g: (3 if _freq.get(g, 0) >= 250 else 2 if _freq.get(g, 0) >= 100 else 1)
         for g in AMBIGUS}


def eleve(P, n):
    """Ce que n Élèves font aux cinq instruments. Un seul endroit, pour `run()` et pour
    `depouiller.py`, comme `multis()` et pour la même raison."""
    return 1 + P['elv_p'] * n


def erreur(P, n):
    """La part des signes ambigus que n Élèves lisent faux. Zéro sans Élève : c'est alors
    le joueur qui tranche."""
    return 1 - (1 - P['elv_e']) ** n


def multis(has, mf, melv=lambda: 1.0):
    """Les cinq multiplicateurs d'instrument et celui du relevé, en un seul endroit.
    Sortis de `run()` le 15/09/2026 pour que `depouiller.py` les lise ici plutôt que
    d'en tenir une troisième copie : `economie.js` a déjà la sienne, et ce fichier
    porte en tête la trace de la fois où les deux ont divergé.
    `has(id)` dit si le signe est acquis, `mf(id, x)` rend son multiplicateur majoré de
    la prime s'il est mal lu (AMB-1). Les deux viennent de l'appelant, qui seul sait
    s'il rejoue une simulation ou un journal d'actions. `melv()` rend le multiplicateur de
    l'Élève, qui porte sur les cinq instruments et jamais sur le relevé : la main suit déjà
    le débit par son tarif (règle 9), la multiplier encore la paierait deux fois."""
    mcop = lambda: (mf('tem', 1.3) * (2 if has('kal') else 1) * (1.5 if has('imme') else 1)
                    * melv())
    return dict(
        cop=mcop,
        ate=lambda: (mcop() * (1.3 if has('mille') else 1) * (1.5 if has('nurhal') else 1)
                     * mf('dun', 1.5)),
        tab=lambda: (mf('kish', 1.3) * (2 if has('kal') else 1) * (1.5 if has('tabsar') else 1)
                     * melv()),
        con=lambda: mf('sar', 1.5) * (2 if has('kal') else 1) * melv(),
        gram=lambda: ((1.5 if has('nurnur') else 1) * (2 if has('kal') else 1) * mf('shen', 1.5)
                      * melv()),
        click=lambda: ((1.25 if has('anna') else 1) * (1.5 if has('tab') else 1)
                       * (2 if has('kal') else 1)),
    )


def run(P, cpm=15, cap_min=600, garde=0.0, compose=(), faux=(), eleves=None, eleve_lit='j',
        eleve_apres=None):
    """cpm = clics manuels par minute. `garde` = fraction de la partie pendant laquelle
    le joueur s'interdit de relever, pour tarifer ses tablettes au débit maximal —
    c'est le pire cas contre lequel il faut se prémunir. `compose` = les signes que le
    joueur pose à la grille dès qu'il peut les payer. `faux` = les signes ambigus que le
    joueur a mal lus. `eleves` = le nombre d'Élèves que le joueur s'autorise (None : autant
    que l'acheteur en veut). `eleve_lit` = ce que lisent les Élèves quand ils tranchent à sa
    place, 'j' ou 'f' : les deux extrêmes, comme pour le joueur — ce simulateur n'a pas de
    dé, et la part de chaque extrême se lit dans `elv_lus`. `eleve_apres` = le signe que le
    joueur tient à lire lui-même avant d'engager son premier Élève. Retourne (durée, jalons, ...)."""
    O = H = C = 0.0
    b = {'cop': 0, 'tab': 0, 'con': 0, 'ate': 0, 'gram': 0, 'elv': 0, 'lec': 0, 'jum': 0}
    gl, rec, t, dt = set(), 0, 0.0, 0.1
    marks, c_rec, c_con = [], 0.0, 0.0
    hyp_gl, comp_faits = {}, 0     # stock d'hypothèses à chaque jalon · compositions faites
    q = dict(n=0, f=0.0)           # questions venues, surplus vers la suivante (VOIX-3)
    tete = [0.0]                   # tablettes lues par le Lecteur, fraction comprise (GRAINE-2)

    def nourrir(x):
        """Remplit la question suivante, dès ⟨toi⟩ et jusqu'à la douzième."""
        if x > 0 and 'ta' in gl and q['n'] < P['q_max']:
            q['f'] += x
            while q['f'] >= P['q_cout'] and q['n'] < P['q_max']:
                q['f'] -= P['q_cout']; q['n'] += 1

    def gagner(c, x):
        """La Certitude gagnée, plafonnée ; le surplus remplit les questions dès ⟨toi⟩."""
        pris = min(x, max(0.0, P['c_max'] - c))
        nourrir(x - pris)
        return c + pris
    # I6 par tranche de dix minutes : PT7 s'est posé à 31,2 % sur la partie entière en
    # cachant un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes.
    # La moyenne d'une partie ne dit rien de la partie ; les tranches, si.
    tr_rec, tr_ins = [0.0]*12, [0.0]*12
    o_main = o_pass = gis_use = 0.0
    has = lambda x: x in gl
    mal_lus = set(faux)
    elv_lus = []                   # (signe, Élèves à l'achat, taux d'erreur) — ELV-2
    # Armée une seule fois, à l'ouverture du doute, et jamais levée ici faute de révision.
    contr = [False]
    etrangle = lambda: P['contr_div'] if contr[0] else 1.0
    # Le signe qu'on vient d'acquérir est-il le premier de son acte ? (déjà dans `gl`)
    franchit = lambda g: (g[1] in ACTE and not any(
        ACTE.get(x[1], 0) == ACTE[g[1]] for x in ARBRE if x[0] in gl and x[0] != g[0]))
    # Le multiplicateur d'un signe, majoré s'il est mal lu. Le joueur n'en voit rien : la
    # prime ne se lit ni au lexique ni à l'écran de choix (economie.js, `mfx`).
    mf = lambda g, x: (1 + (x - 1) * AMB_R if g in mal_lus else x) if has(g) else 1
    GIS = [-(-n // P['gis_div']) for n in TOKENS]   # gisement : jetons / gis_div
    reste = list(GIS)                               # ce qu'il reste à relever, par tablette
    prix = [None] * len(GIS)                        # tarif figé au premier relevé
    resteJ = [0] * len(GIS)                         # la copie du Corpus jumeau, vide avant lui
    prixJ = [None] * len(GIS)                       # ... et son tarif, figé à part
    # tablettes dégagées : 4 au départ, les 30 au dernier glyphe (cf. revCount() dans rendu.js)
    narbre = lambda: len(gl - SECRETS)      # ce que l'arbre a rendu, pas ce que le joueur sait
    nrev = lambda: min(len(GIS), P['rev_base'] + round(
        (len(GIS) - P['rev_base']) * (narbre() / len(ARBRE)) ** P['rev_r']))
    ouvert = 0
    # La date du premier achat, et non son débit : le mur des dix premières minutes est
    # un problème de seuil, pas de taux — I6 y vaut 100 % tant que la première
    # Concordance n'est pas posée, quelle que soit la cadence de clic.
    premier = {}
    _m = multis(has, mf, lambda: eleve(P, b['elv']))
    mcop, mate, mtab, mcon, mgram = _m['cop'], _m['ate'], _m['tab'], _m['con'], _m['gram']
    # La Grammaire cesse de croître avec les mots de la fin (VOIX-3) : elle compte l'arbre,
    # moins les branches de l'acte V. Suit `nGrammaire()` dans economie.js.
    ngram  = lambda: sum(1 for x in gl - SECRETS if ACTE.get(BRANCHE.get(x), 0) < 5)
    gramp  = lambda: P['gram_p'] * (P['gram_g'] ** ngram()) * mgram()
    mclick = _m['click']
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

    recgain = lambda: min(P['rec_max'], 1 + narbre() // P['rec_div'])

    # Les mots que les réponses ont ouverts, et les questions dépensées pour ça (règle 24).
    ouverts, q_dep = set(), [0]

    def offert(g):
        """Le lexique offre-t-il ce signe ? Un mot de `REP` attend sa réponse, le dernier
        attend tous les autres. La grille ne passe pas par ici."""
        if g[0] in REP and g[0] not in ouverts: return False
        if g[0] == DERNIER and narbre() < len(ARBRE) - 1: return False
        return True

    def avail():                       # premier glyphe non acquis de chaque branche
        out = []
        for lst in BR.values():
            for g in lst:
                if g[0] not in gl:
                    if offert(g): out.append(g)
                    break
        return out

    def questionner():
        """L'acheteur pose la question qui ouvre le mot en tête de chaîne dès qu'il en a une
        en main : il a lu les « si » du corpus. C'est le joueur le plus rapide possible, pas
        le joueur moyen — combien de temps un vrai joueur met à trouver la question est une
        affaire de playtest."""
        for lst in BR.values():
            g = next((x for x in lst if x[0] not in gl), None)
            if g and g[0] in REP and g[0] not in ouverts and q['n'] - q_dep[0] >= 1:
                ouverts.add(g[0]); q_dep[0] += 1

    while narbre() < len(ARBRE) and t < 60 * cap_min:
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
            # et le thésauriseur s'en abstient jusqu'à `garde`, pour les tarifer au maximum.
            # L'original d'abord, la copie du Corpus jumeau ensuite, chacune avec son tarif.
            for rs, px in ((reste, prix), (resteJ, prixJ)):
                i = next((k for k in range(ouvert) if rs[k] > 0 and px[k] is not None), None)
                if i is None and neuves_ok:
                    i = next((k for k in range(ouvert) if rs[k] > 0), None)
                    if i is not None: px[i] = tarif()  # première visite : on tarife
                if i is not None: break
            if i is None: break
            n = min(nc, rs[i])
            rs[i] -= n; gis_use += n; gain += px[i] * n; nc -= n
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
            g = b['con'] * P['con_p'] * mcon() * fr * dt / etrangle()
            C = gagner(C, g); c_con += g; tr_ins[min(11, int(t // 600))] += g
        w = b['gram'] * P['gram_c'] * dt
        if w > 0:
            c = min(w, H); fr = c / w; H -= c
            g = b['gram'] * gramp() * fr * dt / etrangle()
            C = gagner(C, g); c_con += g; tr_ins[min(11, int(t // 600))] += g

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
            # L'Élève passe devant tout dès qu'il rend plus, par occurrence dépensée, qu'une
            # Grammaire de plus : il multiplie la chaîne entière, elle n'en allonge qu'un bout.
            # On n'épargne pas pour lui — c'est un acheteur, pas un joueur qui a compris.
            elv_ok = (P['elv_p'] > 0 and b['gram'] > 0 and O >= cost('elv')
                      and (eleves is None or b['elv'] < eleves)
                      and (eleve_apres is None or has(eleve_apres))
                      and P['elv_p'] / eleve(P, b['elv']) / cost('elv')
                          >= 1.0 / max(1, b['gram']) / cost('gram'))
            if elv_ok:                                                       k = 'elv'
            elif has('nur') and netH >= P['gram_c'] and O >= cost('gram'):   k = 'gram'
            elif epargne:                                                    break
            elif netH >= P['con_c'] and O >= cost('con'):                    k = 'con'
            elif netO >= P['tab_c'] and O >= cost('tab') and b['cop'] > 0:   k = 'tab'
            elif O >= cost(prod):                                            k = prod
            if k is None: break
            O -= cost(k); b[k] += 1
            premier.setdefault(k, t / 60)

        # Le Corpus jumeau : un seul, dès ⟨nous⟩, quand il reste de quoi le payer.
        if 'nash' in gl and not b['jum'] and O >= P['jum_b']:
            O -= P['jum_b']; b['jum'] = 1; premier.setdefault('jum', t / 60)
            resteJ[:] = [-(-g * P['jum_f'] // 1) for g in GIS]

        # Le Lecteur : acheté après tout le reste, quand il reste de quoi ; puis il lit.
        if 'mesh' in gl and O >= cost('lec'):
            O -= cost('lec'); b['lec'] += 1
            premier.setdefault('lec', t / 60)
        if b['lec'] and tete[0] < len(TOKENS):
            avant = int(tete[0])
            tete[0] = min(len(TOKENS), tete[0] + b['lec'] * P['lec_v'] * dt)
            for _ in range(int(tete[0]) - avant):
                nourrir(P['lec_q'])

        # recoupement manuel tant qu'il reste franchement rentable
        rc = reccost()
        while O >= rc[0] * 4 and H >= rc[1] * 4 and rc[0] < O * 0.25:
            O -= rc[0]; H -= rc[1]
            C = gagner(C, recgain()); c_rec += recgain(); rec += 1
            tr_rec[min(11, int(t // 600))] += recgain()
            rc = reccost()

        # achat de glyphes : le moins cher disponible d'abord — sauf quand le joueur épargne
        # pour un signe qu'il a reconnu dans le texte et compte poser à la grille. Sans cette
        # épargne, l'acheteur n'a jamais 600 C de côté et « composer tôt » ne mesure rien.
        # ... et il ne peut épargner que pour une paire qu'il a les moyens de POSER : épargner
        # pour `sinon` avant d'avoir `si` bloquerait la branche qui le donne.
        questionner()
        vise = 'nur' in gl and any(cid not in gl and set(RECETTES.get(cid, ())) <= gl
                                   for cid in compose)
        while not vise:
            a = [g for g in avail() if C >= g[2]]
            if not a: break
            a.sort(key=lambda g: g[2]); g = a[0]
            C -= g[2]; gl.add(g[0]); marks.append((g[0], t / 60)); hyp_gl[g[0]] = H
            # Dès le premier Élève, un signe ambigu n'est plus tranché par le joueur (ELV-2).
            if g[0] in AMBIGUS and b['elv'] > 0:
                elv_lus.append((g[0], b['elv'], erreur(P, b['elv'])))
                (mal_lus.add if eleve_lit == 'f' else mal_lus.discard)(g[0])
            # `peut-être` ouvre le doute ET solde les lectures faites jusque-là — et chaque
            # franchissement d'acte les solde de nouveau, une fois le doute ouvert (règle 19).
            # Le premier signe d'une branche d'acte IV est le premier franchissement que le
            # prototype connaisse ; les lectures tranchées après `peut-être` y passent enfin.
            if g[0] == 'mik' or (has('mik') and franchit(g)):
                contr[0] = contr[0] or sum(DETTE[x] for x in mal_lus if x in gl) > P['contr_s']

        # La composition : elle ne crée ni ne consomme de flux, elle change le catalogue. Un
        # joueur qui a vu ⟨grenier⟩ dans le texte le pose dès qu'il peut ; ce qu'on mesure ici
        # est donc le RETARD que ses 90 C coûtent, la seule chose qu'un simulateur puisse en
        # dire. Qu'il le trouve seul est une question de playtest, pas de simulation.
        # Même chose pour `scribe` et `archive`, qui sont des glyphes d'arbre composables :
        # posés en avance, ils comptent dans la progression — et donc dans les jalons.
        for cid in compose:
            if 'nur' in gl and cid not in gl and set(RECETTES.get(cid, ())) <= gl:
                cible = next((g for g in GL if g[0] == cid), None)
                if cible and C >= cible[2]:
                    C -= cible[2]; gl.add(cid); comp_faits += 1
                    if cid not in SECRETS:
                        marks.append((cid, t / 60)); hyp_gl[cid] = H

    return t / 60, marks, b, dict(rec=rec, c_rec=c_rec, c_con=c_con, contr=contr[0],
                                  obrut=obrut(), cs=b['con'] * P['con_p'] * mcon(),
                                  o_main=o_main, o_pass=o_pass, gis_use=gis_use,
                                  tr_rec=tr_rec, tr_ins=tr_ins, premier=premier,
                                  hyp_gl=hyp_gl, comp=comp_faits, elv_lus=elv_lus, questions=q_dep[0],
                                  lues=int(tete[0]),
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

    # La même partie, toutes lectures fausses (AMB-1), SANS la contradiction : ce bloc mesure
    # la prime de 25 % seule — de combien se tromper paie, la promesse du design doc §8 en
    # minutes. Le joueur ne la voit nulle part ; c'est le seul endroit du projet où elle se lit.
    print("\n--- toutes lectures fausses, sans contradiction ---")
    for cpm in (5, 15, 40):
        tt, marks, b, s = run({**P, 'contr_s': 99}, cpm, faux=AMBIGUS, eleve_lit='f')
        gaps = [marks[i][1] - marks[i - 1][1] for i in range(1, len(marks))] or [0]
        main = 100 * s['o_main'] / max(1e-9, s['o_main'] + s['o_pass'])
        tr = []
        for i in range(12):
            r, ins = s['tr_rec'][i], s['tr_ins'][i]
            if r + ins < 0.5: continue
            tr.append(f"{i*10}-{i*10+10}′ {100*r/(r+ins):.0f} %")
        print(f"--- {cpm:>2} clics/min : {tt:5.1f} min · écart max {max(gaps):4.1f} min · "
              f"{s['rec']:>3} recoup. · la main fournit {main:.1f} % des occurrences")
        print("     I6 par tranche : " + " · ".join(tr))

    # Et ce que la contradiction reprend (CONTR-1). Le pire cas n'est PAS « tout faux » : la
    # prime y compense une partie de la sanction. C'est la paire réparante ⟨grain⟩+⟨maison⟩ —
    # six points de dette, deux signes de prime — qui paie le plus cher, et c'est exactement
    # ce que `docs/corpus.md` §7.3 annonçait en décidant de la laisser passer.
    print("\n--- la contradiction, pour qui ne révise jamais ---")
    for lib, fx in (('lecture parfaite', ()),
                    ('les deux incassables (lire, il-faut)', ('shen', 'dun')),
                    ('la paire réparante (grain + maison)', ('tem', 'ur')),
                    # Le doute passé à cinq points, puis ⟨il-faut⟩ mal lu le panneau ouvert :
                    # rien ne le soldait avant l'acte IV, le franchissement le solde (règle 19).
                    ('doute à 5, puis il-faut (grain, avant)', ('tem', 'pat', 'dun')),
                    ('toutes fausses', AMBIGUS)):
        # Sans Élève : ce bloc mesure ce que le JOUEUR s'inflige, et un Élève relirait
        # à sa place les quatre signes ambigus qui restent après la première Grammaire.
        d = [run(P, c, faux=fx, eleves=0)[0] for c in (5, 15, 40)]
        armee = run(P, 15, faux=fx, eleves=0)[3]['contr']
        print(f"    {lib:38} dette {sum(DETTE[g] for g in fx):>2} · "
              f"{'ARMÉE ' if armee else 'libre '} · {min(d):5.1f}-{max(d):5.1f} min")

    # L'Élève (ELV-1, ELV-2). Chaque ligne est un joueur qui s'en autorise n, lecture parfaite
    # jusque-là, et qui ne révise jamais. Deux extrêmes, parce que ce simulateur n'a pas de
    # dé : les Élèves lisent tout juste, ou tout faux. Entre les deux, le taux d'erreur à
    # chaque signe dit de quel côté la partie tombe — et la dette attendue s'arrête à
    # `peut-être`, puisque la contradiction ne se solde que là (règle 19).
    print("\n--- l'Élève : ce qu'il fait gagner, ce qu'il lit à ma place ---")
    for n in (0, 1, 2, 4, None):
        dj = [run(P, c, eleves=n)[0] for c in (5, 15, 40)]
        df = [run(P, c, eleves=n, eleve_lit='f')[0] for c in (5, 15, 40)]
        _, marks, b, s = run(P, 15, eleves=n, eleve_lit='f')
        ordre = [m[0] for m in marks]
        avant = ordre[:ordre.index('mik')]
        lus = ' · '.join(f"{g} {100 * e:.0f} %" for g, _, e in s['elv_lus'])
        esp = sum(e * DETTE[g] for g, _, e in s['elv_lus'] if g in avant)
        print(f"    {b['elv']} Élève(s) · lisent juste {min(dj):5.1f}-{max(dj):5.1f} min · "
              f"lisent faux {min(df):5.1f}-{max(df):5.1f} "
              f"{'ARMÉE' if s['contr'] else 'libre'} · dette attendue {esp:.1f}")
        if lus:
            print(f"        erreur à l'achat : {lus}")
    # Et celui qui veut trancher lui-même : il lit d'abord, il engage ensuite. Ce qu'il
    # garde de l'Élève est ce que l'attente lui laisse — c'est le prix de la lecture.
    for lib, g in (('⟨avant⟩', 'pat'), ('⟨ne-pas⟩', 'la'), ('⟨lire⟩', 'shen'), ('⟨il-faut⟩', 'dun')):
        d = [run(P, c, eleve_apres=g)[0] for c in (5, 15, 40)]
        _, _, b, s = run(P, 15, eleve_apres=g)
        print(f"    lit lui-même jusqu'à {lib:10} puis engage · {min(d):5.1f}-{max(d):5.1f} min · "
              f"{b['elv']} Élève(s), le premier à {s['premier'].get('elv', 0):.0f}′ · "
              f"{len(s['elv_lus'])} signe(s) lui échappent")
