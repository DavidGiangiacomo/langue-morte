/* « La langue morte » — tracés des 45 signes, composés, numération
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */

"use strict";

/* ============================ signes ============================ */
const P = {
  u1:'M10 4 L10 22',
  u5:'M4 5 L10 21 L16 5',
  t10:'M16.5 13 A6.5 6.5 0 1 1 3.5 13 A6.5 6.5 0 1 1 16.5 13',
  t50:'M16.5 13 A6.5 6.5 0 1 1 3.5 13 A6.5 6.5 0 1 1 16.5 13 M2 13 H18',
  h100:'M10 3 L18 13 L10 23 L2 13 Z',
  h500:'M10 3 L18 13 L10 23 L2 13 Z M2 13 H18',
  k1000:'M10 3 V23 M2 13 H18 M4.5 7.5 L15.5 18.5 M15.5 7.5 L4.5 18.5',
  anna:'M6 4 L6 22 M14 4 L14 22',
  tem:'M10 23 V6 M10 8 L5 12 M10 8 L15 12 M10 13.5 L6 17 M10 13.5 L14 17',
  kish:'M2 9 Q6 5 10 9 T18 9 M2 17 Q6 13 10 17 T18 17',
  gan:'M3 6 H17 V20 H3 Z M3 13 H17 M10 6 V20',
  ur:'M3 21 V11 L10 5 L17 11 V21 Z',
  tab:'M4 5 H16 V21 H4 Z M7 10 H13 M7 13.5 H13 M7 17 H11',
  im:'M4 17 Q10 11 16 17 M6 6 L8 10 M10 4 V9 M14 6 L12 10',
  sar:'M5 22 L14 7.5 M11.5 5 L17 8.5 L14 12.5 Z',
  kal:'M6 5 V21 M12 5 V21 M4 5 H8 M10 5 H14',
  shen:'M2 13 Q10 5 18 13 Q10 21 2 13 Z M12 13 A2 2 0 1 1 8 13 A2 2 0 1 1 12 13',
  nur:'M14 13 A4 4 0 1 1 6 13 A4 4 0 1 1 14 13 M10 2 V5 M10 21 V24 M2 13 H5 M15 13 H18',
  mu:'M10 22 V9 M11.5 5.5 A1.5 1.5 0 1 1 8.5 5.5 A1.5 1.5 0 1 1 11.5 5.5',
  ta:'M10 22 V9 M10 9 L15 6.5 M17.5 5 A1.5 1.5 0 1 1 14.5 5 A1.5 1.5 0 1 1 17.5 5',
  hal:'M10 3 V23 M3 19 L17 7',
  mesh:'M10 23 V13 M10 13 C3.5 13 3.5 5 10 5 C16.5 5 16.5 13 10 13 Z',
  pat:'M14 4 L6 13 L14 22',
  la:'M4 22 L16 4',
  dun:'M3 9 H17 M3 17 H17',
  zur:'M6 4 L14 13 L6 22',
  esh:'M14 3 A10 10 0 1 0 14 23 A7.5 7.5 0 1 1 14 3',
  en:'M10 22 V14 M10 14 L4 6 M10 14 L16 6',
  mik:'M10 4 V9 M10 12 V17 M10 20 V23',
  lash:'M4 6 L16 20 M16 6 L4 20',
  nash:'M7 22 V9 M13 22 V9 M11.5 5.5 A1.5 1.5 0 1 1 8.5 5.5 A1.5 1.5 0 1 1 11.5 5.5',
  ke:'M4 21 Q10 21 10 13 Q10 5 16 5 M16 5 L12 2 M16 5 L12 8',
  nm1:'M2 7 Q6 3 10 7 T18 7 M2 13 Q6 9 10 13 T18 13 M2 19 Q6 15 10 19 T18 19',
  nm2:'M3 22 V12 H8 V22 M8 12 V6 H13 V22 M13 12 H17 V22 M2 22 H18',
  nm3:'M4 4 L10 13 L4 22 M16 4 V22 M10 13 H16',
  nm4:'M10 3 L17 10 L10 17 L3 10 Z M10 17 V23',
  nm5:'M4 20 Q10 2 16 20 M6 14 H14 M10 20 V23',
  nm6:'M5 5 H15 M10 5 V21 M5 21 H15 M7 13 H13'
};
/* Un glyphe de la branche Nombre partage le tracé de son signe de numération : ⟨un⟩ le mot
   et ⟨1⟩ le chiffre sont le même trait. La table les nomme une seule fois, dans les deux sens.
   `sv()` la lit par la gauche pour dessiner ; la composition la lit par la droite, parce qu'un
   joueur qui pose ⟨un⟩ pose le glyphe `an`, et que `COMP` l'attend sous le nom `u1`. */
const ALIAS = { an:'u1', hem:'u5', sela:'t10', meku:'h100', mille:'k1000' };
for(const g in ALIAS) P[g] = P[ALIAS[g]];
const GLTRACE = Object.fromEntries(Object.entries(ALIAS).map(([g,t]) => [t,g]));

/* Les composés se voient comme composés : le signe de « deux » EST le signe de « un »
   redoublé, celui de « grenier » contient « maison » et « grain ». Le joueur reconnaît
   les parties avant de savoir lire le tout — c'est l'intuition que la mécanique de
   composition des actes III+ viendra formaliser. */
const COMP = {
  anna:['u1','u1'],      lan:['la','u1'],       selanna:['t10','t10'],
  urtem:['ur','tem'],    tabsar:['tab','sar'],  shenu:['shen','nash'],
  nurnur:['nur','nur'],  nurhal:['nur','hal'],  mula:['mu','la'],
  nashal:['nash','hal'], meshke:['mesh','ke'],  halnash:['hal','nash'],
  shenke:['shen','ke'],  imme:['im','sar'],     halan:['hal','u1'],
  enla:['en','la'],      taru:['ta','en']
};
/* Le tracé d'un composé, à partir de ses deux parties. Sorti de `sv()` pour que la grille de
   composition puisse dessiner une paire qui n'est PAS dans COMP : le joueur doit voir le signe
   qu'il propose avant de savoir s'il existe — c'est tout ce que la grille lui donne, et c'est
   ce qui la garde du côté de la lecture. Pas de cache ici : il est indexé par id de composé,
   et une paire quelconque n'en a pas. */
function svPaire(a, b){
  return '<svg class="gl gl2" viewBox="0 0 34 26" aria-hidden="true">'
       + '<g transform="translate(0,2.6) scale(0.8)"><path d="'+P[a]+'"/></g>'
       + '<g transform="translate(17,2.6) scale(0.8)"><path d="'+P[b]+'"/></g></svg>';
}
const svCache = {};
function sv(k){
  if(svCache[k]) return svCache[k];
  let out;
  if(COMP[k]){
    out = svPaire(COMP[k][0], COMP[k][1]);
  } else if(P[k]){
    out = '<svg class="gl" viewBox="0 0 20 26" aria-hidden="true"><path d="'+P[k]+'"/></svg>';
  } else {
    out = '<svg class="gl" viewBox="0 0 20 26" aria-hidden="true"><path d="M6 6 H14 M6 20 H14 M10 6 V20"/></svg>';
  }
  return (svCache[k] = out);
}

/* numération : additive, 1 · 5 · 10 · 50 · 100 · 500 · 1000 */
const STEPS = [[1000,'k1000'],[500,'h500'],[100,'h100'],[50,'t50'],[10,'t10'],[5,'u5'],[1,'u1']];

/* Chaque glyphe de la branche NOMBRE ouvre un ou plusieurs signes de numération.
   `hem` (cinq) en ouvre trois d'un coup : comprendre qu'un signe vaut cinq du rang
   inférieur, c'est une seule idée, valable à tous les rangs.
   `anna` (deux) n'ouvre AUCUN signe — il ouvre le principe du redoublement. Savoir que
   ▏ vaut un ne dit rien de ce que vaut ▏▏ : tant qu'on ne l'a pas, on ne sait lire qu'un
   nombre où chaque signe n'apparaît qu'une seule fois. */
const NUMSYM = { an:['u1'], hem:['u5','t50','h500'], sela:['t10'], meku:['h100'], mille:['k1000'] };
let SU = new Set();
function majSignes(){ SU = new Set(); for(const g in NUMSYM) if(has(g)) NUMSYM[g].forEach(k=>SU.add(k)); }

function numSyms(n){
  const out=[]; let left=Math.max(0,Math.floor(n));
  for(const [v,k] of STEPS){ while(left>=v && out.length<24){ out.push(k); left-=v; } }
  return out;
}
/* Un nombre du corpus ne passe en chiffres que si le joueur connaît chacun de ses signes.
   Avec `un` seul, « champ 3 » se lit et « grain 212 » reste opaque : c'est ce qu'il sait. */
function numLisible(n){
  n = Math.floor(n);
  if(n === 0) return has('lan');
  const sy = numSyms(n);
  if(!sy.length) return false;
  for(const k of sy) if(!SU.has(k)) return false;
  if(!has('anna')){
    const vus = new Set();
    for(const k of sy){ if(vus.has(k)) return false; vus.add(k); }
  }
  return true;
}

const numCache = {};
function numGlyphs(n){
  n = Math.max(0, Math.floor(n));
  if(numCache[n]) return numCache[n];
  let out = n===0 ? [sv('lan')] : numSyms(n).map(sv);
  if(!out.length) out=[sv('lan')];
  const s = '<span class="numgl">'+out.join('')+'</span>';
  if(n<=2000) numCache[n]=s;
  return s;
}
