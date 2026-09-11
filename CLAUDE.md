# La langue morte — contexte projet

Jeu incrémental en français. Prototype jouable des actes I à III.
**Tout est en français** : interface, code, commentaires, commits, noms de variables. Ne pas basculer en anglais.

---

## Ce que c'est

Un incrémental classique demande *combien peux-tu produire ?*. Celui-ci demande *combien peux-tu comprendre ?* — et il sépare violemment les deux.

L'écran est illisible au départ. Chaque signe déchiffré rend littéralement une zone d'interface lisible et opérable. **L'arbre d'améliorations EST le lexique.**

Deux courbes divergent, et cette divergence est le propos :

- **Occurrences** (donnée brute) suivent une exponentielle de genre, jusqu'à ~10¹⁰
- **Certitude** (compréhension) reste à échelle humaine, jamais plus de quatre chiffres

Le joueur voit sa masse de données exploser pendant que son savoir avance par paliers durement gagnés.

La vision complète est dans `docs/design-doc.md`. Le contenu textuel dans `docs/corpus.md`. L'historique des décisions et des playtests dans `docs/journal.md`. **Lire ces trois-là avant toute modification de fond.**

---

## Architecture

Pas de framework, pas de bundler, aucune dépendance externe hors les polices Google. Scripts classiques en portée globale partagée, chargés dans l'ordre.

```
src/
  index.html    markup + chargement des sources — se joue directement, sans build
  style.css     thème unique sombre (parti pris assumé : lampe à huile sur argile)
  signes.js     tracés SVG des 45 signes, composés, numération
  lexique.js    les 20 glyphes des actes I–III : coût, effet, texte de journal
  corpus.js     GÉNÉRÉ — ne jamais éditer à la main
  economie.js   état, ressources, instruments, actions, boucle de simulation
  rendu.js      corpus, barre de tablettes, panneaux, infobulle, journal
  traces.js     HORS JEU — journal d'actions horodaté pour les playtests
  jeu.js        liaisons, entrées clavier, sauvegarde
outils/
  balayage.py   simule l'économie avec un ensemble de paramètres
  corpus.py     docs/corpus.md → src/corpus.js
  sim.py        simulateur d'économie (rythme sans jouer 40 min)
  verifier.py   tests bout en bout (Playwright)
docs/           design doc, corpus, journal de bord
dist/           GÉNÉRÉ par build.py
```

**L'ordre de chargement compte** : `signes → lexique → corpus → economie → rendu → traces → jeu`. Un `const` déclaré dans l'un est visible dans les suivants.

### Commandes

```bash
python build.py                 # src/ → dist/langue-morte.html et dist/artefact.html
python outils/corpus.py         # regénère src/corpus.js après modification des tablettes
python outils/sim.py            # simule le rythme d'une partie
python outils/balayage.py       # balaie une grille de constantes, filtre sur les garde-fous
python build.py && python outils/verifier.py    # tests
```

`dist/artefact.html` est la variante sans `<!doctype>/<html>/<head>/<body>`, format attendu par l'outil Artifact de Claude.

---

## Règles à ne pas casser

1. **`src/corpus.js` est généré.** Toute modification du texte se fait dans `outils/corpus.py` (transcription exécutable de `docs/corpus.md`), puis `python outils/corpus.py`, puis `python build.py`. Éditer `corpus.js` à la main, c'est perdre le travail au prochain build.

2. **Aucune action manuelle ne doit dépasser 30 % de la Certitude produite, sur aucune tranche de dix minutes.** C'est le mode de défaillance par défaut du jeu : la Certitude est rare, le joueur cherche le chemin le plus court, et deux playtests de suite une action répétée (le clic, puis le recoupement) est devenue la source principale de la ressource centrale. **Mesuré par tranches depuis PT7** : le ratio sur la partie entière s'était posé à 30,0 % en PT6 en cachant un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes — une moyenne, pas un instrument. `outils/sim.py` affiche les tranches ; les vérifier à chaque ajout d'instrument.

    **Sauf la tranche d'ouverture, qui ne se mesure pas tant qu'aucun instrument n'a produit.** Avant la première Concordance, le recoupement est la seule source de Certitude du jeu — la Grammaire reste fermée jusqu'à `année`. Le ratio y vaut donc 100 % par construction, quel que soit le réglage : ce n'est pas un mauvais score, c'est une division par zéro. Balayé le 08/09/2026 sur 27 combinaisons de `cop_b`/`tab_b`/`con_b`, trois cadences chacune : 0–10 min ne descend jamais sous 65 %, tous prix au plancher, et son chiffre ne suit que la date du premier achat de Concordance — 6,8′ au réglage actuel, 10,0′ avant le Copiste à 10, 3,3′ à `cop_b = 5`. C'est le prix du Copiste qui la déplace de sept minutes, pas celui de la Concordance. D'où `i6_tranches()` dans `outils/balayage.py`, qui rend `None` sous une demi-certitude produite et exclut l'ouverture du verdict. **Ne pas régler contre ce chiffre** : il date un achat, il ne mesure pas un équilibre.

    **Le dépassement de 20–30 min est réglé** (09/09/2026), et la façon dont il l'a été vaut pour la suite. Il tenait 28 à 37 % dans les 27 combinaisons de prix, sans jamais passer sous 28 : la famille « prix » ne pouvait pas le toucher. Une analyse de sensibilité une constante à la fois a montré que `rec_o`, `rec_h`, `rec_max`, `tab_p` et `tab_b` sont **inertes** — dans une économie exponentielle les coûts de base ne pèsent rien, seuls les taux de croissance mordent, ce que le commentaire de `REC_R` écrivait déjà depuis PT4. Le levier est donc `REC_R`, porté de 1,18 à **1,30**, compensé par un premier Copiste à **10** au lieu de 15 pour tenir le rythme que l'un allongeait et l'autre raccourcit. Mesuré : 71,8–76,1 min, écart max 5,6 min, toutes les tranches à partir de 10′ sous 26 %. Coût assumé : le joueur recoupe 32 fois au lieu de 49. **À valider en PT10** — le simulateur ne modélise qu'un joueur qui recoupe « tant que c'est rentable » (voir `docs/journal.md`, « le mur des dix premières minutes »).

3. **La numération s'acquiert signe par signe, jamais d'un bloc.** Un nombre du corpus ne passe en chiffres que si le joueur connaît *chacun* de ses signes — et `deux` n'ouvre aucun signe, il ouvre le principe du redoublement (sans lui, on ne lit qu'un nombre où chaque signe apparaît une seule fois). Voir `numLisible()` dans `signes.js` et le tableau dans `docs/journal.md`.

4. **Les composés se dessinent comme composés.** `sv()` rend un signe composé à partir de ses deux parties (table `COMP` dans `signes.js`). Le joueur doit pouvoir reconnaître ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ avant de savoir le lire.

5. **Le corpus n'a aucun en-tête ajouté par le jeu.** Chaque tablette se numérote elle-même dans sa première ligne. Rien dans cette colonne qui ne soit du texte ancien.

6. **Pas de dépendance externe, pas de framework.** Un seul fichier doit rester distribuable.

7. **Ne jamais annoncer un chiffre de rythme sans l'avoir simulé ou mesuré.** Les neuf playtests ont tous invalidé une intuition d'équilibrage — le simulateur lui-même, deux fois.

8. **Les deux actions manuelles se font dans le corpus.** Le relevé, sur un signe ; le recoupement, sur deux attestations d'un même signe dans deux tablettes différentes. Aucun bouton ne produit plus rien directement — c'est le point de bascule entre « un incrémental habillé en déchiffrement » et un jeu où l'on agit en lisant. Ne pas remettre de raccourci qui contourne le texte.

9. **Le relevé : le tarif d'une tablette est figé au premier relevé qu'on y fait**, jamais à son dégagement — le figer au dégagement laisse à 1 occurrence, pour toute la partie, les seules tablettes qu'on atteint tôt (PT6 : la main retombée à 0,1 % des occurrences). Deux versions plus simples ont échoué au simulateur avant d'atteindre le jeu : un gisement qui coupe vraiment verrouille l'ouverture (13 relevés disponibles pour un premier Copiste alors à 15 ; le Copiste est passé à 10 le 09/09/2026, et la main peut désormais le payer), et un tarif indexé sur le débit courant se thésaurise (72 % des occurrences au lieu de 17 %). Le gisement, et non la cadence de clic, décide de ce que la main rapporte — c'est ce qui rend impossible le retour du défaut de PT1.

10. **La date d'une tablette n'est jamais ajoutée par le jeu.** Chaque tablette porte la sienne dans sa première ligne depuis la première seconde ; `année` ne fait que la rendre lisible, et il faut encore savoir lire le nombre, signe par signe. Corollaire : le rangement chronologique ne réordonne que ce que le joueur sait dater — le reste garde l'ordre de sortie de terre. Ne jamais dater depuis une table externe : la vérité est dans `tb.l[0]`.

11. **Un instrument nommé d'après une méthode philologique doit faire cette méthode.** La Table de fréquences compte les occurrences au survol ; la Concordance rassemble les attestations d'un signe. Sans ça le nom ment, et le jeu redevient un incrémental habillé. Corollaire trouvé en PT8 : **ranger n'est pas rassembler** — l'ordre chronologique ne sert à rien tant que 8 à 57 lignes de registre séparent deux relevés de la même série.

12. **Le dégagement suit la sortie de terre, l'affichage suit le temps.** `IDX` (rang dans `ORDRE`) décide de ce qui est visible, l'ordre du DOM décide de ce qu'on lit. Les confondre ferait dégager des tablettes en rangeant. `ranger()` déplace les nœuds existants au lieu de les reconstruire — les jetons relevés et les caches de peinture y survivent.

13. **Le compte de l'arbre n'est pas le compte des glyphes acquis.** Depuis la composition, un signe s'apprend de deux façons : en remontant une branche, ou en le posant soi-même. `nArbre()` compte ce que **l'arbre a rendu** ; `S_.gl.length` compte ce que **le joueur sait**. Tout ce qui mesure une *progression* passe par le premier : la fin de partie, les tablettes dégagées (`revCount()`), l'exposant de la Grammaire (`gramMul()`), le gain du recoupement et le compteur du lexique. Tout ce qui mesure une *compréhension* passe par le second, ou par `mesures()` dans le corpus. Les confondre fait avancer le jeu en composant — un composé secret dégagerait une tablette et donnerait 16 % de Grammaire gratuits — et déplace une économie réglée sur neuf playtests. Un test le vérifie (`verifier.py`, section 14) : après composition, `#lexr` affiche toujours « x / 23 » et aucune tablette n'est dégagée. L'inverse vaut pour un composé **d'arbre** (`deux`, `siècle`, `scribe`, `archive`) : posé à la grille, il avance la partie comme s'il avait été acheté.

14. **La grille de composition ne renseigne jamais.** Elle dessine le signe qu'on propose, sans dire s'il existe — l'indice est dans le corpus, où les composés sont dessinés comme composés (règle 4), et nulle part ailleurs. Corollaire trouvé en l'écrivant : une paire juste que le joueur n'a pas les moyens de payer perd quand même ses hypothèses, parce que la gratuité serait un renseignement. Et la carte de fin ne compte les compositions que si on en a tenté : sinon elle apprendrait qu'il y avait quelque chose à trouver.

15. **Une recette n'existe que si sa cible et ses deux parties sont au lexique.** `COMP` dit comment un signe se *dessine* — ses valeurs sont des clés de tracé, et la branche Nombre y paraît sous ses chiffres (`u1` pour ⟨un⟩). `RECETTES` en dérive ce qu'on peut *poser*, via `ALIAS`, et filtre. Sans ce filtre la grille offre `vingt`, retiré du lexique mais toujours dessinable, et `dernière-année` composée avec un `finir` qui n'existe pas. Ne jamais recopier `COMP` à la main : les recettes des actes IV et V s'ouvriront d'elles-mêmes quand leurs glyphes entreront dans `GL`.

---

## Ce qui a été tranché

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.
- **L'invariant I5 du design doc (« progression quasi linéaire ») est retiré.** Aucune mesure de progression n'est linéaire : les signes sont front-chargés, les lignes back-chargées. L'écart entre les deux *est* le propos — on peut lire presque tous les mots et ne comprendre presque rien. L'afficher, ne pas le lisser.
- Lexique porté à **45 signes** (la branche Nombre gagne `cinq` et `mille`, perd `vingt`).
- **17 composés** au lieu des 9 prévus.
- **⟨N1⟩ et ⟨N2⟩, 11/09/2026 : semés comme intitulés des registres.** Un nom seul sur sa ligne en tête de chaque bloc généré — ⟨N1⟩ (le fleuve) sur `champs` et `veille`, ⟨N2⟩ (la cité) sur `maisons` et `archive`, rien sur `consignes`. 13 et 16 occurrences : fréquence moyenne, choisie contre un titre courant. Seule exception admise au principe « aucun signe uniquement dans un bloc » (`docs/corpus.md` §6) : un nom propre ne se déchiffre pas, sa fréquence ne ment donc à personne. Rythme simulé inchangé, gisement 397 → 399.

---

## État actuel et suite

**Fait** : actes I à III (première moitié, **la composition**, et la Parole III sans `les-lecteurs`), **23 signes d'arbre sur 45**, plus un composé secret, corpus complet des 30 tablettes (705 lignes, 3 838 signes), économie réglée sur neuf playtests, numération signe par signe jusqu'à `mille`, barre de navigation entre tablettes, infobulles, comptage d'occurrences dans le lexique, journal d'actions horodaté, relevé et recoupement dans le corpus avec gisement par tablette, **datation et réordonnancement chronologique**, instrument **Grammaire**, progression **hors ligne**, **grille de composition** avec carnet des tentatives.

**PT7 fait** (07/09/2026) : 44 min 50. R9 est tranché — le tarif figé à la première visite ramène la main de 0,1 % à **17,9 % des occurrences**, sur 22 tablettes au lieu de 3, jusqu'à la quarantième minute au lieu de la quinzième. I6 global à 31,2 %, mais découpé par tranches il montre deux défauts opposés : 83 % au premier quart d'heure (le mur d'ouverture, connu, non réglé) et 103 % aux cinq dernières minutes (5 232 hypothèses que les Concordances ne buvaient pas). D'où la mesure d'I6 par tranches, et la Grammaire.

**L'acte III, première moitié** (07/09/2026) :

- branche **Temps** — `année`, `avant`, `après`, `siècle`, `nuit`, `dernière-année` — et `mille`
- **datation** : chaque tablette porte sa date depuis la première seconde ; `année` la rend lisible, à condition de savoir lire le nombre. Les deux dernières attendent `dernière-année`.
- **réordonnancement** : `avant` range la barre, `après` range le corpus. Une fois trié, l'ordre chronologique *est* l'ordre des numéros — ce que le joueur ne pouvait pas savoir, et ce que le rangement démontre. La série de la crue devient lisible ; personne ne la commente.
- instrument **Grammaire** : `0,0012 × 1,16^lexique` cert./s, −3 hyp./s, fermé jusqu'à `année`. Première vraie exponentielle, et la seule chose capable d'absorber les hypothèses que PT7 laissait s'entasser.
- **hors ligne** par `nuit` : 40 % du débit, 4 h au plus.

Mesuré : **78,6 à 83,5 min** pour les 20 signes, écart max 6,2 min entre deux déblocages, I6 global 5 %. Avec l'acheteur d'avant PT9 : recalé, le simulateur donne **71 à 77 min**, écart max 5,7.

**PT8 fait** (07/09/2026) : 63 min 12 pour les 20 signes — le simulateur surestimait de 20 %. I6 tombe à 6,0 % et le déversoir de fin de PT7 est réparé. Mais **le rangement chronologique n'a pas suffi** : 60 lignes du corpus portent un relevé d'eau sur 676, et de 8 à 57 lignes de registre séparent deux relevés consécutifs. Trier ordonne les contenants, ça ne rassemble pas le signal — le joueur est allé sur la tablette 26 (le relevé d'eau complet) treize secondes après avoir acheté `avant`, y a fait vingt relevés, et n'a pas vu la série.

**La Concordance fait enfin son métier** (07/09/2026) : choisir un signe replie le corpus sur ses seules attestations, chaque tablette gardant sa première ligne — celle où elle se date elle-même. Sur `eau`, corpus rangé : 92 lignes au lieu de 676, et vingt relevés qui descendent de 14 à 0. Rien d'ajouté, rien de commenté. C'est aussi le geste répétable qui manquait à l'acte III, dont la fin se jouait en attendant (4 min 51 sans une action dans le corpus en PT8).

**PT9 fait** (08/09/2026) : 66 min 49 pour les 20 signes. **La crue qui baisse se voit** — le joueur a concordé `eau` 23 secondes après `avant` et 5 secondes après `après`, et l'a dit. Mais c'est l'auteur qui jouait : la question se repose à un autre joueur. I6 à 8,2 %, toutes les tranches sous 30 % sauf l'ouverture (75 %). L'idle de fin d'acte de PT8 a disparu, rempli par le relevé (219 des 393 relevés de gisement après `année`) et non par la concordance, qui reste un geste de lecture. La main fournit **36,3 % des occurrences** — le chiffre du thésauriseur, sans thésauriser : les quatorze dernières tablettes valent 11 996 par relevé, une tablette neuve vaut une Grammaire. À surveiller, pas à régler. Le simulateur surestimait de 20 % deux fois de suite : c'était son acheteur, qui ne prenait jamais d'Atelier tant qu'un Copiste était payable — recalé, il donne 71 à 77 min.

**Réglage du 09/09/2026 — la tranche 20–30 min** : elle tenait 36 % et résistait à tous les prix. `REC_R` passe à 1,30 et le Copiste à 10 ; toutes les tranches à partir de 10′ tombent sous 26 %, pour 71,8–76,1 min et un écart max de 5,6. Aucun playtest derrière ce chiffre pour l'instant : c'est un réglage de simulateur, avec le défaut d'un simulateur — il suppose un joueur qui recoupe tant que c'est rentable, et il ne sait pas si 32 recoupements au lieu de 49 laissent au geste sa place (règle 8).

**La composition** (10/09/2026) : une grille assemble deux signes acquis, dans l'ordre. Ouverte par `année`, comme la Grammaire. L'aperçu dessine le signe proposé sans dire s'il existe. Réussite : le coût normal en Certitude. Échec : 250 hypothèses ×1,40 par paire déjà tentée, **jamais de Certitude** (R3), et la paire entre au carnet — cinq essais coûtent quatre minutes de production, dix en coûtent vingt-sept, un balayage des 225 paires est hors de portée. Le stock d'hypothèses ne mesurait rien : à six cents par minute nettes, seul un taux mord — encore la leçon de `REC_R`. Trois recettes ouvertes : `deux`, `siècle`, et **`grenier`**, premier composé qu'aucune branche n'offre (60 C, aucun effet mécanique, 24 attestations qui passent en français). Mesuré : 71,8–76,1 min, écart 5,6, tranches ≥ 10′ sous 26 % — **identique à avant**, c'était le contrat.

**La Parole III** (11/09/2026, PAR-1) : `lire` (300 C, +50 % grammaire), `scribe` (600 C, +50 % copiste et atelier), `archive` (900 C, +50 % table), après `copier`. Aucune ligne du corpus ne change. `lire` a un effet chiffré parce que sa lecture fausse « compter » devra le majorer. Mesuré : **81,6–85,0 min pour 23 signes**, écart max 5,2, tranches ≥ 10′ sous 26 %. `scribe` et `archive` se composent dès `année` (règle 15) ; **composer `scribe` tôt est un piège** — seize minutes sans déblocage pour qui épargne, et « Rien ne vient » tant qu'on ne peut pas payer, comme une paire fausse. Non réglé : voir `docs/journal.md`, « La Parole III ».

**Prochaine étape — PT10 avec un autre joueur, puis la suite de l'acte III.** Même question qu'en PT8 et PT9, posée à quelqu'un qui ne sait pas ce qu'il cherche. Dans le même TSV : la part manuelle des occurrences (au-delà de 40 %, plafonner `REL_K`) le stock d'hypothèses entre `année` et la dixième Grammaire (27 090 en PT9), **le nombre de recoupements** — sous une vingtaine sur la partie, le réglage du 09/09 a vidé un des deux gestes manuels et il faut revenir en arrière — et **les tentatives de composition** : le journal d'actions les compte avec leur paire et leur minute. La question neuve est celle-là : un joueur qui ignore qu'il y a quelque chose à chercher reconnaît-il ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ ? Aucun simulateur ne répond à ça.

Restent ensuite : **`les-lecteurs`**, dernier signe de la Parole III et fin de l'acte (PAR-2), et la branche **Modalité** — d'où `zéro` = `ne-pas` + `un`, qui attend `ne-pas` et sera le premier composé à faire mordre une branche tardive sur la branche Nombre —, l'instrument **Élève**, puis les **contradictions** de l'acte IV. Voir `docs/design-doc.md` §7 et §8, et `docs/backlog-1.0.md` pour le découpage.

---

## Conventions

- Commentaires en français, au-dessus de ce qui est non évident. Expliquer **pourquoi**, pas quoi.
- Les noms de fonctions et variables suivent la fiction quand c'est naturel : `veille()`, `consignes()`, `recouper()`, `tablette`.
- Le sélecteur de vitesse ×1/×3/×10, le chronomètre et les boutons `traces`/`copier` en haut à droite sont des **outils de test**, marqués « hors jeu ». À retirer de toute version publique.
- `src/traces.js` n'édite aucune règle : il **enveloppe** les actions déjà déclarées. Le retirer = supprimer le fichier, sa ligne dans `index.html` et dans `build.py`, et les deux boutons. Ne jamais y mettre de logique de jeu.
- Écrire les nombres à la française dans l'interface (espace fine insécable, virgule décimale) — `nf` et `f()` s'en chargent.
