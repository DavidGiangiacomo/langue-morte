/* « La langue morte » — les 13 glyphes du MVP (actes I-II)
   Scripts classiques, portée globale partagée, chargés dans l'ordre de index.html.
   Aucune dépendance externe hors les polices Google. */
"use strict";

/* ============================ lexique ============================ */
const GL = [
  {id:'an',   br:'nombre',  mot:'un',       cost:2,  eff:'les relevés en chiffres · le signe « un » dans les tablettes',
   log:'Un trait. Un. Mes propres comptes se tiennent enfin — les leurs, à peine.'},
  {id:'anna', br:'nombre',  mot:'deux',     cost:5,  eff:'le redoublement : un signe répété s’additionne · nombres jusqu’à 4 · les coûts en chiffres · +25 % au relevé',
   log:'Deux traits pour deux. Un signe répété s’ajoute à lui-même — tout le système tient là-dedans.'},
  {id:'hem',  br:'nombre',  mot:'cinq',     cost:11, eff:'le principe du cinq · nombres jusqu’à 9',
   log:'Cinq. Un signe qui vaut cinq du rang d’en dessous — et à tous les rangs.'},
  {id:'sela', br:'nombre',  mot:'dix',      cost:18, eff:'les débits en chiffres · nombres jusqu’à 99',
   log:'La main : dix. Ils comptaient sur les mains, comme tout le monde.'},
  {id:'meku', br:'nombre',  mot:'cent',     cost:33, eff:'nombres jusqu’à 999 · grands nombres repliés · achat ×10',
   log:'Cent. Les récoltes deviennent lisibles. Et elles baissent.'},
  {id:'tem',  br:'matiere', mot:'grain',    cost:3,  eff:'+30 % au copiste',
   log:'Du grain. Ce ne sont pas des prières : ce sont des inventaires.'},
  {id:'ur',   br:'matiere', mot:'maison',   cost:6,  eff:'les instruments prennent leur nom',
   log:'Une maison. Les outils du corpus prennent un nom.'},
  {id:'tab',  br:'matiere', mot:'tablette', cost:14, eff:'+50 % au relevé',
   log:'La tablette se nomme elle-même. Ils comptaient leurs tablettes comme leur grain.'},
  {id:'kish', br:'matiere', mot:'eau',      cost:22, eff:'+30 % à la table de fréquences',
   log:'L’eau. Un relevé par année, tenu sur deux siècles.'},
  {id:'gan',  br:'matiere', mot:'champ',    cost:40, eff:'recoupement −25 % de coût',
   log:'Le champ. Quatre champs, et les nombres qui baissent d’une tablette à l’autre.'},
  {id:'im',   br:'parole',  mot:'dire',     cost:8,  eff:'le lexique annonce ce qu’il fait',
   log:'Dire. Le lexique cesse d’être un pari.'},
  {id:'sar',  br:'parole',  mot:'graver',   cost:27, eff:'+50 % à la concordance',
   log:'Graver. Quelqu’un a tenu ce stylet, et l’a écrit.'},
  {id:'kal',  br:'parole',  mot:'copier',   cost:48, eff:'×2 sur toute la production',
   log:'Copier. Deux fois, puis dix, puis cent. Bien plus qu’il n’en fallait pour garder.'}
];
const NGL = GL.length;
const BR = [['nombre','Nombre'],['matiere','Matière'],['parole','Parole']];
const byId = Object.fromEntries(GL.map(g=>[g.id,g]));
