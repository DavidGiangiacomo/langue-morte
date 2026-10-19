/* « La langue morte » — état, ressources, instruments, boucle de simulation
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ état ============================ */
/* La clé ne change plus (LIV-3). Elle s'appelait `langue-morte-mvp-v2` avant de devenir
   `langue-morte-actes-i-iii` à l'ouverture de l'acte III, parce qu'une partie du MVP, `done` à
   treize glyphes, rouvrait sur l'écran de fin sans moyen de continuer — et toutes les parties
   en cours ont été perdues avec elle. Ce qu'un lot change à la sauvegarde se dit désormais
   DANS la sauvegarde, par son numéro de version, et se migre (`charger()`). */
const KEY='langue-morte-partie';
/* Les clés d'avant, lues seulement quand la nouvelle est vide. Une partie trouvée là déménage :
   elle ne se dédouble pas, parce que deux copies d'une même partie finissent par diverger et
   que rien ne dirait laquelle est la bonne.
   `langue-morte-mvp-v2` n'y est pas, et c'est un choix : ses parties sont celles du prototype
   à treize signes, abandonnées le 08/09/2026, et l'économie qui les a produites n'existe plus. */
const CLES_ANCIENNES = ['langue-morte-actes-i-iii'];
const fresh = () => ({O:0,H:0,C:0,rec:0,clicks:0,b:{cop:0,tab:0,con:0,ate:0,gram:0,elv:0,lec:0,jum:0},gl:[],t:0,done:false,
  rel:{}, prix:{}, carnet:[], comp:0, lect:{}, dte:{}, conc:{}, recs:{}, rev:0, contr:0,
  qn:0, qf:0, qa:[], fin:null, efface:false, fautes:{}, lusEleve:{}, tete:0, relJ:{}, prixJ:{}});
/* rel : jetons relevés par tablette · prix : tarif du gisement, verrouillé
   carnet : les paires déjà tentées et fausses · comp : le nombre de tentatives, toutes issues
   confondues — c'est lui que PT10 doit lire, pas la seule liste des échecs.
   lect : la lecture tranchée pour chaque signe ambigu ('j' ou 'f'), d'où la dette se
   déduit — elle n'est pas stockée, voir `dette()`.
   dte : le degré de doute figé à la décision · conc, recs : les signes concordés et le
   nombre de recoupements par signe, qui sont ce sur quoi ce degré se calcule · rev : les
   révisions faites, dont dépend le prix de la suivante (CONTR-3) · contr : la contradiction,
   armée ou non (CONTR-1) — le seul de ces champs que le joueur voie.
   qn : les questions venues depuis le début, douze au plus · qf : le surplus de Certitude
   accumulé vers la suivante · qa : les conditions déjà posées, dans l'ordre (VOIX-3). Les
   questions en main ne se stockent pas : elles se déduisent des deux premiers
   (`questionsEnMain()`).
   fin : comment la partie s'est terminée, 'achevee' ou 'interrompue' (FIN-1, FIN-2) — null
   tant qu'elle court · efface : l'effacement d'une partie achevée est allé à son terme, et
   il n'y a plus que la page vide à rouvrir.
   fautes : chaque signe lu faux un jour, et par qui — 'moi' ou 'eleve' —, même si une
   révision l'a corrigé depuis · lusEleve : les signes dont la lecture en place vient d'un
   Élève. Ni l'un ni l'autre ne se lit pendant la partie ; ils sont ce que la relecture
   avouera (FIN-3). Ce n'est pas un solde à part pour l'Élève (règle 21) : la dette, la
   prime et la contradiction ne lisent que `lect`. Une partie d'avant ce lot les reçoit vides,
   et sa relecture ne montre que les erreurs encore en place, toutes attribuées au joueur.
   tete : où en est le Lecteur dans le corpus, en tablettes, fraction comprise — de 0 à 30
   (GRAINE-2).
   relJ, prixJ : les relevés faits sur la copie du Corpus jumeau, et le tarif de chaque
   tablette de la copie, figé au premier relevé qu'on y fait (VOIX-4) — les jumeaux de `rel`
   et de `prix`.
   Une partie d'avant la composition, ou d'avant l'ambiguïté, les reçoit vides au chargement
   (`fusionner()`) : un champ ajouté ne demande ni nouvelle clé ni migration. */
let S_ = fresh(), speed = 1;
/* Le sélecteur ×1/×3/×10 est hors jeu, mais il multiplie les secondes de JEU — celles que
   le journal d'actions horodate, et celles sur lesquelles `outils/depouiller.py` rejoue le
   modèle. Un ×3 ignoré rend toute la timeline d'un playtest inexploitable **sans qu'aucun
   contrôle puisse le voir** : le contrôle de `depouiller.py` travaille lui aussi en secondes
   de jeu, où tout reste cohérent. D'où cette fonction, qui ne fait rien de plus que
   l'affectation — mais `traces.js` n'édite jamais une règle, il enveloppe ce qui existe, et
   il n'y avait ici qu'un écouteur anonyme. */
function vitesse(n){ speed = n; }

/* ======================== la sauvegarde (LIV-3) ========================
   Le numéro de version ne se règle pas, il se COMPTE : c'est le nombre de migrations écrites,
   plus un. On ne peut donc ni oublier de l'incrémenter, ni l'incrémenter sans dire comment on
   passe d'une version à l'autre. MIGRATIONS[0] fait passer une sauvegarde de la version 1 à la
   2, MIGRATIONS[1] de la 2 à la 3 ; chacune reçoit la sauvegarde brute, telle qu'elle sort du
   JSON, et la modifie en place. Aucune ne se retire : une partie laissée en version 1 doit
   pouvoir les traverser toutes, le jour où son joueur revient.

   **Un champ AJOUTÉ n'en demande pas**, et c'est le cas de chaque lot depuis l'acte III :
   `fresh()` le donne à toute partie qui ne l'a pas. En demandent une : un champ qui change de
   sens, de nom ou de forme, et un signe qui quitte le lexique ou change d'identifiant.

   Version 1 : tout ce qui s'écrit depuis l'acte III. Les sauvegardes d'avant LIV-3 n'ont pas
   de numéro ; elles sont en version 1, il ne leur manque que le chiffre.
   Version 2 : les deux fins (FIN-1, FIN-2). */
const MIGRATIONS = [
  /* 1 → 2. `fin` est un champ ajouté, mais sa valeur neuve est fausse pour une partie déjà
     finie : `fresh()` dirait « elle court encore », et c'est pour ça qu'il faut une migration
     et non un défaut. Avant ce lot il n'y avait qu'une façon de finir — le dernier signe de
     l'arbre, puis la carte de statistiques —, donc une partie `done` est une partie ACHEVÉE,
     et ce qui en tenait lieu d'effacement a eu lieu. Sans ce champ, la règle qui rouvre une
     partie que l'arbre a dépassée (`S_.done`, plus bas) rouvrirait aussi une partie
     interrompue, qui a un signe de moins par définition. */
  p => { if(p.done){ p.fin = 'achevee'; p.efface = true; } },
];
const versionSauvegarde = () => MIGRATIONS.length + 1;
/* Vrai quand la clé porte une sauvegarde que ce jeu ne sait pas lire : il ne la charge pas,
   et rien ici ne l'écrit ni ne l'efface (`sauver`, `recommencer`). On joue alors une partie
   neuve, qui ne se garde pas. */
let sauvegardeIntouchable = false;

function migrer(p){
  if(!Number.isInteger(p.v) || p.v < 1) p.v = 1;
  while(p.v < versionSauvegarde()){ MIGRATIONS[p.v - 1](p); p.v++; }
  return p;
}
/* Une sauvegarde se pose sur une partie neuve, champ par champ : ce qu'elle n'a pas, `fresh()`
   le donne — un niveau plus bas aussi, et c'est pour `b`, où un instrument neuf doit arriver à
   zéro. La liste des instruments était recopiée à la main dans le chargement : tout instrument
   neuf s'écrivait donc à deux endroits, et, oublié au second, il arrivait à `undefined` dans
   toute partie d'avant lui — `insCost()` rendait NaN, et rien ne le disait. Un champ nul garde sa
   valeur neuve : JSON écrit `null` pour un NaN, et une partie ne doit pas casser au chargement
   pour un chiffre qu'elle avait déjà perdu. */
function fusionner(p){
  const s = fresh();
  for(const k of Object.keys(p)){
    const v = p[k], d = s[k];
    if(v === null) continue;
    s[k] = d && typeof d === 'object' && !Array.isArray(d) && typeof v === 'object' && !Array.isArray(v)
         ? Object.assign(d, v) : v;
  }
  return s;
}
/* La partie sauvegardée, migrée, posée sur une partie neuve — ou null, et la partie neuve
   reste. */
function charger(){
  let raw = null, ancienne = null;
  try{
    raw = localStorage.getItem(KEY);
    for(const k of CLES_ANCIENNES) if(raw === null && (raw = localStorage.getItem(k)) !== null) ancienne = k;
  }catch(e){ return null; }
  let p = null;
  try{ p = JSON.parse(raw); }catch(e){}
  if(!p || typeof p !== 'object' || !p.b) return null;
  /* Deux cas où la sauvegarde existe et où ce jeu ne sait pas la lire, et une seule réponse :
     ne pas y toucher. Écrite par un jeu PLUS RÉCENT — un déploiement défait, un vieux fichier
     rouvert dans le navigateur où l'on joue le neuf —, ce jeu-ci ignore ce que ses champs
     veulent dire. Une migration qui CASSE, c'est un défaut du jeu, pas de la partie. Dans les
     deux cas, jouer par-dessus — la charger telle quelle, ou repartir de zéro et laisser la
     sauvegarde des quatre secondes faire le reste — c'est la perdre ; la laisser intacte, c'est
     la rendre entière au jeu qui saura la lire. */
  if(Number.isInteger(p.v) && p.v > versionSauvegarde()){ sauvegardeIntouchable = true; return null; }
  try{ migrer(p); }catch(e){ sauvegardeIntouchable = true; return null; }
  /* Trouvée sous une clé d'avant : écrite sous la nouvelle, puis effacée de l'ancienne — dans
     cet ordre, pour qu'une écriture qui échoue ne perde rien. Elle part telle quelle, `ts`
     compris : c'est lui qui mesure la nuit au retour (`veillee()`), et le déménagement ne
     doit pas la manger. */
  if(ancienne){ try{ localStorage.setItem(KEY, JSON.stringify(p)); localStorage.removeItem(ancienne); }catch(e){} }
  return fusionner(p);
}
S_ = charger() || S_;
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
/* Une partie ACHEVÉE quand l'arbre comptait moins de signes n'est plus finie : l'arbre a
   grandi sous elle. Sans ça elle rouvrirait sur la page vide, `tick` arrêté, sans moyen de
   continuer — le cas exact qui a déjà coûté un changement de `KEY` et toutes les parties en
   cours. Chaque lot de glyphes le reproduirait.
   Ce n'est pas une migration : l'arbre grandit sans que le format bouge, donc ceci passe à
   chaque chargement, quelle que soit la version.
   Une partie INTERROMPUE ne rouvre jamais (design doc §11 : le jeu « ne propose pas de
   reprendre »). Elle a un signe non lu par définition, et c'est ce qui la distingue d'une
   partie dont l'arbre a grandi — non sa taille, que la règle n'a donc pas besoin de
   connaître : c'est `fin` qui le dit, et la migration 1 → 2 qui l'écrit pour les parties
   finies avant les deux fins. */
if(S_.done && S_.fin !== 'interrompue' && nArbre() < NGL){ S_.done = false; S_.fin = null; S_.efface = false; }

/* ======================== la lecture retenue ========================
   `S_.lect` retient, pour chacun des signes ambigus acquis, laquelle des deux lectures le
   joueur a tranchée : 'j' ou 'f'. Un signe absent de la table est lu juste — c'est le cas
   d'une partie commencée avant ce lot, et celui d'un composé posé à la grille, qui n'offre
   aucun choix. Le défaut est donc ce que le joueur voyait déjà ; rien ne se perd. */
const faux = id => S_.lect[id] === 'f';

/* Les parties mal lues d'un composé, dans l'ordre de sa recette et sans doublon : c'est la
   clé de `COMPFAUX`. ⟨année⟩⟨année⟩ n'a qu'une partie à salir, et sa clé est donc `nur` et
   non `nur+nur`. */
function partsFausses(id, lect){
  const pr = PARTIES[id]; if(!pr) return '';
  const L = lect || S_.lect, out = [];
  for(const k of pr) if(L[k] === 'f' && out.indexOf(k) < 0) out.push(k);
  return out.join('+');
}
/* Le mot qu'affiche le jeu — corpus, infobulle, lexique, grille, carnet, concordance. Rien
   d'autre ne doit lire `.mot` directement : c'est cette fonction, et elle seule, qui tient
   la promesse d'AMB-2 (le mot faux partout, y compris dans les blocs générés et dans les
   tablettes déjà lues). Le corpus se repeint entièrement à chaque achat, il n'y a donc
   aucune reprise à faire. */
function motDe(id){ return motSous(id, S_.lect); }
/* Le même mot, sous d'autres lectures : `{}` donne le mot juste, et la relecture (FIN-3) s'en
   sert pour retrouver ce que le joueur lisait avant une révision. Une fonction à part, et non
   un second argument de `motDe` : `motDe` se passe telle quelle à `map`, qui lui donnerait
   l'indice pour lectures. */
function motSous(id, lect){
  const g = byId[id]; if(!g) return null;
  const v = COMPFAUX[id];
  if(v){ const k = partsFausses(id, lect); if(k && v[k]) return v[k].mot; }
  return lect[id] === 'f' ? AMB[id].mot : g.mot;
}
/* La ligne de journal suit la même règle, et pour la même raison : annoncer « le grenier —
   la maison du grain » à un joueur dont le corpus dit « caveau », c'est le jeu qui se
   contredit tout seul, donc qui renseigne. */
function logDe(id){
  const g = byId[id]; if(!g) return '';
  const v = COMPFAUX[id];
  if(v){ const k = partsFausses(id); if(k && v[k] && v[k].log) return v[k].log; }
  return faux(id) ? AMB[id].log : g.log;
}
/* La dette d'une lecture fausse (AMB-3) : de 1 à 3 points, déduits des attestations et non
   choisis. Un signe mal lu 315 fois empoisonne davantage qu'un signe mal lu quatre fois, et
   c'est le corpus qui donne le chiffre — comme le gisement, comme les fréquences.
   Elle n'est lisible NULLE PART avant `peut-être` (MOD-2) : ni compteur, ni infobulle, ni
   carte de fin. Son seul lecteur sera CONTR-1. `freqGlyphe()` est dans rendu.js, chargé
   ensuite — même report que `pushLog` ou `paintCorpus`, appelés d'ici depuis toujours. */
const detteDe = id => { const n = freqGlyphe(id); return n >= 250 ? 3 : n >= 100 ? 2 : 1; };
/* La dette totale se DÉDUIT des lectures, elle ne s'accumule pas. Tenue en solde, elle
   dérivait à la première révision qui ne passait pas exactement par le bon chemin — et un
   solde faux sur un chiffre que personne n'affiche ne se verrait jamais. Dérivée, elle est
   juste par construction, elle survit à n'importe quelle sauvegarde, et CONTR-1 n'aura rien
   à migrer. Elle reste invisible jusque-là (AMB-3). */
const dette = () => S_.gl.reduce((n, id) => n + (AMB[id] && faux(id) ? detteDe(id) : 0), 0);

/* Le multiplicateur d'un signe, majoré de 25 % quand il est mal lu (design doc §8). La prime
   porte sur le BONUS et non sur l'instrument : +30 % devient +37,5 %, pas +62,5 %. Trois
   choses la tiennent :

   - elle est SILENCIEUSE. L'écran de choix affiche la même ligne d'effet pour les deux
     lectures, parce qu'afficher deux chiffres différents ferait de la prime un oracle :
     « prends toujours le plus gros » et l'ambiguïté n'est plus qu'un péage. Le jeu ne
     signale jamais que le choix a été mauvais avant `peut-être` (AMB-1), et un « +37,5 % »
     à l'achat serait ce signal.
   - elle ne décide donc rien à l'achat : elle mord à la RÉVISION (CONTR-2), où corriger une
     lecture coûtera du débit en plus du prix. C'est là qu'est l'optimum local du design
     doc §8 — pas dans le choix, dans le refus de le défaire.
   - un signe qui ne multiplie rien ne gagne rien. Quatre des neuf signes ambigus de l'acte
     III sont dans ce cas, et leur inventer un effet pour porter la prime déplacerait une
     économie réglée sur neuf playtests au profit d'un chiffre que personne ne voit. */
const AMB_R = 1.25;
const mfx = (id, x) => has(id) ? (faux(id) ? 1 + (x - 1)*AMB_R : x) : 1;

/* ======================== le doute, et la révision ========================
   MOD-2 et CONTR-2/3. `peut-être` ne montre pas la vérité — il montre **ce sur quoi la
   décision reposait**. C'est la seule chose que le jeu ait le droit de calculer : la vérité
   ferait un oracle, et rien dans ce jeu ne dit au joueur qu'il s'est trompé (règle 17).

   Le degré de doute d'un signe se fait de deux moitiés, et il fallait les deux : une forme
   multiplicative tassait les neuf signes entre 83 et 99 % — vrai, inutile, et la jauge ne
   classait plus rien.

   - **ce qui était sorti de terre** : la part des attestations du signe que le corpus offrait
     à lire quand le joueur a tranché. On ne peut pas avoir lu ce qui n'était pas déterré.
   - **ce qu'il en a fait** : une concordance sur ce signe vaut plein — c'est l'instrument qui
     rassemble toutes ses attestations d'un coup, et il existe pour ça (règle 11). Un
     recoupement de deux d'entre elles vaut moitié. N'avoir rien fait ne vaut rien, même avec
     les trente tablettes sous les yeux : avoir pu lire n'est pas avoir lu.

   Un signe acheté à la troisième minute sans rien en faire sort à 94 ; le même acheté à la
   fin, concordance faite, sort au plancher. Entre les deux, tout l'éventail.

   Deux propriétés tiennent tout le système :

   1. **Le chiffre est le même pour les deux lectures.** Il ne dit jamais laquelle est juste,
      seulement à quel point on a décidé à l'aveugle. Il ne ment donc pas, et il corrèle quand
      même avec l'erreur : on se trompe davantage sur ce qu'on n'a pas regardé.
   2. **Regarder après coup ne le fait pas baisser.** Une concordance faite aujourd'hui
      n'annule pas une décision prise à la douzième minute. Seule la RÉVISION le recalcule,
      parce qu'elle seule re-décide. C'est ce qui empêche le doute d'être une jauge qu'on
      vide en promenant la souris, et ce qui fait de la lecture le chemin vers la révision
      plutôt que son substitut.

   Le plancher : un signe entièrement travaillé garde cinq points. Le corpus n'a jamais
   confirmé une lecture, il l'a seulement laissée faire — un zéro serait la seule certitude
   que ce jeu n'a pas le droit d'afficher. */
const DOU_MIN = 5;
function douteCalc(id){
  const travail = S_.conc[id] ? 1 : (S_.recs[id] ? 0.5 : 0);
  const vu = 0.5*partOuverte(id) + 0.5*travail;
  return Math.max(DOU_MIN, Math.round(100 * (1 - vu)));
}
/* Les signes ambigus acquis, du plus douteux au moins douteux : l'ordre du panneau, et
   l'ordre dans lequel un joueur qui ne lit pas dépensera ses révisions.
   Un signe acquis avant ce lot n'a pas de relevé de doute — la partie a été jouée quand le
   jeu ne le mesurait pas. Il compte alors pour cent : le jeu ne sait pas ce que le joueur
   avait sous les yeux, et la seule réponse honnête à « je n'en ai aucune trace » est le
   doute entier. Une révision lui en donnera un vrai. */
const douteDe = id => S_.dte[id] === undefined ? 100 : S_.dte[id];
const douteux = () => S_.gl.filter(id => AMB[id])
                           .sort((a, b) => douteDe(b) - douteDe(a));
const douteOuvre = () => has('mik');

/* ---- la révision (CONTR-2) ----
   Rouvrir un signe, repayer, choisir à nouveau. Ce que la révision ne fait PAS, et c'est
   délibéré : elle ne dit pas si l'on avait raison. Elle repeint le corpus, et c'est au
   joueur de lire ce qui en sort — « le grenier pleure trois fois par nuit » n'a pas de sens,
   et c'est la seule chose qui le lui dira (design doc §8). Une révision qui annoncerait
   « juste ! » serait l'oracle que la prime silencieuse d'AMB-1 refuse déjà.
   Le design doc prévoit un **bonus rétroactif** quand on retombe sur la lecture juste. Il
   n'est pas de ce lot, et pour cette raison-là : un bonus visible est un verdict. Il attend
   CONTR-1, où la dette devient lisible et où il pourra être payé en dette effacée plutôt
   qu'en Certitude — c'est-à-dire sans rien annoncer.

   CONTR-3, le coût du brute-force : le prix croît par révision faite, jamais par signe.
   C'est la leçon de `REC_R` et de `COMP_R`, pour la troisième fois — dans une économie
   exponentielle un coût de base ne freine rien, seul un taux mord. Balayer les neuf signes
   ambigus de l'acte III coûte alors plus que ce que le joueur peut gagner d'ici la fin,
   tandis que trois ou quatre révisions choisies restent payables. Mesuré à `outils/sim.py`,
   pas estimé (règle 7). */

/* ======================== la contradiction (CONTR-1) ========================
   « Au franchissement de chaque acte, si dette > seuil, un passage refuse de se résoudre :
   la production de Certitude est divisée par deux jusqu'à révision. On ne perd jamais de
   progression, seulement du débit » (design doc §8).

   **Où elle se déclenche, dans un prototype qui n'a pas le franchissement voulu.** Le design
   place la première contradiction à la fin de l'acte III — c'est-à-dire, ici, sur le dernier
   achat de l'arbre, qui clôt la partie : elle n'aurait pas une seconde pour mordre. Et la
   déclencher plus tôt, à `année`, l'imposerait trente minutes avant que `peut-être` n'existe,
   donc sans explication ni remède : le joueur ne lirait pas une sanction, il lirait un bug.
   Elle se solde donc à **l'ouverture du doute**, et c'est la règle générale dont le prototype
   ne voit que le premier cas : *la contradiction s'évalue à chaque franchissement d'acte à
   partir de `peut-être`*. Avant lui le jeu n'admet pas qu'une lecture puisse être fausse ; il
   ne peut pas en faire payer le prix.

   **Elle se lève dès que la dette repasse sous le seuil**, c'est-à-dire par la révision — et
   c'est là que le « bonus rétroactif » du design doc se paie enfin, en dette effacée et sans
   rien annoncer (voir `reviser`). Levée, elle ne se réarme pas d'elle-même — on ne ballotte
   pas un joueur entre deux états pour un chiffre qu'il ne voit pas : seul le franchissement
   d'acte suivant la re-solde.

   **Le premier franchissement est l'entrée dans l'acte IV** (VOIX-1, 14/10/2026) : le premier
   signe de la Personne, si le doute est ouvert. C'est là que les lectures tranchées APRÈS
   `peut-être` passent enfin au solde — `il-faut`, que le joueur tranche le panneau déjà
   ouvert, et ce que les Élèves ont lu à sa place. Sans lui, qui passait le doute à cinq
   points et lisait ⟨il-faut⟩ de travers n'en payait jamais rien. Mesuré : une dette de 5 à
   l'ouverture du doute (⟨grain⟩ et ⟨avant⟩), plus ⟨il-faut⟩ mal lu, arme la contradiction en
   entrant dans l'acte IV — 136,6-139,9 min au lieu de 115,6-118,9 pour qui ne révise jamais.

   **Le seuil est mesuré.** Les poids de dette étant tirés des attestations, il vaut 0 pour
   une lecture parfaite, 3 pour qui ne rate que les deux signes conçus pour ne pas casser
   (`lire` et `il-faut`, docs/corpus.md §7.4), 6 pour la paire réparante ⟨grain⟩+⟨maison⟩, 8
   en moyenne pour qui tire à pile ou face, 18 pour qui se trompe partout. À **5**, un lecteur
   qui a fait tout ce que le texte permet passe avec de la marge, et la paire réparante
   déclenche — ce que le §7.3 exigeait quand il a été décidé de la laisser passer.

   Mesuré (`outils/sim.py`, joueur qui ne révise jamais, pire cas) : 90,5-93,7 min pour une
   lecture parfaite, 89,1-92,4 pour qui ne rate que les incassables — la prime, sans la
   sanction — et 96,6-103,4 dès qu'elle s'arme. Se tromper faisait gagner cinq minutes et
   demie ; il en coûte onze. Le pire cas n'est pas « tout faux » (96,6, la prime compense) :
   c'est **la paire réparante** à 103,4, qui prend la sanction sans la prime. Le joueur que le
   texte ne peut pas prévenir est celui qui paie le plus, et c'est exactement ce que le §7.3
   annonçait en la laissant passer.

   `S_.contr` est armé à l'achat de `peut-être` ou d'un signe qui franchit un acte, jamais
   ailleurs ; il n'y a pas de tick qui l'allume, pour qu'aucune sanction ne tombe sans un
   geste du joueur juste avant. */
const CONTR_SEUIL = 5;
const CONTR_DIV = 2;
const contrDiv = () => S_.contr ? CONTR_DIV : 1;

/* Le passage qui refuse : tablette 17, quatrième ligne — « eau · ne-pas tablette », la note
   de tri qui dit qu'un relevé manque. Le jeu le fait manquer.
   Elle est FIXE, et elle ne dépend pas des signes mal lus. Choisir la ligne d'après l'erreur
   la désignerait, et ce serait l'oracle que les règles 17 et 18 refusent ; c'est aussi
   pourquoi la ligne de journal dit expressément que ce passage-là n'est pas en cause. Elle
   sort de terre quinzième, donc elle est sous les yeux du joueur depuis longtemps quand elle
   s'éteint, et aucune ligne d'acte IV ou V ne s'y joue — celles-là sont deux lignes plus bas
   (docs/corpus.md, tablette 17). */
const REFUS_T = 17, REFUS_L = 4;
function refusJetons(){
  if(!S_.contr) return null;
  const tb = elCorpus.querySelector('.tablet[data-tb="'+REFUS_T+'"]');
  const ln = tb && tb.children[REFUS_L];
  return ln ? ln.querySelectorAll('.tok') : null;
}

/* Soldée à l'ouverture du doute, puis à chaque franchissement d'acte — et nulle part
   ailleurs. */
function contrSolder(){
  if(S_.contr || dette() <= CONTR_SEUIL) return;
  S_.contr = 1;
  pushLog('Un passage ne se résout plus. Ce n’est pas lui qui est en cause : c’est ce que j’ai lu ailleurs, et je ne sais pas où.');
}
/* Levée par la révision, dès que la dette repasse sous le seuil. Elle ne se réarme pas. */
function contrLever(){
  if(!S_.contr || dette() > CONTR_SEUIL) return;
  S_.contr = 0;
  pushLog('Le passage se résout. Quelque chose que j’avais mal lu ne l’est plus — le corpus ne dira pas quoi.');
}

/* ---- les ruptures vives (MOD-3) ----
   Une rupture est VIVE quand le signe est mal lu et que rien ne la répare. `sauf` est
   l'autre moitié d'une paire réparante : si elle est mal lue aussi, la ligne se tient et ne
   s'allume pas (docs/corpus.md §7.3). C'est la seule endroit du jeu où la décision « on ne
   fait rien » du 14/09 prend une forme exécutable, et elle se lit en une ligne.
   Rien ici ne dépend de `faux` : les ruptures existent depuis la première seconde, dans le
   texte. `faux` ne fait que les allumer — `ruptureLignes()` rend le vide sans lui. */
const ruptureVive = r => faux(r.gl) && !(r.sauf && faux(r.sauf));
const ruptureLignes = () => has('lash') ? RUPTURES.filter(ruptureVive) : [];

const REV_B = 240;      // coût de la première révision, en Certitude
const REV_K = 1.6;      // ... et par révision déjà faite
const revCost = () => Math.ceil(REV_B * Math.pow(REV_K, S_.rev));

/* Rend true si la révision a eu lieu. `lect` vaut 'j' ou 'f' comme à l'achat — et comme à
   l'achat, la fenêtre a tiré l'ordre des deux lectures au sort : repasser par là ne dit
   pas laquelle on avait prise. */
function reviser(id, lect){
  if(!douteOuvre() || !AMB[id] || !has(id)) return false;
  const c = revCost();
  if(S_.C < c) return false;
  S_.C -= c; S_.rev++;
  /* La dette suit d'elle-même : elle se déduit des lectures, donc quitter une lecture fausse
     l'efface et y retomber la refait courir, sans une ligne de comptabilité à tenir. Le
     joueur n'en voit rien dans un cas comme dans l'autre (AMB-3). */
  S_.lect[id] = lect === 'f' ? 'f' : 'j';
  S_.dte[id] = douteCalc(id);
  /* La révision est toujours au joueur, même sur un signe qu'un Élève avait lu ; et une faute
     corrigée reste une faute pour la relecture, qui la montre à part (FIN-3). */
  delete S_.lusEleve[id];
  if(S_.lect[id] === 'f') S_.fautes[id] = 'moi';
  numCache.length = 0;
  pushLog(logDe(id));
  /* Le « bonus rétroactif » du design doc §8, enfin payé — en dette effacée, donc sans rien
     annoncer. Une révision qui fait repasser la dette sous le seuil lève la contradiction ;
     une qui ne suffit pas ne dit rien du tout. */
  contrLever();
  paintCorpus(id);
  return true;
}

/* ======================== l'Élève (ELV-1, ELV-2) ========================
   Septième instrument, et le premier qui soit AMBIVALENT (design doc §5) : il ne produit
   rien, il multiplie ce que rendent les cinq autres — et il déchiffre tout seul.

   **Ce qu'il multiplie.** +5 % par Élève sur le copiste, l'atelier, la table, la concordance
   et la grammaire, linéaire contre un prix géométrique. Pas le relevé : la main suit déjà le
   débit par son tarif (règle 9), la multiplier encore la paierait deux fois. Mesuré
   (`outils/sim.py`) : un multiplicateur global ne touche NI la pire tranche d'I6 — elle est
   à 20-30′, et l'Élève n'ouvre qu'avec la première Grammaire, vers la 48ᵉ minute — NI
   l'écart max entre deux signes. Il ne fait que raccourcir : 6,8 min pour l'acheteur qui en
   prend sept.

   **Ce qu'il déchiffre.** Dès le premier Élève, un signe ambigu n'offre plus ses deux
   lectures : il a été « recopié au propre » avant que le joueur n'y arrive. Le joueur paie
   toujours le signe en Certitude — la règle du §4 tient, on n'achète pas de compréhension
   avec du volume — mais ce n'est plus lui qui tranche. Un Élève seul se trompe 15 fois sur
   cent ; n Élèves, 1 − 0,85ⁿ : 28 % à deux, 48 % à quatre, 68 % à sept. Empiler déchiffre
   vite et faux.

   Trois choses le tiennent du bon côté des règles 17 et 18 :

   - **l'erreur de l'Élève est une LECTURE**, posée dans `S_.lect` comme celle du joueur. La
     dette s'en déduit (`dette()`), la prime silencieuse s'y applique, la contradiction s'en
     solde, `faux` en allume les lignes. Aucun solde à part, aucun chemin à part.
   - **le taux ne s'affiche nulle part.** La ligne de l'instrument dit qu'il déchiffre seul ;
     que ce soit parfois faux se découvre dans le texte, comme tout le reste.
   - **le doute d'un signe lu par l'Élève vaut cent**, quel que soit leur nombre. Le doute dit
     l'aveuglement du joueur au moment de trancher (règle 18), et il n'a rien tranché : c'est
     l'aveuglement entier, identique pour la lecture juste et pour la fausse. L'indexer sur le
     taux d'erreur en ferait un oracle chiffré.

   L'arbitrage, mesuré, joueur qui ne révise jamais : sans Élève 91,1-94,3 min ; sept Élèves
   qui lisent juste, 84,2-87,6 ; sept Élèves qui lisent faux ⟨avant⟩, ⟨ne-pas⟩ et ⟨lire⟩ —
   six points de dette, la contradiction s'arme — 92,6-95,9. Et un seul Élève qui se trompe
   coûte plus cher que sept : 99,5-102,6, la sanction entière pour 5 % de débit.

   Qui veut trancher lui-même lit ses signes ambigus AVANT d'engager le premier Élève, et
   retarde d'autant ce qu'il rapporte. C'est l'arbitrage, et il n'est écrit nulle part. */
const ELV_P = 0.05;     // ce que chaque Élève ajoute à ce que rendent les cinq instruments
const ELV_E = 0.15;     // la part des signes ambigus qu'un Élève seul lit faux
const elvMul = () => 1 + ELV_P*S_.b.elv;
const elvErr = () => 1 - Math.pow(1 - ELV_E, S_.b.elv);
const elvTranche = () => S_.b.elv > 0;
/* Le seul dé du jeu qui décide de quelque chose — celui d'`ambOuvrir` ne tire qu'un ordre
   d'affichage. Il est jeté à l'achat, jamais avant : un tirage fait d'avance et gardé en
   sauvegarde se lirait dans le fichier. */
const elvLecture = () => Math.random() < elvErr() ? 'f' : 'j';

/* ---- économie ---- */
const M = {
  click:()=> 1*(has('anna')?1.25:1)*(has('tab')?1.5:1)*(has('kal')?2:1),
  cop:  ()=> mfx('tem',1.3)*(has('kal')?2:1)*(has('imme')?1.5:1)*elvMul(),
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
  ate:  ()=> mfx('tem',1.3)*(has('kal')?2:1)*(has('mille')?1.3:1)*(has('nurhal')?1.5:1)*(has('imme')?1.5:1)
             *mfx('dun',1.5)*elvMul(),
  tabl: ()=> mfx('kish',1.3)*(has('kal')?2:1)*(has('tabsar')?1.5:1)*elvMul(),
  con:  ()=> mfx('sar',1.5)*(has('kal')?2:1)*elvMul(),
  /* `lire` est le piège majeur de l'ambiguïté (docs/corpus.md §7) : sa lecture fausse,
     « compter », rend 25 % de plus. Il lui fallait donc un effet chiffré, et c'est celui de
     l'instrument qui lit. Cinq multiplicateurs en tout passent par `mfx` — `tem` au copiste
     et à l'atelier, `dun` à l'atelier, `kish` à la table, `sar` à la concordance, `shen`
     ici ; les quatre autres signes ambigus de l'acte III ne multiplient rien. */
  gram: ()=> (has('nurnur')?1.5:1)*(has('kal')?2:1)*mfx('shen',1.5)*elvMul()
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

/* ---- le Corpus jumeau (VOIX-4) ----
   « Une deuxième inscription est trouvée » (design doc §5) : pas un bilingue — la fiction n'en
   a pas —, une copie. La tablette 23 le disait depuis l'acte IV : « si copier 100 · un
   devenir », copié cent fois pour qu'un exemplaire survive. Le jumeau est cet exemplaire-là,
   retrouvé : le même texte, signe pour signe, donc rien de neuf à lire, et tout à relever de
   nouveau. Chaque tablette de la copie a son propre gisement, la MOITIÉ de celui de l'original,
   et son propre tarif, figé au premier relevé qu'on y fait (règle 9) — c'est-à-dire au débit
   de l'acte IV, quand on le fait. Le relevé va à l'original tant qu'il en reste, à la copie
   ensuite.
   Un seul exemplaire à demi-gisement, et c'est ce qui tient la part de la main sous le plafond
   de 40 % : elle remonte à 26-33 % des occurrences avec Élèves et 26 % sans (17,3 et 13,7 sans
   le jumeau) — 26 % à 5 clics par minute, parce qu'un joueur lent ne vide pas la copie avant
   la fin. Un gisement entier la poussait à 43 % à 15 clics par minute (`outils/sim.py`). */
const JUM_F = 0.5;      // le gisement d'une tablette de la copie, en part de l'original
const GIS_COPIE = {};
for(const t in GISEMENT) GIS_COPIE[t] = Math.ceil(GISEMENT[t] * JUM_F);

const gisFait  = t => (S_.rel[t] || []).length;
const gisOrig  = t => GISEMENT[t] - gisFait(t);
const gisCopie = t => S_.b.jum ? GIS_COPIE[t] - (S_.relJ[t] || []).length : 0;
const gisReste = t => gisOrig(t) + gisCopie(t);
/* Le tarif du prochain relevé neuf sur cette tablette : celui de l'original tant qu'il en
   reste, celui de la copie ensuite — `undefined` tant qu'aucun n'est figé. */
const prixEnCours = t => gisOrig(t) > 0 ? S_.prix[t] : S_.prixJ[t];
/* tarif d'un relevé neuf, figé au premier relevé fait sur la tablette (cf. relever()) */
const tarifRel = () => (1 + REL_K*oBrut()) * M.click();
const releveVal = t => (t !== undefined && gisReste(t) > 0) ? (prixEnCours(t) || 1) : M.click();

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
/* La Grammaire cesse de croître avec les mots de la fin (VOIX-3, tranché par l'auteur le
   19/10/2026). Elle compte ce que l'arbre a rendu (règle 13), mais seulement dans les
   branches d'avant l'acte V : une fois les mots de la Personne connus, la grammaire est
   complète, et ⟨finir⟩, ⟨semence⟩ ou ⟨germer⟩ n'en sont pas. C'est l'ordre que la tablette
   28 donne au programme : les nombres, les choses, les verbes.
   Sans ce gel, l'acte V n'a plus de rythme : sous le plafond de 9 999, ses signes tombent
   toutes les 1,4 à 3,7 min, de plus en plus vite. Les questions nées du surplus en portent
   une partie, et ce gel le reste — mesuré, les deux ensemble tiennent I4 avec et sans
   Élèves ; aucun des deux seul ne le fait (`docs/note-questions.md`).
   Dérivé du lexique et non écrit en dur : 36 aujourd'hui, et il le restera quand la branche
   Fin entrera dans `GL`. Sans effet tant qu'elle n'y est pas. */
const nGrammaire = () => { let n=0; for(const id of S_.gl){ const g=byId[id];
  if(g && !g.sec && (ACTE[g.br]||0) < 5) n++; } return n; };
const gramMul = () => Math.pow(GRAM_R, nGrammaire());

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
   unlock:()=>has('nur')},
  /* Ouvert par la première Grammaire, comme chaque instrument l'est par le précédent. Son
     prix est en occurrences, comme les six autres, et c'est sa croissance qui décide de
     combien on en empile — 1,8 en laisse sept à l'acheteur du simulateur, 1,4 en laissait
     dix. Sa ligne dit les deux moitiés de ce qu'il fait, et ne chiffre que la première. */
  {k:'elv', nom:'Élève',                sig:'shen', base:20000,r:1.80,
   ds:()=>'+'+f(ELV_P*100,0)+' % aux autres · déchiffre seul',
   unlock:()=>S_.b.gram>0},
  /* Le Corpus jumeau (VOIX-4) : une copie du corpus, retrouvée — voir `JUM_F`. Ouvert par
     ⟨nous⟩, le premier signe de l'acte IV, et en un seul exemplaire (`max`). */
  {k:'jum', nom:'Corpus jumeau',        sig:'tab',  base:300000,r:1, max:1,
   ds:()=>'une copie de chaque tablette · moitié du gisement',
   unlock:()=>has('nash')},
  /* Le Lecteur (GRAINE-2). « Acheté avant qu'on sache ce que c'est » : pas de ligne d'effet, et
     son nom est un signe du corpus, ⟨devenir-lecture⟩ (`nomLecteur()`), qu'on ne lit qu'au
     dernier achat — sur la tablette 27, « tablette · devenir-lecture ». Ouvert par ⟨semence⟩,
     payé en occurrences comme les huit autres, et 2 de croissance : il en vient trois. */
  {k:'lec', nom:null,                   sig:'tab',  base:500000,r:2.0,
   ds:()=>'',
   unlock:()=>has('mesh')}
];
/* Le nom du Lecteur : le signe tant qu'on ne le sait pas, le mot ensuite — et le mot qu'on
   lit, faux compris (règle 17). Qui compose ⟨devenir-lecture⟩ tôt le lit tôt (règle 25). */
const nomLecteur = () => has('shenke') ? motDe('shenke') : sv('shenke');
const insCost = i => Math.ceil(i.base*Math.pow(i.r,S_.b[i.k]));
/* Un instrument qui ne s'achète qu'une fois : le Corpus jumeau. */
const insPlein = i => !!i.max && S_.b[i.k] >= i.max;
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
/* Rend où le relevé est allé : 'neuf' (l'original), 'copie' (le Corpus jumeau) ou
   'plancher' — le journal d'actions en a besoin, le tarif de la copie ne s'écrivant nulle
   part ailleurs. */
function relever(t, j){
  const l = S_.rel[t] || (S_.rel[t] = []);
  const neuf = t !== undefined && l.length < GISEMENT[t] && l.indexOf(j) < 0;
  const c = t !== undefined && S_.b.jum ? (S_.relJ[t] || (S_.relJ[t] = [])) : null;
  const copie = !neuf && !!c && c.length < GIS_COPIE[t] && c.indexOf(j) < 0;
  /* Première visite : la tablette prend le tarif du débit courant, une fois pour toutes.
     C'est ce qui fait qu'ouvrir une tablette restée intacte vaut de plus en plus cher —
     et donc qu'il reste une raison de parcourir le corpus après la quinzième minute. La
     copie a la sienne, figée de même au premier relevé qu'on y fait. */
  if(neuf){
    if(S_.prix[t] === undefined) S_.prix[t] = tarifRel();
    S_.O += S_.prix[t]; l.push(j);
  } else if(copie){
    if(S_.prixJ[t] === undefined) S_.prixJ[t] = tarifRel();
    S_.O += S_.prixJ[t]; c.push(j);
  } else S_.O += M.click();
  /* Le dire au moment où ça arrive : la cellule qui s'éteint dans la barre est le seul autre
     signal, et le joueur regarde le texte, pas la barre. Quand il n'en reste vraiment plus —
     copie comprise —, pas avant. */
  if((neuf || copie) && gisReste(t) === 0) pushLog('Tablette '+t+' : plus rien à en tirer.');
  S_.clicks++;
  return neuf ? 'neuf' : copie ? 'copie' : 'plancher';
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
  S_.O-=c.O; S_.H-=c.H; gagnerC(recGain()); S_.rec++;
  /* Compté par signe depuis MOD-2 : rapprocher deux attestations d'un même signe est l'un
     des deux gestes sur lesquels se calcule son degré de doute. */
  if(id) S_.recs[id] = (S_.recs[id]||0) + 1;
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
   le journal et la peinture sont l'affaire d'`acheterGl`, qui les fait déjà tous.
   'fin' quand la paire est juste, payable, et donne le dernier signe de l'arbre : rien ne
   bouge encore, c'est la fenêtre des deux fins qui décide, et `achever` rappelle ici pour
   payer. Ça ne renseigne pas plus qu'une réussite, qui l'aurait dit aussi (règle 14). */
function composer(a, b, achever){
  if(!compOuvre() || !has(a) || !has(b) || auCarnet(a, b)) return 'refus';
  const cible = recetteDe(a, b);
  if(cible && has(cible)) return 'refus';        // déjà lu : il n'y a plus rien à trouver
  const c = compCost();
  if(S_.H < c) return 'refus';                   // pas de quoi engager la tentative
  if(cible && !achever && estDernier(cible) && S_.C >= byId[cible].cost) return 'fin';
  S_.comp++;
  if(cible && S_.C >= byId[cible].cost){
    acheterGl(cible);                            // le coût est en Certitude, et lui seul
    return 'acquis';
  }
  /* La tentative a eu lieu : les hypothèses sont perdues dans les deux cas, sans quoi
     l'absence de perte dirait au joueur qu'il vient de trouver. Une paire juste qu'on n'a pas
     les moyens de payer n'entre PAS au carnet — elle se retentera plus tard.

     La ligne de journal ne dit pas laquelle des deux on vient de faire, et n'a plus le droit
     de le deviner : elle disait « ces deux signes ne se rencontrent nulle part », ce qui est
     FAUX dès que la paire existe — cinq des six tentatives de PT10 (COMP-6). Le remède n'est
     pas une meilleure explication, c'est aucune : la grille ne renseigne jamais (règle 14),
     donc elle constate, elle n'explique pas.

     L'écran, lui, les distingue quand même, et par trois signes à la fois : la fausse entre au
     carnet, elle y fait monter le prix de la suivante, et elle rend la paire inretentable.
     Aucun des trois n'est un oubli — ce sont les trois faces de « on ne punit pas une
     trouvaille qu'on n'a pas les moyens de payer ». Le seul levier qui les refermerait est le
     prix (l'indexer sur les tentatives et non sur le carnet), et il ferait payer plus cher
     celui qui a LU juste : l'inverse exact de « lire coûte moins cher que chercher ». On
     laisse donc, en le sachant. */
  S_.H -= c;
  if(!cible) S_.carnet.push(a+'+'+b);
  pushLog('Rien ne vient.');
  return 'rate';
}

/* ======================== les Questions (VOIX-3) ========================
   « On peut interroger le texte, il répond, dans les limites de ce qui a été gravé il y a
   quatre mille ans » (design doc §10). Tranché par l'auteur le 19/10/2026, sur une note
   mesurée (`docs/note-questions.md`).

   **Une question est une condition.** La langue n'a pas d'interrogatif ; ⟨si⟩ est ce qui
   s'en approche le plus, et le corpus en pose seize, chacune suivie de ce qui en découle.
   Le joueur pose ⟨si⟩ et des signes qu'il sait lire ; la réponse est ce qui est gravé
   après cette condition-là, dans toutes les tablettes. Jamais un mot écrit pour l'occasion
   (R8) : la table ci-dessous est lue dans le corpus, une fois, au chargement. Le texte
   répond à des questions que personne n'a posées — « si toi lire · nous ne-pas finir » —
   parce qu'il a été écrit pour un lecteur à venir. C'est l'acte V en avance, et rien ne le
   commente.

   **Ce que la réponse ne fait pas.** Elle ne dépend jamais de la justesse des lectures : elle
   s'écrit avec les mots du joueur, et une lecture fausse peut la rendre absurde — c'est le
   texte qui parle, comme pour les ruptures (règles 17 et 20). Elle ne compte pas dans le
   degré de doute : c'est le texte qui montre, pas le joueur qui rassemble (règle 18, même
   décision que le repli de VOIX-2). Et une condition gravée nulle part ne coûte rien — « Le
   texte ne dit rien. » — ce qui ne renseigne pas : une Concordance sur ⟨si⟩ montre les
   mêmes lignes.

   **Ce qu'elle ouvre.** Un signe que le lexique n'offre pas encore (`rep` dans `GL`) s'y
   offre quand une réponse le porte, et se paie en Certitude comme les autres : la question
   donne l'accès, jamais la compréhension (§4 du design doc). Ce sont les trois mots de la Fin
   qui suivent un « si » — ⟨finir⟩, ⟨devenir⟩, ⟨germer⟩ (GRAINE-1). Voir `offert()`.

   **D'où viennent les questions.** De ce qui déborde. La Certitude s'arrête à 9 999, et I1
   cesse d'être une contrainte sur les prix pour devenir une règle du jeu. À partir de
   ⟨toi⟩, le surplus remplit la question suivante ; une question qui obtient une réponse en
   consomme une. C'est le seul levier mesuré qui n'ait pas de plafond : le prix d'une question
   n'est jamais détenu d'un coup, il peut donc croître — et c'est ce qui manquait à l'acte V
   pour avoir un rythme (ECO-3).
   - 4 000 la question, et douze sur la partie : seize conditions, on ne peut pas tout
     demander. Mesuré avec trois questions sur le chemin de l'acte V et la Grammaire gelée
     (`nGrammaire()`) : 28,2 min d'acte V avec Élèves, 40,3 sans, I4 tenu dans les deux cas.
     Chaque question de plus coûte 1,3 à 1,9 min.
   - avant ⟨toi⟩ le surplus est perdu : il n'y a encore personne à qui la poser. La nuit, de
     même (`veillee()`).
   - le plafond ne retire rien : une Certitude déjà au-dessus, d'une partie d'avant ce lot,
     reste où elle est — elle ne monte plus, c'est tout. On ne perd pas ce qu'on a (R2). */
const C_MAX  = 9999;    // la Certitude ne dépasse jamais quatre chiffres (I1)
const Q_COUT = 4000;    // le surplus qui fait une question
const Q_MAX  = 12;      // les questions de toute la partie (design doc §4)
const questionsOuvertes = () => has('ta');

/* Toute la Certitude gagnée passe par ici : la concordance, la grammaire, le recoupement. */
function gagnerC(x, nuit){
  if(!(x > 0)) return;
  const pris = Math.min(x, Math.max(0, C_MAX - S_.C));
  S_.C += pris;
  if(!nuit) nourrirQuestion(x - pris);
}
/* Ce qui remplit la question suivante : le surplus de Certitude, et le Lecteur (GRAINE-2).
   Rien avant ⟨toi⟩, rien au-delà de la douzième. */
function nourrirQuestion(x){
  if(!(x > 0) || !questionsOuvertes() || S_.qn >= Q_MAX) return;
  S_.qf += x;
  while(S_.qf >= Q_COUT && S_.qn < Q_MAX){ S_.qf -= Q_COUT; S_.qn++; }
  if(S_.qn >= Q_MAX) S_.qf = 0;
}

/* La table des réponses : condition → ce qui la suit, chaque suite distincte une fois, avec
   les lignes qui la portent. La condition est faite des signes entre ⟨si⟩ et le « · »
   suivant, nombres exclus — la palette ne pose que des signes, et « si copier 100 · un
   devenir » répond donc à « si copier », avec ses deux autres suites. Une suite vide est une
   réponse : cinquante-huit lignes de registre finissent sur « si lire », et rien après. */
const QUESTIONS = {};
for(const tb of CORPUS) tb.l.forEach((ln, li) => {
  const segs = [[]];
  for(const tk of ln.split(' ')) if(tk === '·') segs.push([]); else segs[segs.length-1].push(tk);
  segs.forEach((s, i) => {
    const k = s.indexOf('en'); if(k < 0) return;
    const cond = s.slice(k+1).filter(x => x.charCodeAt(0) !== 37);
    if(!cond.length) return;
    const cle = cond.join(' '), suite = segs.slice(i+1).map(z => z.join(' ')).join(' · ');
    const rep = QUESTIONS[cle] || (QUESTIONS[cle] = []);
    let e = rep.find(x => x.suite === suite);
    if(!e) rep.push(e = {suite, lignes: []});
    e.lignes.push([tb.t, li]);
  });
});
/* Les questions en main se déduisent : celles qui sont venues, moins celles qui ont obtenu
   une réponse. Un silence ne coûte rien, il ne se décompte donc pas. */
const questionsEnMain = () => S_.qn - S_.qa.filter(k => QUESTIONS[k]).length;
/* Les signes qu'une réponse a ouverts, déduits eux aussi des conditions posées. */
function ouvertsParReponse(){
  const s = new Set();
  for(const k of S_.qa) for(const e of QUESTIONS[k] || [])
    for(const tk of e.suite.split(' ')) if(tk && tk !== '·' && tk.charCodeAt(0) !== 37) s.add(tk);
  return s;
}
/* Le lexique offre-t-il ce signe ? C'est lui qui garde les deux portes de la Fin, et lui
   seul, comme il garde déjà l'ordre des chaînes : `acheterGl` ne vérifie que le prix, et la
   grille de composition donne un composé dès qu'on en a les parties (règle 15). ⟨germer⟩
   posé à la grille fait donc l'économie de sa question, et ⟨devenir-lecture⟩ composé tôt
   « grille la révélation de vitesse » (design doc §6) — c'est voulu.
   - un mot marqué `rep` attend qu'une réponse l'ait porté (VOIX-3) ;
   - le signe marqué `dernier` attend que tout le reste de l'arbre soit lu : son achat clôt
     la partie (règle 16), et c'est ⟨devenir-lecture⟩ (GRAINE-1). */
const offert = g => (!g.rep || ouvertsParReponse().has(g.id))
                 && (!g.dernier || nArbre() === NGL - 1);
/* Ce signe est-il le dernier de l'arbre qui reste à lire ? Celui-là ne s'achète pas d'un clic,
   ni ne se pose d'un geste : il ouvre les deux fins (FIN-1, FIN-2), au lexique comme à la
   grille. Le dernier, quel qu'il soit — qui a composé ⟨devenir-lecture⟩ tôt finit sur un autre
   mot, il a grillé la révélation (règle 25). */
const estDernier = id => !!byId[id] && !byId[id].sec && !has(id) && nArbre() === NGL - 1;

/* `signes` : les signes posés après ⟨si⟩, dans l'ordre. Rend 'reponse', 'silence', ou
   'refus' quand rien n'a bougé. Une condition déjà posée ne se repose pas : sa réponse est
   au panneau. Sans question en main on ne pose rien du tout — refuser seulement les
   conditions gravées dirait lesquelles le sont. */
function questionner(signes){
  if(!questionsOuvertes() || !signes || !signes.length) return 'refus';
  if(!signes.every(has) || questionsEnMain() < 1) return 'refus';
  const cle = signes.join(' ');
  if(S_.qa.indexOf(cle) >= 0) return 'refus';
  S_.qa.push(cle);
  if(!QUESTIONS[cle]){ pushLog('Le texte ne dit rien.'); return 'silence'; }
  return 'reponse';
}
function acheterIns(k){ const i=INS.find(x=>x.k===k), c=insCost(i);
  if(i.unlock()&&!insPlein(i)&&S_.O>=c){ S_.O-=c; S_.b[k]++;
    /* Le jumeau est un événement, pas un niveau de plus : le dire, comme une tablette qui
       sort de terre. Il ne nomme aucun signe (règle 17). */
    if(k === 'jum') pushLog('Une deuxième inscription, gravée ailleurs : le même texte, signe pour signe.'); } }
/* Le signe qu'on vient d'acquérir est-il le premier de son acte ? Appelée après l'ajout à
   `S_.gl`. Un composé secret ne franchit rien : il n'avance pas l'arbre (règle 13). */
const franchit = id => {
  const a = ACTE[byId[id].br];
  return !!a && !byId[id].sec
    && !S_.gl.some(x => x !== id && byId[x] && !byId[x].sec && ACTE[byId[x].br] === a);
};
/* `lect` vaut 'j' ou 'f' pour un signe ambigu, et rien pour tous les autres. Une lecture
   non tranchée est la juste : c'est le cas d'un composé posé à la grille — laquelle n'offre
   aucun choix et ne doit surtout pas en offrir un — et de tout appel d'avant ce lot.
   `eleve` dit que la lecture vient d'un Élève et non du joueur (ELV-2). */
function acheterGl(id, lect, eleve){
  /* Une partie interrompue ne se reprend pas (FIN-2) — et c'est ici que ça se tient, sur le
     seul chemin qui paie, parce que l'interface met quatorze secondes à s'en aller et que la
     carte du signe laissé, ou la grille, restent sous la main pendant ce temps. */
  const g=byId[id]; if(has(id)||S_.C<g.cost||S_.fin==='interrompue') return;
  const avant = CORPUS.map(pctTablette);
  S_.C-=g.cost; S_.gl.push(id);
  /* La dette est posée ici et nulle part ailleurs, à l'instant du choix, et personne ne la
     relit avant CONTR-1. Le joueur n'en verra rien : pas de compteur, pas d'infobulle, pas
     de ligne à la carte de fin (AMB-3). */
  if(AMB[id]){
    S_.lect[id] = lect==='f' ? 'f' : 'j';
    /* Le doute se fige ici, sur l'état du corpus et du travail à cette seconde-là. Rien ne
       le rouvrira qu'une révision : regarder après coup ne rend pas la décision moins
       aveugle (MOD-2). La dette, elle, n'a rien à poser — elle se déduit (`dette()`). */
    S_.dte[id] = eleve ? 100 : douteCalc(id);
    /* Ce que la relecture avouera (FIN-3) : qui a tranché ce signe, et s'il a été lu faux. */
    if(eleve) S_.lusEleve[id] = true; else delete S_.lusEleve[id];
    if(S_.lect[id] === 'f') S_.fautes[id] = eleve ? 'eleve' : 'moi';
    /* Dit avant la ligne du signe, et sans rien dire de la lecture : le joueur qui avait
       vu la fenêtre des deux mots lirait son absence comme une panne. */
    if(eleve) pushLog('Un élève l’avait déjà recopié au propre.');
  }
  majSignes();
  numCache.length = 0;
  touchees = new Set();
  CORPUS.forEach((tb,i)=>{ if(pctTablette(tb) > avant[i] + 1e-9) touchees.add(tb.t); });
  pushLog(logDe(id));
  /* Avant le repeint, et non après : c'est lui qui retire le passage retenu. Le corpus ne se
     repeint qu'à l'achat, jamais à la frame — un solde posé ensuite n'apparaîtrait qu'au
     glyphe suivant, et sur `peut-être` il n'y en a pas forcément. */
  if(id === 'mik' || (douteOuvre() && franchit(id))) contrSolder();
  paintCorpus(id);
  /* ⟨toi⟩ replie le corpus sur ce qui s'adressait au lecteur (VOIX-2, rendu.js). Une fois, à
     l'achat : la relecture suffit. */
  if(id === 'ta') adresser();
  lastPct=-1;
  if(id==='an'||id==='kal'){ const b=$('bloom'); b.classList.remove('on'); void b.offsetWidth; b.classList.add('on'); }
  /* Le dernier signe de l'arbre est lu : c'est « achever » (FIN-1). La fenêtre des deux fins
     est devant, au lexique et à la grille ; `acheterGl` reste le seul chemin qui paie. */
  if(nArbre()===NGL){ S_.done=true; S_.fin='achevee'; finArmer(); }
}
/* « Interrompre » (FIN-2) : laisser le dernier signe non lu. La partie s'arrête là, sur le
   corpus tel qu'il est, et ne se reprend pas — ni maintenant, ni au chargement. Aucune des
   deux fins n'est la bonne : celle-ci ne coûte rien, mais elle ne s'offre qu'à qui pourrait
   payer l'autre, sans quoi elle serait le repli de celui qui ne peut pas. `id` est le signe
   laissé, que le journal d'actions retient. */
function interrompre(id){
  if(S_.done || !estDernier(id) || S_.C < byId[id].cost) return;
  S_.done = true; S_.fin = 'interrompue';
  finDesarmer(); finFiger(false);
}

/* ---- l'effacement attend qu'on ait lu ----
   Le dernier achat de l'arbre est aussi celui qui rend lisible ce que la partie avait à dire :
   ⟨devenir-lecture⟩ n'a qu'une attestation, sur la tablette 27. Commencer à effacer l'écran à
   la seconde du clic, c'est retirer cette tablette-là avant qu'on l'ait regardée. C'était
   déjà vrai de la carte de statistiques qui tenait lieu de fin jusqu'aux deux fins ; ce l'est
   davantage d'un effacement qui emporte le texte. Il attend donc qu'on soit allé voir. Rien
   de neuf pour ça : `touchees` sait déjà quelles tablettes le dernier signe a changées,
   `tabletteVisible()` sait laquelle on a sous les yeux, et l'effacement commence quand les
   deux se rencontrent.
   Les deux bornes sont des garde-fous, pas des réglages. Six secondes au plus tôt, sinon il
   tomberait sur le joueur déjà posé sur la bonne tablette, à l'instant où les mots changent
   sous ses yeux ; quatre-vingt-dix au plus tard, sinon celui qui ne va pas voir n'aurait pas
   de fin du tout.
   `S_.done` est posé tout de suite, lui : la production s'arrête net pendant qu'on lit la
   dernière tablette. À la fin, il ne reste que le texte (design doc §11). */
const FIN_MIN = 6, FIN_MAX = 90;   // secondes d'horloge, et non de jeu : le jeu est arrêté
let finArmee = 0, finLire = null;
/* Les tablettes sont retenues à l'armement, et non relues au moment d'effacer : rien
   n'interdit de composer un signe une fois l'arbre fini, et `touchees` désignerait alors les
   tablettes de ce composé-là, pas celles du dernier signe de l'arbre. */
const finArmer = () => { finArmee = performance.now(); finLire = new Set(touchees); };
/* « recommencer » ne recharge pas la page : un effacement armé sur la partie d'avant
   viendrait vider la partie neuve, deux secondes après le clic. C'est le défaut qu'avait déjà
   `majSignes()` — 229 nombres encore lisibles sur une partie censée vierge. */
const finDesarmer = () => { finArmee = 0; };
function finRegarder(now){
  if(!finArmee) return;
  const dt = (now - finArmee)/1000;
  if(dt < FIN_MIN) return;
  /* Un dernier signe qui ne rendrait rien lisible n'aurait rien à faire lire : l'effacement
     ne se ferait pas attendre pour rien. Vrai d'aucun signe aujourd'hui ; vrai du jour où
     l'ordre de l'arbre changera. */
  const vue = tabletteVisible();
  if(finLire.size && dt < FIN_MAX && !(vue && finLire.has(+vue.dataset.tb))) return;
  finArmee = 0; finEffacer();
}

/* ============================ boucle ============================ */
function tick(dt){
  S_.t += dt;
  produire(dt);
  lireCorpus(dt);
}
/* ---- le Lecteur (GRAINE-2) ----
   « Ce n'est pas un instrument : c'est le corpus qui a commencé à lire » (design doc §5). Il ne
   produit rien. Il lit le corpus tout seul, une tablette par minute et par Lecteur, dans
   l'ordre des numéros — l'ordre du temps, une fois le corpus rangé —, et chaque tablette lue
   remplit un peu la question suivante : trente tablettes, 9 000 au plus. Rien ne le dit ; on
   le voit faire, dans la barre et dans le texte (`peindreLecteur()`), comme on avait vu le
   compteur monter à l'acte I.
   Il lit les tablettes encore sous terre aussi : le corpus lit ce que le joueur n'a pas
   encore dégagé. Il ne lit pas la nuit — `tick` ne tourne pas hors ligne —, et la nuit ne
   remplit jamais une question (règle 24).
   Mesuré (`outils/sim.py`) : l'acte V passe de 28,2 à 25,6 min avec Élèves et de 40,3 à
   36,3 sans, et le pire trou sans Élève de 7,2 à 5,8 min. Ce sont les attentes de question
   qu'il comble. */
const LEC_V = 1/60;     // tablettes lues par seconde et par Lecteur
const LEC_Q = 300;      // ce qu'une tablette lue verse à la question suivante
function lireCorpus(dt){
  if(!S_.b.lec || S_.tete >= CORPUS.length) return;
  const avant = Math.floor(S_.tete);
  S_.tete = Math.min(CORPUS.length, S_.tete + S_.b.lec * LEC_V * dt);
  for(let k = avant; k < Math.floor(S_.tete); k++) nourrirQuestion(LEC_Q);
}
/* La production, séparée du temps de jeu : la nuit passée hors ligne se rattrape par ici
   sans avancer le chronomètre ni traverser l'horloge instrumentée du journal d'actions. */
/* `nuit` : la production vient de la veillée. Elle remplit la Certitude jusqu'au plafond,
   jamais une question (VOIX-3). */
function produire(dt, nuit){
  S_.O += oBrut()*dt;
  // table de fréquences : consomme des occurrences
  const wantO = S_.b.tab*1.0*dt;
  if(wantO>0){ const canO=Math.min(wantO,S_.O); const fr=canO/wantO;
    S_.O-=canO; S_.H += S_.b.tab*0.6*M.tabl()*fr*dt; }
  // concordance : consomme des hypothèses
  const wantH = S_.b.con*0.5*dt;
  if(wantH>0){ const canH=Math.min(wantH,S_.H); const fr=canH/wantH;
    S_.H-=canH; gagnerC(S_.b.con*CON_P*M.con()*fr*dt/contrDiv(), nuit); }
  // grammaire : en consomme beaucoup plus, et rend d'autant plus qu'on a déchiffré
  const wantG = S_.b.gram*GRAM_C*dt;
  if(wantG>0){ const canG=Math.min(wantG,S_.H); const fr=canG/wantG;
    S_.H-=canG; gagnerC(S_.b.gram*GRAM_P*gramMul()*M.gram()*fr*dt/contrDiv(), nuit); }
}

/* ---- la nuit ----
   `nuit` est le seul glyphe dont l'effet se produit quand le jeu est fermé : 40 % du débit,
   quatre heures au plus (design doc §9). Avant lui il ne se passe rien hors ligne, et c'est
   diégétique — il n'y a personne pour lire. On rattrape en tranches d'une minute plutôt
   qu'en un seul bond : les convertisseurs se coupent quand leur intrant manque, et un
   unique appel de quatre heures leur ferait ignorer cette coupure.
   Depuis VOIX-3, la nuit remplit la Certitude jusqu'à 9 999 et pas au-delà. Elle rapportait
   avant ça quatorze à dix-sept mille Certitude dès l'achat de `nuit`, et soixante-six à
   quatre-vingt-neuf mille à celui de ⟨nous⟩ — deux fois toute la branche Personne, à dépenser
   au retour (`docs/note-questions.md`, §5). Et elle ne remplit pas de question : une question
   demande quelqu'un pour la poser. */
function veillee(){
  if(!has('esh') || S_.done || !S_.ts) return 0;
  const ecoule = Math.min((Date.now() - S_.ts)/1000, 4*3600);
  if(ecoule < 60) return 0;
  const avant = S_.O;
  let reste = ecoule * 0.4;
  while(reste > 0){ const pas = Math.min(60, reste); produire(pas, true); reste -= pas; }
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
  paintRes(); paintActs(); paintInstr(); paintComp(); paintQuest(); paintDoute(); paintLex(); paintMeter();
  peindreLecteur();
  finRegarder(now);
  /* Le chrono est hors jeu : la version publique n'en a pas, et une boucle qui le cherche
     quand même s'arrêterait à la première frame. */
  const el=$('chrono');
  if(el){ const ch=Math.floor(S_.t/60)+':'+String(Math.floor(S_.t%60)).padStart(2,'0');
    if(el.textContent!==ch) el.textContent=ch; }
  requestAnimationFrame(frame);
}
