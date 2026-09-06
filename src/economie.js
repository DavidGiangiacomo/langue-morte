/* « La langue morte » — état, ressources, instruments, boucle de simulation
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ état ============================ */
const KEY='langue-morte-mvp-v2';
const fresh = () => ({O:0,H:0,C:0,rec:0,clicks:0,b:{cop:0,tab:0,con:0,ate:0},gl:[],t:0,done:false,
  rel:{}, prix:{}});   // rel : jetons relevés par tablette · prix : tarif du gisement, verrouillé
let S_ = fresh(), speed = 1;
try{ const raw=localStorage.getItem(KEY); if(raw){ const p=JSON.parse(raw);
  if(p&&p.b){ const b=Object.assign({cop:0,tab:0,con:0,ate:0},p.b); S_=Object.assign(fresh(),p); S_.b=b; } } }catch(e){}
const has = id => S_.gl.indexOf(id)>=0;

/* ---- économie ---- */
const M = {
  click:()=> 1*(has('anna')?1.25:1)*(has('tab')?1.5:1)*(has('kal')?2:1),
  cop:  ()=> (has('tem')?1.3:1)*(has('kal')?2:1),
  tabl: ()=> (has('kish')?1.3:1)*(has('kal')?2:1),
  con:  ()=> (has('sar')?1.5:1)*(has('kal')?2:1)
};
/* production brute d'occurrences par seconde (sert au barème du relevé manuel) */
const oBrut = () => (S_.b.cop*1.0 + S_.b.ate*25)*M.cop();

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
   s'allonge pas. Mesuré : I6 = 27,8 %, 52,7 min (`python outils/sim.py`).
   Nommées parce qu'elles servaient à trois endroits chacune, et que c'est cette
   duplication-là qui avait laissé le simulateur diverger du jeu. */
const REC_R = 1.18;     // croissance du coût du recoupement, par usage
const CON_P = 0.0039;   // certitude par seconde et par concordance

const INS = [
  {k:'cop', nom:'Copiste',              sig:'sar',  base:15,   r:1.12,
   ds:()=>'+'+f(1.0*M.cop(),1)+' occ./s',  unlock:()=>true},
  {k:'tab', nom:'Table de fréquences',  sig:'tab',  base:100,  r:1.15,
   ds:()=>'−1 occ./s → +'+f(0.6*M.tabl(),2)+' hyp./s', unlock:()=>S_.b.cop>0||S_.O>=70},
  {k:'con', nom:'Concordance',          sig:'gan',  base:450,  r:1.18,
   ds:()=>'−0,5 hyp./s → +'+f(CON_P*M.con(),4)+' cert./s', unlock:()=>S_.b.tab>0||S_.H>=15},
  {k:'ate', nom:'Atelier de copie',     sig:'kal',  base:1800, r:1.15,
   ds:()=>'+'+f(25*M.cop(),0)+' occ./s',   unlock:()=>S_.b.con>0||S_.O>=900}
];
const insCost = i => Math.ceil(i.base*Math.pow(i.r,S_.b[i.k]));
const recCost = () => { const m=Math.pow(REC_R,S_.rec)*(has('gan')?0.75:1);
  return {O:Math.ceil(12*m), H:Math.ceil(3*m)}; };
const recGain = () => Math.min(3, 1 + Math.floor(S_.gl.length/5));
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
  if(S_.gl.length===NGL){ S_.done=true; showEnd(); }
}

function showEnd(){
  const m=Math.floor(S_.t/60), s=Math.floor(S_.t%60);
  $('endstats').innerHTML=[
    ['temps de lecture', m+' min '+String(s).padStart(2,'0')],
    ['signes relevés à la main', nf.format(S_.clicks)],
    ['recoupements', nf.format(S_.rec)],
    ['lignes entièrement lues', mesures().lig+' %'],
    ['signes déchiffrés', mesures().sig+' %']
  ].map(([k,v])=>'<div>'+k+' <b>'+v+'</b></div>').join('');
  $('end').hidden=false;
}

/* ============================ boucle ============================ */
function tick(dt){
  S_.t += dt;
  S_.O += oBrut()*dt;
  // table de fréquences : consomme des occurrences
  const wantO = S_.b.tab*1.0*dt;
  if(wantO>0){ const canO=Math.min(wantO,S_.O); const fr=canO/wantO;
    S_.O-=canO; S_.H += S_.b.tab*0.6*M.tabl()*fr*dt; }
  // concordance : consomme des hypothèses
  const wantH = S_.b.con*0.5*dt;
  if(wantH>0){ const canH=Math.min(wantH,S_.H); const fr=canH/wantH;
    S_.H-=canH; S_.C += S_.b.con*CON_P*M.con()*fr*dt; }
}
let last=performance.now();
function frame(now){
  let dt=(now-last)/1000; last=now;
  if(dt>0.5) dt=0.5;
  if(!S_.done) tick(dt*speed);
  paintRes(); paintActs(); paintInstr(); paintLex(); paintMeter();
  const ch=Math.floor(S_.t/60)+':'+String(Math.floor(S_.t%60)).padStart(2,'0');
  if($('chrono').textContent!==ch) $('chrono').textContent=ch;
  requestAnimationFrame(frame);
}
