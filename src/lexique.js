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
  /* ---- acte III : la Parole ----
     Le corpus se met à parler de lui-même : qui grave, ce qu’on garde, et ce qu’il faut en
     faire. Les trois signes y sont depuis la première seconde — `scribe` signe vingt-sept
     tablettes, et il se dessine ⟨dire⟩ sur ⟨graver⟩ ; `archive`, ⟨tablette⟩ sur ⟨graver⟩.
     Tous deux se composent donc dès que la grille s’ouvre (règle 15), et un joueur qui les a
     reconnus peut les poser avant que la branche ne les offre. Ce sont des signes d’arbre :
     posés en avance, ils avancent la partie, comme `deux` et `siècle`.
     `lire` sera le piège majeur de l’ambiguïté (docs/corpus.md §7) : son effet est chiffré
     parce que sa lecture fausse devra le majorer. Son texte ne doit rien en laisser deviner. */
  {id:'shen', br:'parole',  mot:'lire',     cost:300, eff:'+50 % à la grammaire',
   log:'Lire. Ce n’est pas un inventaire qui le dit, c’est une consigne — et elle revient d’une tablette à l’autre.'},
  {id:'imme', br:'parole',  mot:'scribe',   cost:600, eff:'+50 % au copiste et à l’atelier de copie',
   log:'Scribe. Celui qui dit et qui grave. Chaque tablette finit sur ce mot : je lisais une signature sans le savoir.'},
  {id:'tabsar',br:'parole', mot:'archive',  cost:900, eff:'+50 % à la table de fréquences',
   log:'L’archive. Une tablette, puis trois cents, puis mille deux cents. Ils ne rangeaient pas le grain : ils rangeaient les tablettes.'},
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
  /* ---- acte III : la modalité ----
     Quatre signes pour 816 attestations, un signe du corpus sur cinq. Ce sont les plus
     fréquents qui restaient, et ils étaient illisibles : ⟨ne-pas⟩ seul paraît 290 fois.
     La branche ne donne presque pas de multiplicateurs, et c'est mesuré, pas oublié —
     donner à `si` le troisième ×1,5 de la Grammaire faisait finir l'acte en 82,5 min au
     lieu de 87,0, soit quatre signes de plus pour une minute de jeu (`outils/sim.py`).
     Dans une économie exponentielle, un bonus sur l'instrument qui porte la Certitude
     rend plus qu'il ne coûte : la même leçon que `REC_R`, par l'autre bout.
     Ce que la branche donne, c'est de la lecture. Les registres de distribution sont
     salés de conditions depuis la première seconde — « ur %24 · la · urtem la · pat ·
     nur la », le foyer sans grenier et sans année — et le protocole de copie s'achève
     sur un mot qu'on ne savait pas lire. La zone d'interface de la Modalité (le panneau
     de révision, les indices de confiance, design doc §6) n'existe pas encore : elle
     s'ouvrira à `peut-être`, et ces quatre-là y arrivent en avance.
     `il-faut` est, avec `lire`, l'un des deux signes ambigus conçus pour NE PAS casser
     mécaniquement (docs/corpus.md §7) : sa lecture fausse, « on peut », transforme les ordres
     en permissions sans produire une seule absurdité — un corpus cohérent, et plus plat. Le
     jour où AMB-1 arrivera, ne pas lui chercher de garde-fou : c'est voulu. */
  {id:'la',   br:'modalite',mot:'ne-pas',  cost:150, eff:'ce qui manque se lit : les foyers vides, les greniers vides',
   log:'Ne pas. Le signe le plus fréquent de tout le corpus est une négation — et les colonnes que je croyais inachevées disent qu’il n’y avait rien.'},
  {id:'en',   br:'modalite',mot:'si',      cost:320, eff:'les conditions se lisent — un registre est plein de « si »',
   log:'Si. Ils ne consignaient pas seulement ce qui était : ils gravaient ce qu’il faudrait faire au cas où.'},
  {id:'dun',  br:'modalite',mot:'il-faut', cost:550, eff:'+50 % à l’atelier de copie',
   log:'Il faut. Ce n’est plus un inventaire qui parle, c’est quelqu’un qui ordonne — et sur deux siècles, l’ordre ne change pas : copier.'},
  {id:'enla', br:'modalite',mot:'sinon',   cost:800, eff:'le protocole de copie se lit jusqu’à son dernier mot',
   log:'Sinon. La consigne s’arrête là. Ils n’ont jamais gravé ce qui vient après « sinon » — ou bien c’est arrivé.'},
  /* ---- les composés secrets ----
     `sec` veut dire : aucune branche ne l’offre, il ne s’obtient qu’en le composant. Il ne
     compte donc pas dans la progression de l’arbre — ni pour la fin de partie, ni pour les
     tablettes dégagées, ni pour la Grammaire (voir `nArbre()` dans economie.js). Le seul
     effet de `grenier` est qu’on le lit : vingt-quatre attestations qui passent en français,
     et rien de plus. Un joueur peut finir la partie sans jamais le trouver. */
  {id:'urtem',br:'matiere', sec:true, mot:'grenier', cost:60, eff:'le grenier se lit — un mot qu’aucune branche n’offrait',
   log:'Le grenier — la maison du grain. Personne ne me l’a appris : c’était écrit dans le signe.'},
  /* `zéro` est le seul composé dont les deux parties viennent de deux branches et de deux
     actes — ⟨ne-pas⟩ posé sur ⟨un⟩. Le design doc lui prête « la notation compacte des
     grands nombres » ; elle est déjà celle de `cent`, acquise par tout le monde, et la
     déplacer sur un composé facultatif la retirerait à la plupart des joueurs. Son effet
     est donc celui du grenier : on le lit, et c'est tout. Ce qu'on lit, c'est la
     tablette 29 — un registre de zéros, un seul signe répété pendant toute la partie
     (docs/corpus.md §5), qui passe d'un coup en chiffres. `numLisible()` l'attend depuis
     l'acte I : un nombre nul n'est lisible que si l'on a ce signe-là. */
  {id:'lan',  br:'nombre',  sec:true, mot:'zéro',    cost:120, eff:'le zéro se lit — les registres vides passent en chiffres',
   log:'Zéro. Ne-pas un : ils ont écrit l’absence comme un nombre et l’ont rangée dans la colonne des nombres. Je le regardais depuis le début sans le compter.'}
];
/* Le lexique compte ce que l’arbre offre. Un composé secret s’ajoute au savoir du joueur sans
   s’ajouter à sa progression : le compteur reste « x / 20 », et l’économie mesurée sur neuf
   playtests ne bouge pas parce qu’on a trouvé un signe de plus. */
const NGL = GL.filter(g=>!g.sec).length;
const BR = [['nombre','Nombre'],['matiere','Matière'],['parole','Parole'],['temps','Temps'],['modalite','Modalité']];
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
