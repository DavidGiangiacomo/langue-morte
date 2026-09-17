/* « La langue morte » — liaisons, entrées, sauvegarde
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ liaisons ============================ */
/* Le compte de l'arbre, écrit une fois : recopié dans le HTML, il mentait dès le lot suivant. */
document.querySelectorAll('.ngl').forEach(el => { el.textContent = NGL; });
majSignes();
buildRail(); buildCorpus(); buildInstr(); buildComp(); buildDoute(); buildLex();
if(S_.gl.length){ paintCorpus(null); pushLog(logDe(S_.gl[S_.gl.length-1])); }
/* `nuit` acquis, le corpus se lit sans le joueur — 40 % du débit, quatre heures au plus.
   Dit au retour, une seule fois, et seulement s'il s'est passé quelque chose. */
const nuitPassee = veillee();
if(nuitPassee > 0) pushLog('La nuit a passé. '+big(Math.round(nuitPassee))+' occurrences relevées sans moi.');
if(S_.done) showEnd();

/* Le relevé n'existe plus que là : dans le texte, sur un signe précis. Le bouton « Relever
   un signe » a disparu — il rapportait 0,6 % des occurrences de PT5 en 414 clics. */
elCorpus.addEventListener('click', e=>{
  const el = e.target.closest('.tok');
  if(!el || el.classList.contains('sep')) return;
  const tb = +el.closest('.tablet').dataset.tb, j = +el.dataset.j;
  if(concArme){ concChoisir(el.dataset.w); return; }
  if(recArme){ recChoisir(tb, j, el.dataset.w); return; }
  relever(tb, j);
  el.classList.add('rel'); el.__v += 'r';
  peindreGisement();          // la tablette vient peut-être de perdre sa marque d'intacte
});
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
$('rail').addEventListener('pointerover', e=>{ const b=e.target.closest('[data-go]');
  if(b) b.title = titreCell(+b.dataset.go); });
/* La fin du prototype ne doit pas être un cul-de-sac : `tick` ne tourne plus une fois
   `S_.done`, donc le corpus derrière est figé sur la partie terminée et se relit tel quel.
   Recharger la page ramène la fenêtre. */
const fermerFin = () => { $('end').hidden = true; };
window.addEventListener('keydown', e=>{
  if(e.metaKey||e.ctrlKey||e.altKey) return;
  const k=e.key.toLowerCase();
  if(k==='j'){ e.preventDefault(); saut(1); }
  else if(k==='k'){ e.preventDefault(); saut(-1); }
  /* La concordance a sa touche : c'est le geste qu'on refait le plus souvent une fois le
     corpus rangé, et il n'a pas à passer par la souris. */
  else if(k==='c'){ e.preventDefault(); if(S_.b.con>0){ if(concSel||concArme) concFermer(); else concArmer(true); } }
  else if(k==='escape'){ if(!$('amb').hidden) ambFermer();
    else if(!$('end').hidden) fermerFin();
    else if(recArme) recArmer(false);
    else if(concArme || concSel) concFermer();
    else if(compSel[0] || compSel[1]) compVider(); }
});
$('instr').addEventListener('click', e=>{ const b=e.target.closest('[data-ins]'); if(b&&!b.disabled) acheterIns(b.dataset.ins); });
/* Un signe ambigu ne s'achète pas d'un clic : il ouvre les deux lectures, et c'est le
   second clic qui paie. Les trente-quatre autres n'ont rien à trancher et passent droit. */
$('lex').addEventListener('click', e=>{ const b=e.target.closest('[data-gl]');
  if(!b||b.disabled) return;
  if(AMB[b.dataset.gl]) ambOuvrir(b.dataset.gl); else acheterGl(b.dataset.gl); });
$('amb-choix').addEventListener('click', e=>{
  const b=e.target.closest('[data-amb]'); if(b) ambChoisir(+b.dataset.amb); });
$('amb-annuler').addEventListener('click', ambFermer);
/* Rouvrir une lecture. Le panneau n'existe qu'avec `peut-être`, et la fenêtre qui s'ouvre
   est celle de l'achat : mêmes deux mots, même prix affiché, même tirage de l'ordre. */
$('doutes').addEventListener('click', e=>{
  const b=e.target.closest('[data-dou]'); if(b&&!b.disabled) ambOuvrir(b.dataset.dou,'revision'); });
$('amb').addEventListener('click', e=>{ if(e.target===$('amb')) ambFermer(); });
/* La grille de composition. Pas de raccourci clavier et pas de répétition : poser un signe sur
   un autre n'est pas un geste qu'on martèle, c'est un geste qu'on a préparé en lisant. */
$('comp-choix').addEventListener('click', e=>{
  const b=e.target.closest('[data-pion]'); if(b&&!b.hidden) compPoser(b.dataset.pion); });
$('pcomp').addEventListener('click', e=>{
  const b=e.target.closest('[data-slot]'); if(b) compSel[+b.dataset.slot]=null; });
$('a-comp').addEventListener('click', ()=>{
  if(composer(compSel[0], compSel[1]) !== 'refus') compVider(); });

function repeat(btn, fn){
  let iv=null, to=null;
  const stop=()=>{ clearTimeout(to); clearInterval(iv); iv=to=null; };
  btn.addEventListener('pointerdown', e=>{ if(btn.disabled) return; fn();
    to=setTimeout(()=>{ iv=setInterval(()=>{ if(btn.disabled){stop();return;} fn(); },110); },420); });
  ['pointerup','pointerleave','pointercancel'].forEach(ev=>btn.addEventListener(ev,stop));
  btn.addEventListener('keydown', e=>{ if(e.key==='Enter'||e.key===' '){ e.preventDefault(); if(!btn.disabled) fn(); } });
}
repeat($('a-hyp'), formuler);
/* Pas de `repeat` ici : le recoupement n'est plus une pression, c'est un choix de deux
   passages. Le bouton ne fait plus qu'armer le corpus. */
$('a-rec').addEventListener('click', ()=>recArmer(!recArme));
/* Le bouton ouvre le mode, puis referme la concordance : un aller-retour, jamais un piège. */
$('a-con').addEventListener('click', ()=> concSel ? concFermer() : concArmer(!concArme));

/* Les deux boutons hors jeu ne sont pas dans tous les builds : le sélecteur de vitesse et
   « réinitialiser » sortent du build de playtest, toute la barre sort de la version publique
   (LIV-2). Les liaisons doivent donc supporter leur absence — une seule ligne qui suppose le
   bouton là, et c'est le reste du fichier qui ne s'exécute pas, `requestAnimationFrame`
   compris. `querySelectorAll` s'en charge tout seul ; `$('reset')`, non. */
document.querySelectorAll('[data-spd]').forEach(b=>b.addEventListener('click',()=>{
  vitesse(+b.dataset.spd);
  document.querySelectorAll('[data-spd]').forEach(x=>x.setAttribute('aria-pressed', x===b?'true':'false'));
}));
const bReset=$('reset');
if(bReset) bReset.addEventListener('click', recommencer);
/* « recommencer » appelle la fonction et non le bouton : la carte de fin existe dans tous
   les builds, le bouton de la barre non. */
$('again').addEventListener('click', recommencer);
$('fermer').addEventListener('click', fermerFin);
$('end').addEventListener('click', e=>{ if(e.target===$('end')) fermerFin(); });

/* `ts` est l'heure de la dernière sauvegarde : c'est elle, et rien d'autre, qui mesure
   la nuit au retour. Écrite à chaque enregistrement, y compris à la fermeture. */
const sauver = () => { try{ S_.ts = Date.now(); localStorage.setItem(KEY, JSON.stringify(S_)); }catch(e){} };
setInterval(sauver, 4000);
window.addEventListener('pagehide', sauver);

requestAnimationFrame(frame);
