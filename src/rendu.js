/* « La langue morte » — corpus, barre de tablettes, panneaux, infobulle, journal
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ rendu corpus ============================ */
const elCorpus=document.getElementById('corpus');
/* Nombre de tablettes dégagées : 4 au départ, les 30 au douzième glyphe. */
const revCount = () => Math.min(TB.length, 4 + Math.round(S_.gl.length * (TB.length-4) / NGL));
let lastRev = 0;

function buildCorpus(){
  let h='';
  TB.forEach((tb,i)=>{
    h+='<div class="tablet" data-tb="'+tb.t+'" hidden>';
    for(const line of tb.l){
      h+='<div class="ln">';
      for(const tk of line.split(' ')){
        if(tk==='·') h+='<span class="tok sep">·</span>';
        else if(tk.charCodeAt(0)===37) h+='<span class="tok" data-n="'+tk.slice(1)+'"></span>';
        else h+='<span class="tok" data-w="'+tk+'"></span>';
      }
      h+='</div>';
    }
    h+='</div>';
  });
  elCorpus.innerHTML=h;
  paintCorpus(null);
}

function paintCorpus(flashId){
  elCorpus.querySelectorAll('[data-w]').forEach(el=>{
    const id=el.dataset.w, known=!!byId[id] && has(id);
    const want = known ? 'w:'+byId[id].mot : 'g';
    if(el.__v===want && flashId!==id) return;
    el.__v=want;
    el.className='tok '+(known?'w':'g')+(flashId===id?' flash':'');
    el.innerHTML = known ? byId[id].mot : sv(id);
  });
  elCorpus.querySelectorAll('[data-n]').forEach(el=>{
    const n=+el.dataset.n, lis=numLisible(n), want=lis?'n':'g';
    if(el.__v===want) return;
    el.__v=want;
    el.className='tok '+(lis?'num':'g');
    el.innerHTML = lis ? nf.format(n) : numGlyphs(n);
  });
  revealer(); paintRail();
}

/* Un nouveau mot donne envie de relire les 30 tablettes — encore faut-il pouvoir y aller.
   La barre indique, par tablette, la part de lignes entièrement lues ; à chaque glyphe
   acquis elle marque en ocre les tablettes où ce signe apparaît. La relecture devient
   une tournée guidée au lieu d'un défilement. */
let touchees = new Set();
function buildRail(){
  $('rail').innerHTML = TB.map(tb =>
    '<button class="rcell" data-go="'+tb.t+'" title="tablette '+tb.t+'">'+
      '<span class="rn"></span><span class="rb"><i></i></span></button>').join('');
}
function paintRail(){
  const n=revCount(), lisNum=has('tab')&&has('an');
  const cells=$('rail').children;
  for(let i=0;i<cells.length;i++){
    const c=cells[i], t=TB[i].t;
    const v=i>=n; if(c.hidden!==v) c.hidden=v; if(v) continue;
    const num = lisNum ? String(t) : null;
    const wantN = num || 'g';
    const rn=c.querySelector('.rn');
    if(rn.__v!==wantN){ rn.__v=wantN; rn.innerHTML = num || numGlyphs(t); }
    const p=Math.round(100*pctTablette(TB[i]));
    const bar=c.querySelector('.rb i');
    if(bar.__v!==p){ bar.__v=p; bar.style.width=p+'%'; }
    const tch = touchees.has(t);
    if(c.classList.contains('touche')!==tch) c.classList.toggle('touche',tch);
  }
}
function versTablette(t){
  const el=elCorpus.querySelector('.tablet[data-tb="'+t+'"]');
  if(!el || el.hidden) return;
  elCorpus.scrollTo({top: el.offsetTop - elCorpus.firstElementChild.offsetTop - 8, behavior:'smooth'});
  const cells=$('rail').children;
  for(let i=0;i<cells.length;i++) cells[i].classList.toggle('ici', TB[i].t===t);
}
function tabletteVisible(){
  const y=elCorpus.scrollTop, base=elCorpus.firstElementChild.offsetTop;
  let best=null;
  for(const el of elCorpus.querySelectorAll('.tablet')){
    if(el.hidden) continue;
    if(el.offsetTop - base <= y + 40) best=el; else break;
  }
  return best;
}
function saut(d){
  const vis=tabletteVisible(); const list=[...elCorpus.querySelectorAll('.tablet')].filter(e=>!e.hidden);
  let i=list.indexOf(vis); i = Math.max(0, Math.min(list.length-1, (i<0?0:i)+d));
  versTablette(+list[i].dataset.tb);
}

function revealer(){
  const n = revCount();
  const tabs = elCorpus.querySelectorAll('.tablet');
  for(let i=0;i<tabs.length;i++){ const v = i>=n; if(tabs[i].hidden!==v) tabs[i].hidden=v; }
  if(n>lastRev && lastRev>0) pushLog(n-lastRev>1 ? (n-lastRev)+' tablettes dégagées.' : 'Une tablette dégagée.');
  lastRev = n;
}

/* Deux mesures. « Signes » sature tôt : on peut lire presque tous les mots d'un
   inventaire sans rien comprendre. « Lignes » ne compte qu'une ligne dont AUCUN signe
   ne reste opaque — elle progresse avec le sens, pas avec le volume. */
function tokLisible(tk){
  if(tk==='·') return true;
  if(tk.charCodeAt(0)===37) return numLisible(+tk.slice(1));
  return !!byId[tk] && has(tk);
}
function mesures(){
  let tot=0, ok=0, nl=0, nlOk=0;
  for(const tb of CORPUS) for(const l of tb.l){
    let pleine=true, vide=true;
    for(const tk of l.split(' ')){
      if(tk==='·') continue;
      vide=false; tot++;
      if(tokLisible(tk)) ok++; else pleine=false;
    }
    if(!vide){ nl++; if(pleine) nlOk++; }
  }
  return {sig:Math.round(100*ok/tot), lig:Math.round(100*nlOk/nl)};
}
function pctTablette(tb){
  let tot=0, ok=0;
  for(const l of tb.l) for(const tk of l.split(' ')){
    if(tk==='·') continue; tot++; if(tokLisible(tk)) ok++;
  }
  return tot? ok/tot : 0;
}

/* ============================ panneaux ============================ */
const $=id=>document.getElementById(id);
function setHTML(el,h){ if(el.__h!==h){ el.__h=h; el.innerHTML=h; } }

function buildInstr(){
  setHTML($('instr'), INS.map(i=>
    '<button class="ins" data-ins="'+i.k+'">'+
      '<span class="nm"><span class="sg"></span><span class="nn"></span></span>'+
      '<span class="lv"></span><span class="ds"></span><span class="cs"></span>'+
    '</button>').join(''));
}
function paintInstr(){
  for(const i of INS){
    const b=$('instr').querySelector('[data-ins="'+i.k+'"]');
    const open=i.unlock(), c=insCost(i), can=open&&S_.O>=c;
    b.classList.toggle('locked',!open);
    b.classList.toggle('afford',can);
    b.disabled=!can;
    setHTML(b.querySelector('.sg'), sv(i.sig));
    const muet={cop:'kal',tab:'im',con:'shen',ate:'mesh'}[i.k];
    setHTML(b.querySelector('.nn'), (open&&has('ur')) ? i.nom
      : '<span style="color:var(--dim)">'+sv('dun')+sv(muet)+sv('la')+'</span>');
    setHTML(b.querySelector('.lv'), open? nf.format(S_.b[i.k]) : '');
    setHTML(b.querySelector('.ds'), open&&has('im') ? i.ds() : '');
    setHTML(b.querySelector('.cs'), open ? (readC()? big(c) : numGlyphs(c)) : '');
  }
}

function buildLex(){
  setHTML($('lex'), BR.map(([k,label])=>{
    const list=GL.filter(g=>g.br===k);
    return '<div class="branch"><div class="bh">'+label+'</div><div class="chain">'+
      list.map(g=>'<button class="gcard" data-gl="'+g.id+'">'+
        '<span class="sig">'+sv(g.id)+'</span>'+
        '<span class="ttl"></span><span class="cost"></span><span class="eff"></span></button>').join('')+
    '</div></div>';
  }).join(''));
}
function paintLex(){
  for(const [k] of BR){
    const list=GL.filter(g=>g.br===k);
    let prevDone=true;
    for(const g of list){
      const b=$('lex').querySelector('[data-gl="'+g.id+'"]');
      const done=has(g.id), open=prevDone&&!done, can=open&&S_.C>=g.cost;
      const cls='gcard'+(done?' done':can?' afford':open?'':' locked');
      if(b.className!==cls) b.className=cls;
      b.disabled=!can;
      setHTML(b.querySelector('.ttl'), done? g.mot : '');
      setHTML(b.querySelector('.cost'), done? '✓' : open? (readC()? String(g.cost) : numGlyphs(g.cost)) : '');
      setHTML(b.querySelector('.eff'), (done || (open && has('im'))) ? g.eff : '');
      if(!done) prevDone=false;
    }
  }
  $('lexr').textContent = S_.gl.length+' / '+NGL;
}

function paintRes(){
  const tb=S_.b.tab, cn=S_.b.con;
  const oNet = oBrut() - tb*1.0, hNet = tb*0.6*M.tabl() - cn*0.5, cNet = cn*0.003*M.con();
  setHTML($('vl-O'), amount(S_.O, readN()));
  setHTML($('vl-H'), amount(S_.H, readN()));
  setHTML($('vl-C'), amount(S_.C, readN()));
  const rt=(v,el,dry)=>{ setHTML(el, readR()? (v?( (v>0?'+':'−')+f(Math.abs(v),v<0.1&&v!==0?3:2)+'/s'):'') : '');
    el.classList.toggle('dry',!!dry); };
  rt(oNet,$('rt-O'), tb>0 && S_.O<1 && oNet<0);
  rt(hNet,$('rt-H'), cn>0 && S_.H<1 && hNet<0);
  rt(cNet,$('rt-C'), false);
}

function paintActs(){
  const hc=hypCost(), rc=recCost(), cv=clickVal(), rg=recGain();
  setHTML($('ac-rel'), readC()? ('+'+(cv<10? f(cv,1).replace(',0','') : big(Math.round(cv)))) : ('+'+numGlyphs(Math.round(cv))));
  setHTML($('ac-hyp'), readC()? hc+' occ.' : numGlyphs(hc));
  setHTML($('ac-rec'), (readC()? (big(rc.O)+' occ. · '+big(rc.H)+' hyp.') : (numGlyphs(rc.O)+'<span style="width:6px"></span>'+numGlyphs(rc.H)))
    + (rg>1? '<span style="color:var(--slate)">→ '+(readC()? rg : '')+'</span>' : ''));
  $('a-hyp').disabled = S_.O < hc;
  $('a-rec').disabled = S_.O < rc.O || S_.H < rc.H;
}

let lastPct=-1;
function paintMeter(){
  const m=mesures();
  const key=m.sig*1000+m.lig;
  if(key===lastPct) return; lastPct=key;
  $('meter').style.width=m.sig+'%';
  $('pct').textContent='signes '+m.sig+' % · lignes '+m.lig+' %';
}

/* ============================ infobulle ============================ */
/* Une fois un mot traduit, son signe disparaît de l'écran. Le survol le redonne :
   on peut vérifier ce qu'on lit sans défaire ce qu'on a appris.
   Sur un signe encore inconnu, l'infobulle donne son nombre d'occurrences dans tout
   le corpus — mais seulement si on possède une Table de fréquences. L'instrument
   fait alors visiblement ce que son nom annonce. */
const FREQ = {};
for(const tb of CORPUS) for(const l of tb.l) for(const tk of l.split(' ')){
  if(tk==='·' || tk.charCodeAt(0)===37) continue;
  FREQ[tk] = (FREQ[tk]||0) + 1;
}
const partMot = k => (k==='u1' && has('an')) ? 'un'
                   : (k==='t10' && has('sela')) ? 'dix'
                   : (k==='h100' && has('meku')) ? 'cent'
                   : (byId[k] && has(k)) ? byId[k].mot : null;

function tipHTML(el){
  if(el.dataset.w !== undefined){
    const id = el.dataset.w, connu = !!byId[id] && has(id);
    if(connu){
      if(COMP[id]){
        const [a,b] = COMP[id], ma = partMot(a), mb = partMot(b);
        return sv(a) + '<span class="plus">+</span>' + sv(b)
             + '<span class="lab">' + (ma&&mb ? ma+' + '+mb : 'signe composé') + '</span>';
      }
      return sv(id) + '<span class="lab">' + byId[id].mot + '</span>';
    }
    if(S_.b.tab > 0)
      return sv(id) + '<span class="lab"><b>' + FREQ[id] + '</b> occurrence' + (FREQ[id]>1?'s':'') + '</span>';
    return null;
  }
  if(el.dataset.n !== undefined){
    const n = +el.dataset.n;
    if(numLisible(n)) return numGlyphs(n) + '<span class="lab">' + nf.format(n) + '</span>';
  }
  return null;
}

let tipCle = null;
function tipPlace(x,y){
  const t=$('tip'), r=t.getBoundingClientRect();
  let px=x+15, py=y+17;
  if(px+r.width  > innerWidth  - 8) px = x - r.width  - 13;
  if(py+r.height > innerHeight - 8) py = y - r.height - 13;
  t.style.left=Math.max(6,px)+'px'; t.style.top=Math.max(6,py)+'px';
}
function tipCacher(){ if(tipCle!==null){ tipCle=null; $('tip').hidden=true; } }

/* ============================ journal ============================ */
const LOGS=[];
function pushLog(txt){
  LOGS.push(txt); if(LOGS.length>2) LOGS.shift();
  $('log').innerHTML = LOGS.map((t,i)=>'<p'+(i===LOGS.length-1?' class="new"':'')+'>'+t+'</p>').join('');
}
