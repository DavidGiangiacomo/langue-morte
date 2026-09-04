/* « La langue morte » — état, ressources, instruments, boucle de simulation
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ état ============================ */
const KEY='langue-morte-mvp-v2';
const fresh = () => ({O:0,H:0,C:0,rec:0,clicks:0,b:{cop:0,tab:0,con:0,ate:0},gl:[],t:0,done:false});
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
/* le relevé manuel vaut au minimum 1, puis 3 % du débit : il reste utile sans être la colonne vertébrale */
const clickVal = () => (1 + 0.03*oBrut()) * M.click();

const INS = [
  {k:'cop', nom:'Copiste',              sig:'sar',  base:15,   r:1.12,
   ds:()=>'+'+f(1.0*M.cop(),1)+' occ./s',  unlock:()=>true},
  {k:'tab', nom:'Table de fréquences',  sig:'tab',  base:100,  r:1.15,
   ds:()=>'−1 occ./s → +'+f(0.6*M.tabl(),2)+' hyp./s', unlock:()=>S_.b.cop>0||S_.O>=70},
  {k:'con', nom:'Concordance',          sig:'gan',  base:450,  r:1.18,
   ds:()=>'−0,5 hyp./s → +'+f(0.003*M.con(),3)+' cert./s', unlock:()=>S_.b.tab>0||S_.H>=15},
  {k:'ate', nom:'Atelier de copie',     sig:'kal',  base:1800, r:1.15,
   ds:()=>'+'+f(25*M.cop(),0)+' occ./s',   unlock:()=>S_.b.con>0||S_.O>=900}
];
const insCost = i => Math.ceil(i.base*Math.pow(i.r,S_.b[i.k]));
const recCost = () => { const m=Math.pow(1.12,S_.rec)*(has('gan')?0.75:1);
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
function relever(){ S_.O += clickVal(); S_.clicks++; }
function formuler(){ const c=hypCost(); if(S_.O>=c){ S_.O-=c; S_.H+=1; } }
function recouper(){ const c=recCost(); if(S_.O>=c.O&&S_.H>=c.H){ S_.O-=c.O; S_.H-=c.H; S_.C+=recGain(); S_.rec++; } }
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
    S_.H-=canH; S_.C += S_.b.con*0.003*M.con()*fr*dt; }
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
