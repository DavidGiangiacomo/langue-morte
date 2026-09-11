/* « La langue morte » — corpus, barre de tablettes, panneaux, infobulle, journal
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ rendu corpus ============================ */
const elCorpus=document.getElementById('corpus');
/* Nombre de tablettes dégagées : 4 au départ, les 30 au dernier glyphe. Le corpus
   s'ouvre donc sur les trois actes, et non plus sur les deux premiers.
   Sur le compte de l'arbre et non sur les glyphes acquis : composer ⟨grenier⟩ fait comprendre
   le corpus, ça ne le fait pas sortir de terre. */
const revCount = () => Math.min(TB.length, 4 + Math.round(nArbre() * (TB.length-4) / NGL));
let lastRev = 0;

function buildCorpus(){
  let h='';
  TB.forEach((tb,i)=>{
    h+='<div class="tablet" data-tb="'+tb.t+'" hidden>';
    let j=0;
    for(const line of tb.l){
      h+='<div class="ln">';
      for(const tk of line.split(' ')){
        /* data-j : rang du jeton dans sa tablette. C'est lui qui permet au relevé de savoir
           si l'on découvre un signe ou si l'on repasse sur ses propres pas. */
        if(tk==='·') h+='<span class="tok sep">·</span>';
        else if(tk.charCodeAt(0)===37) h+='<span class="tok" data-j="'+(j++)+'" data-n="'+tk.slice(1)+'"></span>';
        else h+='<span class="tok" data-j="'+(j++)+'" data-w="'+tk+'"></span>';
      }
      h+='</div>';
    }
    h+='</div>';
  });
  elCorpus.innerHTML=h;
  paintCorpus(null);
}

/* Un jeton relevé reste marqué : c'est la trace du travail déjà fait, et la seule façon
   de voir d'un coup d'œil ce qu'il reste à parcourir sur une tablette. */
function releves(){
  const s = new Set();
  for(const t in S_.rel) for(const j of S_.rel[t]) s.add(t+':'+j);
  return s;
}
const cleTok = el => el.closest('.tablet').dataset.tb + ':' + el.dataset.j;

function paintCorpus(flashId){
  const rel = releves();
  elCorpus.querySelectorAll('[data-w]').forEach(el=>{
    const id=el.dataset.w, known=!!byId[id] && has(id);
    const r = rel.has(cleTok(el)) ? 'r' : '';
    const want = (known ? 'w:'+byId[id].mot : 'g') + r;
    if(el.__v===want && flashId!==id) return;
    el.__v=want;
    el.className='tok '+(known?'w':'g')+(r?' rel':'')+(flashId===id?' flash':'');
    el.innerHTML = known ? byId[id].mot : sv(id);
  });
  elCorpus.querySelectorAll('[data-n]').forEach(el=>{
    const n=+el.dataset.n, lis=numLisible(n), r = rel.has(cleTok(el)) ? 'r' : '';
    const want=(lis?'n':'g')+r;
    if(el.__v===want) return;
    el.__v=want;
    el.className='tok '+(lis?'num':'g')+(r?' rel':'');
    el.innerHTML = lis ? nf.format(n) : numGlyphs(n);
  });
  ranger(); revealer(); paintRail(); peindreRec(); peindreConc();
}

/* ============================ la datation ============================ */
/* Le jeu n'ajoute aucune date au corpus : chaque tablette porte la sienne dans sa
   première ligne — « tablette 12 · année 103 » — depuis la première seconde de la partie.
   Tout ce que `année` change, c'est que le joueur sait la lire ; et il faut encore qu'il
   sache lire le nombre, signe par signe, comme partout ailleurs. Les deux dernières
   tablettes ne portent aucun nombre : elles disent « dernière-année », et c'est ce
   glyphe-là qui les date — après elle, personne n'a plus compté. */
const ANNEE = {};
for(const tb of CORPUS){
  const tk = tb.l[0].split(' '), i = tk.indexOf('nur');
  if(i >= 0 && tk[i+1] && tk[i+1].charCodeAt(0) === 37) ANNEE[tb.t] = {n:+tk[i+1].slice(1)};
  else if(tk.indexOf('nurhal') >= 0) ANNEE[tb.t] = {fin:true};
}
const datee = t => { const a = ANNEE[t];
  return !!a && (a.fin ? has('nurhal') : (has('nur') && numLisible(a.n))); };

/* Six années portent deux tablettes — 40, 54, 88, 150, 183, 201 — et la dernière aussi.
   Le numéro tranche, et c'est le corpus qui le dit : la 16 et la 17 sont toutes deux de
   l'année 150, dans cet ordre-là.
   Une tablette qu'on ne sait pas dater ne se range pas : elle reste avec ses pareilles,
   dans l'ordre où elle est sortie de terre. On n'ordonne que ce qu'on sait lire. */
const cleTemps = t => (ANNEE[t].fin ? 100000 : ANNEE[t].n)*100 + t;
function ordre(tri){
  if(!tri) return TB;
  return TB.filter(tb=>datee(tb.t)).sort((a,b)=>cleTemps(a.t)-cleTemps(b.t))
    .concat(TB.filter(tb=>!datee(tb.t)));
}

/* Ranger déplace les nœuds déjà construits au lieu de les reconstruire : les jetons
   relevés, les caches de peinture et la marque du gisement survivent au rangement.
   `avant` range l'index, `après` range le texte — deux gestes d'archiviste, dans cet
   ordre, et le second est celui qui met deux siècles de crue en colonne. */
let ordreVu = '';
function ranger(){
  const oB = ordre(has('pat')), oC = ordre(has('zur'));
  const sig = oB.map(t=>t.t).join(',') + '|' + oC.map(t=>t.t).join(',');
  if(sig === ordreVu) return;
  const neuf = ordreVu !== '';
  ordreVu = sig;
  const rail = $('rail'), cells = {};
  for(const c of [...rail.children]) cells[c.dataset.go] = c;
  for(const tb of oB) rail.appendChild(cells[tb.t]);
  const tabs = {};
  for(const el of [...elCorpus.children]) tabs[el.dataset.tb] = el;
  for(const tb of oC) elCorpus.appendChild(tabs[tb.t]);
  if(neuf) elCorpus.scrollTop = 0;
}

/* Un nouveau mot donne envie de relire les 30 tablettes — encore faut-il pouvoir y aller.
   La barre indique, par tablette, la part de lignes entièrement lues ; à chaque glyphe
   acquis elle marque en ocre les tablettes où ce signe apparaît. La relecture devient
   une tournée guidée au lieu d'un défilement. */
let touchees = new Set();

/* Les tablettes où chaque signe apparaît. Sert à la barre pendant un recoupement :
   choisir un passage doit désigner où chercher le second, sinon c'est une chasse au
   trésor dans trente tablettes dont une seule tient à l'écran. */
const TBSIGNE = {};
for(const tb of CORPUS) for(const l of tb.l) for(const tk of l.split(' ')){
  if(tk==='·' || tk.charCodeAt(0)===37) continue;
  (TBSIGNE[tk] || (TBSIGNE[tk] = new Set())).add(tb.t);
}

/* Rang de sortie de terre, fixé une fois pour toutes : c'est lui qui décide de ce qui est
   dégagé, et le rangement chronologique ne doit pas y toucher. Ce qu'on a sous les yeux
   change d'ordre ; ce qu'on a sorti de terre, non. */
const IDX = {}; TB.forEach((tb,i)=>{ IDX[tb.t] = i; });
const TBN = {}; for(const tb of CORPUS) TBN[tb.t] = tb;
const degagee = t => IDX[t] < revCount();

function buildRail(){
  $('rail').innerHTML = TB.map(tb =>
    '<button class="rcell" data-go="'+tb.t+'" title="tablette '+tb.t+'">'+
      '<span class="rn"></span><span class="ry"></span><span class="rb"><i></i></span></button>').join('');
}
function paintRail(){
  const lisNum=has('tab')&&has('an');
  for(const c of $('rail').children){
    const t=+c.dataset.go;
    const v=!degagee(t); if(c.hidden!==v) c.hidden=v; if(v) continue;
    const num = lisNum ? String(t) : null;
    const wantN = num || 'g';
    const rn=c.querySelector('.rn');
    if(rn.__v!==wantN){ rn.__v=wantN; rn.innerHTML = num || numGlyphs(t); }
    /* La date, sous le numéro. Une tablette dont on ne sait pas encore lire l'année garde
       la ligne vide : la barre montre exactement l'étendue de ce qu'on sait dater. */
    const ry=c.querySelector('.ry');
    const wantY = !datee(t) ? '' : ANNEE[t].fin ? 'fin' : String(ANNEE[t].n);
    if(ry.__v!==wantY){ ry.__v=wantY;
      ry.innerHTML = wantY==='fin' ? sv('nurhal') : wantY; }
    const p=Math.round(100*pctTablette(TBN[t]));
    const bar=c.querySelector('.rb i');
    if(bar.__v!==p){ bar.__v=p; bar.style.width=p+'%'; }
    const tch = touchees.has(t);
    if(c.classList.contains('touche')!==tch) c.classList.toggle('touche',tch);
    const vise = !!recSel && t!==recSel.tb && !!TBSIGNE[recSel.id] && TBSIGNE[recSel.id].has(t);
    if(c.classList.contains('cible')!==vise) c.classList.toggle('cible',vise);
  }
  peindreGisement();
}

/* Une seule échelle sur la cellule, celle du gisement : intacte, la tablette reste pleine ;
   lue, elle rentre dans le fond ; épuisée, elle s'éteint. C'est la tablette lue qui porte la
   marque, et non l'intacte, pour deux raisons. La première est que l'intacte est le cas
   général — PT6 n'a touché que 3 tablettes sur 26 — et qu'un signe porté par presque tout
   ne signale rien ; ce qui instruit, c'est de voir reculer ce qu'on a lu, donc de
   comprendre que le corpus s'use et qu'ailleurs il ne l'est pas. La seconde est que marquer
   l'intacte l'aurait fait monter, et en montant elle serait entrée en conflit avec le
   survol, qui monte aussi, et avec l'ocre de `touche`, qui prend déjà le cadre et le
   numéro. Descendre ne heurte personne.
   Repeinte à part, et non dans `paintRail` : le gisement change à chaque relevé quand la
   lisibilité ne change qu'à chaque glyphe, et recompter les 3 838 signes du corpus à
   chaque clic coûterait cent fois ce que coûtent ces deux classes. */
function peindreGisement(){
  for(const c of $('rail').children){
    if(c.hidden) continue;
    const t=+c.dataset.go;
    const sec = gisReste(t) <= 0, lue = !sec && S_.prix[t] !== undefined;
    if(c.classList.contains('sec')!==sec) c.classList.toggle('sec',sec);
    if(c.classList.contains('lue')!==lue) c.classList.toggle('lue',lue);
  }
}

/* L'infobulle chiffre ce que la marque ne peut que suggérer : sur une tablette intacte, le
   tarif du moment, c'est-à-dire ce qu'on perd à ne pas y aller. Il suit la production et ne
   peut donc pas être figé dans l'attribut : il s'écrit au survol (cf. jeu.js). */
function titreCell(t){
  const r = gisReste(t);
  /* La date est dans le texte de la tablette ; l'infobulle ne fait que la répéter, et
     seulement quand le joueur sait la lire. */
  const d = !datee(t) ? '' : ANNEE[t].fin ? ' · dernière année' : ' · année '+ANNEE[t].n;
  return 'tablette '+t+d+' — gisement '+r+'/'+GISEMENT[t]
    + (r <= 0 ? ' · épuisée'
      : S_.prix[t] === undefined
        ? " · intacte : "+nf.format(Math.round(tarifRel()))
          +" occ. par relevé si tu l'ouvres maintenant"
        : ' · '+nf.format(Math.round(S_.prix[t]))+' occ. par relevé');
}
/* ---- le recoupement, dans le texte ----
   Armé depuis le bouton, il se joue en deux clics : un premier passage, puis la même
   attestation ailleurs. Choisir un signe allume toutes ses autres attestations dans le
   corpus — l'analyse de fréquences rendue littérale, et la seule façon de rendre le
   comptage d'occurrences opérant plutôt que décoratif.
   Deux tablettes différentes sont exigées : c'est ce qui fait du recoupement un parcours
   et non un geste local. Six signes sont présents dans les quatre tablettes du départ,
   donc l'ouverture n'est jamais bloquée — le recoupement fournit 100 % de la Certitude
   des dix premières minutes, il ne peut jamais devenir impossible. */
let recArme = false, recSel = null, recPeints = [];

function peindreRec(){
  for(const e of recPeints) e.classList.remove('pick','echo');
  recPeints.length = 0;
  paintRail();
  elCorpus.classList.toggle('armed', recArme);
  if(!recArme || !recSel) return;
  const tbl = elCorpus.querySelector('.tablet[data-tb="'+recSel.tb+'"]');
  const sel = tbl && tbl.querySelector('[data-j="'+recSel.j+'"]');
  if(sel){ sel.classList.add('pick'); recPeints.push(sel); }
  for(const e of elCorpus.querySelectorAll('[data-w="'+recSel.id+'"]')){
    const p = e.closest('.tablet');
    if(p.hidden || p.dataset.tb === String(recSel.tb)) continue;
    e.classList.add('echo'); recPeints.push(e);
  }
}

function recArmer(v){ recArme = v; if(!v) recSel = null; peindreRec(); }

function recChoisir(tb, j, id){
  if(id === undefined) return;            // un nombre n'est pas un signe : rien à recouper
  if(recSel && recSel.id === id && recSel.tb !== tb){
    if(!recouper(id)) return;             // plus les moyens : on garde le premier passage
    for(const e of recPeints) if(e.classList.contains('pick')) rejouerFlash(e);
    const tbl = elCorpus.querySelector('.tablet[data-tb="'+tb+'"]');
    if(tbl) rejouerFlash(tbl.querySelector('[data-j="'+j+'"]'));
    /* Le second passage devient le point d'appui du suivant : on suit un signe de
       tablette en tablette. Sa tablette étant exclue des attestations allumées, on ne
       peut pas rapprocher deux fois le même endroit — la tournée est forcée. */
    recSel = {id, tb, j};
  } else {
    recSel = {id, tb, j};
  }
  peindreRec();
}

/* `.flash` est une animation : il faut la retirer et forcer un reflow pour la rejouer. */
function rejouerFlash(el){
  if(!el) return;
  el.classList.remove('flash'); void el.offsetWidth; el.classList.add('flash');
  setTimeout(()=>el.classList.remove('flash'), 900);
}

/* ---- la concordance, dans le texte ----
   PT8 : le rangement chronologique n'a pas suffi. Soixante lignes du corpus portent un
   relevé d'eau, sur six cent soixante-seize, et de huit à cinquante-sept lignes de
   registre séparent deux relevés consécutifs. Ranger les tablettes ordonne les
   contenants ; ça ne rassemble pas le signal. Le joueur de PT8 est allé sur la tablette
   26 — le relevé d'eau complet, vingt-deux années dans un seul document — treize secondes
   après avoir acheté `avant`, y a fait vingt relevés, et n'a pas vu la série. Le défaut
   n'était donc pas que la donnée soit illisible : c'est que la lecture n'était pas
   assemblée.

   Une concordance, en philologie, est le relevé de toutes les attestations d'un mot avec
   leur contexte. L'instrument porte ce nom depuis l'acte II sans rien faire de visible ;
   il fait maintenant ce qu'il annonce. Choisir un signe replie le corpus sur ses seules
   attestations, dans l'ordre d'affichage courant, chaque tablette gardant sa première
   ligne — celle où elle se numérote et se date elle-même (règle 5 : rien d'ajouté).
   Sur `eau`, corpus rangé, la colonne donne 14 · 13 · 15 · 12 · 11 · 12 · 10 · 9 · 8 …
   jusqu'à 0, en soixante-dix lignes au lieu de six cent soixante-seize. Personne ne la
   commente ; c'est au joueur de lire les nombres. */
let concArme = false, concSel = null, concN = 0;

function concArmer(v){
  concArme = v;
  if(v) recArmer(false);          // deux modes se disputeraient le même clic
  peindreConc();
}
/* Un signe inconnu se concorde aussi bien qu'un signe lu — c'est même là que l'instrument
   sert le plus. Rassembler les contextes d'une forme qu'on ne sait pas encore lire est
   le geste de l'épigraphiste, et le pendant du comptage d'occurrences de la Table. */
function concChoisir(id){
  if(id === undefined) return;    // un nombre n'est pas un signe : rien à concorder
  concSel = id; concArme = false;
  peindreConc();
}
function concFermer(){ concSel = null; concArme = false; peindreConc(); }

function peindreConc(){
  elCorpus.classList.toggle('filtre', !!concSel);
  elCorpus.classList.toggle('conc-arme', concArme);
  concN = 0;
  for(const tb of elCorpus.children){
    if(!concSel){
      tb.classList.remove('vide');
      for(const ln of tb.children) ln.classList.remove('off');
      continue;
    }
    let n = 0, premiere = true;
    for(const ln of tb.children){
      const a = ln.querySelectorAll('[data-w="'+concSel+'"]').length;
      n += a;
      /* La première ligne reste toujours : sans elle, la colonne n'aurait plus de date —
         et cette date est du texte ancien, pas un en-tête ajouté par le jeu. */
      ln.classList.toggle('off', !a && !premiere);
      premiere = false;
    }
    tb.classList.toggle('vide', n === 0);
    if(n && !tb.hidden) concN += n;
  }
  majConc();
}

function majConc(){
  const b = $('a-con'), ouvert = S_.b.con > 0;
  if(b.hidden !== !ouvert) b.hidden = !ouvert;
  if(!ouvert) return;
  const mot = concSel && byId[concSel] && has(concSel) ? byId[concSel].mot : null;
  setHTML(b, !concSel ? (concArme ? 'choisis un signe' : 'concorder')
    : (mot || sv(concSel)) + ' · ' + nf.format(concN)
      + ' attestation' + (concN > 1 ? 's' : '') + ' ✕');
  b.classList.toggle('on', concArme || !!concSel);
}

/* Une tablette repliée par la concordance n'est pas une destination : on ne saute pas
   dessus au clavier, et la barre n'y mène pas. */
const repliee = el => el.hidden || el.classList.contains('vide');

function versTablette(t){
  const el=elCorpus.querySelector('.tablet[data-tb="'+t+'"]');
  if(!el || repliee(el)) return;
  elCorpus.scrollTo({top: el.offsetTop - elCorpus.firstElementChild.offsetTop - 8, behavior:'smooth'});
  for(const c of $('rail').children) c.classList.toggle('ici', +c.dataset.go===t);
}
function tabletteVisible(){
  const y=elCorpus.scrollTop, base=elCorpus.firstElementChild.offsetTop;
  let best=null;
  for(const el of elCorpus.querySelectorAll('.tablet')){
    if(repliee(el)) continue;
    if(el.offsetTop - base <= y + 40) best=el; else break;
  }
  return best;
}
function saut(d){
  const vis=tabletteVisible(); const list=[...elCorpus.querySelectorAll('.tablet')].filter(e=>!repliee(e));
  let i=list.indexOf(vis); i = Math.max(0, Math.min(list.length-1, (i<0?0:i)+d));
  versTablette(+list[i].dataset.tb);
}

function revealer(){
  const n = revCount();
  for(const el of elCorpus.querySelectorAll('.tablet')){
    const v = !degagee(+el.dataset.tb); if(el.hidden!==v) el.hidden=v;
  }
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
    const muet={cop:'kal',tab:'im',con:'shen',ate:'mesh',gram:'en'}[i.k];
    setHTML(b.querySelector('.nn'), (open&&has('ur')) ? i.nom
      : '<span style="color:var(--dim)">'+sv('dun')+sv(muet)+sv('la')+'</span>');
    setHTML(b.querySelector('.lv'), open? nf.format(S_.b[i.k]) : '');
    setHTML(b.querySelector('.ds'), open&&has('im') ? i.ds() : '');
    setHTML(b.querySelector('.cs'), open ? (readC()? big(c) : numGlyphs(c)) : '');
  }
}

/* Les branches, puis les composés. Un glyphe secret n'appartient à aucune chaîne — il y
   entrerait dans le `prevDone` de `paintLex` et bloquerait la suite de sa branche, alors qu'il
   n'est pas sur le chemin. Son bloc reste caché tant qu'on n'en a trouvé aucun : le lexique ne
   doit pas annoncer qu'il existe des signes qu'aucune branche n'offre. */
const CARTE = g => '<button class="gcard" data-gl="'+g.id+'">'+
  '<span class="sig">'+sv(g.id)+'</span>'+
  '<span class="ttl"></span><span class="cost"></span><span class="eff"></span></button>';
const SECRETS = GL.filter(g=>g.sec);

/* ==================== la grille de composition ==================== */
/* Deux emplacements, et l'aperçu de ce qu'ils font ensemble. L'aperçu ne dit pas si la paire
   existe : il dessine le signe proposé, exactement comme le corpus dessine les siens depuis la
   première seconde. Le reconnaître dans le texte est tout le jeu, et c'est le seul indice
   qu'il y ait — la grille, elle, ne souffle rien (design doc §7).
   Les composés déjà trouvés restent posables : les exclure dirait qu'aucune recette ne les
   emploie, et ce serait un renseignement. */
let compSel = [null, null];

function compPoser(id){
  const i = compSel.indexOf(id);
  if(i >= 0){ compSel[i] = null; return; }      // recliquer retire
  if(compSel[0] === null) compSel[0] = id;
  else compSel[1] = id;                          // les deux pleins : le second cède la place
}
function compVider(){ compSel = [null, null]; }

function buildComp(){
  setHTML($('comp-choix'), GL.map(g =>
    '<button class="pion" data-pion="'+g.id+'" hidden>'+sv(g.id)+'</button>').join(''));
}

function paintComp(){
  const ouvert = compOuvre();
  if($('pcomp').hidden !== !ouvert) $('pcomp').hidden = !ouvert;
  if(!ouvert) return;

  for(const g of GL){
    const b = $('comp-choix').querySelector('[data-pion="'+g.id+'"]'), vu = has(g.id);
    if(b.hidden !== !vu) b.hidden = !vu;
    if(!vu) continue;
    if(b.title !== g.mot) b.title = g.mot;
    b.classList.toggle('pose', compSel.indexOf(g.id) >= 0);
  }

  const slots = $('pcomp').querySelectorAll('.slot');
  for(let i = 0; i < 2; i++){
    setHTML(slots[i], compSel[i] ? sv(compSel[i]) : '');
    slots[i].classList.toggle('plein', !!compSel[i]);
  }
  const a = compSel[0], b = compSel[1], pret = !!(a && b);
  $('pcomp').querySelector('.pose').classList.toggle('pret', pret);
  setHTML($('comp-ap'), pret ? svPaire(a, b) : '');

  const c = compCost(), bt = $('a-comp');
  bt.disabled = !pret || auCarnet(a, b) || S_.H < c;
  setHTML($('ac-comp'), (readC() ? big(c) : numGlyphs(c)) + ' hyp.');

  /* Le carnet. Il n'existe pas avant la première tentative — le panneau n'annonce pas qu'on
     peut se tromper, il le montre une fois que c'est arrivé. */
  const n = S_.carnet.length;
  if($('carnet').hidden !== !n) $('carnet').hidden = !n;
  if(n) setHTML($('carnet'), '<div class="ch">Déjà tentées</div>' + S_.carnet.map(pr => {
    const [x, y] = pr.split('+');
    return '<span class="cpair" title="'+byId[x].mot+' + '+byId[y].mot+'">'+svPaire(x, y)+'</span>';
  }).join(''));
}

function buildLex(){
  setHTML($('lex'), BR.map(([k,label])=>{
    const list=GL.filter(g=>g.br===k && !g.sec);
    return '<div class="branch"><div class="bh">'+label+'</div><div class="chain">'+
      list.map(CARTE).join('')+
    '</div></div>';
  }).join('')
  + '<div class="branch" id="lexsec" hidden><div class="bh">Composés</div><div class="chain">'+
      SECRETS.map(CARTE).join('')+
    '</div></div>');
}
function paintLex(){
  for(const [k] of BR){
    const list=GL.filter(g=>g.br===k && !g.sec);
    let prevDone=true;
    for(const g of list){
      const b=$('lex').querySelector('[data-gl="'+g.id+'"]');
      const done=has(g.id), open=prevDone&&!done, can=open&&S_.C>=g.cost;
      const cls='gcard'+(done?' done':can?' afford':open?'':' locked');
      if(b.className!==cls) b.className=cls;
      b.disabled=!can;
      /* Le comptage d'occurrences sur les signes encore à acheter. En infobulle il n'était
         qu'un ornement ; ici c'est l'arbitrage de l'épigraphiste — 3 C pour 315 signes ou
         40 C pour 49 ? Conditionné à la Table de fréquences, qui fait alors visiblement ce
         que son nom annonce, et à `deux`, sans lequel le nombre serait lui-même illisible :
         du coup la question ne se pose jamais pour `deux`, le seul glyphe dont le comptage
         mentirait (il n'ouvre aucun signe, il ouvre le principe du redoublement). */
      const montreFreq = open && S_.b.tab > 0 && readC();
      setHTML(b.querySelector('.ttl'), done ? g.mot
        : montreFreq ? '<span class="frq">'+nf.format(freqGlyphe(g.id))+' occ.</span>' : '');
      setHTML(b.querySelector('.cost'), done? '✓' : open? (readC()? String(g.cost) : numGlyphs(g.cost)) : '');
      setHTML(b.querySelector('.eff'), (done || (open && has('im'))) ? g.eff : '');
      if(!done) prevDone=false;
    }
  }
  /* Les composés trouvés. Jamais cliquables : on ne les achète pas ici, on les a posés. */
  let vus=0;
  for(const g of SECRETS){
    const b=$('lex').querySelector('[data-gl="'+g.id+'"]'), done=has(g.id);
    if(b.hidden!==!done) b.hidden=!done;
    if(!done) continue;
    vus++;
    if(b.className!=='gcard done') b.className='gcard done';
    b.disabled=true;
    setHTML(b.querySelector('.ttl'), g.mot);
    setHTML(b.querySelector('.cost'), '✓');
    setHTML(b.querySelector('.eff'), g.eff);
  }
  if($('lexsec').hidden !== !vus) $('lexsec').hidden = !vus;
  /* Le compteur suit l'arbre : trouver un composé n'avance pas la progression, il ajoute au
     savoir. Sans ça il afficherait « 21 / 20 ». */
  $('lexr').textContent = nArbre()+' / '+NGL;
}

function paintRes(){
  const tb=S_.b.tab, cn=S_.b.con, gr=S_.b.gram;
  const oNet = oBrut() - tb*1.0,
        hNet = tb*0.6*M.tabl() - cn*0.5 - gr*GRAM_C,
        cNet = cn*CON_P*M.con() + gr*GRAM_P*gramMul()*M.gram();
  setHTML($('vl-O'), amount(S_.O, readN()));
  setHTML($('vl-H'), amount(S_.H, readN()));
  setHTML($('vl-C'), amount(S_.C, readN()));
  const rt=(v,el,dry)=>{ setHTML(el, readR()? (v?( (v>0?'+':'−')+f(Math.abs(v),v<0.1&&v!==0?3:2)+'/s'):'') : '');
    el.classList.toggle('dry',!!dry); };
  rt(oNet,$('rt-O'), tb>0 && S_.O<1 && oNet<0);
  rt(hNet,$('rt-H'), (cn+gr)>0 && S_.H<1 && hNet<0);
  rt(cNet,$('rt-C'), false);
}

function paintActs(){
  const hc=hypCost(), rc=recCost(), rg=recGain();
  /* Ce qu'il reste à relever dans les tablettes dégagées. La main est une ressource finie :
     le dire, c'est la seule façon d'empêcher qu'on la prenne pour un débit. */
  let reste=0; const n=revCount();
  for(let i=0;i<n;i++) reste += gisReste(TB[i].t);
  setHTML($('gis'), reste? 'gisement '+(readC()? nf.format(reste) : numGlyphs(reste)) : '');
  setHTML($('ac-hyp'), readC()? hc+' occ.' : numGlyphs(hc));
  setHTML($('ac-rec'), (readC()? (big(rc.O)+' occ. · '+big(rc.H)+' hyp.') : (numGlyphs(rc.O)+'<span style="width:6px"></span>'+numGlyphs(rc.H)))
    + (rg>1? '<span style="color:var(--slate)">→ '+(readC()? rg : '')+'</span>' : ''));
  /* Le bouton n'exécute plus le recoupement : il l'arme, et dit où en est le geste. */
  const peutRec = S_.O >= rc.O && S_.H >= rc.H;
  setHTML($('a-rec').querySelector('.an'), !recArme ? 'Recouper deux passages'
    : !peutRec ? 'pas de quoi recouper'
    : !recSel ? 'choisis un passage dans le corpus' : 'et le même signe, ailleurs');
  $('a-rec').classList.toggle('armed', recArme);
  $('a-rec').title = recArme ? 'clique pour renoncer — ou échap' : '';
  $('a-hyp').disabled = S_.O < hc;
  /* Armé, le bouton reste toujours cliquable : c'est la seule sortie du mode, et le corpus
     armé ne relève plus. Le désactiver faute de ressources enfermait le joueur — signalé
     en PT6. Il ne se désactive donc que pour empêcher d'armer, jamais de désarmer. */
  $('a-rec').disabled = !recArme && !peutRec;
  majConc();   // la première Concordance achetée fait apparaître son bouton
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
const FREQ = {}, FREQNUM = {};
for(const tb of CORPUS) for(const l of tb.l) for(const tk of l.split(' ')){
  if(tk==='·') continue;
  if(tk.charCodeAt(0)===37) for(const k of numSyms(+tk.slice(1))) FREQNUM[k] = (FREQNUM[k]||0) + 1;
  else FREQ[tk] = (FREQ[tk]||0) + 1;
}
/* Ce que la Table de fréquences sait d'un glyphe : les occurrences de son SIGNE, pas de
   son mot. La distinction ne change rien hors de la branche Nombre, et tout à l'intérieur :
   ⟨un⟩ n'est écrit que 8 fois comme mot, mais 1 668 fois comme chiffre, dans les nombres.
   Compter les mots seuls afficherait 8, 4, 0, 2, 1 sur les cinq glyphes de nombre et ferait
   passer la branche la plus rentable du jeu pour la plus pauvre. */
const freqGlyphe = id => (FREQ[id]||0) + (NUMSYM[id]||[]).reduce((n,k)=>n+(FREQNUM[k]||0), 0);
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
    if(S_.b.tab > 0){
      const n = freqGlyphe(id);
      return sv(id) + '<span class="lab"><b>' + nf.format(n) + '</b> occurrence' + (n>1?'s':'') + '</span>';
    }
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
