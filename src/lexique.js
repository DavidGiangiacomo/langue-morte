/* « La langue morte » — les glyphes des actes I à III
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
  {id:'mille',br:'nombre',  mot:'mille',    cost:110, eff:'tous les nombres du corpus · +30 % à l’atelier de copie',
   log:'Mille. Ils comptaient leurs tablettes par milliers, et le grain par dizaines.'},
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
   log:'Copier. Deux fois, puis dix, puis cent. Bien plus qu’il n’en fallait pour garder.'},
  /* ---- acte III : le temps ----
     La branche ne donne pas un bonus de plus, elle donne une dimension. `année` fait
     apparaître une date que le corpus portait depuis la première seconde ; `avant` range
     l’index, `après` range le texte lui-même. Ce que ce rangement découvre — la crue qui
     baisse sur deux siècles — n’est écrit nulle part et n’est commenté par personne :
     c’est dans les chiffres, et il faut les avoir mis en ordre pour le voir. */
  {id:'nur',  br:'temps',   mot:'année',    cost:60, eff:'chaque tablette porte sa date · la grammaire devient possible',
   log:'Année. Chaque tablette est datée depuis le début — je ne savais pas lire la date.'},
  {id:'pat',  br:'temps',   mot:'avant',    cost:130, eff:'la barre se range dans l’ordre du temps',
   log:'Avant. Ce qui est sorti de terre en premier n’a pas été gravé en premier.'},
  {id:'zur',  br:'temps',   mot:'après',    cost:190, eff:'le corpus se range dans l’ordre du temps',
   log:'Après. Le corpus se remet en ordre. Deux siècles, du premier relevé au dernier.'},
  {id:'nurnur',br:'temps',  mot:'siècle',   cost:260,eff:'+50 % à la grammaire',
   log:'Siècle. Ils mesuraient par centaines d’années. Il leur en restait deux.'},
  {id:'esh',  br:'temps',   mot:'nuit',     cost:360,eff:'la lecture continue hors ligne — 40 % du débit, 4 h au plus',
   log:'Nuit. Ils gravaient la nuit. Le corpus se lit maintenant sans moi.'},
  {id:'nurhal',br:'temps',  mot:'dernière-année',cost:500,eff:'les deux dernières tablettes se datent · +50 % à l’atelier de copie',
   log:'La dernière année. Elle n’a pas de nombre : après elle, personne n’a plus compté.'},
  /* ---- les composés secrets ----
     `sec` veut dire : aucune branche ne l’offre, il ne s’obtient qu’en le composant. Il ne
     compte donc pas dans la progression de l’arbre — ni pour la fin de partie, ni pour les
     tablettes dégagées, ni pour la Grammaire (voir `nArbre()` dans economie.js). Le seul
     effet de `grenier` est qu’on le lit : vingt-quatre attestations qui passent en français,
     et rien de plus. Un joueur peut finir la partie sans jamais le trouver. */
  {id:'urtem',br:'matiere', sec:true, mot:'grenier', cost:60, eff:'le grenier se lit — un mot qu’aucune branche n’offrait',
   log:'Le grenier — la maison du grain. Personne ne me l’a appris : c’était écrit dans le signe.'}
];
/* Le lexique compte ce que l’arbre offre. Un composé secret s’ajoute au savoir du joueur sans
   s’ajouter à sa progression : le compteur reste « x / 20 », et l’économie mesurée sur neuf
   playtests ne bouge pas parce qu’on a trouvé un signe de plus. */
const NGL = GL.filter(g=>!g.sec).length;
const BR = [['nombre','Nombre'],['matiere','Matière'],['parole','Parole'],['temps','Temps']];
const byId = Object.fromEntries(GL.map(g=>[g.id,g]));

/* ============================ recettes ============================ */
/* `COMP` dit comment un signe se DESSINE : ses valeurs sont des clés de tracé, et la branche
   Nombre y paraît sous son chiffre (`u1` pour ⟨un⟩, `t10` pour ⟨dix⟩). Une recette dit ce qu’on
   peut POSER : deux glyphes du lexique. La traduction se fait une fois, ici.

   Le filtre est ce qui empêche la grille d’offrir un signe qui n’existe pas — `selanna`
   (vingt) reste dessinable mais a été retiré du lexique, et les composés des actes IV et V
   n’ont pas encore leurs parties. Chaque recette apparaîtra d’elle-même le jour où sa cible et
   ses deux parties seront au lexique : il n’y a aucune liste à tenir à jour. */
const RECETTES = {};
for(const cible in COMP){
  const [a, b] = COMP[cible].map(k => GLTRACE[k] || k);
  if(byId[cible] && byId[a] && byId[b]) RECETTES[cible] = [a, b];
}
/* L’ordre fait partie de la recette : `notre-fin` et `nous-fûmes` sont les deux mêmes signes
   dans les deux sens. Le corpus le dit — ⟨grenier⟩ porte la maison à gauche et le grain à
   droite depuis la première seconde. Qui lit, voit l’ordre. */
const PAIRES = Object.fromEntries(Object.entries(RECETTES).map(([c,[a,b]]) => [a+'+'+b, c]));
const recetteDe = (a, b) => PAIRES[a+'+'+b];
