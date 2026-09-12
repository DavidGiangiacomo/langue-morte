/* « La langue morte » — état, ressources, instruments, boucle de simulation
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ état ============================ */
/* Changé à l'ouverture de l'acte III : une partie sauvegardée au MVP est `done` à treize
   glyphes et rouvrirait sur l'écran de fin, sans moyen de continuer. */
const KEY='langue-morte-actes-i-iii';
const fresh = () => ({O:0,H:0,C:0,rec:0,clicks:0,b:{cop:0,tab:0,con:0,ate:0,gram:0},gl:[],t:0,done:false,
  rel:{}, prix:{}, carnet:[], comp:0});
/* rel : jetons relevés par tablette · prix : tarif du gisement, verrouillé
   carnet : les paires déjà tentées et fausses · comp : le nombre de tentatives, toutes issues
   confondues — c'est lui que PT10 doit lire, pas la seule liste des échecs.
   Champs de premier niveau, donc une partie d'avant la composition les reçoit vides au
   chargement, sans qu'on touche à `KEY`. */
let S_ = fresh(), speed = 1;
try{ const raw=localStorage.getItem(KEY); if(raw){ const p=JSON.parse(raw);
  if(p&&p.b){ const b=Object.assign({cop:0,tab:0,con:0,ate:0,gram:0},p.b); S_=Object.assign(fresh(),p); S_.b=b; } } }catch(e){}
const has = id => S_.gl.indexOf(id)>=0;
/* Ce que l'arbre a rendu, qui n'est pas ce que le joueur sait : un composé secret s'acquiert
   hors de toute branche. Les deux comptes se confondaient tant qu'il n'y avait qu'une façon
   d'apprendre un signe ; depuis la grille de composition, tout ce qui mesure une PROGRESSION
   passe par ici — la fin de partie, les tablettes dégagées (`revCount`), la Grammaire
   (`gramMul`), le gain du recoupement et le compteur du lexique. Les confondre ferait avancer
   le jeu en composant, et déplacerait une économie réglée sur neuf playtests.
   Ce que le joueur COMPREND se mesure ailleurs, dans le corpus : `mesures()`, qui compte bien
   le grenier parce que c'est justement ce qu'il a gagné. */
const nArbre = () => { let n=0; for(const id of S_.gl){ const g=byId[id]; if(!g||!g.sec) n++; } return n; };
/* Une partie finie quand l'arbre comptait moins de signes n'est plus finie : l'arbre a
   grandi sous elle. Sans ça elle rouvrirait sur l'écran de fin, `tick` arrêté, sans moyen
   de continuer — le cas exact qui a déjà coûté un changement de `KEY` et toutes les
   parties en cours. Chaque lot de glyphes le reproduirait. */
if(S_.done && nArbre() < NGL) S_.done = false;

/* ---- économie ---- */
const M = {
  click:()=> 1*(has('anna')?1.25:1)*(has('tab')?1.5:1)*(has('kal')?2:1),
  cop:  ()=> (has('tem')?1.3:1)*(has('kal')?2:1)*(has('imme')?1.5:1),
  /* L'atelier suivait le copiste jusqu'à l'acte III ; les deux bonus de la branche Temps
     le détachent — c'est le seul instrument qui porte encore l'échelle des occurrences
     quand la Certitude, elle, passe à la grammaire. `scribe` porte les deux : l'atelier
     n'est qu'une salle pleine de scribes.
     `il-faut` le porte aussi, bien qu'il soit le signe dessiné SUR l'instrument Grammaire :
     la consigne du corpus est « il-faut copier », gravée vingt-sept fois, et l'atelier est la
     salle où on la suit. Mesuré au passage — ce bonus-là ne déplace pas la durée de l'acte
     (87,0 min avec ou sans), parce qu'en fin de partie les occurrences ne sont plus ce qui
     manque ; un bonus de grammaire l'aurait raccourci de cinq minutes. La Modalité reçoit
     donc ce qui se lit, pas ce qui accélère. */
  ate:  ()=> (has('tem')?1.3:1)*(has('kal')?2:1)*(has('mille')?1.3:1)*(has('nurhal')?1.5:1)*(has('imme')?1.5:1)
             *(has('dun')?1.5:1),
  tabl: ()=> (has('kish')?1.3:1)*(has('kal')?2:1)*(has('tabsar')?1.5:1),
  con:  ()=> (has('sar')?1.5:1)*(has('kal')?2:1),
  /* `lire` est le piège majeur de l'ambiguïté (docs/corpus.md §7) : sa lecture fausse,
     « compter », devra rendre 25 % de plus. Il lui faut donc un effet chiffré, et c'est
     celui de l'instrument qui lit. */
  gram: ()=> (has('nurnur')?1.5:1)*(has('kal')?2:1)*(has('shen')?1.5:1)
};
/* production brute d'occurrences par seconde (sert au barème du relevé manuel) */
const oBrut = () => S_.b.cop*1.0*M.cop() + S_.b.ate*25*M.ate();

/* ---- le relevé, acte de lecture ----
   PT5 : 414 relevés, tous au bouton, aucun dans le corpus, pour 0,6 % des occurrences de
   la partie. Le geste ne faisait rien et le texte n'était qu'un décor. Le relevé se fait
   désormais dans le corpus, sur un signe, et chaque tablette n'offre qu'un gisement fini —
   un dixième de ses jetons. Il faut donc parcourir le texte, et non marteler un point.

   Trois pièges, tous trouvés au simulateur avant d'écrire une ligne de jeu :

   1. Un gisement qui coupe vraiment verrouille l'ouverture : les quatre tablettes du départ
      n'offrent que 13 relevés quand le premier Copiste en coûte 15. Épuisé, le gisement
      rend donc le plancher (1), jamais zéro — et au départ, débit nul, les deux se valent.
   2. Un tarif indexé sur le débit courant se thésaurise : ne rien relever pendant quarante
      minutes puis tout vider au débit maximal donnait 72 % des occurrences au lieu de 17 %.
      Le tarif d'une tablette est donc figé — mais **au premier relevé qu'on y fait**, et
      non à son dégagement. Le figer au dégagement laissait à 1 ou 2 occurrences, pour
      toute la partie, les seules tablettes qu'on atteint tôt : PT6 a mesuré la main à
      0,1 % des occurrences, moins bien qu'avec le bouton qu'on venait de supprimer.
      Arriver sur une tablette neuve à la trentième minute vaut maintenant plus de mille
      occurrences par relevé, et c'est ce qui doit donner envie d'y aller.
      La thésaurisation reste possible — garder les tablettes neuves pour la fin donne
      42 % des occurrences au lieu de 19 — mais elle se punit d'elle-même : le simulateur
      lui fait finir la partie 4,7 minutes plus tard, faute des occurrences du début.
   3. Le gisement, et non la vitesse de la main, décide de ce que la main rapporte : à 5, 15
      ou 40 clics/minute la part est la même. Le cliqueur frénétique et le joueur posé
      convergent — c'est ce qui rend structurellement impossible le défaut de PT1.

   Mesuré (`python outils/sim.py`) : 44,4 à 51,3 min pour une cible de 45, I6 ≤ 29,96 %,
   la main fournit 14 à 19 % des occurrences contre 0,6 % en PT5. La marge sur I6 est
   nulle et le simulateur sous-estime de trois points (PT5 : 27,8 % simulé, 30,8 % réel) —
   à revérifier au premier playtest, c'est la mesure qui tranche. */
const REL_K = 1.2;      // un relevé neuf vaut 1,5 seconde de production, au tarif de la tablette
const REL_DIV = 10;     // gisement d'une tablette = ses jetons / REL_DIV

const GISEMENT = {};
for(const tb of CORPUS) GISEMENT[tb.t] = Math.ceil(
  tb.l.reduce((n,l)=> n + l.split(' ').filter(tk=>tk!=='·').length, 0) / REL_DIV);
const GIS_TOTAL = Object.values(GISEMENT).reduce((a,b)=>a+b, 0);

const gisFait  = t => (S_.rel[t] || []).length;
const gisReste = t => GISEMENT[t] - gisFait(t);
/* tarif d'un relevé neuf, figé au premier relevé fait sur la tablette (cf. relever()) */
const tarifRel = () => (1 + REL_K*oBrut()) * M.click();
const releveVal = t => (t !== undefined && gisReste(t) > 0) ? (S_.prix[t] || 1) : M.click();

/* Réglage sorti de PT4. Le recoupement manuel fournissait 43 % de la Certitude, pour un
   plafond I6 de 30 %. Plafonner son gain ne change rien — le joueur recoupe simplement
   plus souvent : seule la croissance de son coût mord. Les 30 % rendus à la concordance
   redonnent à la chaîne d'instruments ce qu'on retire à la main, si bien que la partie ne
   s'allonge pas. Mesuré alors, à REC_R = 1,18 : I6 = 27,8 %, 52,7 min.
   Nommées parce qu'elles servaient à trois endroits chacune, et que c'est cette
   duplication-là qui avait laissé le simulateur diverger du jeu.

   09/09/2026 — REC_R passe à 1,30. La tranche 20-30 min tenait 36 % et résistait à toute la
   famille des prix : 27 combinaisons de cop_b/tab_b/con_b, aucune sous 28 %. Une analyse de
   sensibilité, une constante à la fois, confirme la phrase ci-dessus cinq playtests plus
   tard — rec_o, rec_h et rec_max sont inertes, seul REC_R déplace la tranche. Et on sait
   maintenant pourquoi : le joueur recoupe tant que le coût reste sous une fraction de son
   stock, lequel croît exponentiellement. Un coût de base doublé, c'est quelques secondes de
   retard que l'exponentielle efface ; seul le taux mord. Vrai de toute cette économie.
   Renchérir le recoupement allonge la partie — d'où le premier Copiste ramené de 15 à 10,
   qui la raccourcit d'autant. Mesuré : 71,8-76,1 min, écart max 5,6, toutes les tranches à
   partir de dix minutes sous 26 %, 32 recoupements au lieu de 49 (`python outils/sim.py`).
   Aucun playtest derrière : PT10 doit compter les recoupements. Sous une vingtaine sur la
   partie, ce réglage a vidé un des deux gestes manuels (règle 8) et il faut le défaire. */
const REC_R = 1.30;     // croissance du coût du recoupement, par usage
const CON_P = 0.0039;   // certitude par seconde et par concordance

/* ---- la Grammaire, instrument de l'acte III ----
   Les quatre premiers instruments rendent toujours le même service : leur nombre seul
   décide de ce qu'ils produisent. La Grammaire est le premier dont le rendement dépend
   de ce que le joueur a compris — chaque signe déchiffré aide à en déchiffrer d'autres,
   et c'est la première vraie exponentielle du jeu (design doc §5).
   Elle boit aussi six fois plus d'hypothèses qu'une Concordance, et ce n'est pas un
   détail d'équilibrage : PT7 a fini avec 5 232 hypothèses en réserve et un joueur qui
   les convertissait à la main faute d'instrument capable de les absorber — 103 % de la
   Certitude des cinq dernières minutes venait du recoupement. */
const GRAM_P = 0.0012;  // certitude par seconde et par grammaire, avant l'effet du lexique
const GRAM_R = 1.16;    // ... qui croît de 16 % par signe déchiffré
const GRAM_C = 3.0;     // hypothèses par seconde consommées
const gramMul = () => Math.pow(GRAM_R, nArbre());

const INS = [
  {k:'cop', nom:'Copiste',              sig:'sar',  base:10,   r:1.12,
   ds:()=>'+'+f(1.0*M.cop(),1)+' occ./s',  unlock:()=>true},
  {k:'tab', nom:'Table de fréquences',  sig:'tab',  base:100,  r:1.15,
   ds:()=>'−1 occ./s → +'+f(0.6*M.tabl(),2)+' hyp./s', unlock:()=>S_.b.cop>0||S_.O>=70},
  {k:'con', nom:'Concordance',          sig:'gan',  base:450,  r:1.18,
   ds:()=>'−0,5 hyp./s → +'+f(CON_P*M.con(),4)+' cert./s', unlock:()=>S_.b.tab>0||S_.H>=15},
  {k:'ate', nom:'Atelier de copie',     sig:'kal',  base:1800, r:1.15,
   ds:()=>'+'+f(25*M.ate(),0)+' occ./s',   unlock:()=>S_.b.con>0||S_.O>=900},
  {k:'gram',nom:'Grammaire',            sig:'dun',  base:12000,r:1.20,
   ds:()=>'−'+f(GRAM_C,0)+' hyp./s → +'+f(GRAM_P*gramMul()*M.gram(),4)+' cert./s',
   unlock:()=>has('nur')}
];
const insCost = i => Math.ceil(i.base*Math.pow(i.r,S_.b[i.k]));
const recCost = () => { const m=Math.pow(REC_R,S_.rec)*(has('gan')?0.75:1);
  return {O:Math.ceil(12*m), H:Math.ceil(3*m)}; };
const recGain = () => Math.min(3, 1 + Math.floor(nArbre()/5));
const hypCost = () => 3;

/* ---- formats ---- */
const nf = new Intl.NumberFormat('fr-FR');
function f(n,d){ return n.toFixed(d).replace('.',','); }
function big(n){
  n = Math.floor(n);
  if(has('meku')){
    if(n>=1e9) return f(n/1e9,2)+' Md';
    if(n>=1e6) return f(n/1e6,2)+' M';
    if(n>=1e4) return f(n/1e3,1)+' k';
  }
  return nf.format(n);
}
const readN  = () => has('an');
const readC  = () => has('anna');
const readR  = () => has('sela');
function amount(n, lisible){ return lisible ? big(n) : numGlyphs(n); }

/* ============================ actions ============================ */
/* t : numéro de tablette, j : rang du jeton dans cette tablette. Un jeton déjà relevé,
   ou une tablette épuisée, ne rend que le plancher : c'est le déplacement qui paie. */
function relever(t, j){
  const l = S_.rel[t] || (S_.rel[t] = []);
  const neuf = t !== undefined && l.length < GISEMENT[t] && l.indexOf(j) < 0;
  /* Première visite : la tablette prend le tarif du débit courant, une fois pour toutes.
     C'est ce qui fait qu'ouvrir une tablette restée intacte vaut de plus en plus cher —
     et donc qu'il reste une raison de parcourir le corpus après la quinzième minute. */
  if(neuf && S_.prix[t] === undefined) S_.prix[t] = tarifRel();
  S_.O += neuf ? S_.prix[t] : M.click();
  if(neuf){
    l.push(j);
    /* Le dire au moment où ça arrive : la cellule qui s'éteint dans la barre est le seul
       autre signal, et le joueur regarde le texte, pas la barre. */
    if(l.length === GISEMENT[t]) pushLog('Tablette '+t+' : plus rien à en tirer.');
  }
  S_.clicks++;
}
function formuler(){ const c=hypCost(); if(S_.O>=c){ S_.O-=c; S_.H+=1; } }
/* « Recouper deux passages » : le rapprochement de deux attestations d'un même signe,
   dans deux tablettes différentes. Le choix des deux passages se fait dans le corpus
   (recChoisir() dans rendu.js) ; ici il ne reste que la transaction, inchangée depuis PT4 —
   même coût, même gain, même part dans I6. Seul le geste a bougé.
   `id` ne sert pas à l'économie : il sert au journal d'actions, qui doit pouvoir dire si
   le joueur recoupe des signes fréquents ou rares. */
function recouper(id){
  const c=recCost();
  if(S_.O<c.O||S_.H<c.H) return false;
  S_.O-=c.O; S_.H-=c.H; S_.C+=recGain(); S_.rec++;
  return true;
}
/* ---- la composition ----
   « Poser un signe sur un autre » (design doc §7). Le joueur ne cherche pas au hasard : les
   dix-sept composés sont dessinés comme composés depuis le premier écran, et ⟨grenier⟩ porte
   ⟨maison⟩ et ⟨grain⟩ dans vingt-quatre lignes du corpus. L'indice est dans le texte, il n'est
   nulle part ailleurs, et la grille ne dit jamais si une paire existe avant qu'on la pose.

   L'échec ne coûte QUE des hypothèses (R3) — jamais de Certitude, qui est la mesure de ce
   qu'on a compris et ne peut pas se perdre à une erreur. Il croît vite, et c'est là toute la
   mécanique : le stock d'hypothèses à l'ouverture de la grille est de l'ordre de vingt mille,
   pour environ six cents par minute nettes une fois la Grammaire installée. Une tentative
   coûte alors une vingtaine de secondes, cinq en coûtent quatre minutes, dix en coûtent
   vingt-sept, et quinze sont hors de portée — quand il y a plus de deux cents paires à
   balayer. Lire revient donc structurellement moins cher que chercher, ce qui est le cœur du
   design (design doc §8) et la réponse au risque R3. Mesuré à `python outils/sim.py`.

   Une paire déjà fausse ne se retente pas : elle est au carnet, et le jeu la refuse au lieu
   de la faire repayer. On ne punit pas l'oubli, on empêche seulement de balayer. */
const COMP_H = 250;     // hypothèses perdues à la première tentative fausse
const COMP_R = 1.40;    // ... et par tentative fausse déjà inscrite au carnet
const compCost  = () => Math.ceil(COMP_H*Math.pow(COMP_R, S_.carnet.length));
const compOuvre = () => has('nur');   // même porte que la Grammaire : l'acte III s'ouvre là
const auCarnet  = (a,b) => S_.carnet.indexOf(a+'+'+b) >= 0;

/* Rend ce qui s'est passé — 'acquis', 'rate', ou 'refus' quand rien n'a bougé. Le corpus,
   le journal et la peinture sont l'affaire d'`acheterGl`, qui les fait déjà tous. */
function composer(a, b){
  if(!compOuvre() || !has(a) || !has(b) || auCarnet(a, b)) return 'refus';
  const cible = recetteDe(a, b);
  if(cible && has(cible)) return 'refus';        // déjà lu : il n'y a plus rien à trouver
  const c = compCost();
  if(S_.H < c) return 'refus';                   // pas de quoi engager la tentative
  S_.comp++;
  if(cible && S_.C >= byId[cible].cost){
    acheterGl(cible);                            // le coût est en Certitude, et lui seul
    return 'acquis';
  }
  /* La tentative a eu lieu : les hypothèses sont perdues dans les deux cas. Une paire juste
     qu'on n'a pas les moyens de payer n'entre PAS au carnet — elle se retentera plus tard —
     mais elle coûte comme une autre et ne se distingue de rien à l'écran. Sans ça, l'absence
     de perte dirait au joueur qu'il vient de trouver. */
  S_.H -= c;
  if(!cible) S_.carnet.push(a+'+'+b);
  pushLog('Rien ne vient. Ces deux signes ne se rencontrent nulle part.');
  return 'rate';
}
function acheterIns(k){ const i=INS.find(x=>x.k===k), c=insCost(i);
  if(i.unlock()&&S_.O>=c){ S_.O-=c; S_.b[k]++; } }
function acheterGl(id){
  const g=byId[id]; if(has(id)||S_.C<g.cost) return;
  const avant = CORPUS.map(pctTablette);
  S_.C-=g.cost; S_.gl.push(id);
  majSignes();
  numCache.length = 0;
  touchees = new Set();
  CORPUS.forEach((tb,i)=>{ if(pctTablette(tb) > avant[i] + 1e-9) touchees.add(tb.t); });
  pushLog(g.log);
  paintCorpus(id);
  lastPct=-1;
  if(id==='an'||id==='kal'){ const b=$('bloom'); b.classList.remove('on'); void b.offsetWidth; b.classList.add('on'); }
  if(nArbre()===NGL){ S_.done=true; showEnd(); }
}

function showEnd(){
  const m=Math.floor(S_.t/60), s=Math.floor(S_.t%60);
  const lignes=[
    ['temps de lecture', m+' min '+String(s).padStart(2,'0')],
    ['signes relevés à la main', nf.format(S_.clicks)],
    ['recoupements', nf.format(S_.rec)],
    ['lignes entièrement lues', mesures().lig+' %'],
    ['signes déchiffrés', mesures().sig+' %']
  ];
  /* Les compositions ne se comptent que si on en a tenté. Un joueur qui n'a jamais ouvert la
     grille ne doit pas apprendre à l'écran de fin qu'il y avait quelque chose à y trouver :
     c'est le journal d'actions qui le dira à l'auteur, pas la carte au joueur. */
  if(S_.comp > 0) lignes.push(['signes posés l’un sur l’autre', nf.format(S_.comp)]);
  $('endstats').innerHTML=lignes.map(([k,v])=>'<div>'+k+' <b>'+v+'</b></div>').join('');
  $('end').hidden=false;
}

/* ============================ boucle ============================ */
function tick(dt){
  S_.t += dt;
  produire(dt);
}
/* La production, séparée du temps de jeu : la nuit passée hors ligne se rattrape par ici
   sans avancer le chronomètre ni traverser l'horloge instrumentée du journal d'actions. */
function produire(dt){
  S_.O += oBrut()*dt;
  // table de fréquences : consomme des occurrences
  const wantO = S_.b.tab*1.0*dt;
  if(wantO>0){ const canO=Math.min(wantO,S_.O); const fr=canO/wantO;
    S_.O-=canO; S_.H += S_.b.tab*0.6*M.tabl()*fr*dt; }
  // concordance : consomme des hypothèses
  const wantH = S_.b.con*0.5*dt;
  if(wantH>0){ const canH=Math.min(wantH,S_.H); const fr=canH/wantH;
    S_.H-=canH; S_.C += S_.b.con*CON_P*M.con()*fr*dt; }
  // grammaire : en consomme beaucoup plus, et rend d'autant plus qu'on a déchiffré
  const wantG = S_.b.gram*GRAM_C*dt;
  if(wantG>0){ const canG=Math.min(wantG,S_.H); const fr=canG/wantG;
    S_.H-=canG; S_.C += S_.b.gram*GRAM_P*gramMul()*M.gram()*fr*dt; }
}

/* ---- la nuit ----
   `nuit` est le seul glyphe dont l'effet se produit quand le jeu est fermé : 40 % du débit,
   quatre heures au plus (design doc §9). Avant lui il ne se passe rien hors ligne, et c'est
   diégétique — il n'y a personne pour lire. On rattrape en tranches d'une minute plutôt
   qu'en un seul bond : les convertisseurs se coupent quand leur intrant manque, et un
   unique appel de quatre heures leur ferait ignorer cette coupure. */
function veillee(){
  if(!has('esh') || S_.done || !S_.ts) return 0;
  const ecoule = Math.min((Date.now() - S_.ts)/1000, 4*3600);
  if(ecoule < 60) return 0;
  const avant = S_.O;
  let reste = ecoule * 0.4;
  while(reste > 0){ const pas = Math.min(60, reste); produire(pas); reste -= pas; }
  /* La nuit est consommée : sans cela, rouvrir deux fois de suite la même sauvegarde la
     paierait deux fois — la sauvegarde n'horodate que toutes les quatre secondes. */
  S_.ts = Date.now();
  return S_.O - avant;
}
let last=performance.now();
function frame(now){
  let dt=(now-last)/1000; last=now;
  if(dt>0.5) dt=0.5;
  if(!S_.done) tick(dt*speed);
  paintRes(); paintActs(); paintInstr(); paintComp(); paintLex(); paintMeter();
  const ch=Math.floor(S_.t/60)+':'+String(Math.floor(S_.t%60)).padStart(2,'0');
  if($('chrono').textContent!==ch) $('chrono').textContent=ch;
  requestAnimationFrame(frame);
}
