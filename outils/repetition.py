#!/usr/bin/env python3
"""
Répétition générale du dépouillement — « La langue morte ».

Usage :  python build.py && python outils/repetition.py
         python outils/repetition.py --sortie traces-repetition.tsv

Un journal de playtest ne se refait pas. Le jour où il revient, `depouiller.py` doit le lire
du premier coup, et ses chiffres doivent être vrais — or il n'avait jamais lu un journal de
cinq actes sorti du jeu lui-même. `verifier.py` contrôle chaque ligne de trace une à une ;
il ne fait jamais jouer une partie entière, et c'est sur une partie entière que le rejeu
d'économie de `depouiller.py` peut dériver sans que rien ne casse.

Ce script fait jouer une partie au **build de playtest** — celui que Pages déploie —, de la
première seconde à la relecture, en deux séances avec une coupure entre les deux. Le joueur
est l'acheteur de `sim.py` (mêmes règles d'achat, même cadence de relevé), qui agit **dans
l'interface** : il clique les jetons du corpus, la barre, le lexique, les fenêtres des deux
lectures et des deux fins, la grille, le panneau des questions. Le temps est celui d'une
horloge simulée (Playwright), qui avance par pas d'une demi-seconde : chaque pas est une
frame du jeu, `tick` et peinture compris, et une partie de deux heures passe en quelques
minutes. Ni le sélecteur de vitesse, ni un appel direct à `tick` : les secondes du journal
sont celles que le jeu a comptées, comme pour un joueur.

Pendant ce temps il tient sa propre comptabilité — ce que chaque relevé a rendu, ce que les
instruments ont produit, ce que chaque recoupement a gagné, ce que la nuit a crédité —,
mesurée dans le jeu et non rejouée. À la fin, il dépouille le journal exporté et confronte,
ligne à ligne, ce que le jeu a fait à ce que `depouiller.py` en dit.
"""
import contextlib
import datetime
import io
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import depouiller   # noqa: E402
import sim          # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("playwright manquant :  pip install playwright && playwright install chromium")

RACINE = pathlib.Path(__file__).parent.parent
PAGE = RACINE / 'dist' / 'playtest.html'

# Le joueur. La cadence de relevé est celle de `sim.py` par défaut ; les lectures fausses sont
# choisies pour faire passer la partie par la contradiction — ⟨grain⟩, ⟨tablette⟩ … pèsent
# sept points avant les Élèves, deux de plus que le seuil — et donc par la révision qui la
# lève. Ce n'est pas un joueur probable : c'est celui qui emprunte le plus de chemins du
# journal. Les Élèves, eux, tirent leurs lectures au dé ; le dé est semé (`GRAINE`), et la
# partie est la même à chaque lancement.
JOUEUR = dict(
    cpm=15,
    faux=['ur', 'kish', 'sar', 'nur'],
    concorder_avant=['kish', 'nur'],
    ate_socle=sim.P['ate_socle'],
    # ce que le texte répond, et qui ouvre le mot en tête de chaîne (règle 24)
    conditions={'hal': ['ta', 'shen'], 'ke': ['shen'], 'meshke': ['tab']},
)
GRAINE = 20261020
COUPURE_MIN = 85          # la première séance s'arrête là, à la première frame après ⟨nuit⟩
ABSENCE_MIN = 55          # … et la seconde reprend tant de minutes d'horloge plus tard
PLAFOND_MIN = 260         # au-delà, la partie ne finit pas : c'est un défaut à rapporter
DEBUT = datetime.datetime(2026, 10, 21, 20, 0, 0)

# Le Math.random du jeu, remplacé par un générateur semé. Deux tirages seulement en dépendent
# — l'ordre des deux lectures et des deux fins, et les lectures des Élèves —, et sans graine
# deux répétitions ne passeraient pas par les mêmes chemins.
HASARD = """(() => { let a = %d >>> 0;
  Math.random = () => { a = (a + 0x6D2B79F5) >>> 0; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();"""

# Le joueur, dans la page. Tout passe par l'interface quand l'interface a un geste : un clic
# sur un jeton, une carte, un bouton de fenêtre. Les fonctions de peinture sont appelées avant
# un clic pour que l'état `disabled` des boutons suive les ressources, comme à la frame
# suivante d'une vraie partie.
JOUEUR_JS = r"""(cfg) => {
  const R = cfg.etat || {
    v: {o_main:0, o_auto:0, c_main:0, c_brut:0, neuf:0, copie:0, plancher:0, recs:0,
        comps:[], qs:[], revs:[], concs:[], navs:[], achats:[], contr:[], zeros:null,
        toi:null, fins:[], finjeu:null, fin:null, relu:null, elv:[], lec:[], err:[]},
    clic:0, nav:0, recIdx:0, finRetour:0, finsVus:0, silence:false, compFaux:false,
    compImp:false, concAv:{}, navIdx:0, contrVu:false, toiT:null, finNav:false
  };
  window.__R = R;
  const V = R.v;

  // ---- la comptabilité de vérité : mesurée dans le jeu, jamais rejouée ----
  const _produire = produire;
  produire = function(dt, nuit){ if(!nuit) V.o_auto += oBrut()*dt; return _produire(dt, nuit); };
  const _gagnerC = gagnerC;
  gagnerC = function(x, nuit){ if(x > 0 && !nuit) V.c_brut += x; return _gagnerC(x, nuit); };

  const q = s => document.querySelector(s);
  const clic = el => { if(el){ el.click(); return true; } return false; };
  const cout = k => insCost(INS.find(i => i.k === k));
  const tabEl = t => elCorpus.querySelector('.tablet[data-tb="'+t+'"]');
  const visibles = () => ORDRE.filter(t => { const e = tabEl(t); return e && !e.hidden; });
  const tetes = () => BR.map(([k]) => GL.find(g => g.br === k && !g.sec && !has(g.id)))
                        .filter(g => g && offert(g));

  // ---- le relevé : l'ordre de `sim.py`, original puis copie, tablettes déjà tarifées d'abord
  function cible(){
    const vis = visibles();
    const orig = t => (S_.rel[t] || []).length < GISEMENT[t];
    const cop  = t => S_.b.jum && (S_.relJ[t] || []).length < GIS_COPIE[t];
    let t = vis.find(t => orig(t) && S_.prix[t] !== undefined);
    if(t === undefined) t = vis.find(orig);
    if(t !== undefined) return [t, S_.rel[t] || []];
    t = vis.find(t => cop(t) && S_.prixJ[t] !== undefined);
    if(t === undefined) t = vis.find(cop);
    if(t !== undefined) return [t, S_.relJ[t] || []];
    return [vis[0], null];
  }
  function relever1(){
    const [t, deja] = cible();
    if(t === undefined) return;
    const toks = [...tabEl(t).querySelectorAll('.tok[data-j]')];
    const el = deja ? toks.find(e => deja.indexOf(+e.dataset.j) < 0) : toks[0];
    if(!el) return;
    const o = S_.O, n = (S_.rel[t] || []).length, nj = (S_.relJ[t] || []).length;
    clic(el);
    V.o_main += S_.O - o;
    if((S_.rel[t] || []).length > n) V.neuf++;
    else if((S_.relJ[t] || []).length > nj) V.copie++;
    else V.plancher++;
  }

  // ---- les instruments : la boucle d'achat de `sim.py`, au même ordre de préférence
  function acheter(k){
    paintInstr();
    const b = q('#instr [data-ins="'+k+'"]');
    if(!b || b.disabled) return false;
    const n = S_.b[k];
    clic(b);
    if(S_.b[k] <= n) return false;
    if(k === 'elv' || k === 'lec') V[k].push([S_.t, S_.b[k]]);
    return true;
  }
  function instruments(){
    for(let n = 0; n < 60; n++){
      const netO = oBrut() - S_.b.tab*1.0;
      const netH = S_.b.tab*0.6*M.tabl() - S_.b.con*0.5 - S_.b.gram*GRAM_C;
      const effCop = cout('cop')/(1.0*M.cop()), effAte = cout('ate')/(25*M.ate());
      const prod = S_.b.cop >= cfg.ate_socle && effAte <= effCop ? 'ate' : 'cop';
      const epargne = prod === 'ate' && S_.O < cout('ate');
      const elvOk = S_.b.gram > 0 && S_.O >= cout('elv')
        && ELV_P/(1 + ELV_P*S_.b.elv)/cout('elv') >= 1/Math.max(1, S_.b.gram)/cout('gram');
      let k = null;
      if(elvOk) k = 'elv';
      else if(has('nur') && netH >= GRAM_C && S_.O >= cout('gram')) k = 'gram';
      else if(epargne) break;
      else if(netH >= 0.5 && S_.O >= cout('con')) k = 'con';
      else if(netO >= 1.0 && S_.O >= cout('tab') && S_.b.cop > 0) k = 'tab';
      else if(S_.O >= cout(prod)) k = prod;
      if(k === null || !acheter(k)) break;
    }
    if(has('nash') && !S_.b.jum && S_.O >= cout('jum')) acheter('jum');
    if(has('mesh') && S_.O >= cout('lec')) acheter('lec');
  }

  // ---- le recoupement : deux attestations d'un même signe, dans deux tablettes
  function recouper1(){
    const vis = visibles();
    if(vis.length < 2) return false;
    for(let essai = 0; essai < vis.length; essai++){
      const ta = vis[R.recIdx % vis.length], dec = R.recIdx * 7;
      R.recIdx++;
      const toks = [...tabEl(ta).querySelectorAll('.tok[data-w]')];
      for(let i = 0; i < toks.length; i++){
        const ea = toks[(i + dec) % toks.length], w = ea.dataset.w;
        const tb = vis.find(t => t !== ta && tabEl(t).querySelector('.tok[data-w="'+w+'"]'));
        if(tb === undefined) continue;
        paintActs();
        if(!recArme) clic($('a-rec'));
        if(!recArme) return false;
        const g = recGain(), n = S_.rec;
        clic(ea); clic(tabEl(tb).querySelector('.tok[data-w="'+w+'"]'));
        paintActs(); clic($('a-rec'));
        if(S_.rec > n){ V.recs++; V.c_main += g; return true; }
        return false;
      }
    }
    return false;
  }
  function recoupements(){
    for(let n = 0; n < 40; n++){
      const rc = recCost();
      if(!(S_.O >= rc.O*4 && S_.H >= rc.H*4 && rc.O < S_.O*0.25)) return;
      if(!recouper1()) return;
    }
  }

  // ---- la concordance, avant de trancher
  function concorder(id){
    if(!S_.b.con) return false;
    const t = visibles().find(t => tabEl(t).querySelector('.tok[data-w="'+id+'"]'));
    if(t === undefined) return false;
    if(concSel || concToi) clic($('a-con'));
    clic($('a-con'));
    clic(tabEl(t).querySelector('.tok[data-w="'+id+'"]'));
    const ok = concSel === id;
    if(ok) V.concs.push([S_.t, id]);
    clic($('a-con'));
    return ok;
  }

  // ---- les questions : un silence d'abord, puis celle qui ouvre le mot en tête de chaîne
  function poser(sig){
    qVider(); paintQuest();
    for(const s of sig){ const b = q('#q-choix [data-qpion="'+s+'"]'); if(!b || b.hidden) return false; clic(b); }
    paintQuest();
    const n = S_.qa.length;
    clic($('a-quest'));
    return S_.qa.length > n;
  }
  function questions(){
    if(!questionsOuvertes() || questionsEnMain() < 1) return;
    if(!R.silence && has('nash') && has('mu')){
      R.silence = true;
      if(poser(['nash', 'mu'])) V.qs.push([S_.t, 'nash mu', 'silence']);
    }
    for(const g of tetes().concat(BR.map(([k]) => GL.find(g => g.br === k && !g.sec && !has(g.id))))){
      if(!g || !g.rep || ouvertsParReponse().has(g.id) || questionsEnMain() < 1) continue;
      const c = cfg.conditions[g.id];
      if(c && c.every(has) && poser(c)) V.qs.push([S_.t, c.join(' '), g.id]);
    }
  }

  // ---- la révision : seulement pour lever une contradiction, le signe le plus lourd d'abord
  function reviser1(){
    if(!has('mik') || !S_.contr || S_.C < revCost() || !$('amb').hidden) return;
    const fx = S_.gl.filter(id => AMB[id] && faux(id)).sort((a, b) => detteDe(b) - detteDe(a));
    if(!fx.length) return;
    paintDoute();
    const b = q('#doutes [data-dou="'+fx[0]+'"]');
    if(!b || b.disabled) return;
    clic(b);
    if($('amb').hidden) return;
    const n = S_.rev;
    clic(q('#amb-choix [data-amb="'+ambOrdre.indexOf('j')+'"]'));
    if(S_.rev > n) V.revs.push([S_.t, fx[0]]);
  }

  // ---- le lexique : le moins cher d'abord ; la fenêtre des deux fins s'ouvre, se referme une
  //      fois, et s'achève vingt secondes plus tard
  function fins(){
    V.fins.push(S_.t);
    if(R.finsVus++ === 0){ clic($('fins-annuler')); R.finRetour = S_.t + 20; return; }
    // La seconde fois, la fenêtre reste ouverte le temps que la partie soit copiée dans un
    // autre navigateur, qui choisira l'autre fin (`interrompue()` côté Python).
    if(!R.jumelle){ R.jumelle = 'attend'; return; }
    clic(q('#fins-choix [data-fin="achever"]'));
  }
  function glyphes(){
    for(let n = 0; n < 50; n++){
      if(!$('amb').hidden || !$('fins').hidden || S_.done) return;
      const a = tetes().filter(g => S_.C >= g.cost).sort((x, y) => x.cost - y.cost);
      if(!a.length) return;
      const g = a[0];
      if(estDernier(g.id) && S_.t < R.finRetour) return;
      if(AMB[g.id] && !elvTranche() && cfg.concorder_avant.includes(g.id) && !R.concAv[g.id]){
        R.concAv[g.id] = 1; concorder(g.id);
      }
      paintLex();
      const b = q('#lex [data-gl="'+g.id+'"]');
      if(!b || b.disabled) return;
      const nb = S_.gl.length, elv = AMB[g.id] && elvTranche() ? S_.b.elv : 0;
      clic(b);
      if(!$('amb').hidden){
        const voulu = cfg.faux.includes(g.id) ? 'f' : 'j';
        clic(q('#amb-choix [data-amb="'+ambOrdre.indexOf(voulu)+'"]'));
      }
      if(!$('fins').hidden){ fins(); if(!S_.done) return; }
      if(S_.gl.length <= nb) return;
      V.achats.push([S_.t, g.id, AMB[g.id] ? S_.lect[g.id] : '', elv]);
    }
  }

  // ---- la grille : une paire fausse, une paire juste impayable, ⟨grenier⟩, et ⟨zéro⟩ dix
  //      minutes après que les nombres ont pris leurs zéros
  function grille(a, b){
    compVider(); paintComp();
    const pa = q('#comp-choix [data-pion="'+a+'"]'), pb = q('#comp-choix [data-pion="'+b+'"]');
    if(!pa || pa.hidden || !pb || pb.hidden) return null;
    clic(pa); clic(pb); paintComp();
    const n = S_.comp, ng = S_.gl.length, nc = S_.carnet.length;
    clic($('a-comp'));
    const issue = S_.gl.length > ng ? 'acquis' : S_.carnet.length > nc ? 'carnet'
                : S_.comp > n ? 'impayable' : null;
    if(issue) V.comps.push([S_.t, a+' + '+b, issue]);
    compVider();
    return issue;
  }
  function composition(){
    if(!compOuvre()) return;
    if(!R.compFaux && has('an') && has('tem') && S_.H >= compCost() + 2000){
      R.compFaux = true; grille('an', 'tem'); }
    if(!R.compImp && has('tab') && has('sar') && !has('tabsar') && S_.C < byId.tabsar.cost
       && S_.H >= compCost() + 2000){ R.compImp = true; grille('tab', 'sar'); }
    if(has('ur') && has('tem') && !has('urtem') && S_.C >= byId.urtem.cost) grille('ur', 'tem');
    if(has('la') && has('an') && !has('lan') && S_.C >= byId.lan.cost
       && ((V.zeros && S_.t > V.zeros[0] + 600) || has('nashal'))) grille('la', 'an');
  }

  // ---- la barre : une tablette toutes les trois minutes, celle que le Lecteur vient de lire
  //      quand il y en a une
  function naviguer(){
    if(S_.t < R.nav) return;
    R.nav = S_.t + 180;
    const vis = visibles();
    let t = vis[(R.navIdx++) % vis.length];
    if(S_.b.lec && S_.tete >= 1 && vis.includes(Math.floor(S_.tete))) t = Math.floor(S_.tete);
    aller(t);
  }
  // Un saut vers la tablette où l'on est déjà n'est pas une navigation : le journal l'ignore,
  // exprès (traces.js), et la vérité se compte de même.
  function aller(t){
    if(clic(q('#rail [data-go="'+t+'"]')) && t !== R.derniere){ V.navs.push([S_.t, t]); R.derniere = t; }
  }

  function suivre(){
    if(S_.contr !== R.contrVu){ V.contr.push([S_.t, S_.contr]); R.contrVu = S_.contr; }
    if(!V.zeros && zerosVus) V.zeros = [S_.t];
    if(concToi && R.toiT === null) R.toiT = S_.t;
    if(concToi && S_.t > R.toiT + 90){ clic($('a-con')); V.toi = [R.toiT, S_.t]; }
  }

  // ---- après le dernier signe : aller lire la tablette qu'il a rendue lisible, puis relire
  function apres(){
    if(V.finjeu === null) V.finjeu = S_.t;
    suivre();
    if(!R.finNav && S_.fin === 'achevee' && finLire){
      R.finNav = true;
      aller([...finLire][0]);
    }
    if(V.fin === null && document.body.classList.contains('fin')) V.fin = performance.now();
    if(V.relu === null && S_.efface && !relecture){
      clic($('relire')); if(relecture) V.relu = performance.now();
    }
  }

  function pas(){
    try{
      if(S_.done){ apres(); return; }
      if(R.jumelle === 'faite' && !$('fins').hidden){
        R.jumelle = 'finie'; clic(q('#fins-choix [data-fin="achever"]'));
        if(S_.done){ apres(); return; }
      }
      suivre();
      R.clic += cfg.cpm/60*2;
      for(; R.clic >= 1; R.clic--) relever1();
      instruments();
      recoupements();
      questions();
      reviser1();
      glyphes();
      composition();
      naviguer();
      suivre();
    }catch(e){ V.err.push(String(e && e.stack || e)); }
  }
  setInterval(pas, 2000);
  return true;
}"""

ETAT_JS = """() => ({t: S_.t, done: S_.done, fin: S_.fin, efface: !!S_.efface, relu: relecture,
  esh: has('esh'), n: S_.gl.length, err: __R.v.err.slice(0, 3), O: S_.O, jumelle: __R.jumelle})"""


def interrompue(nav, page):
    """L'autre fin, sur la même partie. La fenêtre des deux fins est ouverte : la sauvegarde et
    le journal sont copiés dans un second navigateur, qui recharge la partie — un joueur qui
    rouvre l'onglet au pied du dernier signe —, rouvre la fenêtre au lexique et choisit
    d'interrompre. Rend le journal exporté et ce que le jeu dit de la partie."""
    d = page.evaluate("""() => { sauver(); sauverTraces();
      return {cle: KEY, tcle: TKEY, s: localStorage.getItem(KEY), tr: localStorage.getItem(TKEY),
              now: Date.now(), t: S_.t}; }""")
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900})
    ctx.add_init_script(HASARD % GRAINE)
    ctx.add_init_script('localStorage.setItem(%s, %s); localStorage.setItem(%s, %s);'
                        % (json.dumps(d['cle']), json.dumps(d['s']),
                           json.dumps(d['tcle']), json.dumps(d['tr'])))
    p2, erreurs = nouvelle_page(ctx, datetime.datetime.fromtimestamp(d['now'] / 1000))
    p2.evaluate("""() => { paintLex();
      const id = GL.find(g => estDernier(g.id)).id;
      document.querySelector('#lex [data-gl="' + id + '"]').click();
      document.querySelector('#fins-choix [data-fin="interrompre"]').click(); }""")
    for _ in range(40):
        p2.clock.fast_forward(500)
    tsv = p2.evaluate('() => tracesTSV()')
    jeu = p2.evaluate("() => ({fin: S_.fin, done: S_.done, t: S_.t, apres: !$('apres').hidden,"
                      " relire: !$('relire').hidden})")
    ctx.close()
    if erreurs:
        sys.exit('la partie interrompue a planté : %s' % erreurs[:3])
    return tsv, dict(jeu, t_arret=d['t'])


def nouvelle_page(ctx, quand):
    page = ctx.new_page()
    erreurs = []
    page.on('pageerror', lambda e: erreurs.append(str(e)))
    page.clock.install(time=DEBUT)
    page.clock.pause_at(quand)
    page.goto(PAGE.resolve().as_uri())
    return page, erreurs


def jouer(nav):
    """La partie entière, en deux séances. Rend le journal exporté, la comptabilité de vérité,
    et ce que la coupure a coûté et crédité."""
    ctx = nav.new_context(viewport={'width': 1440, 'height': 900})
    ctx.add_init_script(HASARD % GRAINE)
    page, erreurs = nouvelle_page(ctx, DEBUT)
    page.evaluate(JOUEUR_JS, dict(JOUEUR, etat=None))
    coupure, frames, t_reel, autre = None, 0, time.time(), None
    while True:
        for _ in range(120):
            page.clock.fast_forward(500)
            frames += 1
            # La fenêtre des deux fins attend, ouverte : on copie la partie avant qu'elle
            # n'avance, pour que l'autre fin se joue sur exactement la même.
            if frames % 4 == 0 and autre is None and page.evaluate('() => __R.jumelle') == 'attend':
                autre = interrompue(nav, page)
                page.evaluate("() => { __R.jumelle = 'faite'; }")
        e = page.evaluate(ETAT_JS)
        if e['err'] or erreurs:
            sys.exit('le joueur automatique a planté : %s' % (e['err'] or erreurs)[:3])
        # La coupure entre les deux séances (PT11 se joue en deux fois au plus). On ferme la
        # page comme un joueur ferme l'onglet, et on la rouvre tant de minutes d'horloge plus
        # tard : ce qui se lit au retour — la ligne `reprise`, la nuit — est ce que le journal
        # d'un vrai joueur portera.
        if coupure is None and e['t'] >= COUPURE_MIN * 60 and e['esh'] and not e['done']:
            avant = page.evaluate("""() => { sauver(); sauverTraces();
              return {R: __R, O: S_.O, ob: oBrut(), now: Date.now(), t: S_.t}; }""")
            page.close()
            reprise = datetime.datetime.fromtimestamp(avant['now'] / 1000) \
                + datetime.timedelta(minutes=ABSENCE_MIN)
            page, erreurs = nouvelle_page(ctx, reprise)
            o_retour = page.evaluate('() => S_.O')
            ecoule = min(ABSENCE_MIN * 60, 4 * 3600)
            coupure = dict(t=avant['t'], absence=ABSENCE_MIN,
                           nuit_nette=o_retour - avant['O'], nuit_brute=avant['ob'] * ecoule * 0.4)
            page.evaluate(JOUEUR_JS, dict(JOUEUR, etat=avant['R']))
            continue
        if e['relu']:
            for _ in range(20):
                page.clock.fast_forward(500)
            break
        if e['t'] > PLAFOND_MIN * 60 or frames > PLAFOND_MIN * 60 * 2 + 4000:
            sys.exit('la partie ne finit pas : %d signes à %d min' % (e['n'], e['t'] / 60))
    tsv = page.evaluate('() => tracesTSV()')
    R = page.evaluate('() => __R')
    fin = page.evaluate("""() => ({t: S_.t, lect: S_.lect, gl: S_.gl, tete: S_.tete, rev: S_.rev,
      b: S_.b, contr: S_.contr, fin: S_.fin})""")
    ctx.close()
    if autre is None:
        sys.exit('la fenêtre des deux fins ne s\'est jamais ouverte deux fois')
    return tsv, R['v'], coupure, fin, frames, time.time() - t_reel, autre


def confronter(tsv, v, coupure, fin):
    """Ce que le jeu a fait, contre ce que `depouiller.py` en lit."""
    ev = depouiller.lire(io.StringIO(tsv))
    ps = [p for p in depouiller.parties(ev) if depouiller.agit(p) >= 5]
    p = ps[-1]
    s = depouiller.Rejeu(p).jouer()
    lignes, ecarts = [], []

    def ligne(quoi, jeu, lu, tol=0.0):
        """`tol` : écart relatif admis. Zéro pour un compte, qui doit tomber juste."""
        if isinstance(jeu, (int, float)) and isinstance(lu, (int, float)):
            ok = abs(lu - jeu) <= tol * max(abs(jeu), 1e-9) + (0 if tol else 1e-9)
        else:
            ok = jeu == lu
        lignes.append((quoi, jeu, lu, ok))
        if not ok:
            ecarts.append(quoi)

    v_achats = [(round(t, 1), g, l, e) for t, g, l, e in v['achats']]
    ligne('signes acquis (lexique et grille)', len(fin['gl']), len(s['achats']))
    ligne("signes d'arbre", sum(1 for g in fin['gl'] if g not in sim.SECRETS),
          sum(1 for x in s['achats'] if x[1] not in sim.SECRETS))
    ligne('relevés utiles (original + copie)', v['neuf'] + v['copie'], s['relev'])
    ligne('… dont sur la copie', v['copie'], s['copie'])
    ligne('relevés à vide', v['plancher'], s['vides'])
    ligne('occurrences relevées à la main', round(v['o_main']), round(s['o_main']), 0.001)
    o_auto_jeu = v['o_auto'] + (coupure['nuit_brute'] if coupure else 0)
    ligne('occurrences des instruments, nuit comprise', round(o_auto_jeu), round(s['o_auto']), 0.01)
    if coupure:
        ligne('… dont la nuit', round(coupure['nuit_brute']), round(s['o_nuit']), 0.05)
    o_tot_jeu, o_tot_lu = o_auto_jeu + v['o_main'], s['o_auto'] + s['o_main']
    ligne('part de la main (%)', round(100 * v['o_main'] / o_tot_jeu, 1),
          round(100 * s['o_main'] / o_tot_lu, 1), 0.02)
    ligne('recoupements', v['recs'], len(s['recs']))
    ligne('Certitude recoupée', round(v['c_main']), round(s['cert_main']))
    ligne('révisions', [g for _, g in v['revs']], [r[1] for r in s['revs']])
    # les lectures : le dernier état, révisions comprises, et qui a tranché
    lu_f = sorted(g for g, l in fin['lect'].items() if l == 'f')
    rejeu_f = sorted(g for g in sim.AMBIGUS if s['achats'] and any(
        x[1] == g for x in s['achats']) and depouiller_lecture(s, g) == 'f')
    ligne('lectures fausses à la fin', lu_f, rejeu_f)
    ligne('signes lus par un Élève', sorted(g for _, g, _, e in v_achats if e),
          sorted(s['eleve']))
    ligne('Élèves', fin['b']['elv'], s['elv_achats'][-1][1] if s['elv_achats'] else 0)
    ligne('Lecteurs', fin['b']['lec'], s['lec'][-1][1] if s['lec'] else 0)
    ligne('tablettes lues par le Lecteur', int(fin['tete']), sum(len(n) for _, n in s['lues']))
    # Chaque fois qu'elle s'arme et se lève, à la minute : le jeu les note au pas du joueur,
    # le journal à l'instant de l'achat ou de la révision qui les cause — le même.
    episodes = []
    for t, armee in v['contr']:
        if armee:
            episodes.append([round(t / 60, 1), None])
        elif episodes:
            episodes[-1][1] = round(t / 60, 1)
    ligne('contradiction : armée puis levée (min)', episodes,
          [[round(a / 60, 1), round(l / 60, 1) if l is not None else None] for a, l in s['contrs']])
    ligne('contradiction : levée à la fin', not fin['contr'],
          not s['contrs'] or s['contrs'][-1][1] is not None)
    ligne('compositions', [(c, i) for _, c, i in v['comps']],
          [(d.split(' ✓')[0].split(' ✗')[0], {'acquis': 'acquis', 'impayable': 'impayable',
            'carnet': 'carnet'}[iss[0]]) for _, d, iss in s['comps']])
    ligne('questions posées', [c for _, c, _ in v['qs']],
          [d.split(' (')[0] for _, d in s['questions']])
    ligne('concordances', len(v['concs']), len(s['concs']))
    ligne('navigations', len(v['navs']), len(s['navs']))
    if coupure:
        ligne('coupure', '%d min' % coupure['absence'],
              s['reprises'][0][1].split(' ')[0] + ' min' if s['reprises'] else 'aucune')
    ligne('repli « à toi » ouvert puis refermé', v['toi'] is not None,
          bool(s['toi'] and s['toi'][1] is not None))
    ligne('nombres pris par leurs zéros', v['zeros'] is not None, s['zeros'] is not None)
    if v['zeros'] and s['zeros']:
        ligne('… à la minute', round(v['zeros'][0] / 60, 1), round(s['zeros'][0] / 60, 1), 0.01)
    ligne('fenêtre des deux fins ouverte', len(v['fins']), len(s['fins']))
    ligne("arrêt de la partie (min)", round(v['finjeu'] / 60, 1),
          round(s['finjeu'] / 60, 1) if s['finjeu'] else None, 0.002)
    ligne('effacement commencé', v['fin'] is not None, s['fin'] is not None)
    ligne('relecture ouverte', v['relu'] is not None, s['relu'] is not None)
    return p, lignes, ecarts


def depouiller_lecture(s, g):
    """La lecture d'un signe à la fin, d'après le rejeu : l'achat, puis la dernière révision."""
    lect = None
    for x in s['achats']:
        if x[1] == g:
            lect = 'f' if x[3] else 'j'
    for r in s['revs']:
        if r[1] == g:
            lect = 'f' if '✗' in r[3] else 'j'
    return lect


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
    if not PAGE.exists():
        sys.exit(f"{PAGE} absent — lancer d'abord : python build.py")
    sortie = None
    if '--sortie' in sys.argv:
        sortie = pathlib.Path(sys.argv[sys.argv.index('--sortie') + 1])

    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        tsv, v, coupure, fin, frames, duree, autre = jouer(nav)
        nav.close()
    if sortie:
        sortie.write_text(tsv + '\n', encoding='utf-8')

    print('répétition : %d frames du build de playtest en %.0f s, partie de %s'
          % (frames, duree, depouiller.mmss(v['finjeu'])))
    if sortie:
        print('journal écrit dans %s' % sortie)

    p, lignes, ecarts = confronter(tsv, v, coupure, fin)
    depouiller.titre('ce que le jeu a fait, contre ce que le dépouillement en lit')
    afficher(lignes)
    texte, plante, med = relire(p)
    print(texte)

    # L'autre fin, sur la même partie : ce que le rapport en dit doit être vrai aussi.
    tsv2, jeu2 = autre
    p2, lignes2, ecarts2 = confronter_interrompue(tsv2, jeu2)
    depouiller.titre('la même partie, interrompue au dernier signe')
    afficher(lignes2)
    texte2, plante2, med2 = relire(p2)
    print('\n'.join(l for l in texte2.split('\n') if 'INTERROMPUE' in l or 'durée' in l
                    or 'relecture' in l or 'écart médian' in l))

    print()
    echec = False
    for nom, pl, md, ec in (('achevée', plante, med, ecarts), ('interrompue', plante2, med2, ecarts2)):
        if pl:
            print('ÉCHEC (%s) : le rapport de dépouillement plante — %s' % (nom, pl))
        if md is None or abs(md) > 0.05:
            print('ÉCHEC (%s) : le contrôle ΔO de depouiller.py ne tombe pas à 0,0 %% (%s)' % (nom, md))
        if ec:
            print('ÉCHEC (%s) : %d écart%s entre le jeu et le dépouillement : %s'
                  % (nom, len(ec), 's' if len(ec) > 1 else '', ', '.join(ec)))
        echec = echec or bool(pl or ec) or md is None or abs(md) > 0.05
    if echec:
        sys.exit(1)
    print('répétition tenue : le dépouillement lit la partie telle que le jeu l’a jouée, '
          'achevée comme interrompue')


def afficher(lignes):
    for quoi, jeu, lu, ok in lignes:
        print('  %s %-42s %-24s %s' % ('ok ' if ok else 'ÉCART', quoi, str(jeu)[:24], str(lu)[:60]))


def relire(p):
    """Le rapport tel que l'auteur le lira le jour où le journal revient — il doit sortir
    entier —, et l'écart médian du contrôle ΔO."""
    tampon = io.StringIO()
    try:
        with contextlib.redirect_stdout(tampon):
            depouiller.rapport(p, 'répétition')
        plante = None
    except Exception as e:      # noqa: BLE001 — c'est précisément ce qu'on cherche
        plante = repr(e)
    ec, _ = depouiller.controle(p)
    return tampon.getvalue(), plante, (ec[len(ec) // 2] if ec else None)


def confronter_interrompue(tsv, jeu):
    ev = depouiller.lire(io.StringIO(tsv))
    p = [x for x in depouiller.parties(ev) if depouiller.agit(x) >= 5][-1]
    s = depouiller.Rejeu(p).jouer()
    lignes, ecarts = [], []
    def ligne(quoi, a, b, tol=0.0):
        ok = abs(a - b) <= tol if isinstance(a, float) and isinstance(b, float) else a == b
        lignes.append((quoi, a, b, ok))
        if not ok:
            ecarts.append(quoi)
    ligne('interrompue', jeu['fin'] == 'interrompue', s['interrompu'] is not None)
    ligne("arrêt de la partie (min)", round(jeu['t_arret'] / 60, 1),
          round(s['finjeu'] / 60, 1) if s['finjeu'] else None)
    ligne('effacement commencé', False, s['fin'] is not None)
    ligne('relecture ouverte', False, s['relu'] is not None)
    # la coupure entre les deux séances, et le rechargement au pied du dernier signe
    ligne('coupures', 2, len(s['reprises']))
    return p, lignes, ecarts


if __name__ == '__main__':
    main()
