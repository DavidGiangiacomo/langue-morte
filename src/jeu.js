/* « La langue morte » — liaisons, entrées, sauvegarde
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ liaisons ============================ */
majSignes();
buildRail(); buildCorpus(); buildInstr(); buildLex();
if(S_.gl.length){ paintCorpus(null); pushLog(byId[S_.gl[S_.gl.length-1]].log); }
if(S_.done) showEnd();

elCorpus.addEventListener('click', e=>{ if(e.target.closest('.tok')) relever('corpus'); });
elCorpus.addEventListener('mousemove', e=>{
  const el = e.target.closest('.tok');
  if(!el || el.classList.contains('sep')){ tipCacher(); return; }
  const cle = (el.dataset.w!==undefined ? 'w'+el.dataset.w : 'n'+el.dataset.n) + ':' + el.__v;
  if(cle !== tipCle){
    const h = tipHTML(el);
    if(!h){ tipCacher(); return; }
    tipCle = cle; $('tip').innerHTML = h; $('tip').hidden = false;
  }
  tipPlace(e.clientX, e.clientY);
});
elCorpus.addEventListener('mouseleave', tipCacher);
elCorpus.addEventListener('scroll', tipCacher, {passive:true});
$('rail').addEventListener('click', e=>{ const b=e.target.closest('[data-go]'); if(b) versTablette(+b.dataset.go); });
/* La fin du prototype ne doit pas être un cul-de-sac : `tick` ne tourne plus une fois
   `S_.done`, donc le corpus derrière est figé sur la partie terminée et se relit tel quel.
   Recharger la page ramène la fenêtre. */
const fermerFin = () => { $('end').hidden = true; };
window.addEventListener('keydown', e=>{
  if(e.metaKey||e.ctrlKey||e.altKey) return;
  const k=e.key.toLowerCase();
  if(k==='j'){ e.preventDefault(); saut(1); }
  else if(k==='k'){ e.preventDefault(); saut(-1); }
  else if(k==='escape' && !$('end').hidden){ fermerFin(); }
});
$('a-rel').addEventListener('click', relever);
$('instr').addEventListener('click', e=>{ const b=e.target.closest('[data-ins]'); if(b&&!b.disabled) acheterIns(b.dataset.ins); });
$('lex').addEventListener('click', e=>{ const b=e.target.closest('[data-gl]'); if(b&&!b.disabled) acheterGl(b.dataset.gl); });

function repeat(btn, fn){
  let iv=null, to=null;
  const stop=()=>{ clearTimeout(to); clearInterval(iv); iv=to=null; };
  btn.addEventListener('pointerdown', e=>{ if(btn.disabled) return; fn();
    to=setTimeout(()=>{ iv=setInterval(()=>{ if(btn.disabled){stop();return;} fn(); },110); },420); });
  ['pointerup','pointerleave','pointercancel'].forEach(ev=>btn.addEventListener(ev,stop));
  btn.addEventListener('keydown', e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); if(!btn.disabled) fn(); } });
}
repeat($('a-hyp'), formuler);
repeat($('a-rec'), recouper);

document.querySelectorAll('[data-spd]').forEach(b=>b.addEventListener('click',()=>{
  speed=+b.dataset.spd;
  document.querySelectorAll('[data-spd]').forEach(x=>x.setAttribute('aria-pressed', x===b?'true':'false'));
}));
$('reset').addEventListener('click',()=>{
  S_=fresh(); LOGS.length=0; lastPct=-1; $('end').hidden=true;
  /* Sans ceci la table des signes de numération garde ceux de la partie précédente :
     on repart de zéro glyphe avec 229 nombres encore lisibles à l'écran. */
  majSignes(); touchees=new Set();
  $('log').innerHTML='<p class="hint">commence</p>';
  paintCorpus(null); try{localStorage.removeItem(KEY);}catch(e){}
});
$('again').addEventListener('click',()=>$('reset').click());
$('fermer').addEventListener('click', fermerFin);
$('end').addEventListener('click', e=>{ if(e.target===$('end')) fermerFin(); });

setInterval(()=>{ try{ localStorage.setItem(KEY, JSON.stringify(S_)); }catch(e){} }, 4000);
window.addEventListener('pagehide',()=>{ try{ localStorage.setItem(KEY, JSON.stringify(S_)); }catch(e){} });

requestAnimationFrame(frame);
