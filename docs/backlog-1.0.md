# Feuille de route 1.0 — épics et récits

*Établi le 10/09/2026, à partir de `docs/design-doc.md`, `docs/corpus.md`, `docs/journal.md` et de l'état du code au commit `fb78100`.*

> Ce document est un **plan de travail**, pas une décision de conception. Tout ce qu'il
> découpe existe déjà comme intention dans le design doc ; il ne fait que le mettre en
> tâches, en dépendances et en ordre. Là où il chiffre un rythme, il ne chiffre que ce qui
> a été mesuré (règle 7) — le reste est explicitement marqué *à simuler*.

---

## 1. Où on en est

| | Fait | Reste pour 1.0 |
|---|---|---|
| Glyphes | **27 / 45** *(+ `grenier` et `zéro`, composés, hors arbre)* | **17** |
| Instruments | 6 / 9 (Œil, Copiste, Table, Concordance, Atelier, Grammaire) | 3 (Élève, Corpus jumeau, Le Lecteur) |
| Actes | I, II, III *(tout sauf `les-lecteurs`)* | III *(un signe)*, IV, V |
| Corpus | **30 tablettes, 705 lignes, 3 838 signes — intégral**, ⟨N1⟩/⟨N2⟩ semés | les 11 lectures fausses |
| Mécaniques centrales | relevé, recoupement, datation, rangement, concordance, hors-ligne, **composition** | confiance, contradiction, révision, Questions |
| Fins | aucune *(écran « fin du prototype »)* | Achever, Interrompre, relecture |
| Rythme mesuré | 66 min 49 pour 20 glyphes (PT9) · 87 à 90 min simulées pour 27 | cible design doc : 3 h – 3 h 30 pour 45 |

Le corpus étant écrit intégralement, **la majeure partie du reste est du code et de
l'équilibrage** — l'inverse de la situation des actes I–II, où le texte était le budget.
L'exception est TXT-1 (les lectures fausses) ; TXT-2 (⟨N1⟩/⟨N2⟩) est tranché depuis le 11/09/2026.

---

## 2. Définition de « 1.0 »

Une version 1.0 est atteinte quand **toutes** ces conditions sont vraies :

1. Les **45 glyphes** sont achetables, chacun avec son coût, son effet, son texte de journal et sa zone d'interface.
2. Les **9 instruments** existent, l'Élève avec son taux d'erreur.
3. Les **cinq actes** s'enchaînent sans écran « fin du prototype ».
4. Les **deux fins** (Achever / Interrompre) et la **relecture** sont jouables.
5. Les invariants I1, I2, I3, I4 et I6 sont **mesurés** sur la partie entière — I6 par tranches de dix minutes, ouverture exclue (règle 2).
6. Au moins **trois playtests complets** par des joueurs qui ne sont pas l'auteur, dépouillés au journal d'actions.
7. La version publique ne contient **ni la barre hors-jeu, ni `traces.js`** (conventions), et s'ouvre sans explication préalable (R1).
8. `python build.py && python outils/verifier.py` passe, et `outils/sim.py` couvre les cinq actes.

---

## 3. Les épics

Onze épics. `T` = taille indicative (S / M / L / XL) — un ordre de grandeur d'effort, pas
un engagement de date.

---

### E1 — La composition *(acte III, seconde moitié)*

*Le système qui fait la différence entre ce jeu et un Cookie Clicker rethématisé : un espace de découverte que le jeu ne guide pas (design doc §7).*

> **COMP-1, COMP-2 et COMP-5 sont faits** (10/09/2026), avec `grenier` — la moitié de COMP-4
> qui était atteignable. Voir `docs/journal.md`, « La composition ». Une correction au passage :
> `COMP` **ne peut pas** servir de vérité telle quelle, ses valeurs sont des clés de tracé ;
> `RECETTES` en dérive ce qu'on peut poser, filtré sur les glyphes qui existent.

**COMP-1 — Poser un signe sur un autre** · ~~T:M~~ **fait**
> En tant que joueur, je veux assembler deux signes que je connais pour tenter un composé, sans que le jeu me dise lesquels marchent.

- Fini quand : une grille permet de sélectionner deux glyphes acquis et de valider une tentative ; la table `COMP` de `src/signes.js` (17 entrées) sert de vérité ; l'ordre des deux parties compte comme dans `COMP`.
- Une tentative valide acquiert le composé au coût normal en Certitude.
- Dépend de : rien. **C'est la première brique de la seconde moitié de l'acte III.**

**COMP-2 — Rater sans être puni** · ~~T:S~~ **fait**
> En tant que joueur, je veux pouvoir me tromper sans perdre ma compréhension.

- Fini quand : un échec coûte des Hypothèses, **jamais de Certitude** (R3) ; la paire est inscrite dans un carnet consultable, et le jeu refuse de la retenter au même prix.

**COMP-3 — `zéro`, et les compteurs qui se replient** · ~~T:M~~ **fait** (12/09/2026)
> En tant que joueur, je veux découvrir moi-même que `ne-pas` + `un` fait un signe que je regarde depuis la première seconde.

- Fini quand : `zéro` n'est offert par aucune branche, ne s'obtient que par COMP-1, et rend lisibles les onze zéros du corpus (`numLisible()`, règle 3).
- Dépend de : COMP-1, **et de `ne-pas`** (MOD-1) — c'est la première fois qu'une branche de l'acte IV mord sur une branche de l'acte I.
- Attention : la tablette 29 (registre de zéros) doit rester un seul signe répété jusque-là (`docs/corpus.md` §5, note « heureux accident »).
- *Fait* : 120 C, hors arbre, sans effet mécanique. **La notation compacte des grands nombres ne lui revient pas** — elle est déjà celle de `cent`, acquise par tout le monde, et la déplacer sur un composé facultatif la retirerait à la plupart des joueurs (voir `docs/journal.md`, « La Modalité, et le zéro »). Onze zéros passent en chiffres, dont les neuf de la tablette 29, qui reste un seul signe répété jusque-là. Coût mesuré pour qui le pose : deux minutes de progression, écart max porté à 6,2 min.

**COMP-4 — `grenier` et `devenir-lecture`** · T:S — *`grenier` fait ; reste `devenir-lecture`, qui attend `lire` et `devenir` (actes IV–V)*
> En tant que joueur, je veux que les deux autres composés secrets soient atteignables en avance sur le récit.

- Fini quand : les deux ne sont offerts par aucune progression ; `devenir-lecture` composé tôt fait recevoir la tablette 17 « en pleine figure » sans que rien ne soit ajouté au texte.

**COMP-5 — Le carnet** · ~~T:S~~ **fait**
> En tant que joueur, je veux relire ce que j'ai déjà tenté.

- Fini quand : le carnet liste les tentatives ratées, survit à la sauvegarde, et n'apparaît qu'après la première tentative.

---

### E2 — Parole III et Modalité *(10 glyphes)*

**PAR-1 — `lire`, `scribe`, `archive`** · ~~T:M~~ **fait** (11/09/2026)
> En tant que joueur, je veux que le corpus se mette à parler de lui-même.

- Fini quand : les trois glyphes ont coût, effet, texte de journal, et sont posés dans l'arbre après `copier`.
- `lire` est **le piège majeur** de l'ambiguïté (AMB-*) : le coder en sachant qu'il aura deux lectures.
- *Fait* : 300 · 600 · 900 C ; +50 % à la grammaire, au copiste et à l'atelier, à la table. 81,6–85,0 min pour 23 signes, écart max 5,2. `scribe` et `archive` se composent dès `année` (règle 15) — et composer `scribe` tôt coûte seize minutes sans déblocage, avec un « Rien ne vient » tant qu'on ne peut pas payer. Ouvert, à regarder en PT10 : voir `docs/journal.md`, « La Parole III ».

**PAR-2 — `les-lecteurs`, fin de l'acte III** · T:M
> En tant que joueur, je veux apprendre comment ce peuple s'appelait, et comprendre que le nom est une thèse.

- Fini quand : l'achat déclenche le premier basculement narratif ; la tablette 18 devient lisible d'un coup ; **première contradiction majeure** possible ici (CONTR-1).

**MOD-1 — `ne-pas`, `si`, `il-faut`, `sinon`** · ~~T:M~~ **fait** (12/09/2026)
> En tant que joueur, je veux lire les conditions dont le registre est plein.

- Fini quand : les quatre glyphes existent ; les blocs générés (`maisons()`, salés de modalité) deviennent lisibles ; `il-faut` est marqué comme ambigu « qui ne casse jamais mécaniquement ».
- Débloque : COMP-3 (`zéro`).
- *Fait* : 150 · 320 · 550 · 800 C, et **816 attestations** qui passent en français — un signe du corpus sur cinq, le plus gros morceau de lisibilité qui restait. Un seul effet chiffré, `il-faut` ×1,5 à l'atelier : donner à `si` le troisième ×1,5 de la Grammaire raccourcissait l'acte de cinq minutes au lieu de l'allonger. Mesuré 87,0–90,0 min pour 27 signes, écart max 5,2, tranches ≥ 10′ ≤ 27 %. `sinon` se compose de `si` + `ne-pas` (règle 15), donc derrière sa propre branche : le piège de `scribe`, en beaucoup plus doux.

**MOD-2 — `peut-être` et le panneau de confiance** · T:L
> En tant que joueur, je veux découvrir que le jeu ne m'a jamais dit qu'une lecture pouvait être fausse.

- Fini quand : avant `peut-être`, aucun indice de confiance n'existe nulle part dans l'interface ; après, chaque signe ambigu porte son degré de doute, et le panneau de révision s'ouvre.
- **Pic de malaise du jeu** (design doc §6). Ne pas l'adoucir.
- Dépend de : E3 (il n'y a rien à douter tant que rien n'est ambigu).

**MOD-3 — `faux`, rétroactif** · T:M
> En tant que joueur, je veux voir d'un coup tout ce que j'ai mal traduit depuis le début.

- Fini quand : l'achat repeint le corpus entier avec les erreurs commises ; la tablette 26 (« la dernière scribe marque comme fausses les tablettes qui espéraient ») se lit alors comme le geste que le joueur vient de faire.
- Dépend de : E3, MOD-2.

---

### E3 — Confiance et ambiguïté *(11 signes)*

*Le piège est délibéré : se tromper paie mieux à court terme (design doc §8).*

**AMB-1 — Trancher à l'achat** · T:L
> En tant que joueur, je veux choisir entre deux lectures possibles d'un signe, sans savoir laquelle est juste.

- Fini quand : les 11 signes de `docs/corpus.md` §7 proposent deux lectures à l'achat ; la lecture fausse rend **+25 %** d'effet mécanique ; le choix est enregistré dans la sauvegarde.
- Le jeu ne signale **jamais** que le choix a été mauvais avant `peut-être`.

**AMB-2 — Le mot faux, partout** · T:M
> En tant que joueur, je veux que ma mauvaise lecture contamine tout le corpus, pas seulement une infobulle.

- Fini quand : le mot faux remplace le juste dans **toutes** les occurrences du signe, y compris les blocs générés et les tablettes déjà lues.
- Dépend de : TXT-1 (le texte des lectures fausses).

**AMB-3 — La dette** · T:S
> En tant que game designer, je veux que chaque erreur porte un coût différé et invisible.

- Fini quand : chaque lecture fausse ajoute +1 à +3 points de dette ; la dette n'est lisible nulle part avant `peut-être` ; elle est le seul intrant de CONTR-1.

**AMB-4 — L'indice est dans le texte, et nulle part ailleurs** · T:M
> En tant que joueur qui lit, je veux pouvoir trouver le signe fautif sans que le jeu me le dise.

- Fini quand : chacune des 11 lectures fausses produit une absurdité **repérable à un endroit précis du corpus** (table de `docs/corpus.md` §7) ; un test de `verifier.py` vérifie que la phrase absurde est bien rendue.
- Vérifier que `lire` et `il-faut` **ne cassent pas** mécaniquement : c'est voulu.

---

### E4 — Contradiction et révision

**CONTR-1 — Un passage refuse de se résoudre** · T:M
> En tant que joueur, je veux que mes erreurs finissent par bloquer quelque chose, sans jamais me faire perdre ce que j'ai acquis.

- Fini quand : au franchissement d'acte, dette > seuil divise par deux la production de Certitude ; **aucune progression n'est perdue, seulement du débit** (R2) ; l'état est affiché sans ambiguïté.
- Dépend de : AMB-3.

**CONTR-2 — Rouvrir un signe** · T:M
> En tant que joueur, je veux revenir sur une lecture et payer pour la corriger.

- Fini quand : la révision est **toujours disponible** ; juste → dette effacée + bonus rétroactif ; faux → on repaie ; le corpus se repeint dans les deux cas.

**CONTR-3 — Le coût du brute-force** · T:S
> En tant que game designer, je veux que réviser au hasard coûte plus cher que lire.

- Fini quand : le coût de révision croît assez pour qu'un balayage systématique des 11 signes soit plus cher que la lecture — **à mesurer avec `outils/sim.py`, pas à estimer** (règle 7).

---

### E5 — L'Élève *(instrument ambivalent)*

**ELV-1 — L'instrument qui multiplie tout** · T:M
> En tant que joueur, je veux un générateur qui accélère tout le reste.

**ELV-2 — …et qui se trompe** · T:L
> En tant que joueur, je veux découvrir que ce que l'Élève déchiffre tout seul est parfois faux.

- Fini quand : l'Élève déchiffre de lui-même, avec un taux d'erreur croissant avec leur nombre ; ses erreurs alimentent la dette (AMB-3) ; empiler des Élèves déchiffre **vite et faux**.
- Dépend de : E3 en entier. **Sans lectures fausses, son taux d'erreur n'a rien à fausser** (journal, « ce qui reste de l'acte III »).

---

### E6 — Acte IV : la voix

**VOIX-1 — La branche Personne** *(`je`, `toi`, `nous`, `toi-qui`, `moi-absent`, `nous-fûmes`)* · T:L
> En tant que joueur, je veux découvrir qui parle.

- Fini quand : les six glyphes existent ; `nous-fûmes` verrouille le récit au passé, **y compris les passages déjà lus**, et n'apparaît qu'une fois dans tout le corpus (dernier mot de la tablette 30).

**VOIX-2 — Le corpus était à la deuxième personne depuis le début** · T:M
> En tant que joueur, je veux qu'on me réaffiche ce que j'ai déjà lu, désormais adressé à moi.

- Fini quand : `toi` déclenche un réaffichage des passages déjà lus ; rien n'est ajouté au texte — la relecture suffit (règle 5).

**VOIX-3 — Les Questions** · T:XL
> En tant que joueur, je veux interroger le texte et qu'il réponde, dans les limites de ce qui a été gravé il y a quatre mille ans.

- Fini quand : la ressource Q existe (0 à 12 sur toute la partie, design doc §4) ; poser une question consomme un Q ; **chaque réponse est une ligne du corpus, jamais un texte écrit pour l'occasion**.
- Le plus gros risque de conception du lot : c'est le seul système où le jeu peut se mettre à *parler* au lieu de laisser lire.

**VOIX-4 — Le Corpus jumeau** *(instrument 8)* · T:M
> En tant que joueur, je veux qu'une deuxième inscription soit trouvée.

**VOIX-5 — I2 : perdre la lisibilité de ses propres nombres** · T:M
> En tant que joueur, je veux que la notation scientifique arrive **en signes non déchiffrés**, au moment précis où mes nombres deviennent énormes.

- Fini quand : pas de notation scientifique avant l'acte IV ; à son apparition, elle est illisible ; elle se déchiffre ensuite comme le reste.

---

### E7 — Acte V : la graine

**GRAINE-1 — La branche Fin** *(`finir`, `semence`, `devenir`, `le-dernier`, `germer`, `notre-fin`, `devenir-lecture`)* · T:L
> En tant que joueur, je veux lire la fin dans leur langue.

- `devenir-lecture` est le dernier signe et n'est accessible que par composition (COMP-4).
- `notre-fin · ne-pas` ne se tranche jamais : « notre fin : non » ou « pas notre fin ». **Le jeu ne dira pas laquelle.**

**GRAINE-2 — Le Lecteur** *(instrument 9)* · T:M
> En tant que joueur, je veux acheter un instrument avant de savoir ce que c'est, et découvrir que ce n'en est pas un.

- Fini quand : l'instrument est achetable sans description ; la révélation (« c'est le corpus qui a commencé à lire ») arrive par le texte, pas par une infobulle.

**GRAINE-3 — La révélation** · T:M
> En tant que joueur, je veux comprendre que la langue a été conçue pour être cassée par un inconnu.

- Fini quand : les tablettes 28 (« la fabrique ») et 21 (« l'abécédaire ») sont pleinement lisibles et se répondent ; le joueur reconnaît dans la tablette 28 **l'ordre des branches de l'arbre qu'il suit depuis trois heures**.

---

### E8 — Fins et relecture

**FIN-1 — Achever** · T:M
> En tant que joueur, je veux lire le dernier signe et voir l'interface disparaître.

- Fini quand : le corpus passe à 100 % ; l'écran se vide progressivement (compteurs, instruments, lexique), il ne reste que le texte, entièrement en français ; puis le texte s'efface.

**FIN-2 — Interrompre** · T:S
> En tant que joueur, je veux pouvoir laisser un signe non lu.

- Fini quand : le jeu se ferme sur le corpus figé et **ne propose pas de reprendre** ; aucune des deux fins n'est présentée comme la bonne ; aucun score.

**FIN-3 — La relecture** · T:M
> En tant que joueur qui a achevé, je veux relire le corpus en sachant tout, y compris ce que j'ai raté.

- Fini quand : le corpus est intégralement lisible dès le départ ; **toutes** les erreurs de traduction de la partie sont surlignées, y compris celles jamais détectées ; environ vingt minutes, aucune mécanique.
- Dépend de : AMB-1 (le journal des choix), FIN-1.
- « Ce n'est pas un prestige, c'est un épilogue. » Coût de production faible, valeur émotionnelle haute — **ne pas le sacrifier au planning.**

---

### E9 — Économie sur trois heures

**ECO-1 — Le mur des dix premières minutes** · T:M
> En tant que joueur qui découvre, je veux que l'ouverture ne repose pas entièrement sur ma main.

- Le seul défaut d'équilibrage connu qui ne soit pas réglé : 83 % de la Certitude à la main avant la première Concordance en PT7, 63 % en PT8, 75 % en PT9 — et c'est là que la partie 1 de PT5 a été abandonnée.
- Se traite **par l'ouverture** (un instrument plus tôt, ou un premier signe moins cher), pas par le recoupement.
- Rappel règle 2 : la tranche 0–10 min ne se *mesure* pas (division par zéro) ; c'est l'abandon qu'on traite, pas le chiffre.

**ECO-2 — Étendre `sim.py` aux actes IV et V** · T:L
> En tant qu'auteur, je veux vérifier le rythme de trois heures sans jouer trois heures.

- Fini quand : le simulateur modélise l'Élève, les Questions, la dette et la contradiction ; il sort les tranches d'I6 sur toute la partie ; `balayage.py` peut balayer les nouvelles constantes.
- **Bloquant pour tout réglage des actes IV–V** (règle 7).

**ECO-3 — Tenir I1 et I4 sur 45 glyphes** · T:L
> En tant que joueur, je veux un déblocage toutes les 4 à 6 minutes, et jamais plus de 8 minutes sans rien.

- La Certitude ne dépasse jamais 4 chiffres à l'écran (I1) alors que les Occurrences vont à ~10¹⁰. **La divergence est le propos ; la tenir sur 25 glyphes de plus est le vrai travail d'équilibrage restant.**

**ECO-4 — PT10 et suivants** · T:M *(récurrent)*
> En tant qu'auteur, je veux qu'un joueur qui ne sait pas ce qu'il cherche voie la crue baisser.

- PT10 : la question de PT8/PT9, reposée à quelqu'un d'autre. Dans le même TSV : la part manuelle des occurrences (36,3 % en PT9 ; **au-delà de 40 %, plafonner `REL_K`**), le stock d'hypothèses entre `année` et la dixième Grammaire (27 090 en PT9), et **le nombre de recoupements** — sous une vingtaine, le réglage du 09/09 a vidé un des deux gestes manuels et il faut revenir en arrière.
- **Le réglage du 09/09/2026 (`REC_R` 1,18 → 1,30, Copiste à 10) n'a aucun playtest derrière lui.** C'est la première chose que PT10 valide ou casse. La composition ne l'a pas touché — mesuré identique au chiffre près, c'était la condition du lot.
- **Question neuve de PT10** : ⟨grenier⟩ se trouve-t-il ? Et ⟨ne-pas⟩ posé sur ⟨un⟩, quand le joueur vient d'acheter ⟨ne-pas⟩ et qu'il a neuf zéros sous les yeux sur la tablette 29 ? Le journal d'actions compte les tentatives de composition, avec leur paire et leur minute. Aucun simulateur ne peut y répondre.
- **La tranche 20-30′ monte d'un lot à l'autre** — 25,8 % à 23 glyphes, 27,0 % à 27 — par `revCount()` et non par les lots eux-mêmes : plus l'arbre est grand, plus lentement les tablettes se dégagent par signe acquis. Sous 30 % (règle 2), à surveiller au prochain lot.
- **Le garde-fou de durée de `balayage.py` suit la taille du lexique**, et doit être re-basé à chaque lot : resté à (71, 77) — PT9, vingt glyphes — il rejetait ses dix-huit combinaisons depuis `da61b19`, réglage en place compris, en affichant « 0 sur 18 ». Re-basé à (84, 92).

---

### E10 — Texte et corpus

**TXT-1 — Écrire les 11 lectures fausses** · T:L
> En tant que joueur, je veux que ma mauvaise lecture produise un corpus cohérent, plausible, et faux.

- Fini quand : chacun des 11 signes a sa lecture fausse écrite, et l'endroit exact où elle casse est vérifié dans le texte rendu (`docs/corpus.md` §7).
- **Du travail d'écriture, pas de code.** Bloque AMB-2 et donc E5.

**TXT-2 — Trancher ⟨N1⟩ et ⟨N2⟩** · ~~T:S~~ **fait** (11/09/2026)
> En tant que joueur, je veux rencontrer des formes très fréquentes que je ne résoudrai jamais.

- Semés comme **intitulés des registres**, un par bloc : ⟨N1⟩ en tête des champs et de la veille (13 fois), ⟨N2⟩ en tête des maisons et de l'archive (16 fois). Fréquence moyenne et non « très fréquente » — un titre courant l'aurait haussée pour ⟨N2⟩ seul. Rythme simulé inchangé (71,8–76,2 min, écart 5,6), gisement 397 → 399. Voir `docs/corpus.md` §6 et `docs/journal.md`.

**TXT-3 — Vérifier la densité de l'acte II** · T:S
> En tant que joueur, je ne veux pas décrocher dans le passage volontairement plat.

- Si un playtest montre un décrochage, la réponse **n'est pas d'ajouter du drame** : c'est d'avancer la tablette 6 dans l'ordre de révélation.

---

### E11 — Livraison

**LIV-1 — L'ouverture sans mode d'emploi** · T:L
> En tant que nouveau joueur, je veux comprendre quoi faire dans les soixante premières secondes d'un écran illisible.

- Écart assumé n°7 du journal : le chrome de l'interface est aujourd'hui **en français dès t=0**, parce que l'idéal du doc (un seul mot français à l'écran, *commence*) rend le prototype injouable sans onboarding. À réexaminer une fois l'onboarding écrit.
- Fini quand : R1 est tenu — premier signe accessible en < 60 s, un mot français en clair à t=0, le compteur bouge visiblement à chaque relevé — **et vérifié sur un joueur qui n'a rien lu.**

**LIV-2 — Retirer les outils hors jeu** · T:S
> En tant qu'auteur, je veux une version publique sans instrumentation.

- Fini quand : la barre `devbar` (chrono, ×1/×3/×10, `traces`, `copier`, `réinitialiser`) et `src/traces.js` sortent de la version publique — fichier, ligne dans `index.html`, ligne dans `build.py`, deux boutons — **sans être supprimés du dépôt** : ils servent aux playtests suivants.
- Prévoir un drapeau de build plutôt qu'une suppression manuelle.

**LIV-3 — La sauvegarde survit aux actes** · T:M
> En tant que joueur, je veux qu'une partie commencée ne soit pas perdue à la mise à jour.

- La clé a déjà changé une fois (`langue-morte-actes-i-iii`) parce qu'une partie du MVP rouvrait sur l'écran de fin sans moyen de continuer. **Ça va se reproduire à chaque acte livré.** Fini quand : une sauvegarde porte un numéro de version et se migre, au lieu d'être abandonnée.

**LIV-4 — Le corpus reste fluide à 45 glyphes** · T:M
> En tant que joueur, je veux que le corpus se repeigne sans à-coups.

- Fini quand : `verifier.py` mesure le temps de rendu avec les 45 glyphes acquis, la composition ouverte et une concordance active, et le seuil `RENDU_MAX_S` tient.

**LIV-5 — Étendre `verifier.py`** · T:L
> En tant qu'auteur, je veux que chaque mécanique nouvelle soit couverte bout en bout.

- Le fichier porte aujourd'hui **134 assertions** sur le relevé, le recoupement, la numération, le gisement, la datation, les infobulles, la composition, et la reprise d'une sauvegarde d'avant une mécanique neuve. Chaque épic de cette feuille de route doit y ajouter ses vérifications — en particulier AMB-4 (la phrase absurde est bien rendue) et COMP-3 (`zéro` replie les compteurs).

**LIV-6 — README, écran-titre, distribution** · T:S
> En tant que curieux, je veux ouvrir un fichier et jouer.

- Fini quand : le README ne dit plus « prototype des actes I et II » ; le sous-titre `prototype · actes I–III · 20 glyphes sur 45` disparaît ; `dist/langue-morte.html` et `dist/artefact.html` sont produits par le même build.

---

## 4. Ordre conseillé

Le graphe de dépendances a une seule vraie contrainte forte : **le texte des lectures
fausses (TXT-1) bloque l'ambiguïté, qui bloque l'Élève, la Modalité et la relecture.**
C'est le chemin critique du projet, et c'est de l'écriture — donc à lancer en premier, en
parallèle du code.

| Jalon | Contenu | Ce qu'on peut jouer à la fin |
|---|---|---|
| **J1 — L'acte III se termine** | ~~E1 (composition)~~ + ~~PAR-1~~ + ~~MOD-1~~ + ~~COMP-3~~ *faits* + PAR-2 | 28 glyphes, la composition, `les-lecteurs` |
| **J2 — Le mensonge** | TXT-1 → E3 → MOD-2/MOD-3 + E4 + E5 (Élève) | l'acte III entier, la confiance, la contradiction |
| **J3 — La voix** | E6 (Personne, Questions, Corpus jumeau, I2) | l'acte IV |
| **J4 — La graine** | E7 + E8 | les cinq actes, les deux fins, la relecture |
| **J5 — 1.0** | E9 (final) + E11 | une version publique |

**En parallèle, en continu** : ECO-2 (le simulateur doit précéder chaque réglage), ECO-4
(un playtest par jalon, jamais par l'auteur seul), LIV-5 (les tests suivent le code).

~~TXT-2 (⟨N1⟩/⟨N2⟩) se tranche avant J1, parce qu'il touche les blocs générés — donc les
fréquences, donc l'équilibrage.~~ *Tranché le 11/09/2026, avant J1 comme prévu.*

---

## 5. Risques transverses

| | Risque | Réponse déjà décidée |
|---|---|---|
| **R1** | L'illisibilité initiale fait fuir | LIV-1 ; premier signe en < 60 s |
| **R2** | La contradiction paraît punitive | On ne perd que du débit, jamais de la progression |
| **R3** | La composition devient un jeu de devinettes | *Traité le 10/09/2026* : échec en H seulement, **au taux** (×1,40 par tentative) et non au montant — un coût fixe ne freine rien dans une économie exponentielle ; carnet ; 3 composés secrets ; et la grille ne renseigne jamais, pas même par son silence |
| **R4** | Le texte doit tenir trois heures | Corpus écrit ; le risque s'est déplacé sur VOIX-3 (les Questions) |
| **R6** | Une action manuelle redevient la source principale de Certitude | I6 par tranches, à chaque ajout d'instrument (règle 2) |
| **R7** *(nouveau)* | Le simulateur a surestimé de 20 % **deux fois de suite** | ECO-2 avant tout réglage des actes IV–V ; aucun chiffre annoncé sans mesure (règle 7) |
| **R8** *(nouveau)* | Les Questions font parler le jeu au lieu de le faire lire | Chaque réponse est une ligne du corpus existant, jamais un texte écrit pour l'occasion |

---

## 6. Hors périmètre 1.0

- **Localisation.** Tranché le 04/09/2026 (R5) : français seul, pas de localisation sans réécriture complète du corpus.
- **Prestige / NG+ mécanique.** La relecture (FIN-3) est un épilogue, pas un cycle.
- **Framework, bundler, dépendance externe.** Règle 6 : un seul fichier doit rester distribuable.
- **Son, mobile, sauvegarde en ligne.** Aucun n'est mentionné dans le design doc ; à décider après 1.0.
