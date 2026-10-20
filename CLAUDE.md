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
  lexique.js    les 43 glyphes des actes I–V + 2 composés : coût, effet, texte de journal,
                les onze lectures fausses (`AMB`, `COMPFAUX`) et leurs points de rupture
                (`RUPTURES`)
  corpus.js     GÉNÉRÉ — ne jamais éditer à la main
  economie.js   état et son chargement versionné, ressources, instruments, actions,
                boucle de simulation
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

    **La tranche 20–30′ ne dérive pas avec la taille de l'arbre : elle oscille.** Trois lots l'ont crue en pente (25,8 % à 23 glyphes, 27,0 % à 27, 27,8 % à 28) et ont eu raison sur le mécanisme — elle suit le dénominateur de `revCount()`, et lui seul, ce qu'une décomposition vérifie au dixième près — mais faux sur la conclusion : balayé de 28 à 45, ce chiffre fait 27,8 · 27,7 · 26,2 · 26,2 · 23,9 · 23,9 · 26,4 … une dent de scie de quatre points dont 28 se trouvait être le sommet. Traité le 14/09/2026 par `REV_R = 1,1` dans `revCount()`, qui en ramène l'amplitude à 1,1 point et **rend ce chiffre indépendant de la taille du lexique** — c'est ça qu'on achète, pas le point et demi. Voir `docs/journal.md`, « Le dégagement ne dérive pas, il oscille ». Et le garde-fou de **durée** de `outils/balayage.py`, lui, n'est pas un invariant du tout : resté à (71, 77) — la mesure de PT9, vingt glyphes — pendant que l'arbre passait à vingt-trois, il rejetait ses dix-huit combinaisons, réglage en place compris, en affichant « 0 sur 18 » sans que rien ne soit cassé. Re-basé à (84, 92), puis à (86, 95) à 28 glyphes, puis à (81, 95) le 15/09/2026 — non parce que l'arbre a grandi, mais parce qu'AMB-1 a ajouté une variable : une partie toutes lectures fausses finit 5,5 min plus tôt, et la fenêtre couvre les deux bouts — puis à (82, 96) à 29 glyphes et à **(83, 96)** à 30, le même jour — et à **(76, 96)** le 12/10/2026 avec l'Élève, qui lui ajoute une troisième variable : sept minutes de moins pour qui en empile sept. Elle trie d'autant moins, et c'est assumé : aucun des trois autres garde-fous n'est touché par la lecture. L'écart max et le plafond par tranche, eux, ne bougent jamais.

3. **La numération s'acquiert signe par signe, jamais d'un bloc.** Un nombre du corpus ne passe en chiffres que si le joueur connaît *chacun* de ses signes — et `deux` n'ouvre aucun signe, il ouvre le principe du redoublement (sans lui, on ne lit qu'un nombre où chaque signe apparaît une seule fois). Voir `numLisible()` dans `signes.js` et le tableau dans `docs/journal.md`. `zéro` suit la même règle par l'autre bout : il n'ouvre que le zéro, il ne s'obtient qu'en le composant, et il ne donne pas la notation compacte des grands nombres — elle est celle de `cent` depuis l'acte I.

    **Les compteurs du joueur n'en relèvent pas, et ce n'est pas un oubli à réparer.** La règle dit « un nombre **du corpus** ». L'interface a trois portes à elle, trois booléens globaux (`src/economie.js:434-436`) : `readN` = ⟨un⟩ pour les trois compteurs O/H/C, `readC` = ⟨deux⟩ pour les coûts, le gisement et les fréquences, `readR` = ⟨dix⟩ pour les débits. Les trois sont annoncées dans les lignes d'effet, et la fiction les porte — les compteurs sont la notation **du joueur**, pas celle de la langue morte, ce que dit la ligne de journal de ⟨un⟩ (« mes propres comptes se tiennent enfin — les leurs, à peine ») et ce que l'invariant I2 reprend à l'acte IV (règle 30). Appliquer `numLisible()` aux compteurs les ferait scintiller entre chiffres et glyphes au rythme de la production (avec ⟨un⟩ et ⟨dix⟩ sans ⟨deux⟩ : 11 se lit, 12 non) et les laisserait en barre pleine au-delà de 2 000. **Ce qui reste ouvert, c'est le seuil d'⟨un⟩, pas le principe** — mesure de PT11, issue [#57](https://github.com/DavidGiangiacomo/langue-morte/issues/57). **Et ce qu'⟨un⟩ a donné, l'acte IV le reprend en partie** (VOIX-5, règle 30) : au million, les zéros des compteurs et des coûts passent au tracé de ⟨zéro⟩. C'est une quatrième porte, posée dans `big()` après les trois autres — jamais `numLisible()`, et pour la même raison : les chiffres restent ceux du joueur, seuls les zéros changent d'écriture.

4. **Les composés se dessinent comme composés.** `sv()` rend un signe composé à partir de ses deux parties (table `COMP` dans `signes.js`). Le joueur doit pouvoir reconnaître ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ avant de savoir le lire.

5. **Le corpus n'a aucun en-tête ajouté par le jeu.** Chaque tablette se numérote elle-même dans sa première ligne. Rien dans cette colonne qui ne soit du texte ancien.

6. **Pas de dépendance externe, pas de framework.** Un seul fichier doit rester distribuable.

7. **Ne jamais annoncer un chiffre de rythme sans l'avoir simulé ou mesuré.** Les neuf playtests ont tous invalidé une intuition d'équilibrage — le simulateur lui-même, deux fois.

8. **Les deux actions manuelles se font dans le corpus.** Le relevé, sur un signe ; le recoupement, sur deux attestations d'un même signe dans deux tablettes différentes. Aucun bouton ne produit plus rien directement — c'est le point de bascule entre « un incrémental habillé en déchiffrement » et un jeu où l'on agit en lisant. Ne pas remettre de raccourci qui contourne le texte.

9. **Le relevé : le tarif d'une tablette est figé au premier relevé qu'on y fait**, jamais à son dégagement — le figer au dégagement laisse à 1 occurrence, pour toute la partie, les seules tablettes qu'on atteint tôt (PT6 : la main retombée à 0,1 % des occurrences). Deux versions plus simples ont échoué au simulateur avant d'atteindre le jeu : un gisement qui coupe vraiment verrouille l'ouverture (13 relevés disponibles pour un premier Copiste alors à 15 ; le Copiste est passé à 10 le 09/09/2026, et la main peut désormais le payer), et un tarif indexé sur le débit courant se thésaurise (72 % des occurrences au lieu de 17 %). Le gisement, et non la cadence de clic, décide de ce que la main rapporte — c'est ce qui rend impossible le retour du défaut de PT1. Corollaire mesuré le 14/09/2026 : **la vitesse de dégagement fixe le prix de la main.** Tout sortir de terre à 80 % de l'arbre ramène la part manuelle des occurrences de 22,9 % à 12,4 % — une tablette dégagée tôt est relevée tôt, donc tarifée au débit du début, donc bon marché pour toute la partie. C'est PT6 en miniature, et aucun garde-fou ne le voyait : `outils/balayage.py` trie désormais aussi sur cette part, plancher à 15 % — **11 % depuis la Fin** (19/10/2026), qui la fait baisser par la seule longueur de la partie : le gisement est fini, la production passive non. **Et le plancher n'a pas suffi : PT10 mesure 1,0 %** (15/09/2026), avec 147 des 148 relevés utiles avant la trente-deuxième minute et un relevé moyen à 1 120 occurrences contre 11 996 en PT9. Le corollaire du 14/09 avait la bonne cause et le mauvais agent : ce n'est pas la vitesse de dégagement qui fixe le prix de la main, c'est **la date des relevés**, et le dégagement n'en est qu'un des deux maîtres. L'autre est le joueur, qui vide le gisement tôt et ne revient pas — ce que le plancher de `balayage.py` ne peut pas voir, puisqu'il mesure un acheteur simulé qui relève tant que c'est rentable. Ne pas régler contre ce chiffre avant PT11, et surtout ne pas toucher `REL_K` : le tarif n'est pas en cause.

10. **La date d'une tablette n'est jamais ajoutée par le jeu.** Chaque tablette porte la sienne dans sa première ligne depuis la première seconde ; `année` ne fait que la rendre lisible, et il faut encore savoir lire le nombre, signe par signe. Corollaire : le rangement chronologique ne réordonne que ce que le joueur sait dater — le reste garde l'ordre de sortie de terre. Ne jamais dater depuis une table externe : la vérité est dans `tb.l[0]`.

11. **Un instrument nommé d'après une méthode philologique doit faire cette méthode.** La Table de fréquences compte les occurrences au survol ; la Concordance rassemble les attestations d'un signe. Sans ça le nom ment, et le jeu redevient un incrémental habillé. Corollaire trouvé en PT8 : **ranger n'est pas rassembler** — l'ordre chronologique ne sert à rien tant que 8 à 57 lignes de registre séparent deux relevés de la même série.

12. **Le dégagement suit la sortie de terre, l'affichage suit le temps.** Sa *vitesse* est `REV_R` (`revCount()`), un exposant mesuré et non choisi : il tire à lui seul la part manuelle des occurrences (règle 9) et la pire tranche d'I6 (règle 2), et il les tire dans le même sens — ralentir améliore les deux. `IDX` (rang dans `ORDRE`) décide de ce qui est visible, l'ordre du DOM décide de ce qu'on lit. Les confondre ferait dégager des tablettes en rangeant. `ranger()` déplace les nœuds existants au lieu de les reconstruire — les jetons relevés et les caches de peinture y survivent.

13. **Le compte de l'arbre n'est pas le compte des glyphes acquis.** Depuis la composition, un signe s'apprend de deux façons : en remontant une branche, ou en le posant soi-même. `nArbre()` compte ce que **l'arbre a rendu** ; `S_.gl.length` compte ce que **le joueur sait**. Tout ce qui mesure une *progression* passe par le premier : la fin de partie, les tablettes dégagées (`revCount()`), l'exposant de la Grammaire (`gramMul()`, qui s'arrête aux branches d'avant l'acte V — règle 24), le gain du recoupement et le compteur du lexique. Tout ce qui mesure une *compréhension* passe par le second, ou par `mesures()` dans le corpus. Les confondre fait avancer le jeu en composant — un composé secret dégagerait une tablette et donnerait 16 % de Grammaire gratuits — et déplace une économie réglée sur neuf playtests. Un test le vérifie (`verifier.py`, section 14) : après composition, `#lexr` affiche toujours « x / 28 » et aucune tablette n'est dégagée. L'inverse vaut pour un composé **d'arbre** (`deux`, `siècle`, `scribe`, `archive`) : posé à la grille, il avance la partie comme s'il avait été acheté.

14. **La grille de composition ne renseigne jamais.** Elle dessine le signe qu'on propose, sans dire s'il existe — l'indice est dans le corpus, où les composés sont dessinés comme composés (règle 4), et nulle part ailleurs. Corollaire trouvé en l'écrivant : une paire juste que le joueur n'a pas les moyens de payer perd quand même ses hypothèses, parce que la gratuité serait un renseignement. La carte de fin ne comptait les compositions que si on en avait tenté, pour ne pas apprendre qu'il y avait quelque chose à trouver ; depuis les deux fins (règle 26) il n'y a plus de carte, et la fin ne compte plus rien.

    **Mais elle ne se tait jamais sur elle-même.** Ce qu'elle cache est l'affaire du corpus ; ses propres règles s'écrivent à l'écran. La palette ne montre que les signes acquis et ne le disait que dans son `aria-label` — le seul endroit qu'un joueur voyant ne lit pas, et le seul retour qualitatif de PT10 ; elle porte son intitulé depuis le 17/09/2026, dans le même caractère que celui du carnet. Un refus, lui, **ne s'explique pas** : « Rien ne vient. » et rien de plus. La phrase qui suivait — « ces deux signes ne se rencontrent nulle part » — était fausse dès que la paire existait, soit cinq des six tentatives de PT10. Quand le jeu ne peut pas dire vrai sans renseigner, il en dit moins ; il n'en dit jamais autre chose. Même famille que les règles 18 et 20.

    **Ce que la palette protège n'est pas la taille du lexique**, qui est publique — le sous-titre affiche « 43 glyphes sur 45 » et le panneau lexique rend les quarante-trois tracés de l'arbre dès t = 0, trente-six à 28 % d'opacité — **c'est l'existence de signes hors de l'arbre.** Ne jamais y afficher les pions non acquis, même grisés : le lexique peut tout montrer parce que son bloc « Composés » est caché en entier tant qu'on n'a rien trouvé, une absence qu'on ne voit pas ; la palette est une seule rangée, et le pion de trop qui y apparaîtrait le jour d'un composé secret ferait en comptant ce que la règle 4 confie à la lecture.

    **Les trois signaux qui distinguent quand même une paire fausse d'une paire juste impayable — l'entrée au carnet, le prix de la suivante qui monte, la paire inretentable — sont connus et assumés** (17/09/2026). Le seul levier qui les refermerait est le prix : **ne pas indexer `compCost()` sur `S_.comp`**, il ferait payer plus cher celui qui a lu juste, l'inverse exact de « lire coûte moins cher que chercher » (design doc §8, risque R3). Ils sont le prix de « on ne punit pas une trouvaille qu'on ne peut pas payer » — et, accessoirement, la seule mémoire d'une recette trouvée et impayable.

15. **Une recette n'existe que si sa cible et ses deux parties sont au lexique.** `COMP` dit comment un signe se *dessine* — ses valeurs sont des clés de tracé, et la branche Nombre y paraît sous ses chiffres (`u1` pour ⟨un⟩). `RECETTES` en dérive ce qu'on peut *poser*, via `ALIAS`, et filtre. Sans ce filtre la grille offre `vingt`, retiré du lexique mais toujours dessinable, et `dernière-année` composée avec un `finir` qui n'existe pas. Ne jamais recopier `COMP` à la main : les recettes des actes IV et V s'ouvriront d'elles-mêmes quand leurs glyphes entreront dans `GL`.

16. **Le dernier signe de l'arbre ne porte pas d'effet chiffré, et l'effacement attend qu'on l'ait lu.** Les deux tiennent au même fait : `nArbre() === NGL` clôt la partie à l'instant de ce dernier achat. Un multiplicateur posé là n'a pas le temps de rendre — mesuré sur `les-lecteurs`, cinq effets possibles à quatre prix et trois cadences donnent la même durée à la décimale près, et le ×1,5 à la table d'`archive`, qui occupait cette place au lot précédent, ne déplaçait rien non plus. Et `showEnd()`, appelée dans la foulée d'`acheterGl()`, couvrait d'un écran de statistiques la tablette que ce dernier signe venait justement de rendre lisible. La fin est donc **armée** et non montrée (`finArmer()` / `finRegarder()` dans `economie.js`) : elle vient quand `tabletteVisible()` rencontre une des tablettes retenues à l'armement, jamais avant six secondes, jamais après quatre-vingt-dix. `S_.done` est posé à l'achat, lui : la production s'arrête pendant cette lecture. Depuis les deux fins (règle 26), ce qui vient n'est plus une carte mais l'effacement (`finEffacer()`) ; la règle est la même, et elle vaut davantage pour un effacement qui emporte le texte. Ne pas le lancer depuis `acheterGl()` — cinq tests le vérifient. **Depuis VOIX-1 (14/10/2026), ce dernier signe est ⟨nous-fûmes⟩** — une seule attestation, le dernier mot du corpus — et la carte attend la tablette 30. `les-lecteurs`, passé au milieu de l'arbre, a été remesuré comme la règle le demandait : un ×1,5 à la grammaire raccourcirait l'acte IV de six à huit minutes, les trois autres instruments ne déplacent presque rien. Il reste sans effet. **Depuis GRAINE-1 (19/10/2026), c'est ⟨devenir-lecture⟩** : le lexique ne l'offre que quand les quarante-deux autres sont lus, et l'effacement attend la tablette 27, sa seule attestation. Mais la grille le donne dès qu'on a ⟨lire⟩ et ⟨devenir⟩ — composé tôt, il compte dans l'arbre sans rien fermer, et c'est le dernier signe acheté qui clôt la partie, quel qu'il soit (règle 25).

17. **Un mot français affiché passe par `motDe()`, et rien de ce que le jeu écrit ne présuppose une lecture.** Neuf des onze signes ambigus sont posés depuis le 15/09/2026 : 1 726 attestations sur 3 838 — 45 % du corpus — changent de mot selon ce que le joueur a tranché. Le corpus était la partie facile. Le piège est ailleurs : **partout où le jeu répète un mot de son côté**, il peut se contredire, et une contradiction du jeu avec lui-même est un renseignement (R3, règle 14). Quatre lignes d'effet le faisaient — « chaque tablette porte sa *date* » s'affichait **avant** le choix entre ⟨année⟩ et ⟨soleil⟩ — ainsi que l'infobulle de la barre, la citation de la carte de fin, et les lignes de journal des composés, que `docs/corpus.md` §7.2 ne donnait pas. Tout texte neuf qui nomme un signe doit tenir sous les deux lectures, ou passer par `motDe()`/`logDe()`. Résidu connu et assumé : les effets d'⟨avant⟩ et ⟨après⟩ disent « dans l'ordre du temps » — à traiter avec MOD-2.

    **La prime de 25 % est silencieuse, et c'est ce qui fait tenir le système.** Les deux lectures portent le même tracé, le même prix, la même ligne d'effet : deux chiffres différents feraient de la prime un oracle (« prends toujours le plus gros ») et les onze signes deviendraient onze péages. Elle porte sur le **bonus** et non sur l'instrument (+30 % → +37,5 %) ; un signe qui ne multiplie rien ne gagne rien, et on ne lui invente pas un effet pour porter la prime — quatre des neuf sont dans ce cas. Conséquence mesurée et meilleure que prévu : **la prime ne décide rien à l'achat, elle mord à la révision** (CONTR-2). L'optimum local du design doc §8 n'est pas dans le choix, il est dans le refus de le défaire. Ne pas non plus marquer les signes ambigus dans l'arbre : ils se distinguent au clic, et nulle part avant.

18. **Le doute ne dit jamais l'erreur, il dit l'aveuglement.** Le jeu connaît la vérité et n'a pas le droit de s'en servir : un degré de doute calculé sur la justesse serait l'oracle que la règle 17 refuse. Et le corpus est le même sous les deux lectures, donc **tout doute honnête est identique pour la juste et pour la fausse** — c'est la contrainte, et c'est elle qui a donné la réponse. `douteCalc()` mesure ce qui produit l'erreur : moitié « quelle part des attestations du signe était sortie de terre quand le joueur a tranché », moitié « qu'en avait-il fait » — une concordance sur ce signe vaut plein (règle 11), un recoupement moitié, n'avoir rien fait ne vaut rien même avec les trente tablettes sous les yeux. **Regarder après coup ne le baisse pas** : on ne dé-aveugle pas une décision prise, et sans cette règle le doute serait une jauge qu'on vide en promenant la souris. Seule la révision le recalcule, parce qu'elle seule re-décide — la lecture devient le chemin vers la révision, pas son substitut. Un premier réglage multiplicatif a été jeté : il tassait les neuf signes entre 83 et 99 %, vrai et inutile.

    **La révision ne rend aucun verdict.** Elle coûte, elle repeint le corpus, et c'est au joueur de lire ce qui en sort — « vingt mesures de poussière à la maison 1 » n'a pas de sens, et c'est la seule chose qui le lui dira. Le **bonus rétroactif** du design doc §8 n'est donc pas implémenté et ce n'est pas un oubli : un bonus visible est un verdict, et payer pour voir apparaître une récompense, c'est acheter la réponse au lieu de la lire. Il attend CONTR-1, où il se paiera en dette effacée. Ce que la révision coûte, en revanche, est réel et invisible : reprendre la lecture juste **retire les 25 % de prime** d'AMB-1.

    **Corollaire trouvé par un test, et qui vaut hors de ce lot : un état dérivable ne se stocke pas, surtout quand rien ne le lit.** La dette d'AMB-3, tenue en solde, dérivait dès qu'une lecture changeait autrement que par le chemin prévu — et un solde faux sur un chiffre que personne n'affiche ne se manifeste jamais, jusqu'à CONTR-1 qui en fera son unique intrant. Elle se déduit désormais des lectures (`dette()`).

19. **La contradiction se solde à l'ouverture du doute, et le passage qui refuse ne désigne rien.** Le design doc place la première contradiction à la fin de l'acte III ; dans le prototype, cette fin *est* le dernier achat de l'arbre, qui clôt la partie (règle 16) — la sanction n'aurait pas une seconde pour mordre. Et `année`, seul autre franchissement identifiable, la déclencherait **trente minutes avant que `peut-être` n'existe** : sans remède ni explication, le joueur lirait un bug et non une sanction. Règle générale : **elle s'évalue à chaque franchissement d'acte à partir de `peut-être`.** Avant lui le jeu n'admet pas qu'une lecture puisse être fausse ; il ne peut pas en faire payer le prix. Levée, elle ne se réarme pas d'elle-même — on ne ballotte pas un joueur entre deux états sur un chiffre qu'il ne voit pas — et seul le franchissement suivant la re-solde. **Depuis VOIX-1, le prototype en connaît un second : l'entrée dans l'acte IV**, au premier signe de la Personne (`franchit()` dans `economie.js`, `ACTE` dans `lexique.js`). C'est là que passent enfin au solde les lectures tranchées après `peut-être` — `il-faut`, et ce que l'Élève a lu à la place du joueur.

    **Le passage retenu est fixe** — tablette 17, ligne 4 — et il le restera. Le choisir d'après les signes mal lus le ferait pointer exactement ce qu'il faut réviser : l'oracle le plus gros que ce jeu puisse offrir (règles 17 et 18). Le choisir d'après la densité d'ambiguïté donne une ligne de registre générée, identique à quarante autres. Et la tablette 21 a été écartée exprès : y attirer l'œil à la 77ᵉ minute, pour les seuls joueurs endettés, déséquilibrerait la reconnaissance de l'abécédaire à l'acte IV. Corollaire qu'aucun choix de ligne ne supprime : le joueur peut croire que le passage contient ses erreurs, **donc la ligne de journal dit le contraire en toutes lettres**. C'est le seul endroit où le jeu parle de lui-même, et CONTR-1 l'exige — l'état est affiché sans ambiguïté. Il nomme la sanction et sa sortie, jamais un signe.

    **R2 : on ne perd que du débit.** Le passage refuse de se *résoudre*, il ne devient pas illisible : `tokLisible`, `pctTablette`, `mesures()` et le compteur du lexique ignorent le refus, et un test le vérifie en basculant la sanction sans rien acheter. Le joueur sait ces mots ; c'est le texte qui se retient, pas sa compréhension qui recule.

    **Combien de débit : la moitié à l'acte III, un cinquième aux actes IV et V, et les Élèves attendent** (ECO-3, 20/10/2026, règle 31). `CONTR_DIV_TARD` et `elvMul()` dans `economie.js`. Le bandeau dit l'un et l'autre — « Certitude réduite d'un cinquième, et les élèves attendent » —, jamais un signe ni un coupable.

20. **`faux` ne donne pas le corrigé : il allume les lignes où la lecture ne se construit pas.** Le §6 et le §10 du design doc disent « affiche rétroactivement les erreurs déjà commises », ce qui se lit comme le corrigé — mais le §11 promet que la relecture de fin surlignera les erreurs « **y compris celles jamais détectées** ». S'il en reste de jamais détectées à la fin, `faux` ne les a pas nommées. Ce qu'il montre est ce que le §8 appelle depuis le premier jour le seul indice fiable : le texte. Il ne remplace pas la lecture, il rend visible ce qu'un lecteur attentif aurait vu.

    **C'est la LIGNE qui s'allume, jamais le jeton.** Marquer le signe fautif le nommerait — l'oracle que les règles 17, 18 et 19 refusent. (Pendant la partie : la relecture, livre fermé, marque le jeton — règle 27.) Une ligne allumée porte quatre ou cinq signes, dont deux ou trois ambigus : elle réduit le champ, elle ne tranche pas. Le panneau dit *combien* de passages ne se construisent pas, jamais lesquels ni pourquoi. Un test le verrouille : zéro jeton marqué, trois signes ambigus sur la ligne.

    **Trois décisions prises séparément tombent juste d'un coup, et c'est ce qui valide le choix.** Les paires réparantes n'allument rien — « vingt mesures de poussière à la tombe 1 » se tient — donc le §7.3 (« le texte ne trahit rien ») devient mécanique, par le champ `sauf` de `RUPTURES`, au lieu de rester une intention. Les quatre signes sans rupture n'allument rien — `lire` et `il-faut` par conception, `eau` et `année` faute de rupture textuelle (§7.4) — et ce sont exactement les erreurs « jamais détectées » du §11. Et **se tromper sur les neuf n'allume que trois lignes sur cinq** : mal lire partout cache deux de ses propres erreurs.

    Une seule ligne par signe, la plus précoce : ⟨ne-pas⟩ casse sur `sinon` cent trente et une fois, en allumer cent trente et une noierait le signal, et AMB-4 demande « un endroit précis du corpus ».

21. **L'erreur de l'Élève est une lecture, et son taux ne s'affiche nulle part.** Septième instrument, premier *ambivalent* : il ajoute 5 % par tête à ce que rendent les cinq autres — pas au relevé, que son tarif indexe déjà sur le débit (règle 9) — et **dès le premier, ce n'est plus le joueur qui tranche un signe ambigu**. Le joueur paie toujours le signe en Certitude : la règle du §4 tient, l'Élève n'achète rien. Faux `1 − 0,85ⁿ` fois : 15 % à un, 48 % à quatre, 68 % à sept.

    **Rien de neuf dans la comptabilité.** La lecture de l'Élève va dans `S_.lect` comme celle du joueur ; la dette s'en déduit, la prime silencieuse s'y applique, la contradiction s'en solde, `faux` en allume les lignes. Ne jamais lui ouvrir un solde à part (règle 18, corollaire).

    **Le doute d'un signe qu'il a lu vaut cent, à un Élève comme à sept.** Le doute dit l'aveuglement du joueur au moment de trancher, et il n'a rien tranché. L'indexer sur le taux d'erreur ferait de ce chiffre un oracle : à cent, il reste identique pour la lecture juste et pour la fausse. La révision, elle, reste au joueur — elle rouvre les deux lectures et recalcule son doute à lui.

    **La ligne de l'instrument dit « déchiffre seul » et ne chiffre que le multiplicateur.** Que ce soit parfois faux se découvre dans le texte (règle 17). Une ligne de journal dit *qui* a lu, jamais *quoi* : sans elle, l'absence de la fenêtre des deux mots se lirait comme une panne. Le dé se jette à l'achat, jamais avant — tiré d'avance, il se lirait dans la sauvegarde.

    **Un multiplicateur global ne déplace que la durée.** Mesuré sur 36 combinaisons : ni la pire tranche d'I6 (elle est à 20–30′, l'Élève ouvre à la 48ᵉ minute) ni l'écart max ne bougent. Trois constantes pour deux réglages — de combien il raccourcit (`ELV_P`), combien on en empile (le taux `r` de son prix, encore la leçon de `REC_R`) — et une contrainte : à +8 % par tête, sept Élèves qui lisent tout faux finissent avant le joueur qui n'en a aucun, et il n'y a plus d'arbitrage.

    **Depuis ECO-3 (20/10/2026), c'est la contradiction qui tient cette contrainte, plus le prix seul** : adoucie aux actes IV et V, elle laissait sept à neuf Élèves qui lisent tout faux finir douze minutes avant le joueur sans Élève qui lit juste. Tant qu'elle court, les Élèves ne rendent plus leur bonus (`elvMul()`) — ils tranchent toujours à l'achat, c'est leur bonus qui attend. Ils finissent alors **seize minutes après** lui. La suspension ne regarde pas qui a mal lu : elle vaut pour une dette du joueur comme pour la leur (règle 19).

22. **La clé de sauvegarde ne change plus ; ce qui change de sens se migre.** `KEY` vaut `langue-morte-partie` depuis LIV-3 (19/10/2026) et la version est écrite dans la sauvegarde (`v`). Elle avait déjà changé une fois, et toutes les parties en cours avaient été perdues. Un champ **ajouté** ne demande rien : `fresh()` le donne à toute partie qui ne l'a pas, un niveau plus bas compris (`fusionner()`) — **un instrument neuf s'écrit dans `fresh()` et nulle part ailleurs**. Un champ qui change de **sens**, de nom ou de forme, un signe qui quitte le lexique ou change d'identifiant, demande une migration ajoutée à la fin de `MIGRATIONS`, jamais retirée ; la version se compte sur cette liste (`versionSauvegarde()`), elle ne se règle pas. Une sauvegarde que le jeu ne sait pas lire — plus récente que lui, ou dont la migration casse — ne se charge pas et **ne s'écrase pas**, ni par la sauvegarde automatique ni par « recommencer ». **La première migration est écrite, celle de FIN-2** (19/10/2026, version 2) : une partie `done` d'avant les deux fins est achevée, il n'y avait pas d'autre façon de finir. `fin` est un champ ajouté, mais sa valeur neuve (« elle court ») est fausse pour une partie déjà finie — c'est ce qui distingue un champ qui demande une migration d'un champ que `fresh()` suffit à donner. Sans elle, la règle qui rouvre une partie que l'arbre a dépassée rouvrirait aussi une partie interrompue, qui a un signe de moins par définition ; elle lit désormais `fin`, et non la taille de l'arbre. `verifier.py`, sections 20 et 27.

23. **Le verrou du passé est dans la traduction, jamais dans le texte.** ⟨nous-fûmes⟩ « verrouille le récit au passé, y compris les passages déjà lus » (design doc §6), et c'est la seule exception à « la couche d'affichage n'ajoute rien » (`docs/corpus.md` §1). Tranché à l'écran par l'auteur le 14/10/2026. Il se décide **segment par segment** entre deux « · », une fois pour toutes à la construction du corpus (`auPasseLigne()` dans `rendu.js`) : un segment adressé à ⟨toi⟩ reste au présent, parce que le lecteur est vivant ; un segment sans sujet hérite de celui d'avant ; ⟨il-faut⟩ devient « il-fallait » et garde l'infinitif qui le suit ; les autres verbes passent au participe. La table `PASSE` est indexée par le **mot affiché**, pas par le signe, pour tenir sous les deux lectures sans une ligne de plus (règle 17). Le lexique, l'infobulle et la concordance gardent l'infinitif : c'est le récit qui passe au passé, pas le dictionnaire. Un verbe neuf (acte V) s'ajoute à `VERBES` et à `PASSE`, jamais au texte.

24. **Une question est une condition, et la réponse est gravée ; ce qui déborde de 9 999 devient question.** Tranché par l'auteur le 19/10/2026 sur une note mesurée (`docs/note-questions.md`, option 3 avec le gel). La langue n'a pas d'interrogatif : le joueur pose ⟨si⟩ suivi de signes qu'il sait lire, et la réponse est ce que le corpus a gravé après cette condition, dans toutes les tablettes (`QUESTIONS`, lue dans `CORPUS` au chargement, nombres ôtés de la condition — quinze conditions). **Jamais un mot écrit pour l'occasion** (R8) ; un test vérifie que chaque réponse finit une ligne gravée. Le reste tient aux règles d'avant, et c'est ce qui les rend sûres :

    - la réponse s'écrit avec les lectures du joueur (`motDe()`) et ne dépend jamais de leur justesse — une lecture fausse peut la rendre absurde, c'est le texte qui parle (règles 17 et 20) ;
    - poser une question ne touche pas au degré de doute : c'est le texte qui montre, pas le joueur qui rassemble (règle 18, même décision que le repli de VOIX-2) ;
    - la palette ne montre que les signes acquis (règle 14), et le panneau écrit sa propre règle — d'où viennent les questions —, rien sur ce qu'il y a à demander ;
    - une condition gravée nulle part ne coûte rien (« Le texte ne dit rien. ») ; **sans question en main, rien ne se pose**, gravé ou non : refuser seulement les conditions gravées dirait lesquelles le sont.

    **La Certitude s'arrête à 9 999** (`C_MAX`, `gagnerC()`) : I1 cesse d'être une contrainte sur les prix et devient une règle du jeu. À partir de ⟨toi⟩, le surplus remplit la question suivante — 4 000 chacune, douze sur la partie —, et une question qui obtient une réponse en consomme une. Les questions en main se déduisent (`questionsEnMain()`, règle 18 corollaire). Avant ⟨toi⟩ le surplus est perdu, et **la nuit ne remplit jamais une question** : elle porte la Certitude au plafond, plus haut non — elle rapportait avant ça soixante-six à quatre-vingt-neuf mille Certitude à ⟨nous⟩, deux fois toute la Personne. Le plafond ne retire rien : une Certitude déjà au-dessus, d'une partie d'avant, reste où elle est (R2). Corollaire assumé : la neuvième révision coûte 10 308 C et devient impossible.

    **Ce que la réponse ouvre** : un signe marqué `rep` dans `GL` ne s'offre au lexique qu'une fois qu'une réponse l'a porté (`offert()`, et `ouvertsParReponse()`, déduit des conditions posées). La question donne l'accès, jamais la compréhension — le signe se paie en Certitude comme les autres (design doc §4). Ce sont ⟨finir⟩, ⟨devenir⟩ et ⟨germer⟩, les trois mots de la Fin qui suivent un « si » (GRAINE-1). La grille, elle, ne passe pas par le lexique : ⟨germer⟩ est ⟨semence⟩ sur ⟨devenir⟩, et qui le voit fait l'économie de sa question (règle 25).

    **Et la Grammaire gèle aux mots de la fin** (`nGrammaire()`) : elle compte l'arbre moins les branches de l'acte V — la grammaire est complète une fois la Personne connue, et c'est l'ordre que la tablette 28 donne au programme. Mesuré sur un acte V provisoire : trois questions à 4 000 et ce gel tiennent I4 avec et sans Élèves (28,2 et 40,3 min d'acte V) ; **aucun des deux seul ne le fait**. Elle gèle depuis l'entrée de la Fin. `verifier.py`, section 29.

25. **À l'acte V, le prix ne porte plus le rythme ; c'est le lexique qui garde les portes, et la grille passe outre.** Tranché le 19/10/2026 (GRAINE-1). Les sept signes de la Fin sont tous au plafond, 9 999, et c'est une mesure : à ce prix ⟨semence⟩ tombe juste après ⟨nous-fûmes⟩ et l'acte V vient entier après l'acte IV ; ce qui l'espace, ce sont les trois questions de la règle 24 et le gel de la Grammaire. La chaîne alterne les mots qui attendent une réponse et ceux qui n'attendent que leur prix — ⟨semence⟩, ⟨finir⟩, ⟨le-dernier⟩, ⟨devenir⟩, ⟨notre-fin⟩, ⟨germer⟩, ⟨devenir-lecture⟩ —, parce que deux questions de suite feraient deux longues attentes et deux prix une rafale.

    **`offert()` est la seule porte, et elle est au lexique** (`economie.js`) : un mot `rep` attend sa réponse, le signe `dernier` attend que tout le reste de l'arbre soit lu. `acheterGl` ne vérifie que le prix, comme il n'a jamais vérifié l'ordre des chaînes. La grille donne donc un composé dès qu'on en a les parties (règle 15) : ⟨germer⟩ sans sa question, ⟨devenir-lecture⟩ avant tout le reste — « griller la révélation de vitesse » (design doc §6), voulu. Une carte en tête de sa chaîne qui attend autre chose que la Certitude **dit sa règle** — « le texte le donnera à qui l'interroge », « il vient quand tout le reste est lu » — et rien de ce qu'il faut demander (règle 14).

    **« notre-fin · ne-pas » ne se tranche jamais** : « notre fin : non », ou « pas notre fin ». Ni le corpus, télégraphique, ni la ligne de journal ne choisissent, et la ligne ne dit pas non plus qu'il y a à choisir. Et **un texte écrit d'avance se relit quand il entre en jeu** : la ligne fausse de ⟨semence⟩ parlait de « tombes », c'est-à-dire de ⟨maison⟩ mal lu — une lecture que le joueur n'a peut-être pas faite (règle 17). `verifier.py`, section 30.

26. **Deux fins, et aucune n'est la bonne.** Tranché par l'auteur le 19/10/2026 (FIN-1 + FIN-2), sur trois questions. Le dernier signe de l'arbre, quel qu'il soit, ne s'achète pas d'un clic ni ne se pose d'un geste : au lexique comme à la grille, il ouvre une fenêtre à deux boutons, **achever** (le lire) et **interrompre** (le laisser non lu) — et seulement quand on peut le payer, sans quoi interrompre serait le repli de celui qui ne peut pas achever, et non un refus (`estDernier()`, `finsOuvrir()`). Même habit pour les deux, ordre tiré au sort comme celui des deux lectures, et la fenêtre écrit sa règle — « lu ou non, la partie s'arrête là » — sans quoi « le laisser non lu » se lirait « pas maintenant » (règle 14, même famille). Un dernier signe ambigu ouvre ensuite ses deux lectures ; qui a composé ⟨devenir-lecture⟩ tôt finit sur un autre mot (règle 25).

    **Achever efface ; interrompre fige.** Achever : l'effacement attend la lecture (règle 16), puis l'interface s'en va dans l'ordre — compteurs, instruments, panneaux, lexique, cadre du corpus, titre —, le texte glisse au milieu, reste seul, puis s'efface (`finEffacer()`). Interrompre : l'interface s'en va de la même façon, le corpus reste, figé, et **ne se reprend jamais**, pas même au chargement (`finFiger()`, `S_.fin`). Ce qui reste ensuite est « recommencer », et « relire » après avoir achevé (règle 27). **Plus de carte, plus de statistiques** : « signes déchiffrés 87 % » était un score, et le design doc §11 n'en veut aucun ; le journal d'actions les garde pour l'auteur. La barre hors jeu reste, parce que c'est à la fin qu'on exporte le journal (PT5). Les durées de `FIN_EFF` sont des choix de mise en scène, pas des mesures : c'est au playtest de les dire.

    **« Entièrement en français » ne vaut que pour ce que le joueur a lu.** Les noms propres ne se déchiffrent jamais, et un composé secret que le joueur n'a pas trouvé reste en signes : l'effacement montre le corpus tel qu'il a été lu, il ne le corrige pas. Tout rendre lisible est le travail de la relecture (règle 27), qui s'ouvre sur demande. `verifier.py`, section 6.

27. **La relecture avoue tout, et ne compte rien.** Tranché par l'auteur le 19/10/2026 (FIN-3), sur quatre questions. « relire » ne s'offre qu'après avoir achevé et une fois l'effacement allé au bout (`relire()`, `rendu.js`) : interrompre laisse un signe non lu, et la relecture est celle d'un livre lu jusqu'au bout. Le corpus revient, entier, écrit avec les **lectures justes** — `motSous(id, {})` — et ce sont **les jetons** qui se marquent : pendant la partie la règle 20 l'interdisait parce que ç'aurait été l'oracle, et le livre est fermé. Trois marques, qu'une légende nomme sans rien compter (aucun score) :

    - **mal lu** : la lecture en place à la fin ne donnait pas ce mot — détectée ou non, révisable ou non, composés salis compris (`fautifs()`). C'est là que la paire réparante est enfin avouée, et c'est le seul endroit du jeu (§7.3) ;
    - **mal lu, puis corrigé** : une révision l'avait rendu, et la relecture s'en souvient (`S_.fautes`, qui garde chaque signe lu faux un jour) ;
    - **jamais trouvé** : un composé secret que personne n'a posé — ⟨grenier⟩, le zéro. Ce que la règle 14 protégeait pendant la partie, la relecture le montre : il n'y a plus de partie à protéger.

    Ce qu'on avait lu se lit au survol, et **qui** l'avait lu : « j'avais lu … » ou « un élève avait lu … » (`S_.lusEleve`). Ce n'est pas un solde à part pour l'Élève (règle 21) : la dette, la prime et la contradiction ne lisent que `lect`, et ces deux champs ne se lisent qu'ici. Le passage qui refuse et les lignes de `faux` s'éteignent : le texte juste se construit partout. Les noms propres restent en signes. Une partie d'avant ce lot reçoit `fautes` et `lusEleve` vides — sa relecture montre les fautes encore en place, toutes attribuées au joueur ; aucune migration, parce qu'un historique absent n'est pas un historique faux. **Pour le playtest : l'entretien précède « relire »** — la relecture répond à « combien de lectures fausses », à « a-t-on remarqué qu'on choisissait » et à « à qui attribue-t-on un mot faux ». `verifier.py`, section 6.

28. **Le Lecteur ne dit pas ce qu'il est : on le voit lire.** Tranché par l'auteur le 19/10/2026 (GRAINE-2), sur deux questions mesurées. Neuvième instrument, ouvert par ⟨semence⟩, payé en occurrences comme les huit autres (règle structurante du §4) — et le seul sans nom français ni ligne d'effet : son nom est un signe du corpus, ⟨devenir-lecture⟩ (`nomLecteur()`), qu'on ne lit qu'au dernier achat, et qu'on lit alors avec sa propre lecture (règle 17). Il **ne produit rien** : il lit le corpus tout seul, une tablette par minute et par Lecteur, dans l'ordre des numéros, sous terre compris, et chaque tablette lue verse 300 à la question suivante — trente tablettes, 9 000 au plus (`lireCorpus()`, `LEC_V`, `LEC_Q`). Rien ne le décrit ; il se voit faire — un trait sur la tablette lue, dans la barre et au bord du texte, et la ligne qu'il lit qui s'éclaire (`peindreLecteur()`) — comme le compteur se voyait monter à l'acte I. Ce qu'il est, c'est la tablette 27 qui le dit : « tablette · devenir-lecture », la ligne même que l'effacement attend (règle 16). Qui compose ⟨devenir-lecture⟩ tôt lit son nom tôt (règle 25).

    **Il ne lit pas la nuit** : `tick` ne tourne pas hors ligne, et la nuit ne remplit jamais une question (règle 24). Ce que le Lecteur verse passe par `nourrirQuestion()`, le même chemin que le surplus ; il n'a pas de compte à lui.

    **Ce qu'il fait au rythme, mesuré** (`outils/sim.py`) : il comble les attentes de question, et rien d'autre. L'acte V passe de 28,2 à **25,6 min** avec Élèves et de 40,3 à **36,3** sans ; le pire trou sans Élève, de 7,2 à **5,8 min** — I4 tient mieux. Le prix (×2 par Lecteur) en laisse trois à l'acheteur. **Réserve écrite** : avec Élèves, l'acte V tombe à 3,7 min par signe, sous les quatre d'I4 — il y était tout juste à 4,0. **Tranchée le 20/10/2026 (ECO-3, règle 31)** : la borne basse d'I4 se mesure sur le joueur sans Élève, et le Lecteur n'y est pour rien — à un prix qui triple au lieu de doubler, l'acte V ne bouge pas d'un dixième. `verifier.py`, section 31.

29. **Le Corpus jumeau est une copie, et il rend la main au corpus.** Tranché par l'auteur le 19/10/2026 (VOIX-4), sur deux questions mesurées. « Une deuxième inscription est trouvée » (design doc §5) : pas un bilingue — la fiction n'en a pas —, une **copie**, celle que la tablette 23 annonçait : « si copier 100 · un devenir ». Le même texte, signe pour signe, donc rien de neuf à lire et tout à relever de nouveau. Huitième instrument, ouvert par ⟨nous⟩, payé en occurrences, **un seul exemplaire** (`max`, `insPlein()`). Chaque tablette de la copie a **la moitié** du gisement de l'original (`JUM_F`, `GIS_COPIE`) et **son propre tarif**, figé au premier relevé qu'on y fait (`S_.relJ`, `S_.prixJ`) — la règle 9 appliquée à la copie, donc au débit de l'acte IV. Le relevé va à l'original tant qu'il en reste (`relever()` rend `'neuf'`, `'copie'` ou `'plancher'`). La barre rallume les tablettes vidées, l'infobulle dit « copie intacte », un jeton relevé sur les deux porte une marque plus forte, et la ligne de journal ne nomme aucun signe (règle 17).

    **Ce que ça fait à la main, mesuré** (`outils/sim.py`) : la part manuelle des occurrences passe de 17,3 à **26–33 %** avec Élèves (26 à 5 clics par minute, 33 à 15 et 40) et de 13,7 à **26 %** sans, sous le plafond de 40 % ; la partie raccourcit d'une à trois minutes ; I4 ne bouge pas. C'est la première fois depuis PT10 qu'un mécanisme ramène le joueur dans le corpus après la quarantième minute — mais ce n'est **pas** un réglage contre la mesure de PT10 (règle 9) : `REL_K` ne bouge pas, et la branche n'est pas celle que PT11 jouera. **Le journal d'actions dit lequel des deux gisements a payé** (« · copie ») : sans ça, `depouiller.py` ne pourrait pas rejouer le tarif de la copie, qui ne s'écrit nulle part ailleurs. `verifier.py`, section 32.

30. **Au million, les zéros sont les leurs ; ⟨zéro⟩ les rend.** Tranché par l'auteur le 20/10/2026 (VOIX-5, invariant I2), sur trois questions. Une fois l'acte IV ouvert — un signe d'arbre de l'acte IV ou V, jamais un composé secret (`acteIV()`, règle 13) —, tout nombre qui passe par `big()` et atteint 1 000 000 garde **trois chiffres au joueur**, et les zéros qui suivent s'écrivent du tracé de ⟨zéro⟩, ⟨ne-pas⟩ sur ⟨un⟩ (`grandNombre()`, règle 4) : 2 345 678 s'écrit « 234 » et quatre zéros, 1 000 000 « 1 » et six — **un zéro de queue n'est jamais un chiffre au joueur**. Tronqué et non arrondi, comme `big()` : un nombre à lui ne s'affiche jamais plus grand qu'il n'est. Compteurs et coûts passent par la même porte, dans la couleur du nombre et non dans celle des glyphes inertes ; sous le million, la notation compacte de ⟨cent⟩ ne bouge pas. La largeur dit l'ordre de grandeur, et on la déchiffre en la regardant monter — le « premier plaisir du jeu » de l'acte I (design doc §10), rendu une seconde fois à qui avait cessé de regarder ses compteurs.

    **⟨zéro⟩, posé à la grille, la déchiffre** : la notation compacte revient (« 2,35 M »), ce que le design doc §7 promettait au zéro et que COMP-3 avait laissé à ⟨cent⟩ faute d'un moment où le donner. C'est une compréhension, donc `has('lan')` et non l'arbre (règle 13). Ses deux parties sont en main vers la soixantième minute ; posé avant l'acte IV, il fait qu'on ne perd jamais rien, et qui ne le compose pas lit encore en comptant. Sa ligne d'effet le dit (« les registres vides et mes grands nombres passent en chiffres ») : la règle 3 veut que chaque porte s'annonce. **Le seuil est une règle, pas une mesure** : le simulateur n'affiche rien au million avant ⟨nous⟩, mais un joueur qui thésaurise le pourrait — I2 tient par `acteIV()`, pas par l'économie.

    **Ce que ça ne renseigne pas** (règle 14) : le tracé du zéro est sous les yeux du joueur depuis la première seconde — ses compteurs vides, onze zéros du corpus — et la palette ne le montre toujours pas tant qu'il n'est pas posé. **Mesuré** (`outils/sim.py`, affichage seul, rythme inchangé) : avec Élèves, la notation paraît à l'achat même de ⟨nous⟩, sur le prix de l'Élève suivant (88–91 min), et le stock d'occurrences la prend à 90–97 ; sans Élève, à 97–102, le stock à 98–106. Qui ne compose jamais ⟨zéro⟩ joue **40 à 42 minutes** sans lire ses nombres avec Élèves, **55 à 56** sans — le tiers de la partie. Rien ne dépasse cinq millions avant la fin : le 10¹⁰ du design doc n'est jamais affiché, et seule la tranche du million existe dans le prototype. Le journal d'actions date la première fois (`zeros`), et `depouiller.py` en tire le temps passé sans lire. `verifier.py`, section 33.


31. **I4 : la borne haute vaut pour tous les joueurs, la borne basse pour celui qui n'a pas d'Élève ; et la sanction ne la casse plus.** Tranché par l'auteur le 20/10/2026 (ECO-3), sur deux questions mesurées. « Un signe toutes les 4 à 6 min en moyenne ; jamais plus de 8 min sans déblocage » se lit par acte depuis l'acte IV, et il avait deux trous.

    **Le premier : avec Élèves, l'acte V tient 3,45 à 3,58 min par signe** — et l'acte IV 3,0 à 3,2 depuis VOIX-1. **On l'accepte, et la borne basse se mesure sur le joueur sans Élève** (4,2–4,4 à l'acte IV, 5,0–5,1 au V : elle tient). L'Élève est l'instrument qui achète du temps — « un multiplicateur global ne déplace que la durée » (règle 21) — et 3,5 min n'est pas une rafale. Mesuré : aucun levier de prix ne ramène l'acte IV à 4 ; seul un plafond à cinq Élèves ramène l'acte V à 4,0, et un plafond dur sur un instrument que la règle 21 règle par son prix ne vaut pas un demi-point. Le prix des questions (6 000) n'y monte qu'à 3,8 et creuse un trou de 7,5 min sans Élève ; un Lecteur dont le prix triple au lieu de doubler, ou un Élève gelé à l'entrée de l'acte V, ne déplacent rien. L'acheteur en empile neuf, et non plus les sept de la règle 21 : ce sont les occurrences des actes IV et V, pas le Corpus jumeau (neuf aussi sans lui).

    **Le second : la contradiction, chez qui ne révise jamais.** Le ÷2 de CONTR-1 coûtait onze minutes quand la partie s'arrêtait à l'acte III, parce que les occurrences portaient encore une part du rythme. Aux actes IV et V tout se paie en Certitude au plafond, et il doublait tout ce qui restait : +60 à +85 min, huit à onze minutes d'attente **par signe** sur deux actes — pas seulement « avant ⟨finir⟩ ». PT10 a montré que ce joueur existe : la contradiction s'y est déclenchée, et il n'a fait aucune révision. **La sanction ne divise plus que par 1,25 une fois l'acte IV ouvert (`CONTR_DIV_TARD`, `acteIV()`), et les Élèves ne rendent plus leur bonus tant qu'elle court (`elvMul()`).** Les deux vont ensemble : le diviseur seul faisait tenir I4 mais cassait l'arbitrage de la règle 21 — sept à neuf Élèves qui lisent tout faux finissaient douze minutes avant le joueur sans Élève qui lit juste —, et une lamelle seulement (prix des Élèves ×2,5, diviseur 1,35–1,4, déjà à 8,0 min) tenait les deux. Mesuré, joueur qui ne révise jamais : pire attente **6,7 à 7,4 min** dans les six cas (la paire réparante, toutes fausses, un Élève qui lit faux, des Élèves qui lisent faux, le doute à cinq puis ⟨il-faut⟩, la paire réparante avec Élèves), 4,8 à 6,1 min par signe ; la paire réparante coûte **+23 min** (176,8–180,7) au lieu de +60 — 15 % de la partie, contre 12 % à l'acte III ; les Élèves qui lisent faux finissent **seize minutes après** le joueur sans Élève. Les parties sans contradiction ne bougent pas d'un dixième, et `balayage.py`, qui la désarme, non plus. `verifier.py`, section 34.

---

## Ce qui a été tranché

- **ECO-3, 20/10/2026 : la sanction ÷1,25 aux actes IV et V avec l'Élève suspendu, et la borne basse d'I4 mesurée sans Élève.** Deux questions posées à l'auteur, mesurées. Pour la contradiction (contre : ÷1,25 seul, qui faisait tenir I4 mais laissait des Élèves qui lisent tout faux finir avant le joueur sans Élève ; ou garder ÷2 et n'exiger I4 que de qui révise — le joueur qui révise retrouve bien la durée d'une lecture parfaite, mais celui de PT10 ne l'a pas fait). Pour l'acte V trop rapide avec Élèves (contre : ramener les Élèves à sept, croissance 1,8 → 2,2, qui rétrécit le trou sans le fermer ; ou un plafond à cinq Élèves, seul levier qui atteint 4). Voir règle 31.
- **I2, 20/10/2026 : les zéros sont les leurs, ⟨zéro⟩ les rend, au million et pas avant ⟨nous⟩.** Trois questions posées à l'auteur, la troisième mesurée. Trois chiffres au joueur et les zéros qui suivent dessinés en ⟨zéro⟩ (contre : une mantisse et un exposant en chiffres de la langue morte, plus opaque, et dont seul l'exposant 6 paraît jamais dans le prototype ; ou le million dit « mille mille », que le redoublement de ⟨deux⟩ fait lire 2 000 — une énigme plutôt qu'une notation). ⟨zéro⟩ posé à la grille la déchiffre (contre : une porte garantie à un signe de la Personne, qui lui donnerait un effet sans rapport avec lui ; ou une perte définitive, contraire au « elle se déchiffre ensuite comme le reste » du backlog). Au million, une fois l'acte IV ouvert (contre : à l'entrée de l'acte IV dès 10 000, où c'est l'acte qui décide et non la taille des nombres). Voir règle 30.
- **Le Corpus jumeau, 19/10/2026 : une copie à relever, une seule, à demi-gisement.** Deux questions posées à l'auteur, mesurées. Une copie du corpus dont chaque tablette rouvre un gisement tarifé à l'acte IV (contre : un témoin qui renforce Concordance et Grammaire, qui raccourcissait les actes IV et V de cinq à huit minutes et cassait I4 par le bas ; ou une inscription neuve à écrire, qu'on ne pouvait pas mesurer avant). Un seul exemplaire à demi-gisement (contre : plusieurs d'un tiers, qui sur la sonde rendaient la part de la main à la cadence ; un gisement entier la pousse à 43 %, au-delà du plafond). **La mesure soumise à l'auteur était fausse d'un point de modèle** — la sonde remplaçait le gisement restant au lieu d'y ajouter la copie, et annonçait 25 % indépendants de la cadence ; le simulateur définitif donne 26 à 33 % avec Élèves. Le choix tient sur le plafond de 40 %, pas sur l'indépendance. Voir règle 29.
- **Le Lecteur, 19/10/2026 : il lit seul, et il porte le nom du dernier signe.** Deux questions posées à l'auteur, la première mesurée. Il lit le corpus de lui-même et chaque tablette lue remplit la question suivante (contre : qu'il fasse lire le joueur, chaque tablette ramenée sous les yeux comptant une fois — un geste dans le corpus pour l'acte V, mais que rien ne dit ; ou qu'il ne fasse rien, pris au mot, au risque de se lire comme une panne). Son nom est ⟨devenir-lecture⟩ (contre : ⟨les-lecteurs⟩, lisible depuis l'acte III, ou « tablette lire », dont le sens viendrait de la tablette 27). Voir règle 28.
- **La relecture, 19/10/2026 : toutes les fautes, sur le jeton, avec qui les a faites, et ce qui n'a jamais été trouvé.** Quatre questions posées à l'auteur. Toutes les erreurs de la partie, celles qu'une révision a corrigées à part (contre : seulement celles qui restent) ; le texte juste, l'erreur surlignée et le mot lu au survol (contre : basculer entre les deux livres, qui est une mécanique, ou les deux mots côte à côte, qui double la moitié du corpus chez qui s'est trompé partout) ; l'Élève nommé au survol (contre : une erreur est une erreur) ; les composés secrets lisibles et marqués « jamais trouvé » (contre : lisibles sans marque, ou laissés en signes). Voir règle 27.
- **Les deux fins, 19/10/2026 : le choix se fait à l'achat du dernier signe, rien ne reste à l'écran, et la fin se joue sur le signe qui reste.** Trois questions posées à l'auteur. Interrompre n'est offert qu'à qui peut achever, sans quoi il serait un repli (contre : un second geste sur la carte du lexique, ou une fenêtre qui s'ouvre d'elle-même au quarante-deuxième signe). Ni carte ni statistiques après : un compte rendu chiffré est un score, que le design doc refuse (contre : les garder après l'effacement, ou dans le seul build de développement). Et la fenêtre s'ouvre sur le dernier signe qui manque, quel qu'il soit, au lexique comme à la grille (contre : tenir ⟨devenir-lecture⟩ jusqu'au bout, ce qui revenait sur la décision du même jour de laisser la grille le donner tôt). Voir règle 26.

- **⟨devenir-lecture⟩, 19/10/2026 : il compte dans l'arbre, et le lexique l'offre en dernier.** Le design doc en fait « le dernier signe et la clé de tout », et COMP-4 dit qu'aucune progression ne l'offre. Deux lectures ne tenaient pas : grille seulement, la partie se bloquait à 42 sur 43 pour qui n'y pensait pas ; hors de l'arbre, comme ⟨grenier⟩, il n'était plus le dernier. Le lexique l'offre donc quand les quarante-deux autres sont lus, et la grille le donne avant à qui a ⟨lire⟩ et ⟨devenir⟩. Voir règle 25.
- **Les Questions, 19/10/2026 : ce qui déborde devient question, et la Grammaire gèle aux mots de la fin.** Trois options mesurées sur un acte V provisoire (`docs/note-questions.md`). Une réponse qui se lit seulement fait ce que fait déjà une Concordance sur ⟨si⟩ ; une réponse qui ouvre les mots de la fin avec des questions données ne coûte pas de temps, et l'acte V tient alors 16,7 à 23,7 min avec des écarts qui retombent à 1,4 min — I4 cède dès le troisième signe. Seul le surplus au-delà de 9 999 est un levier sans plafond, puisque le prix d'une question n'est jamais détenu d'un coup ; avec trois questions à 4 000 et le gel, I4 tient avec et sans Élèves. Le gel contredit la lettre du design doc §5 (« croît avec la taille du lexique ») : il est noté là. Voir règle 24.
- **Ce que « l'Élève déchiffre tout seul » veut dire, 12/10/2026 : il tranche à l'achat.** Trois lectures du design doc §5 tenaient. Qu'il **relise ce qui est acquis** écrasait des choix du joueur (R2) et offrait des révisions gratuites à qui n'en prenait qu'un ; qu'il **acquière des signes lui-même** était « acheter de la compréhension avec du volume », ce que la règle structurante du §4 existe pour empêcher, et déplaçait I4, la durée, le dégagement et la Grammaire d'un coup. Reste : le joueur paie, l'Élève lit. Ça ne coûte aucune règle, et l'erreur est une lecture comme une autre. Voir règle 21 et `docs/journal.md`, « L'Élève tranche à ma place ».
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

**Fait** : **actes I à III entiers**, **30 signes d'arbre sur 45**, plus deux composés secrets, corpus complet des 30 tablettes (705 lignes, 3 838 signes), économie réglée sur neuf playtests, numération signe par signe de `zéro` à `mille`, barre de navigation entre tablettes, infobulles, comptage d'occurrences dans le lexique, journal d'actions horodaté, relevé et recoupement dans le corpus avec gisement par tablette, **datation et réordonnancement chronologique**, instrument **Grammaire**, progression **hors ligne**, **grille de composition** avec carnet des tentatives, **ambiguïté : deux lectures tranchées à l'achat** sur neuf signes, **degré de doute, révision, contradiction, et les passages qui ne se construisent pas**, **sauvegarde versionnée** qui se migre au lieu d'être abandonnée. Sur la branche `eleve`, pas encore fusionnée : l'instrument **Élève** ; et sur une branche de travail empilée dessus, la branche **Personne** de l'acte IV — et, empilés dessus, **les Questions** et **la branche Fin** de l'acte V : 43 signes d'arbre —, **les deux fins**, **la relecture**, **le Lecteur**, **le Corpus jumeau** et **I2** — l'acte IV est complet.

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

**Le panneau de composition dit vrai sur lui-même** (17/09/2026, COMP-6) : la palette porte son
intitulé « Ce que je sais lire » — le panneau tenait deux listes et n'en nommait qu'une, le
carnet ayant le sien depuis COMP-5 —, un emplacement plein dit « retirer ce signe » au lieu de
« poser un signe », et le refus **cesse d'expliquer** : « Rien ne vient. », sans la phrase qui
suivait et qui était fausse cinq fois sur six en PT10. **La prémisse du backlog était
inexacte** — la taille du lexique et les tracés de l'arbre sont publics dès t = 0 — mais
l'exclusion tient sur une meilleure raison : une liste à trous apprend qu'il y a des trous
(règle 14). Et le commentaire de `composer()` se trompait sur son propre code en affirmant
qu'une paire juste impayable « ne se distingue de rien à l'écran » : elle s'en distingue de
trois façons, qu'on laisse en connaissance de cause parce que le seul levier qui les
refermerait ferait payer plus cher celui qui a lu juste. Économie inchangée (rien n'y touche) ;
`outils/verifier.py` passe de 286 à **296 assertions**. Voir `docs/journal.md`, « Le corpus se
tait, le panneau non ».

**La carte de fin ne souffle plus** (12/10/2026) : elle posait au joueur « la seule question
qui compte » — celle de PT8, la crue qui baisse —, qu'un joueur de PT11 aurait lue **avant**
l'entretien dont la question 5 est faite pour la laisser remonter sans la nommer ; et elle
annonçait pour les actes IV et V le doute et les contradictions qu'il venait de jouer. Il
reste « Le prototype s'arrête ici. La suite appartient aux actes IV et V. » **Un écran de fin
est lu avant l'entretien : il fait partie du protocole.** Économie inchangée ;
`outils/verifier.py` passe de 296 à **297 assertions**. Voir `docs/journal.md`, « La carte de
fin soufflait la réponse ».

**L'Élève** (12/10/2026, ELV-1 + ELV-2) — **sur la branche `eleve`, à ne pas fusionner avant
le retour du journal de PT11.** 20 000 occurrences ×1,8, ouvert par la première Grammaire,
+5 % par tête aux cinq instruments. Dès le premier, un signe ambigu n'offre plus ses deux
lectures : « Un élève l'avait déjà recopié au propre. » Mesuré, joueur qui lisait juste et
ne révise jamais : **91,1–94,3 min sans Élève, 84,2–87,6 avec sept qui lisent juste,
92,6–95,9 avec sept qui lisent faux** — ⟨avant⟩, ⟨ne-pas⟩ et ⟨lire⟩ pèsent six points, un de
plus que le seuil, et arment la contradiction à eux seuls. **Un seul Élève qui se trompe est
le pire cas : 99,5–102,6**, la sanction entière pour 5 % de débit — CONTR-1 par l'autre
bout. Pire tranche d'I6 26 % et écart max 5,2 min, inchangés ; main 21–31 %. Deux réserves
écrites. **Lire soi-même coûte peu ici** : qui lit ⟨avant⟩ et ⟨ne-pas⟩ avant d'engager son
premier Élève ne perd que 0,8 min, donc l'arbitrage ne mord que sur celui qui ne sait pas —
à reprendre quand ⟨semence⟩ et ⟨devenir⟩ seront à cent minutes de là. Et ⟨il-faut⟩ vient
après `peut-être` : son erreur court dans la dette sans jamais rien armer dans le prototype
(règle 19) — jusqu'à VOIX-1, qui lui donne un franchissement. Garde-fou de durée re-basé à **(76, 96)**, par le bas seulement ; `balayage.py`
joue chaque combinaison avec et sans Élève, 34 sur 54 comme avant ; le journal d'actions
marque les achats lus par l'Élève et `depouiller.py` les compte à part. `outils/verifier.py`
passe de 297 à **315 assertions**. Voir `docs/journal.md`, « L'Élève tranche à ma place ».

**La Personne** (14/10/2026, VOIX-1) — **sur une branche de travail empilée sur `eleve`**,
pendant que PT11 attend un joueur : `develop` reste figé sur la page qu'il jouera. Six signes,
⟨nous⟩ (1 800 C) en tête — la porte que la tablette 18 laissait, qu'il rend entière — et
⟨nous-fûmes⟩ (9 500 C) en dernier, qui ferme la partie sur le dernier mot du corpus.
Aucun multiplicateur ; ⟨toi-qui⟩ et ⟨moi-absent⟩ se posent à la grille, ⟨nous-fûmes⟩ attend
⟨finir⟩ ; ⟨moi-absent⟩ n'a aucune attestation. **Les prix butent sur I1** : il faut monter à
9 500 C pour que l'acte IV ait un rythme, et il ne reste plus un cran de prix pour l'acte V
(ECO-3). **Le premier franchissement d'acte** de la règle 19 est en place : entrer dans l'acte IV
re-solde la contradiction, et ⟨il-faut⟩ mal lu après le doute cesse d'être gratuit. **La
sanction coûte trois fois plus** chez qui ne révise jamais — +32 min pour la paire réparante
au lieu de +11, et I4 cède à huit minutes. Non réglé : à observer. ⟨les-lecteurs⟩ remesuré au
milieu de l'arbre, il reste sans effet. **Le verrou du passé est à l'écran** (règle 22) : le
dernier mot du corpus met le récit au passé, jusque dans ce qui est déjà lu — « je gravé ·
toi lire », « après · nous · il-fallait » —, sauf ce qui s'adresse à ⟨toi⟩. Mesuré :
**104,7–108,6 min** (118,6–122,2 sans Élève), écart max 5,2, tranches ≥ 10′ ≤ 25 %, main
22,4–22,7 %. `outils/verifier.py` passe de 315 à **330 assertions**. Voir `docs/journal.md`,
« La Personne ».

**VOIX-2 — ce qui m'était adressé** (14/10/2026, même branche) : l'achat de ⟨toi⟩ replie le
corpus une fois, comme une concordance, sur les quatre-vingt-douze lignes qui portent ⟨toi⟩,
⟨toi-qui⟩ ou ⟨lire⟩ — treize disent « toi », les autres sont déjà lues : « il-faut lire ·
eau », les registres qui finissent sur « si lire », l'abécédaire. Rien n'est ajouté au texte ;
c'est le choix des lignes qui dit « toi » (tranché par l'auteur, contre une relecture déroulée
et une deuxième personne conjuguée). Le choix porte sur les signes, jamais sur les mots
(règle 17), et le repli ne compte pas comme une concordance dans le degré de doute : c'est le
jeu qui montre, pas le joueur qui rassemble (règle 18). Le journal d'actions date l'ouverture
et la sortie, et `depouiller.py` en tire la durée de la relecture. **Pour le playtest qui
jouera cette branche : relit-on, ou referme-t-on tout de suite ?** Et depuis VOIX-3 : **pose-t-on
des questions, lesquelles, et après avoir lu les « si » ou au hasard ?** Le journal d'actions
les date avec leur condition. `outils/verifier.py` passe
de 330 à **332 assertions**. Voir `docs/journal.md`, « VOIX-2 ».

**La sauvegarde survit aux actes** (19/10/2026, LIV-3) : la clé s'appelle `langue-morte-partie`
et **ne change plus** (règle 22) ; la version est écrite dans la sauvegarde, et une partie
trouvée sous `langue-morte-actes-i-iii` y déménage au premier chargement — **nuit comprise** :
la déplacer en l'enregistrant l'aurait datée de maintenant, et `ts` est ce qui mesure la nuit.
La version **se compte** sur la liste des migrations, et **aucune n'est écrite** : chaque lot
depuis l'acte III n'a fait qu'ajouter des champs, ce que `fresh()` couvre déjà. La première
qu'on voit venir est celle de FIN-2. Trouvé en chemin : la liste des instruments était
recopiée à la main dans le chargement, donc chaque instrument neuf s'écrivait deux fois —
`fusionner()` descend désormais d'un niveau, et la PR de l'Élève
([#56](https://github.com/DavidGiangiacomo/langue-morte/pull/56)) s'en trouve allégée d'une
ligne. Une sauvegarde que le jeu ne sait pas lire, plus récente ou dont la migration casse,
**ne s'écrase pas**. Ce que LIV-3 ne fait pas : lever « rien sur `develop` pendant un
playtest » — une version protège le format d'une partie, pas son économie. Économie
inchangée (`sim.py` 91,1–94,3 min, `balayage.py` 34 sur 54) ; `outils/verifier.py` passe de
297 à **307 assertions**, **325** avec l'Élève, **342** avec la Personne. Voir
`docs/journal.md`, « La version entre dans la sauvegarde ».

**Les Questions** (19/10/2026, VOIX-3, même branche) — tranché par l'auteur sur une note de
trois options mesurées (`docs/note-questions.md`). **Une question est une condition** : ⟨si⟩
et des signes qu'on sait lire, et la réponse est ce que le corpus a gravé après — quinze
conditions, et le texte répond à des questions que personne n'a posées : « si toi lire » rend
« nous ne-pas finir ». **La Certitude s'arrête à 9 999** et, à partir de ⟨toi⟩, ce qui
déborde fait des questions, 4 000 chacune, douze sur la partie ; la nuit n'en fait jamais, et
ne porte plus la Certitude au-delà du plafond. **La Grammaire gèle aux mots de la fin.** Ce
qui manque : les mots que les réponses ouvriront, ⟨finir⟩, ⟨devenir⟩ et ⟨germer⟩, qui sont de
GRAINE-1 — d'ici là le panneau répond et n'ouvre rien. Économie des actes I à IV inchangée au
chiffre près (`sim.py` 104,7–108,6 min) ; `outils/verifier.py` passe de 342 à **360
assertions**. Voir règle 24 et `docs/journal.md`, « Les Questions ».

**La Fin** (19/10/2026, GRAINE-1, même branche) : sept signes — ⟨semence⟩, ⟨finir⟩,
⟨le-dernier⟩, ⟨devenir⟩, ⟨notre-fin⟩, ⟨germer⟩, ⟨devenir-lecture⟩ —, tous à **9 999**, aucun
multiplicateur. Trois s'offrent par une réponse (« si toi lire », « si lire », « si
tablette ») et ⟨devenir-lecture⟩ en dernier, tranché par l'auteur ; la grille passe outre
(règle 25). ⟨semence⟩ et ⟨devenir⟩ tranchent leurs deux lectures à l'achat, et leurs ruptures
s'allument enfin — « si enfant · ne-pas né », « il-fallait tablette · porté lu » (AMB-4).
`sim.py` porte l'acte V (ECO-2) : **133,5–136,9 min** au réglage en place, **159,5–162,6** sans
Élève, acte V de 28,2 et 40,3 min, moyenne de 4,0 et 5,8 min par signe, écart max 7,2 — I4
tient. La paire réparante ⟨grain⟩ + ⟨maison⟩ chez qui ne révise jamais : **223,6–226,6**, la
sanction coûte désormais une heure, et I4 y cède à 11,4–12,9 min avant ⟨finir⟩ — la Certitude
divisée par deux divise aussi le surplus qui fait les questions. Non réglé, comme à l'acte IV. La main tombe à **16,7 %** des occurrences, **13,1 %**
sans Élève : l'acte V dure vingt-huit à quarante minutes sur un gisement presque épuisé, et
elle pesait encore 17,2 % en y entrant. `balayage.py` re-basé — durée (121, 165), écart max
à 8, la borne d'I4, et plancher de la main à **11** au lieu de 15 : sur la partie entière
cette part n'est pas plus un invariant que la durée, et à 15 les 54 combinaisons tombaient,
réglage en place compris. 11 rejette encore « tout dégager à 80 % de l'arbre » (9,7 %), avec
trois points de marge au lieu de dix — noté, pas réglé (règle 9). **42 combinaisons sur 54**,
comme à la Personne, dont le réglage en place (124,1–162,6 min, écart 7,2, main 13 %) ;
`outils/verifier.py` passe de 360 à **376 assertions**. Voir règle 25 et `docs/journal.md`,
« La Fin ».

**Les deux fins** (19/10/2026, FIN-1 + FIN-2, même branche) — tranché par l'auteur sur trois
questions. Le dernier signe de l'arbre ouvre une fenêtre, au lexique comme à la grille et
seulement quand on peut le payer : **achever** ou **interrompre**, même habit, ordre tiré au
sort, et la fenêtre dit que la partie s'arrête dans les deux cas. Achever : l'effacement
attend qu'on ait lu la tablette du dernier signe, puis l'interface s'en va pièce à pièce, le
texte glisse au milieu, reste seul, et s'efface. Interrompre : l'interface s'en va, le corpus
reste figé, et la partie ne se reprend jamais, pas même au chargement. Il ne reste qu'un
bouton, « recommencer » ; **la carte de statistiques est retirée**, c'était un score. **La
première migration de sauvegarde est écrite** (version 2) : une partie finie avant ce lot est
achevée. Le journal d'actions date chaque ouverture de la fenêtre et l'interruption, et
`depouiller.py` en tire l'hésitation. Économie inchangée (`sim.py` 133,5–136,9 min) ;
`outils/verifier.py` passe de 376 à **395 assertions**. Voir règle 26 et `docs/journal.md`,
« Les deux fins ». **Pour le playtest qui jouera cette branche : achève-t-on ou
interrompt-on, combien de fois ouvre-t-on la fenêtre avant de choisir, et les quarante
secondes de texte seul sont-elles lues ?**

**La relecture** (19/10/2026, FIN-3, même branche) — tranché par l'auteur sur quatre
questions. Après avoir achevé, « relire » rend le corpus entier, écrit juste, et marque sur
chaque jeton ce qui avait été mal lu — resté faux, ou corrigé par une révision —, et ce qui
n'a jamais été trouvé, ⟨grenier⟩ et le zéro. Le survol dit le mot lu et qui l'avait lu, le
joueur ou un Élève. Une légende nomme les trois marques et ne compte rien. La paire réparante,
que rien n'a jamais trahie, y est enfin avouée : c'est le seul endroit du jeu. Deux champs de
sauvegarde ajoutés, sans migration. Le journal d'actions date la relecture et compte, lui, ce
qu'elle avoue. Économie inchangée ; `outils/verifier.py` passe de 395 à **412 assertions**.
Voir règle 27 et `docs/journal.md`, « La relecture ». **Pour le playtest : l'entretien se fait
avant « relire »**, qui répond à trois de ses questions ; et ouvre-t-on la relecture, combien
de temps y reste-t-on ?

**Le Lecteur** (19/10/2026, GRAINE-2, même branche) — tranché par l'auteur sur deux questions.
Neuvième instrument, ouvert par ⟨semence⟩ : un signe pour nom, ⟨devenir-lecture⟩, et aucune
ligne d'effet. Il ne produit rien ; il lit le corpus tout seul, une tablette par minute et par
Lecteur, et chaque tablette lue verse 300 à la question suivante. On le voit faire — la
tablette lue marquée dans la barre et au bord du texte, la ligne qu'il lit qui s'éclaire — et
la tablette 27 dit ce qu'il était : « tablette · devenir-lecture ». Mesuré : **130,9–134,3 min**
au réglage en place (133,5–136,9 sans lui), **155,5–158,6** sans Élève ; acte V de 25,6 et
36,3 min, pire trou sans Élève 5,8 min au lieu de 7,2. Réserve : avec Élèves, l'acte V tombe à
3,7 min par signe, sous I4. `sim.py` le porte ; `balayage.py` re-basé à (118, 161), **42 combinaisons sur 54** comme avant lui ; `outils/verifier.py` passe de
412 à **421 assertions**. Voir règle 28 et `docs/journal.md`, « Le Lecteur ». **Pour le
playtest : voit-on le Lecteur lire, et à quelle minute va-t-on voir une tablette marquée ?**

**Le Corpus jumeau** (19/10/2026, VOIX-4, même branche) — tranché par l'auteur sur deux
questions. Huitième instrument, ouvert par ⟨nous⟩, un seul exemplaire : une copie du corpus,
« si copier 100 · un devenir ». Chaque tablette rouvre la moitié de son gisement, tarifée au
premier relevé sur la copie, donc au débit de l'acte IV ; l'original passe d'abord. Mesuré :
**128,2–133,6 min** au réglage en place (130,9–134,3 sans lui), **153,2–157,7** sans Élève ; la
main passe à **26–33 %** des occurrences avec Élèves (17,3) et **26 %** sans (13,7), sous le
plafond de 40 ; I4 ne bouge pas. `balayage.py` re-basé à (116, 160), **42 combinaisons sur 54**
comme avant lui ; `outils/verifier.py` passe de 421 à **429
assertions**. Trouvé en chemin : le Lecteur marquait ses tablettes avec la classe `lue`, que la
barre portait déjà pour « tarif figé » — corrigé (`parcourue`). Voir règle 29 et
`docs/journal.md`, « Le Corpus jumeau ». **Pour le playtest : revient-on relever après
⟨nous⟩, et sur quelles tablettes ?**

**I2 — perdre la lisibilité de ses propres nombres** (20/10/2026, VOIX-5, même branche) —
tranché par l'auteur sur trois questions. Au million, une fois l'acte IV ouvert, un nombre
garde trois chiffres au joueur et ses zéros s'écrivent du tracé de ⟨zéro⟩ — compteurs et
coûts —, et la largeur dit l'ordre de grandeur. ⟨zéro⟩, posé à la grille, rend la notation
compacte de ⟨cent⟩ : ce que le design doc lui promettait depuis le premier jour. Mesuré : avec
Élèves, la notation paraît à l'achat de ⟨nous⟩ (88–91 min) et le stock la prend à 90–97 ; sans
Élève, à 97–102, le stock à 98–106 ; qui ne compose jamais ⟨zéro⟩ joue 40 à 56 minutes sans
lire ses nombres. Affichage seul, rythme inchangé ; `outils/verifier.py` passe de 429 à **438
assertions**. Voir règle 30 et `docs/journal.md`, « I2 ». **Pour le playtest : remarque-t-on
qu'on a perdu ses nombres, les relit-on en les regardant monter, et compose-t-on ⟨zéro⟩
ensuite — à quelle minute ?**

**ECO-3 — les deux trous d'I4** (20/10/2026, même branche) — tranché par l'auteur sur deux
questions mesurées. **La contradiction ne divise plus que par 1,25 aux actes IV et V, et les
Élèves attendent tant qu'elle court.** Le ÷2 doublait tout ce qui restait une fois les prix au
plafond : chez qui ne révise jamais — le joueur de PT10 —, +60 à +85 min et huit à onze minutes
d'attente par signe sur deux actes. Mesuré désormais : pire attente 6,7 à 7,4 min dans les six
cas de contradiction, la paire réparante à 176,8–180,7 min (+23 au lieu de +60), et des Élèves
qui lisent tout faux seize minutes derrière le joueur sans Élève — l'arbitrage de la règle 21,
que le diviseur seul cassait. **La borne basse d'I4 se mesure sur le joueur sans Élève** : avec
Élèves l'acte V reste à 3,45–3,58 min par signe, et c'est ce que l'Élève achète. Parties sans
contradiction inchangées (`sim.py` 128,2–133,6 et 153,2–157,7 min, `balayage.py` 42 sur 54) ;
`outils/verifier.py` passe de 438 à **442 assertions**. Voir règle 31 et `docs/journal.md`,
« ECO-3 ». **Pour le playtest : la contradiction se déclenche-t-elle, et révise-t-on cette
fois ?**

**Prochaine étape — PT11 avec un autre joueur, puis fusionner l'Élève (E5), puis l'acte IV.** *PT11 est en attente depuis le 14/10/2026, faute de joueur : le travail continue sur des branches empilées sur `eleve`, et `develop` ne bouge pas.* Même question qu'en PT8 et PT9, posée à quelqu'un qui ne sait pas ce qu'il cherche — plus celle que PT10 a ouverte : **revient-on dans le corpus après la quarantième minute ?** Dans le même TSV : la part manuelle des occurrences (au-delà de 40 %, plafonner `REL_K`) le stock d'hypothèses entre `année` et la dixième Grammaire (27 090 en PT9), **le nombre de recoupements** — sous une vingtaine sur la partie, le réglage du 09/09 a vidé un des deux gestes manuels et il faut revenir en arrière — et **les tentatives de composition** : le journal d'actions les compte avec leur paire et leur minute. La question neuve est celle-là : un joueur qui ignore qu'il y a quelque chose à chercher reconnaît-il ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩, ou ⟨ne-pas⟩ et ⟨un⟩ dans le zéro qu'il regarde depuis la première seconde ? Aucun simulateur ne répond à ça. S'y ajoutent deux questions depuis `les-lecteurs` : **achète-t-on un signe à 1 200 C qui annonce trois attestations** — le TSV date le moment où il devient payable — et, à poser de vive voix, **a-t-on vu ⟨nous⟩ dans le nom** ? Et une mesure de plus, parce que `REV_R` la déplace sans qu'aucun playtest soit derrière : **le nombre de recoupements et la part manuelle des occurrences**. Si la main descend au lieu de monter, c'est `REV_R` qu'il faut défaire en premier, avant les prix.

**Et depuis AMB-1, trois questions de plus, qu'aucun simulateur ne touche.** Le journal d'actions note désormais la lecture retenue à chaque achat, avec un ✗ pour la fausse. (1) **Combien de lectures fausses sur neuf ?** Neuf pièces à pile ou face donneraient 4,5 ; nettement moins voudrait dire que quelque chose souffle la réponse, nettement plus que le corpus l'induit en erreur. (2) **⟨grain⟩ ou ⟨poussière⟩ à la troisième minute** — c'est le choix où la prime paie le plus et où le joueur a le moins de quoi trancher ; et s'il se trompe, retourne-t-il sur la tablette 5 quand elle sort de terre ? (3) À poser de vive voix, une fois seulement, **et à la fin** : a-t-on remarqué qu'on choisissait ? Le jeu ne le dira jamais avant `peut-être`.

**Et depuis MOD-2, deux questions de plus pour PT10.** Le journal d'actions note la lecture retenue et le degré de doute à chaque achat. (1) **Combien de révisions, et sur quels signes ?** Zéro voudrait dire que le panneau ne pointe rien ; plus de cinq, que le prix ne mord pas. (2) **Le joueur concorde-t-il AVANT de trancher, ou après ?** C'est le seul geste qui fasse baisser le doute, et le jeu ne le dit nulle part — s'il ne le trouve pas, il faudra se demander si le doute pointe vers quelque chose d'atteignable.

**Et une question depuis le 14/10/2026, sur l'ouverture.** ⟨un⟩ coûte 2 C — le signe le moins cher de l'arbre, l'achat évident de la première minute — et il fait passer les trois compteurs en chiffres arabes d'un bloc. Le design doc §10 appelle le décodage du compteur « le premier plaisir du jeu » et demande de le protéger absolument ; il a donc une espérance de vie de deux Certitude, et la branche étant une chaîne stricte, on ne peut pas atteindre ⟨deux⟩ sans passer par ⟨un⟩. **La conversion est-elle reçue comme une récompense ou comme une énigme qu'on vient de perdre ?** L'auteur ne peut pas répondre : il connaît la numération. Le TSV en dit la moitié (la minute du premier achat, et si c'est ⟨un⟩) ; le reste est la question 11 du protocole, à poser **après** ⟨grenier⟩ et le zéro — dans l'autre ordre, elle apprend à lire les signes de nombre comme des composés et donne sa réponse à la question 9. Ne rien régler avant, et surtout pas déplacer `readN` à l'aveugle. Issue [#57](https://github.com/DavidGiangiacomo/langue-morte/issues/57), `docs/journal.md` « Le compteur n'est pas le corpus ».

**Et deux questions de plus depuis CONTR-1 et MOD-3.** (1) **La contradiction se déclenche-t-elle, et le joueur la relie-t-il à ses lectures ?** Le bandeau dit la sanction et sa sortie sans nommer un signe ; s'il la lit comme une panne, c'est le texte du bandeau qu'il faut reprendre, pas le seuil. (2) **Une ligne allumée par `faux` se lit-elle ?** Elle ne nomme rien et porte quatre ou cinq signes ; si le joueur ne s'en sert pas pour choisir sa révision, c'est que la marque ne suffit pas — mais la réponse n'est pas de nommer le signe, jamais.

**Et deux de plus le jour où l'Élève sera fusionné**, donc pour PT12. (1) **Combien d'Élèves, et avant ou après ⟨avant⟩ et ⟨ne-pas⟩ ?** Le simulateur en empile sept sans réfléchir. (2) À poser de vive voix : **à qui le joueur attribue-t-il un mot faux** — à lui, ou à l'Élève ? Et « combien de lectures fausses sur neuf » ne vaut plus que pour les signes qu'il a lus lui-même ; le dépouillement les sépare.

Restent ensuite : fusionner **l'Élève** (E5), écrit et mesuré sur la branche `eleve` — c'est le dernier morceau de J2. L'**acte IV** est écrit en entier (la Personne, son verrou du passé, le réaffichage, les Questions, le Corpus jumeau et I2) . De l'**acte V**, la Fin, le Lecteur, les deux fins et la relecture sont écrits ; reste la révélation, GRAINE-3, qui ne demande plus qu'un playtest. Voir `docs/design-doc.md` §7 et §8, et `docs/backlog-1.0.md` pour le découpage.

---

## Conventions

- Commentaires en français, au-dessus de ce qui est non évident. Expliquer **pourquoi**, pas quoi.
- Les noms de fonctions et variables suivent la fiction quand c'est naturel : `veille()`, `consignes()`, `recouper()`, `tablette`.
- Le sélecteur de vitesse ×1/×3/×10, le chronomètre et les boutons `traces`/`copier` en haut à droite sont des **outils de test**, marqués « hors jeu ». **Ce n'est plus à retirer à la main** : les marqueurs de variante d'`index.html` décident de ce que chaque build en garde. Un bouton hors jeu neuf se pose dans le bloc `#dev`, pas ailleurs, tant qu'on n'a pas dit ce qu'il fait devant un joueur qu'on ne regarde pas jouer.
- `src/traces.js` n'édite aucune règle : il **enveloppe** les actions déjà déclarées — des fonctions, jamais des écouteurs de boutons, qui ne sont pas dans tous les builds. `dist/public.html` le retire déjà (16 Ko de moins). Ne jamais y mettre de logique de jeu, et ne jamais l'appeler depuis le jeu.
- Écrire les nombres à la française dans l'interface (espace fine insécable, virgule décimale) — `nf` et `f()` s'en chargent.
