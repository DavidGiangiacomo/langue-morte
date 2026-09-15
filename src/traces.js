/* « La langue morte » — journal d'actions horodaté (HORS JEU)
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google.

   Instrumentation de playtest. Les cinq nombres de la carte de fin disent ce qu'une
   partie a produit, jamais *quand* elle s'est grippée : on ne voit ni les rafales de
   recoupement, ni les minutes passées sans rien acheter, ni si les tablettes marquées
   en ocre sont relues. Ce module relève chaque action avec son instant depuis le
   début, plus un état toutes les 30 s pour pouvoir retracer les courbes.

   Il ne modifie aucune règle : il ENVELOPPE les actions déjà déclarées au lieu de
   les éditer. Pour le retirer d'une version publique il suffit donc de supprimer ce
   fichier, sa ligne dans index.html et dans build.py, et les deux boutons de la
   barre « hors jeu ».

   Chargé APRÈS rendu.js — il enveloppe versTablette et mesures — et AVANT jeu.js,
   qui lie les boutons : il faut qu'il lie les enveloppes, pas les originales. */
"use strict";

const TKEY = 'langue-morte-traces-v1';
const TMAX = 20000;              // garde-fou : PT1 avait produit 3 853 clics
let TR = [];
try{ const raw = localStorage.getItem(TKEY); if(raw) TR = JSON.parse(raw) || []; }catch(e){}

/* Une entrée = [instant, genre, détail]. Tableau et pas objet : une partie longue en
   produit des milliers et le tout transite par localStorage à chaque sauvegarde.
   L'instant est en secondes de JEU — celles du chrono, que le sélecteur de vitesse
   accélère. C'est le bon axe : c'est aussi celui de la durée affichée en fin de partie. */
/* Après le dernier signe de l'arbre, `frame()` cesse d'appeler `tick` : le chrono de jeu
   gèle, et toutes les actions de la fenêtre de lecture de FIN-1 se retrouvent au même
   instant — PT10 en a six, toutes à 5795,7, dont quatre recoupements en zéro seconde.
   Les secondes d'horloge et les secondes de jeu sont pourtant équivalentes là : la
   production est arrêtée et le sélecteur de vitesse ne multiplie plus rien. On prolonge donc
   le chrono à l'horloge, et la fenêtre où le joueur est censé LIRE se date enfin. */
let doneT0 = 0;
function tJeu(){
  if(!S_.done){ doneT0 = 0; return S_.t; }
  if(!doneT0) doneT0 = performance.now();
  return S_.t + (performance.now() - doneT0)/1000;
}

function tracer(k, d, pos){
  if(TR.length >= TMAX) return;
  const e = [Math.round(tJeu()*10)/10, k, d === undefined ? '' : String(d)];
  if(pos === undefined) TR.push(e); else TR.splice(pos, 0, e);
  /* La partie s'arrête au dernier signe de l'arbre (règle 16), mais la ligne `fin` ne vient
     qu'avec la CARTE, jusqu'à quatre-vingt-dix secondes plus tard — et PT10 a exporté dans
     l'intervalle : son journal n'a aucune ligne de fin, pour une partie terminée. Les deux
     instants sont distincts et tous les deux intéressants, l'écart entre eux étant le temps
     que met le joueur à retourner sur une tablette que le dernier signe vient de rendre
     lisible — c'est-à-dire la mesure même de FIN-1. Posée ici et pas dans une enveloppe :
     `finArmer` est un `const`, il n'y a rien à envelopper. */
  if(S_.done && k !== 'finjeu' && !dejaTracee('finjeu')) tracer('finjeu', mmss(S_.t));
  majBoutonTraces();
}

/* Enveloppe une action globale. Ne journalise que si elle a EU LIEU : les boutons
   restent cliquables une frame de trop et `formuler` ne fait rien quand les
   occurrences manquent — sans ce témoin, le relevé compterait des clics à vide.
   Rien d'asynchrone ne s'intercale entre les deux lectures : la seule cause de
   changement est l'action elle-même. */
function enrober(nom, temoin, detail){
  const orig = globalThis[nom];
  globalThis[nom] = function(...a){
    const avant = temoin(), rang = TR.length;
    const r = orig.apply(this, a);
    /* Insérée à son rang et non à la fin : une action peut en déclencher une autre —
       le dernier signe termine la partie — et la cause doit précéder l'effet. */
    if(temoin() !== avant) tracer(nom, detail ? detail(a, avant) : '', rang);
    return r;
  };
}

const niveaux = () => S_.b.cop + S_.b.tab + S_.b.con + S_.b.ate + S_.b.gram;

/* `relever` reçoit désormais sa tablette : c'est la seule façon de distinguer un joueur qui
   parcourt le corpus d'un joueur qui s'installe sur une tablette et martèle. La question
   décide du sort du gisement, et elle ne se lit nulle part ailleurs que dans ce journal. */
enrober('relever',   () => S_.clicks,     a => 'tablette ' + a[0]);
enrober('formuler',  () => S_.H);
enrober('recouper',  () => S_.rec,        a => '+' + recGain() + ' cert.'
                                               + (a[0] ? ' · ' + a[0] : ''));
enrober('acheterIns', niveaux,            a => a[0] + ' n°' + S_.b[a[0]]);
/* Le mot retenu, et non le mot juste : sur un signe ambigu, c'est la lecture tranchée qui
   fait la partie, et le ✗ la marque pour le dépouillement. Le joueur, lui, n'en saura rien —
   ce fichier est hors jeu et ne s'ouvre qu'après coup.

   Le degré de doute suit, et lui seul dit ce que le joueur avait sous les yeux en tranchant
   (MOD-2). `CLAUDE.md` l'annonçait dans ce journal depuis le lot ; il n'y était pas, et PT10
   s'est dépouillé sans lui. `acheterGl` le fige à l'instant du choix, juste avant qu'on le
   lise ici. Sur un signe non ambigu il ne veut rien dire et n'est pas écrit. */
enrober('acheterGl', () => S_.gl.length,  a => a[0] + ' (' + motDe(a[0]) + ')'
                                               + (faux(a[0]) ? ' ✗' : '')
                                               + ' ' + byId[a[0]].cost + ' C'
                                               + (AMB[a[0]] ? ' · doute ' + douteDe(a[0]) : ''));
/* La nuit ne passe pas par `tick` et n'émettrait donc aucune ligne : une seule, au retour,
   dit ce qu'elle a rapporté. Une partie jouée en plusieurs fois se lit alors sans trou. */
enrober('veillee',   () => Math.round(S_.O), () => Math.round(S_.O) + ' occ. hors ligne');
/* La concordance ne coûte rien et ne produit rien : elle ne laisserait aucune trace dans
   les ressources. C'est pourtant le geste que PT9 doit mesurer — quels signes le joueur
   rassemble, et s'il le fait du tout. */
enrober('concChoisir', () => concSel, a => a[0] + ' · ' + concN + ' attest.');
/* La composition. Le témoin est le compteur de tentatives et non la longueur du carnet : une
   paire juste qu'on n'a pas les moyens de payer n'y entre pas, et son essai passerait à la
   trappe. PT10 doit pouvoir compter les tentatives, voir sur quelles paires, et à quelle
   minute — c'est la seule façon de savoir si ⟨grenier⟩ se trouve en lisant.

   Le ✓ seul ne suffisait pas, et PT10 l'a montré en creux : ses six tentatives s'y lisaient
   comme cinq échecs et une réussite, alors que les six paires étaient JUSTES — `tab+sar`
   (archive) et `im+sar` (scribe) deux fois chacune, `en+la` (sinon) une fois, toutes refusées
   faute de Certitude et non faute d'avoir trouvé. Le dépouillement concluait au balayage
   aveugle là où le joueur avait tout lu, et le carnet est resté vide : `compCost()` n'a jamais
   quitté 250 hypothèses. Trois issues, donc, et le ✓ porte sur la PAIRE et non sur l'achat :
     `ur + tem ✓ urtem`                        juste, payée, acquise
     `tab + sar ✓ tabsar · impayable (900 C)`  juste, pas les moyens ; ne va pas au carnet
     `im + ur ✗ carnet`                        fausse : 250 hypothèses et une ligne de carnet
   Le ✗ d'`acheterGl` marque une lecture fausse, celui-ci une paire qui n'existe pas ; ils ne
   se rencontrent jamais sur la même ligne. */
enrober('composer', () => S_.comp, a => {
  const cible = recetteDe(a[0], a[1]);
  return a[0] + ' + ' + a[1]
       + (!cible     ? ' ✗ carnet'
        : has(cible) ? ' ✓ ' + cible
                     : ' ✓ ' + cible + ' · impayable (' + byId[cible].cost + ' C)');
});

/* La révision (CONTR-2) — la seule action du jeu qui ne laissait aucune trace, et PT10 est
   tombé dedans : zéro ligne, ce qui ne distingue pas « il n'a pas révisé » de « on ne le
   mesurait pas ». C'est pourtant la première question que MOD-2 pose au playtest — combien
   de révisions, et sur quels signes.
   Pas d'`enrober` ici : le détail a besoin de l'état d'AVANT — la lecture quittée, le doute
   quitté, le prix payé — que le témoin ne transporte pas. Rien de tracé ne s'imbrique dans
   `reviser`, qui ne fait que repeindre et, au mieux, lever la contradiction. */
const _reviser = reviser;
reviser = function(id, lect){
  const mot = motDe(id), marque = faux(id) ? ' ✗' : '', dte = douteDe(id), cout = revCost();
  const r = _reviser(id, lect);
  /* Le doute de départ et celui d'arrivée sur la même ligne : c'est la réponse à la seconde
     question de MOD-2. S'il a baissé, le joueur a travaillé le signe entre les deux — il
     concorde donc AVANT de re-trancher, et le panneau pointe vers quelque chose d'atteignable.
     S'il n'a pas bougé, la révision s'est jouée à l'aveugle, sur le seul chiffre du panneau. */
  if(r) tracer('reviser', id + ' · ' + mot + marque
                             + ' → ' + motDe(id) + (faux(id) ? ' ✗' : '')
                             + ' · ' + cout + ' C · doute ' + dte + ' → ' + douteDe(id));
  return r;
};

/* Pas de témoin possible pour la fin : `S_.done` est déjà posé quand showEnd() est
   appelée. On remonte donc le relevé jusqu'au dernier « reset » — jeu.js rappelle
   showEnd() à chaque rechargement d'une partie terminée, et on ne veut pas d'une
   ligne « fin » par visite. */
const dejaTracee = genre => {
  for(let i = TR.length-1; i >= 0; i--){
    if(TR[i][1] === 'reset') return false;
    if(TR[i][1] === genre)   return true;
  }
  return false;
};
const _showEnd = showEnd;
showEnd = function(){
  const r = _showEnd();
  if(!dejaTracee('fin')) tracer('fin', mmss(S_.t));
  return r;
};

/* La navigation dit si la barre de tablettes sert. On ignore les sauts qui n'aboutissent
   pas ailleurs, sinon maintenir `j` en fin de corpus remplirait le relevé. */
let derniereTablette = null;
const _versTablette = versTablette;
versTablette = function(t){
  const r = _versTablette(t);
  const el = elCorpus.querySelector('.tablet[data-tb="' + t + '"]');
  if(el && !el.hidden && t !== derniereTablette){ derniereTablette = t; tracer('tablette', t); }
  return r;
};

/* Relevé d'état toutes les 30 s de jeu. Sans lui on a les actions mais pas les courbes,
   et c'est justement l'écart entre les deux qui montre où la partie s'enlise.
   Accroché à `tick` et non à un setInterval : il doit suivre le temps de jeu, pas
   l'horloge, sinon le sélecteur de vitesse fausse l'échantillonnage. */
let prochainEtat = 0;
const _tick = tick;
tick = function(dt){
  _tick(dt);
  if(S_.t >= prochainEtat){
    prochainEtat = Math.floor(S_.t / 30) * 30 + 30;
    const m = mesures();
    tracer('etat', 'O=' + Math.round(S_.O) + ' H=' + Math.round(S_.H) + ' C=' + Math.round(S_.C)
                 + ' signes=' + S_.gl.length + ' sig%=' + m.sig + ' lig%=' + m.lig
                 + ' gis=' + Object.keys(S_.rel).reduce((n,t)=>n+S_.rel[t].length,0) + '/' + GIS_TOTAL
                 + ' instr=' + [S_.b.cop, S_.b.tab, S_.b.con, S_.b.ate, S_.b.gram].join('/'));
  }
};

/* ============================ export ============================ */
const mmss = s => Math.floor(s/60) + ':' + String(Math.floor(s%60)).padStart(2,'0');

function tracesTSV(){
  const d = new Date(), p = n => String(n).padStart(2,'0');
  const horo = d.getFullYear() + '-' + p(d.getMonth()+1) + '-' + p(d.getDate())
             + ' ' + p(d.getHours()) + ':' + p(d.getMinutes());
  return [
    '# La langue morte — journal d\'actions',
    '# exporté le ' + horo + ' · ' + TR.length + ' entrées',
    '# t = secondes de JEU depuis le début (le sélecteur ×3/×10 les accélère)',
    '# une ligne « reset » marque le début d\'une nouvelle partie : le temps y repart de zéro',
    '# « finjeu » = dernier signe de l\'arbre, la production s\'arrête ; « fin » = la carte s\'ouvre',
    '#   entre les deux le chrono de jeu est gelé : t y compte des secondes d\'horloge',
    ['temps','t_s','genre','détail'].join('\t'),
    ...TR.map(([t,k,d]) => [mmss(t), t.toFixed(1), k, d].join('\t'))
  ].join('\n');
}

function majBoutonTraces(){
  const b = $('tr-dl');
  if(b){ const txt = 'traces · ' + nf.format(TR.length); if(b.textContent !== txt) b.textContent = txt; }
}

function sauverTraces(){ try{ localStorage.setItem(TKEY, JSON.stringify(TR)); }catch(e){} }

if(!TR.length) tracer('debut');
majBoutonTraces();

$('tr-dl').addEventListener('click', () => {
  const d = new Date(), p = n => String(n).padStart(2,'0');
  const nom = 'traces-' + d.getFullYear() + p(d.getMonth()+1) + p(d.getDate())
            + '-' + p(d.getHours()) + p(d.getMinutes()) + '.tsv';
  const url = URL.createObjectURL(new Blob([tracesTSV()], {type:'text/tab-separated-values'}));
  const a = Object.assign(document.createElement('a'), {href:url, download:nom});
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});

$('tr-cp').addEventListener('click', e => {
  const b = e.currentTarget;
  navigator.clipboard.writeText(tracesTSV())
    .then(() => { b.textContent = 'copié'; setTimeout(() => b.textContent = 'copier', 1200); })
    .catch(() => { b.textContent = 'refusé'; setTimeout(() => b.textContent = 'copier', 1200); });
});

/* La partie repart, le relevé non : on garde tout et on marque la coupure. Une soirée
   de playtest tient dans un seul fichier, et rien n'est perdu par un reset distrait. */
$('reset').addEventListener('click', () => {
  tracer('reset'); prochainEtat = 0; derniereTablette = null; doneT0 = 0; });

setInterval(sauverTraces, 4000);
window.addEventListener('pagehide', sauverTraces);
