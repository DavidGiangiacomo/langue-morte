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
function tracer(k, d, pos){
  if(TR.length >= TMAX) return;
  const e = [Math.round(S_.t*10)/10, k, d === undefined ? '' : String(d)];
  if(pos === undefined) TR.push(e); else TR.splice(pos, 0, e);
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
enrober('acheterGl', () => S_.gl.length,  a => a[0] + ' (' + byId[a[0]].mot + ') ' + byId[a[0]].cost + ' C');
/* La nuit ne passe pas par `tick` et n'émettrait donc aucune ligne : une seule, au retour,
   dit ce qu'elle a rapporté. Une partie jouée en plusieurs fois se lit alors sans trou. */
enrober('veillee',   () => Math.round(S_.O), () => Math.round(S_.O) + ' occ. hors ligne');

/* Pas de témoin possible pour la fin : `S_.done` est déjà posé quand showEnd() est
   appelée. On remonte donc le relevé jusqu'au dernier « reset » — jeu.js rappelle
   showEnd() à chaque rechargement d'une partie terminée, et on ne veut pas d'une
   ligne « fin » par visite. */
const finDejaTracee = () => {
  for(let i = TR.length-1; i >= 0; i--){
    if(TR[i][1] === 'reset') return false;
    if(TR[i][1] === 'fin')   return true;
  }
  return false;
};
const _showEnd = showEnd;
showEnd = function(){
  const r = _showEnd();
  if(!finDejaTracee()) tracer('fin', mmss(S_.t));
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
$('reset').addEventListener('click', () => { tracer('reset'); prochainEtat = 0; derniereTablette = null; });

setInterval(sauverTraces, 4000);
window.addEventListener('pagehide', sauverTraces);
