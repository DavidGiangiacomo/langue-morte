#!/usr/bin/env python3
"""
Dépouillement d'un journal d'actions — « La langue morte ».

Usage :  python3 outils/depouiller.py traces-20260915-2030.tsv
         python3 outils/depouiller.py traces.tsv --partie 2
         python3 outils/depouiller.py            (lit l'entrée standard)

PT9 et PT10 ont été dépouillés à la main, et PT10 l'a été deux fois : la première lecture
comptait cinq échecs de composition là où le joueur avait trouvé cinq recettes justes sans
avoir de quoi les payer. Le journal ne faisait pas la différence — c'est corrigé dans
`traces.js` — mais rien n'obligeait non plus à recompter à la main ce que le fichier
contient déjà.

Ce que cet outil fait et que l'œil ne peut pas faire : il REJOUE le modèle d'économie sur la
timeline du journal. Les tarifs figés du relevé (règle 9) ne sont écrits nulle part dans le
TSV — ils dépendent du débit à l'instant de la première visite de chaque tablette — et sans
eux la part manuelle des occurrences, qui est le garde-fou le plus fragile du jeu, n'est pas
calculable. Le modèle se contrôle tout seul contre les relevés d'état : dernière section de
la sortie, et c'est elle qu'il faut lire en premier si un chiffre surprend.

Les constantes et les multiplicateurs viennent de `sim.py`, qui les lit lui-même de `src/`.
Rien n'est recopié ici : une troisième copie du modèle divergerait au premier réglage, ce
qui est déjà arrivé une fois entre le jeu et le simulateur.

Il lit aussi bien les journaux d'avant le 15/09/2026, où `reviser` n'était pas tracée et où
une composition ne disait pas son issue : ce qui peut se reconstituer l'est, et le reste est
annoncé comme manquant plutôt que compté pour zéro.
"""
import math
import pathlib
import re
import sys

import sim


P = sim.P
NGL = len(sim.ARBRE)
BRANCHE = {g[0]: g[1] for g in sim.GL}
COUT = {g[0]: g[2] for g in sim.GL}
GIS = {t: -(-n // P['gis_div']) for t, n in sim.JETONS.items()}
GIS_TOTAL = sum(GIS.values())
# Le mot juste de chaque signe, lu dans lexique.js comme le reste : pour nommer un signe dans
# le rapport sans en tenir une copie ici.
_lex = (pathlib.Path(__file__).parent.parent / 'src' / 'lexique.js').read_text(encoding='utf-8')
MOT = dict(re.findall(r"\{id:'(\w+)',\s*br:'\w+',[^}]*?mot:'([^']+)'", _lex))

# genres d'événement qui se passent DANS le corpus (règle 8 : c'est là que se joue la
# différence entre ce jeu et un incrémental habillé, donc c'est ça qu'on mesure)
CORPUS_GESTES = ('relever', 'recouper', 'concChoisir', 'tablette')

RE_GL = re.compile(r'^(\w+) \((.*?)\)( ✗)? (\d+) C(?: · doute (\d+))?(?: · élève (\d+))?$')
RE_REC = re.compile(r'^\+(\d+) cert\.(?: · (\S+))?$')
RE_INS = re.compile(r'^(\w+) n°(\d+)$')
RE_REL = re.compile(r'tablette (\d+)')
RE_COMP = re.compile(r'^(\w+) \+ (\w+)(.*)$')
RE_REV = re.compile(r'^(\w+) · (.*?) → (.*?) · (\d+) C · doute (\d+) → (\d+)$')
RE_ETAT = re.compile(r'O=(\d+) H=(-?\d+) C=(\d+) signes=(\d+) sig%=(\d+) lig%=(\d+) '
                     r'gis=(\d+)/(\d+) instr=([\d/]+)')


# Ce que les lignes « # » du journal disent de lui-même. Rempli par `lire`, lu par `main` :
# depuis le 17/09/2026 le TSV porte la variante de build qui l'a produit, et c'est la seule
# chose qui dise, trois semaines plus tard, contre quels réglages la partie a été jouée.
ENTETE = {}
RE_BUILD = re.compile(r'#\s*build\s*:\s*(.+)')


def lire(flux):
    """Rend la liste des événements (t, genre, détail), en-têtes et lignes vides ignorés."""
    ev = []
    for l in flux:
        l = l.rstrip('\n').rstrip('\r')
        if not l or l.startswith('#'):
            m = RE_BUILD.match(l) if l else None
            if m:
                ENTETE['build'] = m.group(1).strip()
            continue
        ch = l.split('\t')
        if len(ch) < 3 or ch[0] == 'temps':
            continue
        try:
            t = float(ch[1])
        except ValueError:
            continue
        ev.append((t, ch[2], ch[3] if len(ch) > 3 else ''))
    # Une question qui obtient une réponse fait sauter le corpus à la tablette qui répond
    # (`qMontrer`, VOIX-3), et le journal la date comme une navigation. C'est le jeu qui répond,
    # pas le joueur qui cherche : comptée en navigation, elle bouchait les trous sans un geste
    # dans le texte et se lisait comme « il est allé voir une tablette que le Lecteur venait de
    # lire ». Trouvé par la répétition générale du 20/10/2026. Elle suit la ligne de la question,
    # au même instant ; on la renomme ici, une fois, pour que rien en aval ne la compte.
    for i in range(1, len(ev)):
        if (ev[i][1] == 'tablette' and ev[i - 1][1] == 'questionner' and '→' in ev[i - 1][2]
                and ev[i][0] == ev[i - 1][0]):
            ev[i] = (ev[i][0], 'reponse-vue', ev[i][2])
    return ev


def parties(ev):
    """Découpe sur « reset » et « debut ». Le reset ferme la partie en cours : il est tracé
    avec l'horloge de celle qui s'arrête, pas de celle qui commence."""
    out, cur = [], []
    for e in ev:
        if e[1] == 'debut':
            if cur:
                out.append(cur)
            cur = []
            continue
        if e[1] == 'reset':
            out.append(cur)
            cur = []
            continue
        cur.append(e)
    if cur:
        out.append(cur)
    return [p for p in out if p]


def agit(p):
    """Une partie « jouée » a au moins une action. Une soirée de playtest en contient
    plusieurs qui n'ont jamais démarré — on ne les dépouille pas, on les signale."""
    return sum(1 for _, g, _ in p if g not in ('etat', 'fin', 'finjeu'))


class Rejeu:
    """Rejoue le modèle d'`economie.js` sur la timeline d'une partie."""

    def __init__(self, ev):
        self.ev = ev
        self.gl = {}                 # id -> 'j' | 'f'
        self.b = dict(cop=0, tab=0, con=0, ate=0, gram=0, elv=0, lec=0, jum=0)
        self.prix, self.rel = {}, {}
        self.prixJ = {}              # le tarif de chaque tablette de la copie (VOIX-4)
        has = lambda i: i in self.gl
        mf = lambda i, x: ((1 + (x - 1) * sim.AMB_R) if self.gl.get(i) == 'f' else x) if has(i) else 1
        # Les Élèves ne rendent rien tant que la contradiction court (ECO-3) : le rejeu des
        # occurrences doit le savoir, sans quoi le contrôle ΔO divergerait chez qui en a.
        self.armee = False
        self.m = sim.multis(has, mf, lambda: 1.0 if self.armee else sim.eleve(P, self.b['elv']))
        self.has = has
        self.nrec = 0                # recoupements faits : leur prix croît avec leur nombre

    def obrut(self):
        return self.b['cop'] * P['cop_p'] * self.m['cop']() + self.b['ate'] * P['ate_p'] * self.m['ate']()

    def releve(self, det):
        """Ce qu'un relevé a rendu, et où il est allé : ('neuf' | 'copie' | 'plancher', tablette,
        occurrences), ou (None, None, 0) pour un journal d'avant PT9, dont les relevés ne portent
        pas leur tablette. Le tarif de chaque tablette se fige à son premier relevé (règle 9),
        celui de la copie du Corpus jumeau à part (VOIX-4) — et le journal dit lequel des deux
        gisements a payé, sans quoi rien ne le rejoue. Un seul endroit pour `jouer` et pour
        `controle` : le contrôle vérifie ainsi le tarif lui-même, c'est-à-dire la main."""
        m = RE_REL.search(det)
        if not m:
            return None, None, 0.0
        tb = int(m.group(1))
        tarif = lambda: (1 + P['click_share'] * self.obrut()) * self.m['click']()
        if det.endswith('· copie'):
            if tb not in self.prixJ:
                self.prixJ[tb] = tarif()
            return 'copie', tb, self.prixJ[tb]
        if self.rel.get(tb, 0) < GIS.get(tb, 0):
            if tb not in self.prix:
                self.prix[tb] = tarif()
            self.rel[tb] = self.rel.get(tb, 0) + 1
            return 'neuf', tb, self.prix[tb]
        return 'plancher', tb, P['click_floor'] * self.m['click']()

    def cout_ins(self, k, n):
        """Ce qu'a coûté le n-ième instrument `k` : `insCost()` au niveau d'avant. Le Corpus
        jumeau n'a pas de croissance : il n'y en a qu'un."""
        return math.ceil(P[k + '_b'] * P.get(k + '_r', 1) ** (n - 1))

    def cout_rec(self):
        """Ce que coûte en occurrences le prochain recoupement (`recCost()`)."""
        return math.ceil(P['rec_o'] * (P['rec_r'] ** self.nrec) * (0.75 if self.has('gan') else 1))

    def jouer(self):
        s = dict(o_auto=0.0, o_main=0.0, o_nuit=0.0, cert_main=0.0, cert_couts=0.0,
                 relev=0, vides=0, sans_tb=0, formuler=0, copie=0, sauts=0,
                 recs=[], comps=[], concs=[], navs=[], revs=[], achats=[], etats=[],
                 couts_t=[], main_t=[], contrs=[], dette_fin=0,
                 finjeu=None, fin=None, gis_fichier=None, eleve={}, toi=None, questions=[],
                 fins=[], interrompu=None, relu=None, zeros=None,
                 reprises=[], copie_tb={}, elv_achats=[], lec=[], lues=[])
        prev_t = self.ev[0][0]
        for t, genre, det in self.ev:
            # La production s'arrête avec la partie (`S_.done`), et le journal continue : la
            # fenêtre de lecture, l'effacement, la relecture se datent à l'horloge. Les compter
            # en production faisait monter les instruments de 3 % dans la répétition générale du
            # 20/10/2026 — quatre-vingt-seize secondes de fin —, et de vingt minutes de
            # production chez qui s'attarde dans la relecture : la main en paraissait d'autant
            # plus petite.
            if s['finjeu'] is None:
                s['o_auto'] += self.obrut() * max(0.0, t - prev_t)
            prev_t = t

            if genre == 'relever':
                ou, tb, val = self.releve(det)
                if ou is None:
                    # journaux d'avant PT9 : le relevé ne portait pas sa tablette, donc
                    # ni le gisement ni le tarif figé ne se reconstituent
                    s['sans_tb'] += 1
                    continue
                s['o_main'] += val
                if ou == 'plancher':
                    s['vides'] += 1
                else:
                    s['relev'] += 1
                if ou == 'copie':
                    s['copie'] += 1
                    s['copie_tb'][tb] = s['copie_tb'].get(tb, 0) + 1

            elif genre == 'formuler':
                s['formuler'] += 1

            elif genre == 'acheterIns':
                m = RE_INS.match(det)
                if m:
                    self.b[m.group(1)] = int(m.group(2))
                    # Le premier Élève et le premier Lecteur se datent : le protocole de PT11
                    # demande quand, et avant ou après quels signes.
                    if m.group(1) in ('elv', 'lec'):
                        s['elv_achats' if m.group(1) == 'elv' else 'lec'].append((t, int(m.group(2))))

            # Une coupure entre deux séances (PT11 se joue en deux fois au plus) : avant ⟨nuit⟩
            # rien d'autre ne la marque, et le chrono, qui est du temps de jeu, l'efface.
            elif genre == 'reprise':
                s['reprises'].append((t, det))

            # Les tablettes que le Lecteur a fini de lire (GRAINE-2), et à quelle minute.
            elif genre == 'lireCorpus':
                s['lues'].append((t, [int(x) for x in re.findall(r'\d+', det.split(' ·')[0])]))

            elif genre == 'acheterGl':
                m = RE_GL.match(det)
                if not m:
                    continue
                gid, mot, fx, cout, doute, elv = m.groups()
                self.gl[gid] = 'f' if fx else 'j'
                s['cert_couts'] += float(cout)
                s['couts_t'].append((t, float(cout)))
                s['achats'].append((t, gid, mot, bool(fx), int(cout),
                                    int(doute) if doute else None))
                # Lu par un Élève et non par le joueur (ELV-2) : tenu à part de `achats`,
                # dont six lecteurs déballent déjà les six champs.
                if elv:
                    s['eleve'][gid] = int(elv)
                # Chaque fois qu'elle s'arme, et non la dernière seulement : elle se re-solde à
                # chaque franchissement d'acte (règle 19), et la répétition générale l'a armée à
                # ⟨peut-être⟩ puis à l'entrée de l'acte V — le rapport n'en montrait que la
                # seconde, et taisait la révision qui avait levé la première.
                if self.solder(gid):
                    s['contrs'].append([t, None])

            elif genre == 'recouper':
                m = RE_REC.match(det)
                if m:
                    s['cert_main'] += float(m.group(1))
                    s['recs'].append((t, float(m.group(1)), m.group(2) or '?'))
                    s['main_t'].append((t, float(m.group(1))))

            elif genre == 'reviser':
                m = RE_REV.match(det)
                if m:
                    gid, avant, apres, cout, d0, d1 = m.groups()
                    self.gl[gid] = 'f' if '✗' in apres else 'j'
                    s['cert_couts'] += float(cout)
                    s['couts_t'].append((t, float(cout)))
                    s['revs'].append((t, gid, avant, apres, int(cout), int(d0), int(d1)))
                    if self.lever():
                        s['contrs'][-1][1] = t

            elif genre == 'composer':
                s['comps'].append((t, det, self.issue(det)))

            elif genre == 'concChoisir':
                s['concs'].append((t, det))

            # Le repli « à toi » (VOIX-2) : ouvert par l'achat de ⟨toi⟩, refermé par le joueur.
            # Sa durée est la question du playtest — relit-on ce qui s'adressait à soi ?
            elif genre == 'adresser':
                s['toi'] = [t, None, det]
            elif genre == 'concFermer':
                if det == '@toi' and s['toi'] and s['toi'][1] is None:
                    s['toi'][1] = t

            # Les Questions (VOIX-3) : la condition posée, et si le texte a répondu. Ce qui se
            # demande et à quelle minute dit si le joueur lit les « si » du corpus ou tâtonne.
            elif genre == 'questionner':
                s['questions'].append((t, det))

            elif genre == 'tablette':
                s['navs'].append((t, det))
            elif genre == 'reponse-vue':
                s['sauts'] += 1

            # I2 (VOIX-5) : la première fois qu'un nombre du joueur s'écrit avec leurs zéros,
            # et lequel. Une seule ligne par partie ; ce n'est pas une action.
            elif genre == 'zeros':
                s['zeros'] = (t, det)

            elif genre == 'veillee':
                # La ligne porte le TOTAL d'occurrences au retour, pas le gain. On prend
                # donc le dernier solde connu comme point de départ : c'est approximatif,
                # et c'est dit dans la sortie.
                try:
                    tot = float(re.search(r'(\d+)', det).group(1))
                    base = s['etats'][-1][1] if s['etats'] else 0.0
                    s['o_nuit'] += max(0.0, tot - base)
                except (AttributeError, ValueError):
                    pass

            elif genre == 'finjeu':
                s['finjeu'] = t
            elif genre == 'fin':
                s['fin'] = t
            # Les deux fins (FIN-1, FIN-2) : chaque ouverture de la fenêtre, et le signe laissé
            # quand on interrompt. Achever n'a pas de ligne à lui — c'est l'achat du dernier
            # signe, suivi de « finjeu ».
            elif genre == 'finsOuvrir':
                s['fins'].append(t)
            elif genre == 'interrompre':
                s['interrompu'] = (t, det)
            elif genre == 'relire':
                s['relu'] = (t, det)

            elif genre == 'etat':
                m = RE_ETAT.search(det)
                if m:
                    s['etats'].append((t, float(m.group(1)), float(m.group(3)),
                                       int(m.group(4)), int(m.group(5)), int(m.group(6))))
                    s['gis_fichier'] = int(m.group(8))

        s['o_auto'] += s['o_nuit']
        s['dette_fin'] = self.dette()
        return s

    def dette(self):
        return sum(sim.DETTE[g] for g in sim.AMBIGUS if self.gl.get(g) == 'f')

    def solder(self, gid):
        """La contradiction se solde à l'ouverture du doute, puis au premier signe de chaque
        acte une fois le doute ouvert (règle 19, VOIX-1) — et nulle part ailleurs. On la rejoue
        aux mêmes endroits que le jeu ; rend vrai si elle vient de s'armer."""
        franchi = 'mik' in self.gl and BRANCHE.get(gid) in sim.ACTE and not any(
            x != gid and BRANCHE.get(x) in sim.ACTE
            and sim.ACTE[BRANCHE[x]] == sim.ACTE[BRANCHE[gid]] for x in self.gl)
        if (gid == 'mik' or franchi) and not self.armee and self.dette() > P['contr_s']:
            self.armee = True
            return True
        return False

    def lever(self):
        """Levée par une révision qui fait repasser la dette sous le seuil."""
        if self.armee and self.dette() <= P['contr_s']:
            self.armee = False
            return True
        return False

    def issue(self, det):
        """Les trois issues d'une tentative de composition. Le journal les dit depuis le
        15/09/2026 ; avant, il ne marquait que la réussite, et une paire juste qu'on ne
        pouvait pas payer se lisait comme un coup de sonde au hasard. Ce qui se
        reconstitue, c'est l'existence de la recette — donc la distinction qui manquait."""
        m = RE_COMP.match(det)
        if not m:
            return ('?', '', False)
        a, b, reste = m.groups()
        cible = next((c for c, (x, y) in sim.RECETTES.items() if (x, y) == (a, b)), None)
        if '✗ carnet' in reste:
            return ('carnet', '', False)
        if 'impayable' in reste:
            return ('impayable', cible or '', False)
        if '✓' in reste:
            return ('acquis', cible or '', False)
        # journal d'avant le 15/09/2026 : on reconstitue
        return ('impayable' if cible else 'carnet', cible or '', True)


def mmss(t):
    return '%d:%02d' % (t // 60, t % 60)


def controle(ev):
    """ΔO prédit contre ΔO observé, sur chaque intervalle entre deux relevés d'état. Le solde
    d'occurrences se tient comme un grand livre : ce que les instruments produisent, moins ce
    que la Table boit, plus ce que chaque relevé a rendu, moins le prix de chaque instrument,
    de chaque recoupement et de chaque hypothèse formulée. Si l'écart médian n'est pas nul, le
    modèle a divergé du jeu et TOUS les chiffres de la section « la main » sont à jeter —
    c'est le seul contrôle que ce fichier ait sur lui-même.

    Il ne mesurait jusqu'au 20/10/2026 que les intervalles « que rien ne trouble » : sans un
    relevé, un achat ni un recoupement. La répétition générale l'a trouvé aveugle — à quinze
    relevés par minute il n'en reste aucun, et un joueur qui revient relever sur la copie du
    Corpus jumeau aurait rendu un journal sans contrôle. Le grand livre les garde tous, et il
    contrôle du même coup le tarif figé de chaque tablette (règle 9), c'est-à-dire la main
    elle-même, qu'aucun intervalle calme ne pouvait voir.

    Seule la coupure entre deux séances en sort : la nuit (`veillee`) n'est pas un débit, et
    la ligne porte un total. Et le sélecteur de vitesse n'y change rien — il ne touche ni les
    occurrences ni les multiplicateurs, seulement le rapport entre ces secondes-là et celles
    de la montre —, d'où l'avertissement en tête de rapport, qui ne se déduit d'aucun chiffre.
    Rend les écarts triés, en % de ce qui est entré dans l'intervalle, et le nombre
    d'intervalles écartés par une coupure."""
    r = Rejeu(ev)
    pred = entre = 0.0
    prev_t, prev_o, coupe, ecarts, coupes = ev[0][0], None, False, [], 0
    for t, genre, det in ev:
        if genre == 'finjeu':
            break                    # la production est arrêtée : plus aucun relevé d'état
        flux = r.obrut() * max(0.0, t - prev_t)
        pred += flux - r.b['tab'] * P['tab_c'] * max(0.0, t - prev_t)
        entre += flux
        prev_t = t
        if genre == 'relever':
            ou, _, val = r.releve(det)
            if ou is None:
                coupe = True
            pred += val
            entre += val
        elif genre == 'acheterIns':
            m = RE_INS.match(det)
            if m:
                pred -= r.cout_ins(m.group(1), int(m.group(2)))
                r.b[m.group(1)] = int(m.group(2))
        elif genre == 'recouper':
            pred -= r.cout_rec()
            r.nrec += 1
        elif genre == 'formuler':
            pred -= P['hyp_c']
        elif genre == 'acheterGl':
            m = RE_GL.match(det)
            if m:
                r.gl[m.group(1)] = 'f' if m.group(3) else 'j'
                r.solder(m.group(1))
        elif genre == 'reviser':
            m = RE_REV.match(det)
            if m:
                r.gl[m.group(1)] = 'f' if '✗' in m.group(3) else 'j'
                r.lever()
        elif genre in ('veillee', 'reprise'):
            coupe = True
        elif genre == 'etat':
            m = RE_ETAT.search(det)
            if not m:
                continue
            o = float(m.group(1))
            if prev_o is not None and entre > 1000:
                if coupe:
                    coupes += 1
                else:
                    ecarts.append(100 * ((o - prev_o) - pred) / entre)
            prev_o, pred, entre, coupe = o, 0.0, 0.0, False
    return sorted(ecarts), coupes


def titre(x):
    print('\n' + x)
    print('─' * len(x))


def rapport(ev, nom):
    s = Rejeu(ev).jouer()
    t0, t1 = ev[0][0], ev[-1][0]
    o_tot = s['o_auto'] + s['o_main']
    # Le solde final : le dernier relevé d'état, moins ce qui a été acheté après lui —
    # sans quoi le dernier signe de la partie serait compté deux fois.
    c_fin = s['etats'][-1][2] if s['etats'] else 0.0
    t_dernier = s['etats'][-1][0] if s['etats'] else t1
    c_fin = max(0.0, c_fin - sum(c for tt, c in s['couts_t'] if tt > t_dernier))
    cert_tot = s['cert_couts'] + c_fin
    narbre = sum(1 for _, g, _, _, _, _ in s['achats'] if g not in sim.SECRETS)

    titre('la partie — %s' % nom)
    # La durée est celle du jeu, jusqu'à l'arrêt : après, le journal court à l'horloge — la
    # lecture de la dernière tablette, l'effacement, la relecture —, et une relecture de vingt
    # minutes faisait passer la partie pour vingt minutes plus longue.
    if s['finjeu']:
        print('  durée %s jusqu\'à l\'arrêt de la partie · journal jusqu\'à %s'
              % (mmss(s['finjeu']), mmss(t1)))
    else:
        print('  durée %s au chrono · %s entre le premier et le dernier geste'
              % (mmss(t1), mmss(t1 - t0)))
    print('  %d signes d\'arbre sur %d · %d au lexique' % (narbre, NGL, len(s['achats'])))
    if s['etats']:
        e = s['etats'][-1]
        print('  lisibilité : %d %% des signes, %d %% des lignes' % (e[4], e[5]))
    if s['gis_fichier'] and s['gis_fichier'] != GIS_TOTAL:
        print('  ⚠ gisement du fichier %d, du build actuel %d — journal d\'un AUTRE build,'
              % (s['gis_fichier'], GIS_TOTAL))
        print('    les tarifs reconstruits sont approximatifs')
    # Le sélecteur de vitesse ne sort pas du build de développement (LIV-2) : un journal de
    # playtest n'en portera jamais. Ici, il veut dire que les durées qui suivent ne sont pas
    # des minutes vécues — et aucun chiffre du rapport ne peut le dire à leur place.
    vit = [(t, d) for t, g, d in ev if g == 'vitesse']
    if any(d != '×1' for _, d in vit):
        print('  ⚠ le sélecteur de vitesse a servi : %s'
              % ' · '.join('%s %s' % (mmss(x), d) for x, d in vit[:6]))
        print('    les instants de ce journal sont des secondes de JEU et non de montre ;')
        print('    tout ce qui suit se lit comme tel, y compris les tranches de dix minutes')

    # La coupure entre deux séances, et ce qu'elle a duré à l'horloge. Le chrono du journal
    # est du temps de jeu : sans cette ligne, deux séances se liraient comme une seule.
    if s['reprises']:
        for t, det in s['reprises']:
            print('  coupure : reprise à %s, %s' % (mmss(t), det))
    else:
        print('  aucune coupure : la partie s\'est jouée d\'une traite')
    # I4 : jamais plus de huit minutes sans déblocage. Les attentes se comptent entre deux
    # signes de l'arbre, en temps de jeu — une coupure n'en est pas une.
    arbre = sorted((t, g) for t, g, _, _, _, _ in s['achats'] if g not in sim.SECRETS)
    longues = [(arbre[i][0] - arbre[i - 1][0], arbre[i - 1][0], arbre[i][1])
               for i in range(1, len(arbre)) if arbre[i][0] - arbre[i - 1][0] > 480]
    if longues:
        print('  attentes de plus de 8 min sans déblocage (I4) :')
        for d, a, g in longues:
            print('    %4.1f min — de %s à ⟨%s⟩' % (d / 60, mmss(a), MOT.get(g, g)))
    elif len(arbre) > 1:
        print('  aucune attente de plus de 8 min entre deux signes (I4 tenu)')

    titre('les deux gestes du corpus (règle 8)')
    tot_rel = s['relev'] + s['vides']
    print('  relevés %d — %d utiles, %d à vide (%.0f %%) · gisement %d / %d'
          % (tot_rel, s['relev'], s['vides'], 100 * s['vides'] / max(1, tot_rel),
             s['relev'] - s['copie'], GIS_TOTAL))
    if s['copie']:
        print('  dont %d sur la copie du Corpus jumeau (VOIX-4), chacune tarifée à son premier relevé'
              % s['copie'])
        print('    tablettes de la copie : %s'
              % ', '.join('%d (%d)' % kv for kv in sorted(s['copie_tb'].items())))
    # La question que PT10 a ouverte : revient-on dans le corpus après la quarantième minute ?
    # Depuis le Corpus jumeau, la réponse se lit d'abord après l'entrée dans l'acte IV.
    acte4_t = next((t for t, g, _, _, _, _ in s['achats'] if sim.ACTE.get(BRANCHE.get(g), 0) >= 4), None)
    if acte4_t is not None:
        apres4 = [d for t, g, d in ev if g == 'relever' and t >= acte4_t]
        print('  après l\'entrée dans l\'acte IV (%s) : %d relevés, dont %d sur la copie'
              % (mmss(acte4_t), len(apres4), sum(1 for d in apres4 if d.endswith('· copie'))))
    if s['sans_tb']:
        print('  ⚠ %d relevés sans numéro de tablette (journal d\'avant PT9) : non tarifés'
              % s['sans_tb'])
    print('  recoupements %d · hypothèses formulées à la main %d' % (len(s['recs']), s['formuler']))
    # L'arrêt de la partie : la ligne « finjeu » depuis le 15/09/2026, sinon l'achat du
    # dernier signe de l'arbre — au-delà, le chrono de jeu est gelé et les gestes ne datent
    # plus rien. C'est ce qui faisait dire à PT10 « dernier recoupement 96:35 » pour quatre
    # recoupements faits pendant la carte de fin.
    arbre_t = [t for t, g, _, _, _, _ in s['achats'] if g not in sim.SECRETS]
    borne = s['finjeu'] or (arbre_t[NGL - 1] if len(arbre_t) >= NGL else float('inf'))
    d_rel = max((t for t, g, d in ev if g == 'relever' and t < borne), default=None)
    d_rec = max((t for t, _, _ in s['recs'] if t < borne), default=None)
    if d_rel is not None:
        print('  dernier relevé %s · dernier recoupement %s'
              % (mmss(d_rel), mmss(d_rec) if d_rec is not None else '—'))
    apres = sum(1 for t, g, _ in ev if g in CORPUS_GESTES and t >= borne)
    if apres:
        print("  %d geste%s après l'arrêt de la partie, dans la fenêtre de lecture de FIN-1"
              % (apres, 's' if apres > 1 else ''))

    titre('la main')
    print('  occurrences : %s relevées à la main sur %s produites = %.1f %%'
          % (f'{s["o_main"]:,.0f}'.replace(',', ' '), f'{o_tot:,.0f}'.replace(',', ' '),
             100 * s['o_main'] / max(1e-9, o_tot)))
    if s['o_nuit']:
        print('    dont %s hors ligne, estimées : la ligne « veillee » porte un total, pas un gain'
              % f'{s["o_nuit"]:,.0f}'.replace(',', ' '))
    if s['relev']:
        print('    relevé moyen %s occurrences — c\'est la DATE du premier relevé de chaque'
              % f'{s["o_main"] / s["relev"]:,.0f}'.replace(',', ' '))
        print('    tablette qui le fixe, pas sa cadence (règle 9)')
    print('  Certitude (I6) : %d recoupée sur ~%d produites = %.2f %%'
          % (s['cert_main'], cert_tot, 100 * s['cert_main'] / max(1e-9, cert_tot)))

    if s['etats']:
        print()
        pire = 0.0
        for i in range(0, int(t1) + 1, 600):
            j = i + 600
            ea = [e for e in s['etats'] if e[0] <= i]
            eb = [e for e in s['etats'] if e[0] <= j]
            if not eb:
                break
            dc = eb[-1][2] - (ea[-1][2] if ea else 0.0)
            prod = dc + sum(c for tt, c in s['couts_t'] if i <= tt < j)
            man = sum(g for tt, g in s['main_t'] if i <= tt < j)
            if prod < 0.5:
                continue
            pct = 100 * man / prod
            # Règle 2 : la tranche d'ouverture ne se mesure pas. Avant la première
            # Concordance le recoupement est la seule source de Certitude du jeu, le
            # ratio y vaut 100 % par construction — c'est une division par zéro, pas un
            # mauvais score, et il ne faut surtout pas régler contre lui.
            ouv = i == 0
            if not ouv:
                pire = max(pire, pct)
            print('    %2d–%2d min  main %6.1f / produite %8.1f = %3.0f %%%s'
                  % (i // 60, j // 60, man, prod, pct, '   ← ouverture, hors verdict' if ouv else ''))
        print('    → pire tranche hors ouverture : %.0f %% (plafond 30 %%) — %s'
              % (pire, 'tenu' if pire <= 30 else 'DÉPASSÉ'))

    titre('le corpus')
    print('  concordances %d%s · navigations %d%s'
          % (len(s['concs']),
             (' (' + ', '.join(c[1].split(' ·')[0] for c in s['concs'][:8]) + ')') if s['concs'] else '',
             len(s['navs']),
             ' — sans les %d sauts du jeu vers une réponse' % s['sauts'] if s['sauts'] else ''))
    if s['toi']:
        o, f, det = s['toi']
        print('  repli « à toi » ouvert à %s (%s)%s'
              % (mmss(o), det, ' · refermé à %s, %d s de relecture' % (mmss(f), f - o)
                 if f is not None else ' · jamais refermé'))
    # Jusqu'à l'arrêt seulement : ce qui suit se compte à l'horloge, et une relecture longue
    # y ferait un trou qui n'est pas de la partie.
    fin_t = s['finjeu'] or t1
    gestes = sorted(t for t, g, _ in ev if g in CORPUS_GESTES and t <= fin_t)
    if len(gestes) > 1:
        trous = sorted(((gestes[i + 1] - gestes[i], gestes[i], gestes[i + 1])
                        for i in range(len(gestes) - 1)), reverse=True)[:3]
        print('  les plus longs trous sans un geste dans le texte :')
        for d, a, z in trous:
            print('    %5.1f min — de %s à %s (%.0f %% de la partie)'
                  % (d / 60, mmss(a), mmss(z), 100 * d / max(1e-9, fin_t - t0)))

    titre('les lectures (AMB-1 à 3, CONTR-1)')
    tranches = [(g, m, f) for _, g, m, f, _, _ in s['achats'] if g in sim.AMBIGUS]
    if not tranches:
        print('  aucun signe ambigu acheté — journal d\'avant le 15/09/2026 ?')
    else:
        fx = [g for g, _, f in tranches if f]
        print('  %d signes ambigus tranchés, %d faux : %s'
              % (len(tranches), len(fx), ', '.join(fx) or '—'))
        # La question de PT11 — « combien de lectures fausses sur neuf » — porte sur le
        # JOUEUR. Ce qu'un Élève a lu à sa place n'y entre pas, et se compte à part.
        elv = s['eleve']
        if elv:
            siens = [(g, f) for g, _, f in tranches if g not in elv]
            print('  dont %d par le joueur (%d faux) et %d par l\'Élève (%d faux, %.1f attendus)'
                  % (len(siens), sum(1 for _, f in siens if f), len(elv),
                     sum(1 for g, _, f in tranches if f and g in elv),
                     sum(sim.erreur(P, n) for n in elv.values())))
        # Le seul geste qui fasse baisser le doute est de concorder le signe AVANT de le
        # trancher (règle 18) ; le jeu ne le dit nulle part, et c'est ici qu'on le voit.
        # Dans l'ordre du journal et non à l'instant : deux lignes portent souvent le même.
        vus, avant_achat = set(), set()
        for _, g_, d_ in ev:
            if g_ == 'concChoisir':
                vus.add(d_.split(' ·')[0])
            elif g_ == 'acheterGl' and d_.split(' ')[0] in vus:
                avant_achat.add(d_.split(' ')[0])
        conc_av = lambda g, t: g in avant_achat
        for ta, g, mot, f, _, dte in s['achats']:
            if g in sim.AMBIGUS:
                print('    %-6s %-12s %s%s%s%s' % (g, mot, '✗ faux' if f else 'juste',
                                                   ' · doute %d' % dte if dte is not None else '',
                                                   ' · concordé avant' if conc_av(g, ta) else '',
                                                   ' · lu par %d Élève(s), %d %% d\'erreur'
                                                   % (elv[g], round(100 * sim.erreur(P, elv[g])))
                                                   if g in elv else ''))
        # À l'achat, et après les révisions : c'est la seconde que la contradiction lit. La
        # répétition générale affichait « dette 12 » à côté d'une contradiction levée — douze
        # à l'achat, quatre à la fin.
        d_achat = sum(sim.DETTE[g] for g in fx)
        print('  dette %d à l\'achat%s (seuil %d)'
              % (d_achat, ', %d après les révisions' % s['dette_fin'] if s['dette_fin'] != d_achat
                 else '', P['contr_s']))
    if s['elv_achats']:
        t1e = s['elv_achats'][0][0]
        # Avant ou après ⟨avant⟩ et ⟨ne-pas⟩ — les deux signes dont l'erreur, avec ⟨lire⟩,
        # arme la contradiction à elle seule. Dans l'ordre du journal, pas à l'instant.
        rang = lambda pred: next((i for i, e in enumerate(ev) if pred(e)), None)
        r_elv = rang(lambda e: e[1] == 'acheterIns' and e[2].startswith('elv '))
        def cote(g):
            r = rang(lambda e: e[1] == 'acheterGl' and e[2].split(' ')[0] == g)
            return 'avant' if r is None or r_elv < r else 'après'
        rel = ' · '.join('%s ⟨%s⟩' % (cote(g), MOT.get(g, g)) for g in ('pat', 'la'))
        print('  Élèves : %d, le premier à %s — %s' % (s['elv_achats'][-1][1], mmss(t1e), rel))
    elif tranches:
        print('  aucun Élève')
    if s['contrs']:
        print('  ⚠ contradiction ARMÉE %s : %s'
              % ('une fois' if len(s['contrs']) == 1 else '%d fois' % len(s['contrs']),
                 ' · '.join('à %s, %s' % (mmss(a), 'levée à ' + mmss(l) if l is not None
                                          else 'jamais levée') for a, l in s['contrs'])))
    elif tranches:
        print('  contradiction non déclenchée')
    if s['revs']:
        print('  révisions %d :' % len(s['revs']))
        for t, g, av, ap, c, d0, d1 in s['revs']:
            print('    %s  %-6s %s → %s · %d C · doute %d → %d' % (mmss(t), g, av, ap, c, d0, d1))
    else:
        print('  aucune révision' if any(g == 'mik' for _, g, _, _, _, _ in s['achats'])
              else '  révisions : sans objet, « peut-être » n\'a pas été acheté')

    titre('la grille de composition')
    if not s['comps']:
        print('  aucune tentative')
    else:
        recon = any(r for _, _, (_, _, r) in s['comps'])
        for t, det, (issue, cible, r) in s['comps']:
            lib = {'acquis': 'acquis', 'impayable': 'JUSTE, pas payée', 'carnet': 'fausse, au carnet'}
            print('    %s  %-16s %-18s %s%s'
                  % (mmss(t), det.split(' ✓')[0].split(' ✗')[0], lib.get(issue, issue),
                     cible, ' (reconstitué)' if r else ''))
        n_j = sum(1 for _, _, (i, _, _) in s['comps'] if i != 'carnet')
        print('  %d tentatives · %d paires justes · %d au carnet'
              % (len(s['comps']), n_j, len(s['comps']) - n_j))
        if recon:
            print('  ⚠ issues reconstituées depuis les recettes : journal d\'avant le 15/09/2026')

    titre('les Questions (VOIX-3)')
    if not s['questions']:
        print('  aucune question posée')
    else:
        for t, det in s['questions']:
            print('    %s  %s' % (mmss(t), det))
        n_rep = sum(1 for _, d in s['questions'] if '→' in d)
        n_sil = len(s['questions']) - n_rep
        print('  %d posée%s · %d réponse%s · %d silence%s'
              % (len(s['questions']), 's' if len(s['questions']) > 1 else '',
                 n_rep, 's' if n_rep > 1 else '', n_sil, 's' if n_sil > 1 else ''))

    # Le Lecteur (GRAINE-2) : « on le voit lire ». Ce qui se mesure, c'est si le joueur est
    # allé voir une tablette que le Lecteur venait de marquer.
    if s['lec']:
        titre('le Lecteur (GRAINE-2)')
        lues = [(t, n) for t, ns in s['lues'] for n in ns]
        print('  acheté à %s · %d au plus · %d tablette%s lue%s%s'
              % (mmss(s['lec'][0][0]), s['lec'][-1][1], len(lues), 's' if len(lues) > 1 else '',
                 's' if len(lues) > 1 else '', ', la dernière à %s' % mmss(lues[-1][0]) if lues else ''))
        vues = [(t, d) for t, d in s['navs']
                if any(str(n) == str(d).strip() and tl <= t for tl, n in lues)]
        print('  navigations vers une tablette qu\'il avait déjà lue : %d%s'
              % (len(vues), ', la première à %s' % mmss(vues[0][0]) if vues else ''))

    # I2 (VOIX-5) : au million, une fois l'acte IV ouvert, les zéros des nombres du joueur
    # s'écrivent en ⟨zéro⟩ tant qu'il ne l'a pas composé. Ce qui se mesure : quand, et combien
    # de temps il a joué sans lire ses propres nombres — puis, de vive voix, s'il les a
    # déchiffrés en les regardant monter.
    acte4 = next((t for t, g, _, _, _, _ in s['achats'] if sim.ACTE.get(BRANCHE.get(g), 0) >= 4), None)
    zero = next((t for t, g, _, _, _, _ in s['achats'] if g == 'lan'), None)
    if acte4 is not None or s['zeros'] or zero is not None:
        titre('mes nombres (I2, VOIX-5)')
        print('  acte IV ouvert %s · ⟨zéro⟩ %s'
              % (mmss(acte4) if acte4 is not None else 'jamais',
                 'composé à ' + mmss(zero) if zero is not None else 'jamais composé'))
        if s['zeros']:
            t0, n0 = s['zeros']
            print('  premier nombre écrit avec leurs zéros à %s : %s' % (mmss(t0), n0))
            fin_t = zero if zero is not None and zero > t0 else (s['finjeu'] or (s['interrompu'] or [None])[0])
            if zero is not None and zero > t0:
                print('  %.1f min sans lire ses propres nombres, jusqu\'à ⟨zéro⟩' % ((zero - t0) / 60))
            elif fin_t:
                print('  %.1f min sans lire ses propres nombres, jusqu\'à la fin' % ((fin_t - t0) / 60))
        elif zero is not None:
            print('  ⟨zéro⟩ posé avant que ses nombres n\'atteignent le million : ils ne lui ont jamais été pris')
        elif acte4 is not None:
            print('  aucun nombre n\'a atteint le million')

    if s['finjeu'] or s['fin'] or s['fins']:
        titre('la fin (FIN-1, FIN-2, FIN-3, règle 16)')
        # La fenêtre des deux fins : combien de fois on l'a ouverte, et combien de temps entre la
        # première et le choix. « Aucune n'est présentée comme la bonne » ne se mesure que là.
        if s['fins']:
            choix = s['finjeu'] or (s['interrompu'][0] if s['interrompu'] else None)
            print('  fenêtre des deux fins ouverte %d fois, la première à %s%s'
                  % (len(s['fins']), mmss(s['fins'][0]),
                     ' · %.0f s avant de choisir' % (choix - s['fins'][0]) if choix else ' · rien de choisi'))
        if s['interrompu']:
            print('  INTERROMPUE à %s : %s' % (mmss(s['interrompu'][0]), s['interrompu'][1]))
        else:
            print('  arrêt de la partie %s · effacement %s'
                  % (mmss(s['finjeu']) if s['finjeu'] else '—', mmss(s['fin']) if s['fin'] else 'jamais commencé'))
            if s['finjeu'] and s['fin']:
                print('  %.0f s entre les deux : le temps mis à rouvrir une tablette que le dernier'
                      % (s['fin'] - s['finjeu']))
                print('  signe venait de rendre lisible')
            # La relecture (FIN-3) : ouverte ou non, et ce qu'elle a avoué — en jetons, que
            # l'écran ne compte pas. Sa durée court jusqu'à la ligne suivante, ou jusqu'à
            # l'export : le journal ne sait pas quand on ferme l'onglet.
            if s['relu']:
                print('  relecture ouverte à %s : %s' % (mmss(s['relu'][0]), s['relu'][1]))
            elif s['fin']:
                print('  relecture jamais ouverte')

    titre('contrôle du modèle')
    ec, coupes = controle(ev)
    if not ec:
        print('  aucun intervalle à contrôler — chiffres de « la main » à prendre avec des pincettes')
    else:
        print('  ΔO prédit contre ΔO observé, %d intervalles — relevés, achats et recoupements'
              % len(ec))
        print('  compris%s :' % (', %d écarté%s par la coupure' % (coupes, 's' if coupes > 1 else '')
                                  if coupes else ''))
        print('    écart médian %.1f %% · min %.1f %% · max %.1f %%' % (ec[len(ec) // 2], ec[0], ec[-1]))
        if abs(ec[len(ec) // 2]) > 1:
            print('  ⚠ le modèle a divergé du jeu : la section « la main » est à jeter')


def main():
    # Même parade que les autres outils, et ici elle compte : le rapport porte des ─ et des ⚠
    # que cp1252 ne sait pas écrire, et un rapport de playtest se redirige vers un fichier.
    # L'entrée aussi — un journal passé par un tube arrive sinon décodé en cp1252, et le ✗
    # des lectures fausses ne se reconnaît plus.
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    sys.stdin.reconfigure(encoding='utf-8')
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    choix = None
    for i, a in enumerate(sys.argv):
        if a == '--partie' and i + 1 < len(sys.argv):
            choix = int(sys.argv[i + 1])
    ev = lire(open(args[0], encoding='utf-8') if args else sys.stdin)
    if not ev:
        sys.exit('journal vide — attendu un TSV exporté par le bouton « traces » (hors jeu)')
    ps = parties(ev)
    jouees = [(i, p) for i, p in enumerate(ps, 1) if agit(p) >= 5]
    print('%s · %d parties dans le fichier, %d jouée%s'
          % (args[0] if args else '(entrée standard)', len(ps), len(jouees),
             's' if len(jouees) > 1 else ''))
    print('   build : %s' % ENTETE.get('build', '— (journal d\'avant le 17/09/2026)'))
    if not jouees:
        sys.exit('aucune partie jouée dans ce fichier')
    # À défaut de choix explicite, la plus fournie : une soirée de playtest contient des
    # parties abandonnées au bout de dix secondes, et c'est rarement celles-là qu'on veut.
    i, p = (next(x for x in jouees if x[0] == choix) if choix
            else max(jouees, key=lambda x: agit(x[1])))
    for j, q in jouees:
        print('   %s partie %d : %s, %d actions, %d signes'
              % ('→' if j == i else ' ', j, mmss(q[-1][0]), agit(q),
                 sum(1 for _, g, _ in q if g == 'acheterGl')))
    rapport(p, 'partie %d' % i)


if __name__ == '__main__':
    main()
