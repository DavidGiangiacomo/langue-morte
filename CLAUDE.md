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
  lexique.js    les 30 glyphes des actes I–III + 2 composés : coût, effet, texte de journal,
                les onze lectures fausses (`AMB`, `COMPFAUX`) et leurs points de rupture
                (`RUPTURES`)
  corpus.js     GÉNÉRÉ — ne jamais éditer à la main
  economie.js   état, ressources, instruments, actions, boucle de simulation
  rendu.js      corpus, barre de tablettes, panneaux, infobulle, journal
  traces.js     HORS JEU — journal d'actions horodaté pour les playtests
  jeu.js        liaisons, entrées clavier, sauvegarde
outils/
  balayage.py   simule l'économie avec un ensemble de paramètres
  corpus.py     docs/corpus.md → src/corpus.js
  depouiller.py journal d'actions d'un playtest → les chiffres du journal de bord
  sim.py        simulateur d'économie (rythme sans jouer 40 min) — porte le modèle,
                que `balayage.py` et `depouiller.py` lisent tous les deux
  verifier.py   tests bout en bout (Playwright)
docs/           design doc, corpus, journal de bord
dist/           GÉNÉRÉ par build.py — quatre variantes, voir plus bas
```

**L'ordre de chargement compte** : `signes → lexique → corpus → economie → rendu → traces → jeu`. Un `const` déclaré dans l'un est visible dans les suivants.

### Commandes

```bash
python build.py                 # src/ → les quatre pages de dist/ (voir plus bas)
python outils/corpus.py         # regénère src/corpus.js après modification des tablettes
python outils/sim.py            # simule le rythme d'une partie
python outils/balayage.py       # balaie une grille de constantes, filtre sur les garde-fous
python outils/depouiller.py traces-20260915-2030.tsv   # dépouille un playtest
python build.py && python outils/verifier.py    # tests
```

`depouiller.py` **rejoue le modèle d'économie sur la timeline du journal d'actions** : les
tarifs figés du relevé (règle 9) ne sont écrits nulle part dans le TSV et la part manuelle
des occurrences n'est pas calculable sans eux. Il finit par un contrôle de lui-même — ΔO
prédit contre ΔO observé sur les intervalles calmes, écart médian attendu à 0,0 % — qui est
aussi le seul garde-fou contre une divergence entre `sim.py` et `economie.js`. Si ce chiffre
n'est pas nul, ne rien croire de la section « la main ». Les constantes et les six
multiplicateurs viennent de `sim.py` (`multis()`), qui les lit lui-même de `src/` : ne jamais
en faire une troisième copie.

`python build.py` sort **quatre pages du même `src/`, en un seul passage et sans drapeau** —
une variante qu'il faut penser à réclamer est celle qu'on oublie de reconstruire, et c'est
celle qui part en ligne :

| | barre hors jeu | `traces.js` | pour |
|---|---|---|---|
| `dist/langue-morte.html` | entière | oui | développer |
| `dist/artefact.html` | entière | oui | l'outil Artifact de Claude — sans `<!doctype>/<html>/<head>/<body>` |
| `dist/playtest.html` | chrono + `traces`/`copier` | oui | **un playtest à distance** ; c'est ce que GitHub Pages déploie |
| `dist/public.html` | aucune | non | la version publique (LIV-2) |

Ce que le build de playtest retire n'est pas cosmétique. Le sélecteur ×1/×3/×10 multiplie les
secondes de **jeu** — celles que le journal d'actions horodate et sur lesquelles `depouiller.py`
rejoue le modèle — et **aucun contrôle ne peut le voir après coup** : le contrôle de
`depouiller.py` travaille dans ces mêmes secondes, où tout reste cohérent. Une partie
accélérée par mégarde rend des minutes qui n'ont jamais été vécues. Il laisse donc une ligne
`vitesse` dans le TSV là où il existe, et n'existe pas ailleurs. « Réinitialiser », lui,
efface quatre-vingt-dix minutes sans rien demander, à six pixels de « copier ».

Les variantes se découpent sur des **marqueurs dans `src/index.html`** dont `build.py` porte la
grammaire : ne jamais lister un bouton dans `build.py`. Et l'en-tête du TSV dit désormais de
quel build il sort.

---

## Règles à ne pas casser

1. **`src/corpus.js` est généré.** Toute modification du texte se fait dans `outils/corpus.py` (transcription exécutable de `docs/corpus.md`), puis `python outils/corpus.py`, puis `python build.py`. Éditer `corpus.js` à la main, c'est perdre le travail au prochain build.

2. **Aucune action manuelle ne doit dépasser 30 % de la Certitude produite, sur aucune tranche de dix minutes.** C'est le mode de défaillance par défaut du jeu : la Certitude est rare, le joueur cherche le chemin le plus court, et deux playtests de suite une action répétée (le clic, puis le recoupement) est devenue la source principale de la ressource centrale. **Mesuré par tranches depuis PT7** : le ratio sur la partie entière s'était posé à 30,0 % en PT6 en cachant un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes — une moyenne, pas un instrument. `outils/sim.py` affiche les tranches ; les vérifier à chaque ajout d'instrument.

    **Sauf la tranche d'ouverture, qui ne se mesure pas tant qu'aucun instrument n'a produit.** Avant la première Concordance, le recoupement est la seule source de Certitude du jeu — la Grammaire reste fermée jusqu'à `année`. Le ratio y vaut donc 100 % par construction, quel que soit le réglage : ce n'est pas un mauvais score, c'est une division par zéro. Balayé le 08/09/2026 sur 27 combinaisons de `cop_b`/`tab_b`/`con_b`, trois cadences chacune : 0–10 min ne descend jamais sous 65 %, tous prix au plancher, et son chiffre ne suit que la date du premier achat de Concordance — 6,8′ au réglage actuel, 10,0′ avant le Copiste à 10, 3,3′ à `cop_b = 5`. C'est le prix du Copiste qui la déplace de sept minutes, pas celui de la Concordance. D'où `i6_tranches()` dans `outils/balayage.py`, qui rend `None` sous une demi-certitude produite et exclut l'ouverture du verdict. **Ne pas régler contre ce chiffre** : il date un achat, il ne mesure pas un équilibre.

    **Le dépassement de 20–30 min est réglé** (09/09/2026), et la façon dont il l'a été vaut pour la suite. Il tenait 28 à 37 % dans les 27 combinaisons de prix, sans jamais passer sous 28 : la famille « prix » ne pouvait pas le toucher. Une analyse de sensibilité une constante à la fois a montré que `rec_o`, `rec_h`, `rec_max`, `tab_p` et `tab_b` sont **inertes** — dans une économie exponentielle les coûts de base ne pèsent rien, seuls les taux de croissance mordent, ce que le commentaire de `REC_R` écrivait déjà depuis PT4. Le levier est donc `REC_R`, porté de 1,18 à **1,30**, compensé par un premier Copiste à **10** au lieu de 15 pour tenir le rythme que l'un allongeait et l'autre raccourcit. Mesuré : 71,8–76,1 min, écart max 5,6 min, toutes les tranches à partir de 10′ sous 26 %. Coût assumé : le joueur recoupe 32 fois au lieu de 49. **À valider en PT10** — le simulateur ne modélise qu'un joueur qui recoupe « tant que c'est rentable » (voir `docs/journal.md`, « le mur des dix premières minutes »).

    **La tranche 20–30′ ne dérive pas avec la taille de l'arbre : elle oscille.** Trois lots l'ont crue en pente (25,8 % à 23 glyphes, 27,0 % à 27, 27,8 % à 28) et ont eu raison sur le mécanisme — elle suit le dénominateur de `revCount()`, et lui seul, ce qu'une décomposition vérifie au dixième près — mais faux sur la conclusion : balayé de 28 à 45, ce chiffre fait 27,8 · 27,7 · 26,2 · 26,2 · 23,9 · 23,9 · 26,4 … une dent de scie de quatre points dont 28 se trouvait être le sommet. Traité le 14/09/2026 par `REV_R = 1,1` dans `revCount()`, qui en ramène l'amplitude à 1,1 point et **rend ce chiffre indépendant de la taille du lexique** — c'est ça qu'on achète, pas le point et demi. Voir `docs/journal.md`, « Le dégagement ne dérive pas, il oscille ». Et le garde-fou de **durée** de `outils/balayage.py`, lui, n'est pas un invariant du tout : resté à (71, 77) — la mesure de PT9, vingt glyphes — pendant que l'arbre passait à vingt-trois, il rejetait ses dix-huit combinaisons, réglage en place compris, en affichant « 0 sur 18 » sans que rien ne soit cassé. Re-basé à (84, 92), puis à (86, 95) à 28 glyphes, puis à (81, 95) le 15/09/2026 — non parce que l'arbre a grandi, mais parce qu'AMB-1 a ajouté une variable : une partie toutes lectures fausses finit 5,5 min plus tôt, et la fenêtre couvre les deux bouts — puis à (82, 96) à 29 glyphes et à **(83, 96)** à 30, le même jour. Elle trie d'autant moins, et c'est assumé : aucun des trois autres garde-fous n'est touché par la lecture. L'écart max et le plafond par tranche, eux, ne bougent jamais.

3. **La numération s'acquiert signe par signe, jamais d'un bloc.** Un nombre du corpus ne passe en chiffres que si le joueur connaît *chacun* de ses signes — et `deux` n'ouvre aucun signe, il ouvre le principe du redoublement (sans lui, on ne lit qu'un nombre où chaque signe apparaît une seule fois). Voir `numLisible()` dans `signes.js` et le tableau dans `docs/journal.md`. `zéro` suit la même règle par l'autre bout : il n'ouvre que le zéro, il ne s'obtient qu'en le composant, et il ne donne pas la notation compacte des grands nombres — elle est celle de `cent` depuis l'acte I.

4. **Les composés se dessinent comme composés.** `sv()` rend un signe composé à partir de ses deux parties (table `COMP` dans `signes.js`). Le joueur doit pouvoir reconnaître ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ avant de savoir le lire.

5. **Le corpus n'a aucun en-tête ajouté par le jeu.** Chaque tablette se numérote elle-même dans sa première ligne. Rien dans cette colonne qui ne soit du texte ancien.

6. **Pas de dépendance externe, pas de framework.** Un seul fichier doit rester distribuable.

7. **Ne jamais annoncer un chiffre de rythme sans l'avoir simulé ou mesuré.** Les neuf playtests ont tous invalidé une intuition d'équilibrage — le simulateur lui-même, deux fois.

8. **Les deux actions manuelles se font dans le corpus.** Le relevé, sur un signe ; le recoupement, sur deux attestations d'un même signe dans deux tablettes différentes. Aucun bouton ne produit plus rien directement — c'est le point de bascule entre « un incrémental habillé en déchiffrement » et un jeu où l'on agit en lisant. Ne pas remettre de raccourci qui contourne le texte.

9. **Le relevé : le tarif d'une tablette est figé au premier relevé qu'on y fait**, jamais à son dégagement — le figer au dégagement laisse à 1 occurrence, pour toute la partie, les seules tablettes qu'on atteint tôt (PT6 : la main retombée à 0,1 % des occurrences). Deux versions plus simples ont échoué au simulateur avant d'atteindre le jeu : un gisement qui coupe vraiment verrouille l'ouverture (13 relevés disponibles pour un premier Copiste alors à 15 ; le Copiste est passé à 10 le 09/09/2026, et la main peut désormais le payer), et un tarif indexé sur le débit courant se thésaurise (72 % des occurrences au lieu de 17 %). Le gisement, et non la cadence de clic, décide de ce que la main rapporte — c'est ce qui rend impossible le retour du défaut de PT1. Corollaire mesuré le 14/09/2026 : **la vitesse de dégagement fixe le prix de la main.** Tout sortir de terre à 80 % de l'arbre ramène la part manuelle des occurrences de 22,9 % à 12,4 % — une tablette dégagée tôt est relevée tôt, donc tarifée au débit du début, donc bon marché pour toute la partie. C'est PT6 en miniature, et aucun garde-fou ne le voyait : `outils/balayage.py` trie désormais aussi sur cette part, plancher à 15 %. **Et le plancher n'a pas suffi : PT10 mesure 1,0 %** (15/09/2026), avec 147 des 148 relevés utiles avant la trente-deuxième minute et un relevé moyen à 1 120 occurrences contre 11 996 en PT9. Le corollaire du 14/09 avait la bonne cause et le mauvais agent : ce n'est pas la vitesse de dégagement qui fixe le prix de la main, c'est **la date des relevés**, et le dégagement n'en est qu'un des deux maîtres. L'autre est le joueur, qui vide le gisement tôt et ne revient pas — ce que le plancher de `balayage.py` ne peut pas voir, puisqu'il mesure un acheteur simulé qui relève tant que c'est rentable. Ne pas régler contre ce chiffre avant PT11, et surtout ne pas toucher `REL_K` : le tarif n'est pas en cause.

10. **La date d'une tablette n'est jamais ajoutée par le jeu.** Chaque tablette porte la sienne dans sa première ligne depuis la première seconde ; `année` ne fait que la rendre lisible, et il faut encore savoir lire le nombre, signe par signe. Corollaire : le rangement chronologique ne réordonne que ce que le joueur sait dater — le reste garde l'ordre de sortie de terre. Ne jamais dater depuis une table externe : la vérité est dans `tb.l[0]`.

11. **Un instrument nommé d'après une méthode philologique doit faire cette méthode.** La Table de fréquences compte les occurrences au survol ; la Concordance rassemble les attestations d'un signe. Sans ça le nom ment, et le jeu redevient un incrémental habillé. Corollaire trouvé en PT8 : **ranger n'est pas rassembler** — l'ordre chronologique ne sert à rien tant que 8 à 57 lignes de registre séparent deux relevés de la même série.

12. **Le dégagement suit la sortie de terre, l'affichage suit le temps.** Sa *vitesse* est `REV_R` (`revCount()`), un exposant mesuré et non choisi : il tire à lui seul la part manuelle des occurrences (règle 9) et la pire tranche d'I6 (règle 2), et il les tire dans le même sens — ralentir améliore les deux. `IDX` (rang dans `ORDRE`) décide de ce qui est visible, l'ordre du DOM décide de ce qu'on lit. Les confondre ferait dégager des tablettes en rangeant. `ranger()` déplace les nœuds existants au lieu de les reconstruire — les jetons relevés et les caches de peinture y survivent.

13. **Le compte de l'arbre n'est pas le compte des glyphes acquis.** Depuis la composition, un signe s'apprend de deux façons : en remontant une branche, ou en le posant soi-même. `nArbre()` compte ce que **l'arbre a rendu** ; `S_.gl.length` compte ce que **le joueur sait**. Tout ce qui mesure une *progression* passe par le premier : la fin de partie, les tablettes dégagées (`revCount()`), l'exposant de la Grammaire (`gramMul()`), le gain du recoupement et le compteur du lexique. Tout ce qui mesure une *compréhension* passe par le second, ou par `mesures()` dans le corpus. Les confondre fait avancer le jeu en composant — un composé secret dégagerait une tablette et donnerait 16 % de Grammaire gratuits — et déplace une économie réglée sur neuf playtests. Un test le vérifie (`verifier.py`, section 14) : après composition, `#lexr` affiche toujours « x / 28 » et aucune tablette n'est dégagée. L'inverse vaut pour un composé **d'arbre** (`deux`, `siècle`, `scribe`, `archive`) : posé à la grille, il avance la partie comme s'il avait été acheté.

14. **La grille de composition ne renseigne jamais.** Elle dessine le signe qu'on propose, sans dire s'il existe — l'indice est dans le corpus, où les composés sont dessinés comme composés (règle 4), et nulle part ailleurs. Corollaire trouvé en l'écrivant : une paire juste que le joueur n'a pas les moyens de payer perd quand même ses hypothèses, parce que la gratuité serait un renseignement. Et la carte de fin ne compte les compositions que si on en a tenté : sinon elle apprendrait qu'il y avait quelque chose à trouver.

15. **Une recette n'existe que si sa cible et ses deux parties sont au lexique.** `COMP` dit comment un signe se *dessine* — ses valeurs sont des clés de tracé, et la branche Nombre y paraît sous ses chiffres (`u1` pour ⟨un⟩). `RECETTES` en dérive ce qu'on peut *poser*, via `ALIAS`, et filtre. Sans ce filtre la grille offre `vingt`, retiré du lexique mais toujours dessinable, et `dernière-année` composée avec un `finir` qui n'existe pas. Ne jamais recopier `COMP` à la main : les recettes des actes IV et V s'ouvriront d'elles-mêmes quand leurs glyphes entreront dans `GL`.

16. **Le dernier signe de l'arbre ne porte pas d'effet chiffré, et la carte de fin attend qu'on l'ait lu.** Les deux tiennent au même fait : `nArbre() === NGL` clôt la partie à l'instant de ce dernier achat. Un multiplicateur posé là n'a pas le temps de rendre — mesuré sur `les-lecteurs`, cinq effets possibles à quatre prix et trois cadences donnent la même durée à la décimale près, et le ×1,5 à la table d'`archive`, qui occupait cette place au lot précédent, ne déplaçait rien non plus. Et `showEnd()`, appelée dans la foulée d'`acheterGl()`, couvrait d'un écran de statistiques la tablette que ce dernier signe venait justement de rendre lisible. Elle est donc **armée** et non montrée (`finArmer()` / `finRegarder()` dans `economie.js`) : elle vient quand `tabletteVisible()` rencontre une des tablettes retenues à l'armement, jamais avant six secondes, jamais après quatre-vingt-dix. `S_.done` est posé à l'achat, lui : la production s'arrête pendant cette lecture, et c'est FIN-1 en avance. Ne pas remettre `showEnd()` dans `acheterGl()` — cinq tests le vérifient.

17. **Un mot français affiché passe par `motDe()`, et rien de ce que le jeu écrit ne présuppose une lecture.** Neuf des onze signes ambigus sont posés depuis le 15/09/2026 : 1 726 attestations sur 3 838 — 45 % du corpus — changent de mot selon ce que le joueur a tranché. Le corpus était la partie facile. Le piège est ailleurs : **partout où le jeu répète un mot de son côté**, il peut se contredire, et une contradiction du jeu avec lui-même est un renseignement (R3, règle 14). Quatre lignes d'effet le faisaient — « chaque tablette porte sa *date* » s'affichait **avant** le choix entre ⟨année⟩ et ⟨soleil⟩ — ainsi que l'infobulle de la barre, la citation de la carte de fin, et les lignes de journal des composés, que `docs/corpus.md` §7.2 ne donnait pas. Tout texte neuf qui nomme un signe doit tenir sous les deux lectures, ou passer par `motDe()`/`logDe()`. Résidu connu et assumé : les effets d'⟨avant⟩ et ⟨après⟩ disent « dans l'ordre du temps » — à traiter avec MOD-2.

    **La prime de 25 % est silencieuse, et c'est ce qui fait tenir le système.** Les deux lectures portent le même tracé, le même prix, la même ligne d'effet : deux chiffres différents feraient de la prime un oracle (« prends toujours le plus gros ») et les onze signes deviendraient onze péages. Elle porte sur le **bonus** et non sur l'instrument (+30 % → +37,5 %) ; un signe qui ne multiplie rien ne gagne rien, et on ne lui invente pas un effet pour porter la prime — quatre des neuf sont dans ce cas. Conséquence mesurée et meilleure que prévu : **la prime ne décide rien à l'achat, elle mord à la révision** (CONTR-2). L'optimum local du design doc §8 n'est pas dans le choix, il est dans le refus de le défaire. Ne pas non plus marquer les signes ambigus dans l'arbre : ils se distinguent au clic, et nulle part avant.

18. **Le doute ne dit jamais l'erreur, il dit l'aveuglement.** Le jeu connaît la vérité et n'a pas le droit de s'en servir : un degré de doute calculé sur la justesse serait l'oracle que la règle 17 refuse. Et le corpus est le même sous les deux lectures, donc **tout doute honnête est identique pour la juste et pour la fausse** — c'est la contrainte, et c'est elle qui a donné la réponse. `douteCalc()` mesure ce qui produit l'erreur : moitié « quelle part des attestations du signe était sortie de terre quand le joueur a tranché », moitié « qu'en avait-il fait » — une concordance sur ce signe vaut plein (règle 11), un recoupement moitié, n'avoir rien fait ne vaut rien même avec les trente tablettes sous les yeux. **Regarder après coup ne le baisse pas** : on ne dé-aveugle pas une décision prise, et sans cette règle le doute serait une jauge qu'on vide en promenant la souris. Seule la révision le recalcule, parce qu'elle seule re-décide — la lecture devient le chemin vers la révision, pas son substitut. Un premier réglage multiplicatif a été jeté : il tassait les neuf signes entre 83 et 99 %, vrai et inutile.

    **La révision ne rend aucun verdict.** Elle coûte, elle repeint le corpus, et c'est au joueur de lire ce qui en sort — « vingt mesures de poussière à la maison 1 » n'a pas de sens, et c'est la seule chose qui le lui dira. Le **bonus rétroactif** du design doc §8 n'est donc pas implémenté et ce n'est pas un oubli : un bonus visible est un verdict, et payer pour voir apparaître une récompense, c'est acheter la réponse au lieu de la lire. Il attend CONTR-1, où il se paiera en dette effacée. Ce que la révision coûte, en revanche, est réel et invisible : reprendre la lecture juste **retire les 25 % de prime** d'AMB-1.

    **Corollaire trouvé par un test, et qui vaut hors de ce lot : un état dérivable ne se stocke pas, surtout quand rien ne le lit.** La dette d'AMB-3, tenue en solde, dérivait dès qu'une lecture changeait autrement que par le chemin prévu — et un solde faux sur un chiffre que personne n'affiche ne se manifeste jamais, jusqu'à CONTR-1 qui en fera son unique intrant. Elle se déduit désormais des lectures (`dette()`).

19. **La contradiction se solde à l'ouverture du doute, et le passage qui refuse ne désigne rien.** Le design doc place la première contradiction à la fin de l'acte III ; dans le prototype, cette fin *est* le dernier achat de l'arbre, qui clôt la partie (règle 16) — la sanction n'aurait pas une seconde pour mordre. Et `année`, seul autre franchissement identifiable, la déclencherait **trente minutes avant que `peut-être` n'existe** : sans remède ni explication, le joueur lirait un bug et non une sanction. Règle générale, dont le prototype ne voit que le premier cas : **elle s'évalue à chaque franchissement d'acte à partir de `peut-être`.** Avant lui le jeu n'admet pas qu'une lecture puisse être fausse ; il ne peut pas en faire payer le prix. Levée, elle ne se réarme pas — on ne ballotte pas un joueur entre deux états sur un chiffre qu'il ne voit pas.

    **Le passage retenu est fixe** — tablette 17, ligne 4 — et il le restera. Le choisir d'après les signes mal lus le ferait pointer exactement ce qu'il faut réviser : l'oracle le plus gros que ce jeu puisse offrir (règles 17 et 18). Le choisir d'après la densité d'ambiguïté donne une ligne de registre générée, identique à quarante autres. Et la tablette 21 a été écartée exprès : y attirer l'œil à la 77ᵉ minute, pour les seuls joueurs endettés, déséquilibrerait la reconnaissance de l'abécédaire à l'acte IV. Corollaire qu'aucun choix de ligne ne supprime : le joueur peut croire que le passage contient ses erreurs, **donc la ligne de journal dit le contraire en toutes lettres**. C'est le seul endroit où le jeu parle de lui-même, et CONTR-1 l'exige — l'état est affiché sans ambiguïté. Il nomme la sanction et sa sortie, jamais un signe.

    **R2 : on ne perd que du débit.** Le passage refuse de se *résoudre*, il ne devient pas illisible : `tokLisible`, `pctTablette`, `mesures()` et le compteur du lexique ignorent le refus, et un test le vérifie en basculant la sanction sans rien acheter. Le joueur sait ces mots ; c'est le texte qui se retient, pas sa compréhension qui recule.

20. **`faux` ne donne pas le corrigé : il allume les lignes où la lecture ne se construit pas.** Le §6 et le §10 du design doc disent « affiche rétroactivement les erreurs déjà commises », ce qui se lit comme le corrigé — mais le §11 promet que la relecture de fin surlignera les erreurs « **y compris celles jamais détectées** ». S'il en reste de jamais détectées à la fin, `faux` ne les a pas nommées. Ce qu'il montre est ce que le §8 appelle depuis le premier jour le seul indice fiable : le texte. Il ne remplace pas la lecture, il rend visible ce qu'un lecteur attentif aurait vu.

    **C'est la LIGNE qui s'allume, jamais le jeton.** Marquer le signe fautif le nommerait — l'oracle que les règles 17, 18 et 19 refusent. Une ligne allumée porte quatre ou cinq signes, dont deux ou trois ambigus : elle réduit le champ, elle ne tranche pas. Le panneau dit *combien* de passages ne se construisent pas, jamais lesquels ni pourquoi. Un test le verrouille : zéro jeton marqué, trois signes ambigus sur la ligne.

    **Trois décisions prises séparément tombent juste d'un coup, et c'est ce qui valide le choix.** Les paires réparantes n'allument rien — « vingt mesures de poussière à la tombe 1 » se tient — donc le §7.3 (« le texte ne trahit rien ») devient mécanique, par le champ `sauf` de `RUPTURES`, au lieu de rester une intention. Les quatre signes sans rupture n'allument rien — `lire` et `il-faut` par conception, `eau` et `année` faute de rupture textuelle (§7.4) — et ce sont exactement les erreurs « jamais détectées » du §11. Et **se tromper sur les neuf n'allume que trois lignes sur cinq** : mal lire partout cache deux de ses propres erreurs.

    Une seule ligne par signe, la plus précoce : ⟨ne-pas⟩ casse sur `sinon` cent trente et une fois, en allumer cent trente et une noierait le signal, et AMB-4 demande « un endroit précis du corpus ».

---

## Ce qui a été tranché

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.
- **L'invariant I5 du design doc (« progression quasi linéaire ») est retiré.** Aucune mesure de progression n'est linéaire : les signes sont front-chargés, les lignes back-chargées. L'écart entre les deux *est* le propos — on peut lire presque tous les mots et ne comprendre presque rien. L'afficher, ne pas le lisser.
- Lexique porté à **45 signes** (la branche Nombre gagne `cinq` et `mille`, perd `vingt`).
- **17 composés** au lieu des 9 prévus.
- **Les paires réparantes, 14/09/2026 : on ne fait rien.** Trois paires de lectures fausses s'annulent mutuellement — ⟨grain⟩ « poussière » avec ⟨maison⟩ « tombe », ⟨semence⟩ avec ⟨devenir⟩, ⟨lire⟩ avec ⟨devenir⟩, cette dernière couvrant `devenir-lecture`, dernier signe du jeu. Ni interdiction, ni ligne de corpus ajoutée : interdire une lecture, c'est renseigner (R3, règle 14), et une ligne déplace des fréquences pour couvrir trois cas sur cinquante-cinq paires possibles. Qui se trompe deux fois de la bonne façon finit sur un autre livre, et c'est le propos — même décision que le retrait de l'invariant I5. **Le risque est accepté, pas supprimé** : la dette court quand même (+2 à +6 points), donc la contradiction se déclenche quand même ; le joueur est privé de l'indice, pas de la sanction. Deux épics en héritent — **MOD-2** devient la soupape (le degré de doute par signe est le seul pointeur qui reste, le texte ne trahissant rien) et **FIN-3** devient le seul endroit où le jeu admet jamais qu'on a lu autre chose. L'exception est inscrite au design doc §8, dont la promesse « le seul indice fiable est le texte » ne vaut pas pour ces trois-là. Voir `docs/corpus.md` §7.3.
- **Ce que `faux` révèle, 15/09/2026 : où, jamais quoi.** Le design doc se contredisait — §6 et §10 annoncent le corrigé, §11 promet des erreurs « jamais détectées » à la relecture de fin. Le §11 tranche : `faux` allume les lignes qui ne se construisent pas, et ne nomme aucun signe. Trois décisions antérieures tombent juste d'un coup — les paires réparantes n'allument rien (§7.3 devient mécanique), les quatre signes sans rupture non plus (§7.4, ce sont les « jamais détectées »), et se tromper sur les neuf n'allume que trois lignes sur cinq. Voir règle 20 et `docs/journal.md`, « `faux` ne donne pas le corrigé ».
- **Le seuil de contradiction, 15/09/2026 : 5.** Les poids de dette étant tirés des attestations, le seuil découpe des profils de lecture réels : 0 pour une lecture parfaite, 3 pour qui ne rate que les deux signes conçus pour ne pas casser, 6 pour la paire réparante, 8 en moyenne pour qui tire à pile ou face, 18 pour qui se trompe partout. À 5, un lecteur qui a fait tout ce que le texte permet passe avec de la marge, et **la paire réparante déclenche** — ce que le §7.3 exigeait en décidant de la laisser passer. Mesuré : elle est même le pire cas du jeu (100,5–103,4 min), devant « tout faux » (96,6–99,5), parce qu'elle prend la sanction entière avec la prime de deux signes seulement.
- **Le degré de doute, 15/09/2026 : il dit l'aveuglement, pas l'erreur.** Le §7.3 demandait un doute « calculé par le jeu et non par la lecture ». En l'écrivant on bute sur le mur : le jeu connaît la vérité et n'a pas le droit de s'en servir, et le corpus est le même sous les deux lectures — donc **tout doute honnête est identique pour la juste et pour la fausse**. C'est la contrainte qui a donné la réponse : il mesure ce qui produit l'erreur, la part du signe qu'on n'avait pas sous les yeux en tranchant et ce qu'on en avait travaillé. Corollaires tranchés en même temps : regarder après coup ne le baisse pas, la révision ne rend aucun verdict, et le bonus rétroactif du design doc §8 attend CONTR-1 parce qu'un bonus visible est un verdict. Voir règle 18 et `docs/journal.md`, « Le doute ne dit pas l'erreur ».
- **La rupture distributionnelle, 15/09/2026 : admise, et la prémisse du §7.4 était fausse.** ⟨année⟩ n'est suivi d'un nombre que 67 fois sur 139 — mais 72 fois de ⟨ne-pas⟩, l'absence de compte, qui est un compte puisque ⟨zéro⟩ **est** ⟨ne-pas⟩⟨un⟩. Mesurée en *cadre de nombre*, la distribution donne ⟨année⟩ à 100 % et ⟨nuit⟩ à 0 %, là où la formulation d'origine donnait 48 % contre 0 %. `eau` et `année` ont donc leur indice sans qu'une ligne de corpus soit écrite, et il se trouve **en travaillant**, pas en lisant. Voir `docs/corpus.md` §7.4.
- **La prime de la lecture fausse, 15/09/2026 : silencieuse.** Le design doc §8 promettait « +25 % d'effet mécanique » sans dire si le joueur les voit. Il ne les voit pas : deux lignes d'effet différentes à l'écran de choix feraient de la prime un oracle, et les onze signes ambigus deviendraient onze péages. La conséquence vaut mieux que ce qui était prévu — la prime ne décide rien à l'achat, elle mord à la **révision** (CONTR-2), donc l'optimum local est dans le refus de corriger, pas dans le choix. Mesuré : se tromper sur les neuf signes de l'acte III fait gagner 5,5 min sur 90, soit 6 %, et deux des cinq signes qui portent un multiplicateur ne paient rien du tout. Voir règle 17 et `docs/journal.md`, « Trancher à l'achat ».
- **⟨N1⟩ et ⟨N2⟩, 11/09/2026 : semés comme intitulés des registres.** Un nom seul sur sa ligne en tête de chaque bloc généré — ⟨N1⟩ (le fleuve) sur `champs` et `veille`, ⟨N2⟩ (la cité) sur `maisons` et `archive`, rien sur `consignes`. 13 et 16 occurrences : fréquence moyenne, choisie contre un titre courant. Seule exception admise au principe « aucun signe uniquement dans un bloc » (`docs/corpus.md` §6) : un nom propre ne se déchiffre pas, sa fréquence ne ment donc à personne. Rythme simulé inchangé, gisement 397 → 399.

---

## État actuel et suite

**Fait** : **actes I à III entiers**, **30 signes d'arbre sur 45**, plus deux composés secrets, corpus complet des 30 tablettes (705 lignes, 3 838 signes), économie réglée sur neuf playtests, numération signe par signe de `zéro` à `mille`, barre de navigation entre tablettes, infobulles, comptage d'occurrences dans le lexique, journal d'actions horodaté, relevé et recoupement dans le corpus avec gisement par tablette, **datation et réordonnancement chronologique**, instrument **Grammaire**, progression **hors ligne**, **grille de composition** avec carnet des tentatives, **ambiguïté : deux lectures tranchées à l'achat** sur neuf signes, **degré de doute, révision, contradiction, et les passages qui ne se construisent pas**.

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

**La Modalité, et le zéro** (12/09/2026, MOD-1 + COMP-3) : `ne-pas` (150 C), `si` (320 C),
`il-faut` (550 C, +50 % atelier), `sinon` (800 C) — et `zéro` (120 C) par la grille, ⟨ne-pas⟩
posé sur ⟨un⟩, première fois qu'une branche tardive mord sur la branche Nombre. Aucune ligne
du corpus ne change, mais **816 attestations passent en français**, un signe du corpus sur
cinq : les foyers vides de la tablette 25, le protocole de copie jusqu'à son dernier mot
(« il-faut copier · si ne-pas · sinon » — ce qui vient après n'est gravé nulle part), et les
neuf zéros de la tablette 29. Un seul effet chiffré pour quatre signes, et c'est mesuré :
donner à `si` le troisième ×1,5 de la Grammaire **raccourcissait** l'acte de cinq minutes —
dans cette économie, un taux posé sur l'instrument qui porte la Certitude se rembourse avant
d'être payé (la leçon de `REC_R`, par l'autre bout). Mesuré : **87,0–90,0 min pour 27
signes**, écart max 5,2, tranches ≥ 10′ ≤ 27 %. `zéro` n'a **pas** la notation compacte des
grands nombres que lui prête le design doc §7 : elle est déjà celle de `cent` — voir
`docs/journal.md`, « La Modalité, et le zéro ».

**Les lecteurs, et la fin de l'acte III** (14/09/2026, PAR-2) : `les-lecteurs` (1 200 C),
dernier signe de la Parole, **sans aucun effet chiffré**. Ce n'est pas un oubli, c'est la
règle 16 : dernier achat de l'arbre, il est payé à la seconde où la partie se termine —
cinq effets possibles, quatre prix, trois cadences, la même durée à la décimale près. Trois
attestations, toutes sur la tablette 18, qui passe de 68 % à **80 %** de lisibilité et
s'arrête là : ce qui reste est ⟨nous⟩, quatre fois, **dessiné dans le nom lui-même**
(⟨lire⟩ sur ⟨nous⟩) et posé seul juste devant, sur la même ligne. 41 attestations ailleurs
dans le corpus, aucune au lexique avant la branche Personne : la porte de l'acte IV est dans
le texte, et nulle part ailleurs. Aucune recette ne s'ouvre pour autant (règle 15). La carte
de fin, elle, attend désormais qu'on ait lu cette tablette. Mesuré : **89,7–92,9 min pour
28 signes**, écart max 5,2, tranches ≥ 10′ ≤ 26 %, garde-fou de durée re-basé à (86, 95).
1 200 C suit l'arithmétique de la branche et non le drame : à 1 800 le dernier écart monte à
4,2 min, quatre minutes sans rien à acheter avant la dernière révélation — le trou de fin
d'acte que PT8 avait mesuré à 4 min 51 et que la Concordance avait réparé.

**Le dégagement, traité** (14/09/2026) : `revCount()` gagne un exposant, `REV_R = 1,1` —
`4 + 26 × (nArbre / NGL)^1,1`. La tranche 20-30′ que trois lots croyaient en dérive **oscille**
(dent de scie de quatre points sur les dénominateurs 28 à 45, dont 28 était le sommet) ; ce
qui est traité, c'est l'oscillation elle-même, ramenée de 3,9 points à 1,1. Le premier
candidat — tout dégager à 80 % de l'arbre — gagnait deux points d'I6 en ramenant la main de
22,9 % à **12,4 %** des occurrences : PT6 en miniature, et aucun garde-fou ne le voyait. D'où
la part manuelle entrée dans le tri de `outils/balayage.py` (plancher 15 %), qui balaie aussi
`rev_r` désormais. Mesuré : 89,7–92,9 min, écart 5,2, tranches ≥ 10′ ≤ 26 %, main 22,9–23,4 %.

**Les onze lectures fausses** (14/09/2026, TXT-1) : les onze mots faux, leurs lignes de journal,
leurs composés dérivés et le point de rupture de chacun — **écrits et vérifiés ligne à ligne contre
le corpus rendu**, `docs/corpus.md` §7.1 à §7.5. Le chemin critique du projet est dégagé : AMB-1 ne
dépend plus d'aucun texte. La vérification a invalidé **trois** ruptures que la table annonçait
depuis le premier jour — celle d'`eau` visait une ligne qui n'existe pas, celle de `ne-pas` une
séquence absente des 705 lignes, celle d'`avant` une rupture mécanique là où AMB-4 demande du texte.
Deux se remplacent par mieux et plus tôt ; **`eau` et `année` n'en ont aucune**, soit quatre signes
sans rupture au lieu des deux voulus. Et le défaut que rien n'annonçait : **trois paires de lectures
fausses se réparent l'une l'autre** — qui lit ⟨grain⟩ « poussière » *et* ⟨maison⟩ « tombe » obtient
un culte funéraire cohérent sur trente tablettes, et `lire`+`devenir` couvre `devenir-lecture`,
dernier signe du jeu. Deux décisions passaient à AMB-1 : **celle des paires est tranchée le même
jour — on ne fait rien** (voir « Ce qui a été tranché ») ; celle de la rupture distributionnelle
pour `eau` et `année` reste ouverte au §7.4. Ce que le lot démontre au passage : **le mot
décide, pas le concept** — ⟨devenir⟩ faux dit *porter* et non *tenir*, et c'est le seul rempart entre
« il faut la tablette · porter lire », qui ne se construit pas, et « tenir compte », qui est
invisible. Voir `docs/journal.md`, « Les onze lectures fausses ».

**Trancher à l'achat** (15/09/2026, AMB-1 + AMB-2 + AMB-3) : neuf des onze signes ambigus
proposent leurs deux lectures au moment de payer — `semence` et `devenir` sont de l'acte V et
leurs entrées, écrites d'avance, sont inertes jusque-là. Même tracé, même prix, **même ligne
d'effet** : la prime de 25 % est silencieuse, sans quoi elle serait un oracle (règle 17). Elle
porte sur le bonus (+30 % → +37,5 %) et seuls cinq des neuf signes portent un multiplicateur ;
mesuré, **deux de ces cinq ne paient rien** — `eau` parce qu'en fin de partie les hypothèses ne
sont pas ce qui manque, `il-faut` pour la raison déjà trouvée en MOD-1. Le signe où la prime paie
le plus est ⟨grain⟩ : 3 C, troisième minute, quatre tablettes sorties de terre — le piège est
appâté le plus fort là où le joueur a le moins de quoi trancher, mais sa rupture est aussi la plus
précoce du lot (tablette 5, sixième à sortir de terre). **1 726 attestations sur 3 838 — 45 % du
corpus** — changent de mot, composés compris. La dette court (1 à 3 points par signe, déduits des
attestations ; 18 au maximum) et **personne ne la lit** avant CONTR-1. Mesuré : **89,7–92,9 min
toutes lectures justes — inchangé au dixième, c'était le contrat — et 84,4–87,5 toutes fausses**,
écart max 4,6–5,2, main 22,9–24,8 %, tranches ≥ 10′ ≤ 26 %. `outils/balayage.py` gagne un axe (les
deux lectures extrêmes) et sa fenêtre de durée passe à (81, 95) ; `outils/verifier.py` passe de 177
à 202 assertions. Voir `docs/journal.md`, « Trancher à l'achat ».

**Le doute, et la révision** (15/09/2026, MOD-2 + CONTR-2 + CONTR-3) : `peut-être` (450 C,
entre `si` et `il-faut`, aucun multiplicateur) dit au joueur que onze de ses lectures en
supportaient une autre, et qu'il a tranché sans jamais en être averti. Le prix est une
mesure, pas un cran de branche : au bout de la Modalité il tombe **2,4 min avant la fin** du
prototype, à 450 il laisse **quatorze minutes** — trois ou quatre révisions, payées en signes
non achetés. Effet de bord non cherché : `il-faut` se tranche alors le panneau déjà ouvert,
et c'est la seule décision ambiguë que le joueur prenne en sachant ce qu'il risque. Le degré
de doute **ne peut pas dire l'erreur** (le corpus est le même sous les deux lectures) : il
dit l'aveuglement, et regarder après coup ne le baisse pas (règle 18). La révision coûte
240 C ×1,6 **par révision et jamais par signe** — balayer les neuf coûte 27 088 C contre
4 550 encore dépensables, six fois le budget ; trois révisions choisies en coûtent 1 238.
Elle ne rend **aucun verdict** : elle repeint, et c'est au joueur de lire. Le **§7.4 est
refermé**, et sa prémisse était fausse — ⟨année⟩ n'est suivi d'un nombre que 67 fois sur 139,
mais 72 fois de ⟨ne-pas⟩, l'absence de compte, qui est un compte. En *cadre de nombre*,
⟨année⟩ fait **100 %** et ⟨nuit⟩ **0 %** ; le chiffre paraît en infobulle à partir de
`peut-être`, identique pour les deux lectures. La dette cesse d'être un solde et se déduit
des lectures. Mesuré : **90,5–93,7 min toutes lectures justes, 85,2–88,1 toutes fausses**,
écart max 5,2, main 21,6–25,8 %, tranches ≥ 10′ ≤ 26 %. Garde-fou de durée re-basé à
(82, 96) ; `outils/verifier.py` passe de 202 à 224 assertions. Voir `docs/journal.md`, « Le
doute ne dit pas l'erreur ».

**La contradiction** (15/09/2026, CONTR-1) : dette > **5** au solde du doute, et la Certitude
est divisée par deux jusqu'à ce qu'une révision la fasse repasser sous le seuil. Elle se
solde **à l'ouverture du doute** et non à un franchissement de branche — dans le prototype la
fin de l'acte III est le dernier achat de l'arbre (règle 16), et `année` la déclencherait
trente minutes avant que `peut-être` n'existe, donc sans remède : le joueur lirait un bug, pas
une sanction. Le passage qui refuse est **fixe** — tablette 17 ligne 4, « eau · ne-pas
tablette », la note de tri qui constate qu'un relevé manque, et que le jeu fait manquer.
Aucune progression n'est perdue (R2), c'est vérifié en basculant la sanction sans rien
acheter. Mesuré chez qui ne révise jamais : **90,5–93,7 min** en lecture parfaite,
**89,1–92,4** pour qui ne rate que les deux incassables — la prime sans la sanction, la partie
la plus rapide du tableau — **96,6–99,5** toutes fausses, et **100,5–103,4 pour la paire
réparante**, qui prend la sanction entière avec la prime de deux signes seulement. Le pire cas
du jeu n'est donc pas celui qui se trompe le plus : c'est celui que le texte ne peut pas
prévenir, exactement ce que le §7.3 annonçait en décidant de le laisser passer. Le **bonus
rétroactif** du design doc se paie enfin, en dette effacée, sans rien annoncer.
`outils/balayage.py` désarme la contradiction — il mesure le rythme, pas la peine ;
`outils/verifier.py` passe de 224 à 239 assertions. Voir `docs/journal.md`, « La
contradiction ».

**`faux`** (15/09/2026, MOD-3) : 700 C, entre `il-faut` et `sinon`, aucun multiplicateur. Il
**ne donne pas le corrigé** — il allume les lignes où la lecture retenue ne se construit pas.
C'est le §11 du design doc qui l'impose : la relecture de fin surlignera les erreurs « y
compris celles jamais détectées », donc `faux` ne les a pas nommées. Trois décisions prises
séparément tombent juste d'un coup — **les paires réparantes n'allument rien** (le §7.3
devient mécanique), **les quatre signes sans rupture non plus** (§7.4 : ce sont les erreurs
jamais détectées), et **se tromper sur les neuf n'allume que trois lignes sur cinq**, donc mal
lire partout cache deux de ses propres erreurs. C'est la LIGNE qui s'allume, jamais le jeton :
marquer le signe le nommerait, alors qu'une ligne en porte quatre ou cinq. Le prix est une
mesure — au bout de la branche il tombe 2,1 min avant la fin, à 700 il en laisse six. Seize
attestations, dont les cinq dernières lignes de la tablette 26, où la dernière scribe annule
« peut-être eau » quatre-vingt-dix-sept ans plus tard : le joueur vient de faire le même geste
sur son propre corpus. Mesuré : **91,1–94,3 min** toutes lectures justes, **85,9–89,1** toutes
fausses, **98,1–105,1** contradiction armée ; écart max 5,2, main 22,2–28,0 %, tranches ≥ 10′
≤ 26 %. Garde-fou de durée re-basé à (83, 96), 34 combinaisons sur 54 au balayage ;
`outils/verifier.py` passe de 239 à 256 assertions. Voir `docs/journal.md`, « `faux` ne donne
pas le corrigé ».

**PT10 fait** (15/09/2026) : **96 min 35** pour les trente signes, 94 min 16 de jeu effectif. Mais **l'auteur l'a joué**, donc il ne répond sur aucune des questions de lecture — elles repassent entières à PT11. Ce qu'il mesure à la place, ce sont deux défauts d'économie que neuf playtests et tous les balayages avaient manqués. **La main fournit 1,0 % des occurrences** contre 36,3 % en PT9 (règle 9), et **cinquante minutes d'affilée se jouent sans un geste dans le corpus** — de 36:46 à 86:34, 53 % de la partie, zéro relevé, zéro recoupement, zéro concordance, zéro navigation. Les deux ont la même cause : le gisement sort en trente minutes, il est donc tarifé au débit du début et bon marché pour toujours, et il ne reste plus rien à y faire ensuite. C'est le défaut de PT6 par la porte que R9 ne garde pas — elle fige le tarif à la première visite, elle ne dit rien de qui ne revient jamais. **Le plus grave depuis PT6**, et il attend la mesure de PT11 avant tout réglage. Le reste tient : I6 à 0,7 % (ouverture à 79 %, connue), 32 recoupements exactement comme le simulateur l'annonçait — mais tous dans les trente-sept premières minutes — contradiction déclenchée à dette 6 et sanction vérifiée au chiffre, zéro révision, `les-lecteurs` acheté à 95:20 **devant `sinon` qui coûte 400 de moins**, et **le simulateur tombe juste pour la première fois depuis PT7** (91,1–94,3 annoncées, 94,3 jouées). Six compositions, **six paires justes**, dont cinq refusées faute de Certitude : le carnet est resté vide toute la partie. Voir `docs/journal.md`, « PT10 — la main a disparu du corpus ».

**Le journal d'actions ne mesurait pas quatre des questions qu'on lui posait** (15/09/2026) : `reviser` n'était pas enveloppée, le degré de doute n'était pas écrit à l'achat, une paire juste impayable ne se distinguait pas d'un coup de sonde — c'est ce qui a d'abord fait lire les six compositions de PT10 comme cinq échecs — et le chrono gelait au dernier signe de l'arbre, d'où six actions au même instant et aucune ligne de fin pour une partie terminée. Les quatre sont bouchés ; `finjeu` date l'arrêt et `fin` l'ouverture de la carte, dont l'écart est la mesure de FIN-1. `outils/verifier.py` passe de 256 à **265 assertions**.

**PT11 se jouera à distance — trois builds** (17/09/2026, LIV-2) : `python build.py` sort quatre
pages du même `src/`, et GitHub Pages déploie **`dist/playtest.html`**, qui garde le journal
d'actions mais **pas le sélecteur de vitesse ni « réinitialiser »**. Le premier ne fait pas du
bruit, il fait mentir l'axe : il multiplie les secondes de **jeu**, celles que le TSV horodate,
et **aucun contrôle ne peut le voir après coup** — celui de `depouiller.py` travaille dans ces
mêmes secondes et trouve tout cohérent. Il laisse donc une ligne `vitesse` là où il existe, et
le dépouillement ouvre son rapport par un avertissement. Le second efface quatre-vingt-dix
minutes sans rien demander. Ce que le lot a trouvé en chemin : **retirer un bouton n'est pas une
suppression, c'est un découplage** — `frame()` écrivait dans `#chrono` à chaque frame et
« recommencer » se déléguait à `$('reset').click()` ; la version publique se serait arrêtée à la
première frame, et `requestAnimationFrame` n'aurait jamais été appelé. D'où `recommencer()` dans
`rendu.js`, que `traces.js` enveloppe au lieu d'écouter un bouton. La barre de playtest dit
« journal de partie — à renvoyer », dans la barre et non sur la carte de fin : **la partie
abandonnée est celle dont le journal compte le plus** (ECO-1), et la carte n'arrive qu'à la
quatre-vingt-dixième minute. Économie inchangée au chiffre près (`sim.py` 91,1–94,3 min,
`balayage.py` 34 sur 54) ; `outils/verifier.py` passe de 265 à **286 assertions**. **LIV-3 n'est
pas traité** et la parade est un usage : le workflow déploie à chaque poussée sur `develop`,
donc **pendant PT11, rien ne va sur `develop`** — sans quoi le jeu change sous les pieds du
joueur au rechargement suivant. Voir `docs/journal.md`, « Ce qui mesure ne doit pas pouvoir
fausser ce qu'il mesure ».

**Prochaine étape — PT11 avec un autre joueur, puis l'Élève (E5).** Même question qu'en PT8 et PT9, posée à quelqu'un qui ne sait pas ce qu'il cherche — plus celle que PT10 a ouverte : **revient-on dans le corpus après la quarantième minute ?** Dans le même TSV : la part manuelle des occurrences (au-delà de 40 %, plafonner `REL_K`) le stock d'hypothèses entre `année` et la dixième Grammaire (27 090 en PT9), **le nombre de recoupements** — sous une vingtaine sur la partie, le réglage du 09/09 a vidé un des deux gestes manuels et il faut revenir en arrière — et **les tentatives de composition** : le journal d'actions les compte avec leur paire et leur minute. La question neuve est celle-là : un joueur qui ignore qu'il y a quelque chose à chercher reconnaît-il ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩, ou ⟨ne-pas⟩ et ⟨un⟩ dans le zéro qu'il regarde depuis la première seconde ? Aucun simulateur ne répond à ça. S'y ajoutent deux questions depuis `les-lecteurs` : **achète-t-on un signe à 1 200 C qui annonce trois attestations** — le TSV date le moment où il devient payable — et, à poser de vive voix, **a-t-on vu ⟨nous⟩ dans le nom** ? Et une mesure de plus, parce que `REV_R` la déplace sans qu'aucun playtest soit derrière : **le nombre de recoupements et la part manuelle des occurrences**. Si la main descend au lieu de monter, c'est `REV_R` qu'il faut défaire en premier, avant les prix.

**Et depuis AMB-1, trois questions de plus, qu'aucun simulateur ne touche.** Le journal d'actions note désormais la lecture retenue à chaque achat, avec un ✗ pour la fausse. (1) **Combien de lectures fausses sur neuf ?** Neuf pièces à pile ou face donneraient 4,5 ; nettement moins voudrait dire que quelque chose souffle la réponse, nettement plus que le corpus l'induit en erreur. (2) **⟨grain⟩ ou ⟨poussière⟩ à la troisième minute** — c'est le choix où la prime paie le plus et où le joueur a le moins de quoi trancher ; et s'il se trompe, retourne-t-il sur la tablette 5 quand elle sort de terre ? (3) À poser de vive voix, une fois seulement, **et à la fin** : a-t-on remarqué qu'on choisissait ? Le jeu ne le dira jamais avant `peut-être`.

**Et depuis MOD-2, deux questions de plus pour PT10.** Le journal d'actions note la lecture retenue et le degré de doute à chaque achat. (1) **Combien de révisions, et sur quels signes ?** Zéro voudrait dire que le panneau ne pointe rien ; plus de cinq, que le prix ne mord pas. (2) **Le joueur concorde-t-il AVANT de trancher, ou après ?** C'est le seul geste qui fasse baisser le doute, et le jeu ne le dit nulle part — s'il ne le trouve pas, il faudra se demander si le doute pointe vers quelque chose d'atteignable.

**Et deux questions de plus depuis CONTR-1 et MOD-3.** (1) **La contradiction se déclenche-t-elle, et le joueur la relie-t-il à ses lectures ?** Le bandeau dit la sanction et sa sortie sans nommer un signe ; s'il la lit comme une panne, c'est le texte du bandeau qu'il faut reprendre, pas le seuil. (2) **Une ligne allumée par `faux` se lit-elle ?** Elle ne nomme rien et porte quatre ou cinq signes ; si le joueur ne s'en sert pas pour choisir sa révision, c'est que la marque ne suffit pas — mais la réponse n'est pas de nommer le signe, jamais.

Restent ensuite : **l'Élève** (E5), qui déchiffre tout seul et se trompe — son taux d'erreur a maintenant de quoi se nourrir, et c'est le dernier morceau de J2. Puis l'**acte IV** (la branche Personne, les Questions, le Corpus jumeau), l'**acte V**, et la relecture de fin, seul endroit où le jeu avouera les erreurs jamais détectées. Voir `docs/design-doc.md` §7 et §8, et `docs/backlog-1.0.md` pour le découpage.

---

## Conventions

- Commentaires en français, au-dessus de ce qui est non évident. Expliquer **pourquoi**, pas quoi.
- Les noms de fonctions et variables suivent la fiction quand c'est naturel : `veille()`, `consignes()`, `recouper()`, `tablette`.
- Le sélecteur de vitesse ×1/×3/×10, le chronomètre et les boutons `traces`/`copier` en haut à droite sont des **outils de test**, marqués « hors jeu ». **Ce n'est plus à retirer à la main** : les marqueurs de variante d'`index.html` décident de ce que chaque build en garde. Un bouton hors jeu neuf se pose dans le bloc `#dev`, pas ailleurs, tant qu'on n'a pas dit ce qu'il fait devant un joueur qu'on ne regarde pas jouer.
- `src/traces.js` n'édite aucune règle : il **enveloppe** les actions déjà déclarées — des fonctions, jamais des écouteurs de boutons, qui ne sont pas dans tous les builds. `dist/public.html` le retire déjà (16 Ko de moins). Ne jamais y mettre de logique de jeu, et ne jamais l'appeler depuis le jeu.
- Écrire les nombres à la française dans l'interface (espace fine insécable, virgule décimale) — `nf` et `f()` s'en chargent.
