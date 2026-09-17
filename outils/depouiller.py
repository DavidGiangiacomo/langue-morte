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
import re
import sys

import sim


P = sim.P
NGL = len(sim.ARBRE)
COUT = {g[0]: g[2] for g in sim.GL}
GIS = {t: -(-n // P['gis_div']) for t, n in sim.JETONS.items()}
GIS_TOTAL = sum(GIS.values())

# genres d'événement qui se passent DANS le corpus (règle 8 : c'est là que se joue la
# différence entre ce jeu et un incrémental habillé, donc c'est ça qu'on mesure)
CORPUS_GESTES = ('relever', 'recouper', 'concChoisir', 'tablette')

RE_GL = re.compile(r'^(\w+) \((.*?)\)( ✗)? (\d+) C(?: · doute (\d+))?$')
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
        self.b = dict(cop=0, tab=0, con=0, ate=0, gram=0)
        self.prix, self.rel = {}, {}
        has = lambda i: i in self.gl
        mf = lambda i, x: ((1 + (x - 1) * sim.AMB_R) if self.gl.get(i) == 'f' else x) if has(i) else 1
        self.m = sim.multis(has, mf)
        self.has = has

    def obrut(self):
        return self.b['cop'] * P['cop_p'] * self.m['cop']() + self.b['ate'] * P['ate_p'] * self.m['ate']()

    def jouer(self):
        s = dict(o_auto=0.0, o_main=0.0, o_nuit=0.0, cert_main=0.0, cert_couts=0.0,
                 relev=0, vides=0, sans_tb=0, formuler=0,
                 recs=[], comps=[], concs=[], navs=[], revs=[], achats=[], etats=[],
                 couts_t=[], main_t=[], contr=None, contr_levee=None,
                 finjeu=None, fin=None, gis_fichier=None)
        prev_t = self.ev[0][0]
        for t, genre, det in self.ev:
            s['o_auto'] += self.obrut() * max(0.0, t - prev_t)
            prev_t = t

            if genre == 'relever':
                m = RE_REL.search(det)
                if not m:
                    # journaux d'avant PT9 : le relevé ne portait pas sa tablette, donc
                    # ni le gisement ni le tarif figé ne se reconstituent
                    s['sans_tb'] += 1
                    continue
                tb = int(m.group(1))
                if self.rel.get(tb, 0) < GIS.get(tb, 0):
                    if tb not in self.prix:
                        self.prix[tb] = (1 + P['click_share'] * self.obrut()) * self.m['click']()
                    s['o_main'] += self.prix[tb]
                    self.rel[tb] = self.rel.get(tb, 0) + 1
                    s['relev'] += 1
                else:
                    s['o_main'] += P['click_floor'] * self.m['click']()
                    s['vides'] += 1

            elif genre == 'formuler':
                s['formuler'] += 1

            elif genre == 'acheterIns':
                m = RE_INS.match(det)
                if m:
                    self.b[m.group(1)] = int(m.group(2))

            elif genre == 'acheterGl':
                m = RE_GL.match(det)
                if not m:
                    continue
                gid, mot, fx, cout, doute = m.groups()
                self.gl[gid] = 'f' if fx else 'j'
                s['cert_couts'] += float(cout)
                s['couts_t'].append((t, float(cout)))
                s['achats'].append((t, gid, mot, bool(fx), int(cout),
                                    int(doute) if doute else None))
                # La contradiction se solde à l'ouverture du doute, et nulle part ailleurs
                # (règle 19). On la rejoue au même endroit que le jeu.
                if gid == 'mik' and s['contr'] is None and self.dette() > P['contr_s']:
                    s['contr'] = t

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
                    if s['contr'] and not s['contr_levee'] and self.dette() <= P['contr_s']:
                        s['contr_levee'] = t

            elif genre == 'composer':
                s['comps'].append((t, det, self.issue(det)))

            elif genre == 'concChoisir':
                s['concs'].append((t, det))

            elif genre == 'tablette':
                s['navs'].append((t, det))

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

            elif genre == 'etat':
                m = RE_ETAT.search(det)
                if m:
                    s['etats'].append((t, float(m.group(1)), float(m.group(3)),
                                       int(m.group(4)), int(m.group(5)), int(m.group(6))))
                    s['gis_fichier'] = int(m.group(8))

        s['o_auto'] += s['o_nuit']
        return s

    def dette(self):
        return sum(sim.DETTE[g] for g in sim.AMBIGUS if self.gl.get(g) == 'f')

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


# Les seuls genres qui ne touchent NI le solde d'occurrences ni les multiplicateurs : on
# peut donc mesurer par-dessus eux. Le recoupement et la formulation d'hypothèse coûtent des
# occurrences (`rec_o`, `hyp_c`) — les oublier ici faisait passer trois intervalles pour une
# divergence du modèle, jusqu'à −56 %.
# `vitesse` en fait partie, et c'est là tout le problème qu'il pose : le sélecteur ne
# touche ni les occurrences ni les multiplicateurs, il ne change que le rapport entre ces
# secondes-là et celles de la montre. Le contrôle ci-dessous le trouverait donc parfaitement
# cohérent — d'où l'avertissement en tête de rapport, qui ne se déduit d'aucun chiffre.
INERTES = ('etat', 'tablette', 'concChoisir', 'fin', 'finjeu', 'vitesse')


def controle(ev):
    """ΔO prédit contre ΔO observé, sur les intervalles entre deux relevés d'état que rien
    ne vient troubler. La Table est alors la seule fuite d'occurrences. Si l'écart médian
    n'est pas nul, le modèle a divergé du jeu et TOUS les chiffres de la section « la main »
    sont à jeter — c'est le seul contrôle que ce fichier ait sur lui-même."""
    r = Rejeu(ev)
    prev, ecarts = None, []
    for t, genre, det in ev:
        if genre not in INERTES:
            if genre == 'acheterIns':
                m = RE_INS.match(det)
                if m:
                    r.b[m.group(1)] = int(m.group(2))
            elif genre == 'acheterGl':
                m = RE_GL.match(det)
                if m:
                    r.gl[m.group(1)] = 'f' if m.group(3) else 'j'
            prev = None
            continue
        if genre != 'etat':
            continue
        m = RE_ETAT.search(det)
        if not m:
            continue
        o = float(m.group(1))
        if prev and t - prev[0] > 25:
            pred = (r.obrut() - r.b['tab'] * P['tab_c']) * (t - prev[0])
            if abs(pred) > 1000:
                ecarts.append(100 * ((o - prev[1]) - pred) / pred)
        prev = (t, o)
    return sorted(ecarts)


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

    titre('les deux gestes du corpus (règle 8)')
    tot_rel = s['relev'] + s['vides']
    print('  relevés %d — %d utiles, %d à vide (%.0f %%) · gisement %d / %d'
          % (tot_rel, s['relev'], s['vides'], 100 * s['vides'] / max(1, tot_rel),
             s['relev'], GIS_TOTAL))
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
        print("  %d gestes après l'arrêt de la partie, dans la fenêtre de lecture de FIN-1"
              % apres)

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
    print('  concordances %d%s · navigations %d'
          % (len(s['concs']),
             (' (' + ', '.join(c[1].split(' ·')[0] for c in s['concs'][:8]) + ')') if s['concs'] else '',
             len(s['navs'])))
    gestes = sorted(t for t, g, _ in ev if g in CORPUS_GESTES)
    if len(gestes) > 1:
        trous = sorted(((gestes[i + 1] - gestes[i], gestes[i], gestes[i + 1])
                        for i in range(len(gestes) - 1)), reverse=True)[:3]
        print('  les plus longs trous sans un geste dans le texte :')
        for d, a, z in trous:
            print('    %5.1f min — de %s à %s (%.0f %% de la partie)'
                  % (d / 60, mmss(a), mmss(z), 100 * d / max(1e-9, t1 - t0)))

    titre('les lectures (AMB-1 à 3, CONTR-1)')
    tranches = [(g, m, f) for _, g, m, f, _, _ in s['achats'] if g in sim.AMBIGUS]
    if not tranches:
        print('  aucun signe ambigu acheté — journal d\'avant le 15/09/2026 ?')
    else:
        fx = [g for g, _, f in tranches if f]
        print('  %d signes ambigus tranchés, %d faux : %s'
              % (len(tranches), len(fx), ', '.join(fx) or '—'))
        for _, g, mot, f, _, dte in s['achats']:
            if g in sim.AMBIGUS:
                print('    %-6s %-12s %s%s' % (g, mot, '✗ faux' if f else 'juste',
                                               ' · doute %d' % dte if dte is not None else ''))
        print('  dette %d (seuil %d)' % (sum(sim.DETTE[g] for g in fx), P['contr_s']))
    if s['contr']:
        print('  ⚠ contradiction ARMÉE à %s%s' % (mmss(s['contr']),
              ' · levée à ' + mmss(s['contr_levee']) if s['contr_levee'] else ' · jamais levée'))
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

    if s['finjeu'] or s['fin']:
        titre('la fin (FIN-1, règle 16)')
        print('  arrêt de la partie %s · carte de fin %s'
              % (mmss(s['finjeu']) if s['finjeu'] else '—', mmss(s['fin']) if s['fin'] else 'jamais vue'))
        if s['finjeu'] and s['fin']:
            print('  %.0f s entre les deux : le temps mis à rouvrir une tablette que le dernier'
                  % (s['fin'] - s['finjeu']))
            print('  signe venait de rendre lisible')

    titre('contrôle du modèle')
    ec = controle(ev)
    if not ec:
        print('  pas assez d\'intervalles calmes pour contrôler — chiffres de « la main » à prendre avec des pincettes')
    else:
        print('  ΔO prédit contre ΔO observé, %d intervalles que rien ne trouble :' % len(ec))
        print('    écart médian %.1f %% · min %.1f %% · max %.1f %%' % (ec[len(ec) // 2], ec[0], ec[-1]))
        if abs(ec[len(ec) // 2]) > 1:
            print('  ⚠ le modèle a divergé du jeu : la section « la main » est à jeter')


def main():
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
