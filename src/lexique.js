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
  /* ---- acte III : le nom, et ce qu'il laisse à lire ----
     Dernier signe de l'acte, et de loin le plus rare : trois attestations, toutes sur la
     tablette 18. C'est un mauvais achat pour tout épigraphiste qui compte — 1 200 C pour
     trois occurrences quand `ne-pas` en rendait 290 pour 150 — et la Table de fréquences
     l'affiche en toutes lettres à côté du prix. C'est voulu : ce qu'on paie ici n'est pas
     de la lisibilité, c'est une phrase.
     AUCUN effet chiffré, et ce n'est pas un oubli : c'est une mesure. `les-lecteurs` est le
     dernier achat de l'arbre, donc `nArbre() === NGL` clôt la partie à la seconde même où
     le multiplicateur commencerait à rendre. Cinq variantes — concordance, table, grammaire,
     atelier, aucune — à trois cadences donnent la même durée à la décimale près. Un effet
     posé ici ne serait pas un réglage, ce serait une décoration. Le jour où l'acte IV le
     mettra au milieu de l'arbre, la question se mesurera pour la première fois.
     Ce que l'achat ne donne PAS : ⟨nous⟩. Le signe se dessine ⟨lire⟩ sur ⟨nous⟩ (table COMP),
     et ⟨nous⟩ se tient seul juste devant lui, sur la même ligne — 41 fois dans le corpus,
     jamais au lexique avant la branche Personne. La tablette 18 passe de 68 % à 80 % de
     lisibilité et s'arrête là : ils se nomment, et le mot qui dit « nous » reste à
     déchiffrer. La porte de l'acte IV est dans le texte, pas dans une annonce.
     Aucune recette ne s'ouvre pour autant (règle 15) : `RECETTES` filtre sur les deux
     parties, et `nash` n'est pas au lexique. Il ne se composera que le jour où `nous` y
     entrera — et ce jour-là, la grille l'offrira d'elle-même. */
  {id:'shenu',br:'parole', mot:'les-lecteurs', cost:1200,
   eff:'le nom qu’ils se donnaient se lit — trois attestations, une seule tablette',
   log:'Les lecteurs. Ils se nommaient d’après ce qu’ils faisaient — et la moitié du nom est un signe que je ne sais pas lire, qui se tient seul juste devant, sur la même ligne.'},
  /* ---- acte III : le temps ----
     La branche ne donne pas un bonus de plus, elle donne une dimension. `année` fait
     apparaître une date que le corpus portait depuis la première seconde ; `avant` range
     l’index, `après` range le texte lui-même. Ce que ce rangement découvre — la crue qui
     baisse sur deux siècles — n’est écrit nulle part et n’est commenté par personne :
     c’est dans les chiffres, et il faut les avoir mis en ordre pour le voir. */
  {id:'nur',  br:'temps',   mot:'année',    cost:60, eff:'la première ligne de chaque tablette se lit en entier · la grammaire devient possible',
   log:'Année. Chaque tablette est datée depuis le début — je ne savais pas lire la date.'},
  {id:'pat',  br:'temps',   mot:'avant',    cost:130, eff:'la barre se range dans l’ordre du temps',
   log:'Avant. Ce qui est sorti de terre en premier n’a pas été gravé en premier.'},
  {id:'zur',  br:'temps',   mot:'après',    cost:190, eff:'le corpus se range dans l’ordre du temps',
   log:'Après. Le corpus se remet en ordre. Deux siècles, du premier relevé au dernier.'},
  {id:'nurnur',br:'temps',  mot:'siècle',   cost:260,eff:'+50 % à la grammaire',
   log:'Siècle. Ils mesuraient par centaines d’années. Il leur en restait deux.'},
  {id:'esh',  br:'temps',   mot:'nuit',     cost:360,eff:'la lecture continue hors ligne — 40 % du débit, 4 h au plus',
   log:'Nuit. Ils gravaient la nuit. Le corpus se lit maintenant sans moi.'},
  {id:'nurhal',br:'temps',  mot:'dernière-année',cost:500,eff:'les deux dernières tablettes se lisent · +50 % à l’atelier de copie',
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
  {id:'urtem',br:'matiere', sec:true, mot:'grenier', cost:60, eff:'un mot qu’aucune branche n’offrait — vingt-quatre attestations',
   log:'Le grenier — la maison du grain. Personne ne me l’a appris : c’était écrit dans le signe.'},
  /* `zéro` est le seul composé dont les deux parties viennent de deux branches et de deux
     actes — ⟨ne-pas⟩ posé sur ⟨un⟩. Le design doc lui prête « la notation compacte des
     grands nombres » ; elle est déjà celle de `cent`, acquise par tout le monde, et la
     déplacer sur un composé facultatif la retirerait à la plupart des joueurs. Son effet
     est donc celui du grenier : on le lit, et c'est tout. Ce qu'on lit, c'est la
     tablette 29 — un registre de zéros, un seul signe répété pendant toute la partie
     (docs/corpus.md §5), qui passe d'un coup en chiffres. `numLisible()` l'attend depuis
     l'acte I : un nombre nul n'est lisible que si l'on a ce signe-là. */
  {id:'lan',  br:'nombre',  sec:true, mot:'zéro',    cost:120, eff:'les registres vides passent en chiffres',
   log:'Zéro. Ne-pas un : ils ont écrit l’absence comme un nombre et l’ont rangée dans la colonne des nombres. Je le regardais depuis le début sans le compter.'}
];
/* Le lexique compte ce que l’arbre offre. Un composé secret s’ajoute au savoir du joueur sans
   s’ajouter à sa progression : le compteur reste « x / 20 », et l’économie mesurée sur neuf
   playtests ne bouge pas parce qu’on a trouvé un signe de plus. */
const NGL = GL.filter(g=>!g.sec).length;
const BR = [['nombre','Nombre'],['matiere','Matière'],['parole','Parole'],['temps','Temps'],['modalite','Modalité']];
const byId = Object.fromEntries(GL.map(g=>[g.id,g]));

/* ======================== les onze lectures ========================
   Onze signes sur quarante-cinq supportent deux lectures, et le joueur tranche à l'achat
   (design doc §8). Les mots faux et leurs lignes de journal sont écrits depuis le
   14/09/2026 — `docs/corpus.md` §7.5, vérifiés ligne à ligne contre le corpus rendu — et
   recopiés ici sans y toucher : ce sont eux le contenu du lot, pas la mécanique.

   Ce que la table ne porte PAS, et c'est délibéré :

   - aucune marque de justesse. La lecture juste est `mot` dans `GL`, la fausse est ici, et
     rien dans l'interface ne dit laquelle est laquelle. La grille de composition ne
     renseigne jamais (règle 14) ; l'écran de choix non plus, et pour la même raison.
   - aucun effet chiffré propre. La lecture fausse rend 25 % de plus SUR CE QUE LE SIGNE
     MULTIPLIE DÉJÀ (`mfx()` dans economie.js) ; un signe qui ne multiplie rien ne gagne
     rien à être mal lu. Lui inventer un effet pour porter la prime déplacerait une économie
     réglée sur neuf playtests, pour une prime que le joueur ne voit pas.
   - aucune dette écrite à la main : elle se déduit des attestations (`detteDe()`).

   `mesh` (semence) et `ke` (devenir) sont de l'acte V et n'existent pas encore dans `GL`.
   Leurs entrées sont inertes jusque-là, comme les recettes de `RECETTES` (règle 15) : le
   jour où leur branche entre, elles se mettent à servir d'elles-mêmes. */
const AMB = {
  tem:  {mot:'poussière',
   log:'De la poussière. Ce ne sont pas des prières : ce sont des comptes de cendres, et ils les ont tenus jusqu’au bout.'},
  ur:   {mot:'tombe',
   log:'Une tombe. Les outils du corpus prennent un nom, et ce n’est pas celui d’une ville : trente et une tombes la première année, deux la dernière.'},
  kish: {mot:'sang',
   log:'Le sang. Un relevé par année, tenu sur deux siècles. Je préfère ne pas savoir de quoi ils tenaient le compte si scrupuleusement.'},
  sar:  {mot:'couper',
   log:'Couper. Quelqu’un a tenu ce stylet, et il a entaillé l’argile comme on entaille autre chose.'},
  shen: {mot:'compter',
   log:'Compter. Ce n’est pas un inventaire qui le dit, c’est une consigne — et elle revient d’une tablette à l’autre. Un peuple qui ordonne de compter : je ne suis pas surpris.'},
  nur:  {mot:'soleil',
   log:'Le soleil. Chaque tablette porte le sien depuis le début — je ne savais pas lire la date.'},
  pat:  {mot:'dessous',
   log:'Dessous. Ce qui est sorti de terre en premier était en haut de la pile : ils rangeaient en empilant.'},
  dun:  {mot:'on peut',
   log:'On peut. Ce n’est pas un inventaire qui parle, c’est quelqu’un qui autorise — et sur deux siècles, l’autorisation ne change pas : copier.'},
  la:   {mot:'fin',
   log:'Fin. Le signe le plus fréquent de tout le corpus dit la fin de quelque chose — et les colonnes que je croyais inachevées disent qu’on s’était arrêté là.'},
  /* ---- acte V, écrits d'avance (docs/corpus.md §7.5) ---- */
  mesh: {mot:'enfant',
   log:'Un enfant. Ils les comptaient par soixante, puis par cent, pendant que les tombes se vidaient. C’est le seul nombre du corpus qui monte.'},
  ke:   {mot:'porter',
   log:'Porter. Ce qu’ils demandent à la tablette, ce n’est pas d’être lue : c’est de transporter quelque chose.'}
};

/* ---- ce qu'une lecture fausse emporte avec elle ----
   Un signe faux ne salit pas que ses propres attestations : il salit tout composé qui le
   contient, parce qu'un composé se lit par ses parties (règle 4). Et il DOIT le salir,
   sinon la grille renseigne — un joueur qui lit ⟨ne-pas⟩ « fin » et à qui la grille répond
   « zéro » vient d'apprendre qu'il s'est trompé (règle 14, docs/corpus.md §7.2).

   Le composé faux fait le même saut que le juste, appliqué aux parties fausses :
   ⟨maison⟩⟨grain⟩ ne donne pas « maison-grain » mais « grenier », donc ⟨tombe⟩⟨grain⟩ ne
   donne pas « tombe-grain » mais « caveau ».

   La clé est la liste des parties mal lues, dans l'ordre de la recette et sans doublon —
   ⟨année⟩⟨année⟩ n'a qu'une partie à salir. Ce que `docs/corpus.md` §7.2 ne donnait pas et
   qu'il fallait écrire ici : la ligne de journal de chaque variante. Sans elle, l'achat de
   ⟨maison⟩⟨grain⟩ annoncerait « le grenier — la maison du grain » à un joueur dont le
   corpus dit « caveau » et « tombe », et le jeu se contredirait tout seul. */
const COMPFAUX = {
  urtem: {
    ur:      {mot:'caveau',   log:'Le caveau — la tombe où l’on met le grain. Personne ne me l’a appris : c’était écrit dans le signe.'},
    tem:     {mot:'poussier', log:'Le poussier — la maison de la poussière. Personne ne me l’a appris : c’était écrit dans le signe.'},
    'ur+tem':{mot:'ossuaire', log:'L’ossuaire — la tombe de la poussière. Personne ne me l’a appris : c’était écrit dans le signe.'}
  },
  imme:   {sar:{mot:'le juge',  log:'Le juge. Celui qui dit et qui tranche. Chaque tablette finit sur ce mot : je lisais une signature sans le savoir.'}},
  tabsar: {sar:{mot:'le rebut', log:'Le rebut — la tablette coupée. Une, puis trois cents, puis mille deux cents. Ils ne comptaient pas leur grain : ils comptaient ce qu’ils avaient mis au rebut.'}},
  nurnur: {nur:{mot:'cent-soleils',   log:'Cent soleils. Ils mesuraient par centaines. Il leur en restait deux.'}},
  nurhal: {nur:{mot:'dernier-soleil', log:'Le dernier soleil. Il n’a pas de nombre : après lui, personne n’a plus compté.'}},
  shenu:  {shen:{mot:'les-compteurs', log:'Les compteurs. Ils se nommaient d’après ce qu’ils faisaient — et la moitié du nom est un signe que je ne sais pas lire, qui se tient seul juste devant, sur la même ligne.'}},
  enla:   {la:{mot:'à la fin', log:'À la fin. La consigne s’arrête là. Ils n’ont jamais gravé ce qui vient après — ou bien c’est arrivé.'}},
  /* ⟨fin⟩ posé sur ⟨un⟩ est l'homographe exact de ⟨finir⟩⟨un⟩, qui est `le-dernier`
     (docs/corpus.md §7.2). Le signe replie quand même les registres vides : c'est le
     corpus qui répond, pas la grille, et c'est le seul endroit où il a le droit de le
     faire. */
  lan:    {la:{mot:'fin-un', log:'Fin-un. Le signe de la fin posé sur le un : ils écrivaient l’épuisement comme un nombre et le rangeaient dans la colonne des nombres. Je le regardais depuis le début sans le compter.'}},
  /* ---- actes IV et V, écrits d'avance ; inertes tant que leurs parties ne sont pas au
     lexique, exactement comme les recettes correspondantes ---- */
  shenke: {shen:{mot:'devenir-compte'}, ke:{mot:'porter-lecture'}, 'shen+ke':{mot:'porter-compte'}},
  meshke: {mesh:{mot:'naître'},         ke:{mot:'porter-semence'}, 'mesh+ke':{mot:'porter-enfant'}},
  mula:   {la:{mot:'moi-mort'}}
};
/* Les parties d'un composé, sous les identifiants du LEXIQUE et non sous les clés de tracé :
   `COMP` fait paraître la branche Nombre sous ses chiffres (`u1` pour ⟨un⟩), et c'est `ALIAS`
   qui les rend au lexique. Même traduction que pour `RECETTES`, et pour la même raison. */
const PARTIES = {};
for(const cible in COMP) PARTIES[cible] = COMP[cible].map(k => GLTRACE[k] || k);

/* ============================ recettes ============================ */
/* `COMP` dit comment un signe se DESSINE : ses valeurs sont des clés de tracé, et la branche
   Nombre y paraît sous son chiffre (`u1` pour ⟨un⟩, `t10` pour ⟨dix⟩). Une recette dit ce qu’on
   peut POSER : deux glyphes du lexique. La traduction se fait une fois, ici.

   Le filtre est ce qui empêche la grille d’offrir un signe qui n’existe pas — `selanna`
   (vingt) reste dessinable mais a été retiré du lexique, et les composés des actes IV et V
   n’ont pas encore leurs parties. Chaque recette apparaîtra d’elle-même le jour où sa cible et
   ses deux parties seront au lexique : il n’y a aucune liste à tenir à jour. */
const RECETTES = {};
for(const cible in PARTIES){
  const [a, b] = PARTIES[cible];
  if(byId[cible] && byId[a] && byId[b]) RECETTES[cible] = [a, b];
}
/* L’ordre fait partie de la recette : `notre-fin` et `nous-fûmes` sont les deux mêmes signes
   dans les deux sens. Le corpus le dit — ⟨grenier⟩ porte la maison à gauche et le grain à
   droite depuis la première seconde. Qui lit, voit l’ordre. */
const PAIRES = Object.fromEntries(Object.entries(RECETTES).map(([c,[a,b]]) => [a+'+'+b, c]));
const recetteDe = (a, b) => PAIRES[a+'+'+b];
