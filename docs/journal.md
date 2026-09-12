# Journal de bord

Historique des playtests, des défauts trouvés et des décisions prises. À lire avant de modifier l'équilibrage ou la numération : chacune des règles actuelles est là parce qu'une version plus simple a échoué.

---

## Les playtests

| | PT4 | PT5 | PT6 | PT7 | PT8 | PT9 | Cible |
|---|---|---|---|---|---|---|---|
| Durée | 42 min 12 | 50 min 37 | 43 min 49 | 44 min 50 | **63 min 12** *(20 signes)* | **66 min 49** *(20 signes)* | 45 min *(13 signes)* |
| Signes relevés à la main | 56 | **371** | 180 | **422** | — | **429** | — |
| Hypothèses formulées à la main | — | 264 | 27 | 7 | — | 6 | — |
| Recoupements | **56** | 46 | 44 | 39 | 46 | 49 | — |
| Part manuelle de la Certitude | 43,5 % *(simulé)* | **30,8 %** | **30,0 %** | **31,2 %** | **6,0 %** | **8,2 %** | < 30 % par tranche de 10 min |
| Part manuelle des Occurrences | — | 0,6 % | **0,1 %** | **17,9 %** | — | **36,3 %** | — |
| Gisement consommé | — | — | 54 / 398 | 293 / 398 | **394 / 398** | 393 / 397 | — |
| Lignes entièrement lues | 26 % | 26 % | 26 % | 26 % | **34 %** | 34 % | — |
| Signes déchiffrés | 58 % | 57 % | 57 % | 57 % | **69 %** | 69 % | — |

PT1 à PT3 sortent du tableau : ils datent d'avant le journal d'actions, et leurs chiffres
vivent dans les sections qui les dépouillent. PT8 est la première partie des trois actes —
sa durée et ses parts ne se comparent pas aux précédentes, qui s'arrêtaient à 13 signes.
PT9 : 429 relevés et 49 recoupements sortent du TSV ; la carte de fin collée au-dessus du
TSV (29 min 27, 271, 69, « corpus lisible 68 % ») était celle de PT2, et n'a pas été retenue.

PT1 à PT4 : l'auteur. **PT5 : un second joueur** (mon fils, 06/09/2026), et le premier
playtest instrumenté par le journal d'actions — d'où le détail de ce qui suit. Tout ce qui
y est chiffré sort du TSV, pas du souvenir.

### PT1 — le clic était la colonne vertébrale

Une Table de fréquences consommait 1,5 occ./s quand un Copiste en produisait 0,4 : chaque convertisseur exigeait trois générateurs d'amont pour son seul entretien, le solde net passait négatif, et l'économie ne pouvait pas croître. Seul le clic restait fiable, d'où les 3 853 relevés manuels.

Cause aggravante : l'**Atelier de copie** avait été coupé du MVP. C'était le seul barreau d'échelle permettant à la production d'occurrences de dépasser la consommation des convertisseurs.

→ Atelier réintroduit · ratios producteur/consommateur ramenés de 1:3 à ~1:1 · croissance des coûts adoucie en bas d'échelle · relevé manuel indexé sur le débit (`1 + 3 % du débit brut`).

### PT2 — le recoupement était devenu la colonne vertébrale

271 clics seulement : le clic n'était plus le moteur, objectif atteint. Mais **69 recoupements pour 203 Certitude** — avec le gain d'alors (jusqu'à 4 C par usage), l'action manuelle fournissait ~85 % de la ressource centrale et la chaîne Table → Concordance était décorative.

Le même défaut, déplacé d'un bouton. Sur-correction.

→ Gain du recoupement plafonné à `min(3, 1 + ⌊lexique/5⌋)` · coût porté de ×1,09 à ×1,12 par usage.

**C'est de là que vient l'invariant I6** : *aucune action manuelle au-dessus de 30 % de la Certitude produite sur une partie.* `outils/sim.py` mesure ce ratio ; le vérifier à chaque ajout d'instrument. C'est le mode de défaillance par défaut du jeu, parce que la Certitude est rare et que le joueur cherche le chemin le plus court vers elle.

### PT3 — l'économie est réglée, le texte prend le relais

45 clics manuels. Les deux corrections ont tenu ; le problème d'équilibrage est clos. Le playtest a porté sur le texte et a sorti trois demandes d'interface, toutes traitées.

Verdict qualitatif, aux trois essais : envie de continuer présente tout du long. Remarque décisive du testeur : *la qualité de ce qui se découvre au fil du jeu sera déterminante* — le risque R4 du design doc, confirmé par le jeu.

---

### PT4 — l'invariant I6 n'a jamais été respecté

Les trois demandes d'interface de PT3 ont tenu : la numération signe par signe, la barre
de tablettes et les infobulles se jouent sans accroc, et le marquage ocre est suivi.

Mais PT4 a servi à autre chose : **il a montré que le problème d'équilibrage n'était pas
clos.** PT3 avait mesuré les *clics* (45) et conclu ; le ratio du recoupement, lui, n'avait
pas été revérifié depuis la correction de PT2. Il l'est maintenant : **43 %**, pour un
plafond I6 de 30 %.

`outils/sim.py`, resynchronisé sur `lexique.js`, reproduit la partie de près — 57
recoupements simulés contre 56 relevés. Le balayage des leviers dit lequel mord :

| variante | durée | recoup. | I6 |
|---|---|---|---|
| avant PT4 (coût ×1,12/usage) | 53,3 min | 57 | **43,5 %** |
| gain plafonné à 2 | 54,8 min | 58 | 39,2 % |
| ×1,18 | 58,8 min | 41 | 29,5 % |
| ×1,18 + concordance +30 % | 52,7 min | 39 | 27,8 % |
| ×1,25 | 62,0 min | 31 | 21,5 % |

**Plafonner le gain ne sert à rien** — le joueur recoupe simplement plus souvent. Seule la
croissance du coût par usage déplace le ratio. `×1,18 + concordance +30 %` est le seul
réglage qui repasse sous 30 % sans allonger la partie : il rend à la chaîne d'instruments
ce qu'il retire à la main.

**R6, 05/09/2026 : réglage adopté.** `REC_R = 1.18` et `CON_P = 0.0039` dans
`src/economie.js`, répercutés dans `outils/sim.py`. Les deux constantes sont nommées :
elles servaient à trois endroits chacune, et c'est cette duplication qui avait laissé le
simulateur diverger du jeu. **À vérifier au prochain playtest** — le simulateur dit
27,8 % et 52,7 min, mais il fait tourner un acheteur heuristique, pas un joueur.

> Le simulateur avait divergé de `lexique.js` : 12 signes à 203 C au lieu de 13 à 237 C.
> Il servait d'instrument de contrôle d'I6 (règle 2 de `CLAUDE.md`) tout en mentant.
> Resynchronisé. À revérifier à chaque modification du lexique.

### PT4 — l'achat est un faux choix

Remarque du testeur : « j'ai toujours acheté le truc le moins cher ». Ce n'est pas une
habitude, c'est la stratégie strictement dominante. Apport marginal mesuré, tous les
autres signes acquis :

| signe | coût | Δsignes | Δlignes | signes/C |
|---|---|---|---|---|
| un | 2 | 687 | 155 | **344** |
| deux | 5 | 848 | 155 | **170** |
| grain | 3 | 315 | 69 | **105** |
| maison | 6 | 266 | 20 | 44 |
| cinq | 11 | 464 | 121 | 42 |
| dix | 18 | 746 | 133 | 41 |
| tablette | 14 | 318 | 66 | 23 |
| cent | 33 | 137 | 65 | 4,2 |
| eau | 22 | 70 | 20 | 3,2 |
| graver | 27 | 56 | 0 | 2,1 |
| champ | 40 | 49 | 42 | 1,2 |
| copier | 48 | 57 | 5 | 1,2 |
| **dire** | **8** | **2** | **0** | **0,2** |

Le rendement va de 344 à 0,2 — **un facteur 1700×** — et il décroît avec le prix. Le prix
et la récompense vont dans le même sens : il n'y a jamais d'arbitrage.

**Décorréler les bonus des mots ne réglerait rien** : retirer tous les bonus ne change pas
le classement, parce que la valeur *textuelle* seule range déjà du moins cher au plus cher.
Et inverser les prix serait faux — un signe fréquent doit être le plus facile à casser,
c'est l'analyse de fréquences.

Piste ouverte, non tranchée : rendre les branches **non comparables**, trois monnaies au
lieu d'une. Nombre ouvre des *classes* de nombres (récompense énorme et invisible à un
comptage d'occurrences : `dix` vaut +746 signes alors que le mot « dix » n'apparaît que
2 fois dans le corpus). Matière ouvre du texte. Parole ne devrait ouvrir **aucun texte**,
seulement des *pouvoirs* — c'est déjà à moitié l'intention, mais `dire` à 8 C rapporte
2 signes sur 3 825, le pire achat du jeu, et le simulateur le place en 5ᵉ position.

Corollaire : le comptage d'occurrences restait un ornement tant qu'il n'apparaissait que
dans l'infobulle. Il est maintenant **affiché sur les têtes de branche du panneau lexique**
— voir la section suivante.

### Défauts trouvés en marge de PT4

- **La réinitialisation ne remettait pas la numération à zéro.** `majSignes()` n'était
  appelé qu'au chargement et à l'achat d'un glyphe : après « réinitialiser », `SU` gardait
  les signes de la partie précédente et **229 nombres restaient affichés en chiffres** sur
  une partie censée neuve. Tout playtest lancé par ce bouton démarrait faussé. Corrigé
  dans `jeu.js`, verrouillé par trois contrôles de `outils/verifier.py`.
- **Les tablettes se dégagent peut-être trop vite** — `revCount()` vaut `4 + 2 × signes`,
  donc les 30 sont sorties au 13ᵉ signe, pile à la fin du MVP. Signalé, non traité.

## La Modalité, et le zéro qu'on avait sous les yeux

12/09/2026. Deuxième récit de J1 (`docs/backlog-1.0.md`, MOD-1 et COMP-3). La branche
**Modalité** entre dans l'arbre avec `ne-pas`, `si`, `il-faut`, `sinon` ; `zéro` la suit par
la grille de composition. L'arbre passe de 23 à **27 signes**, et le lexique du joueur à 29
avec les deux composés secrets.

| glyphe | coût | effet |
|---|---|---|
| `ne-pas` | 150 C | ce qui manque se lit : les foyers vides, les greniers vides |
| `si` | 320 C | les conditions se lisent |
| `il-faut` | 550 C | +50 % à l'atelier de copie |
| `sinon` | 800 C | le protocole de copie se lit jusqu'à son dernier mot |
| `zéro` *(composé)* | 120 C | les onze zéros du corpus passent en chiffres |

Aucune ligne du corpus ne change — c'est le quatrième lot de suite. Mais c'est le plus gros
morceau de lisibilité qui restait : **816 attestations, un signe du corpus sur cinq**
(`ne-pas` 290, `si` 239, `il-faut` 156, `sinon` 131). `les-lecteurs`, à côté, en vaut trois.

Ce que ça donne à lire était sous les yeux depuis la première seconde :

```
maison 6 · ne-pas · grenier ne-pas · avant · année ne-pas
champ 1 · ne-pas
champ 2 · ne-pas
champ 3 · grain 21
champ 4 · ne-pas
```

La tablette 25, quatre champs et un seul qui rend quelque chose. Et le protocole de copie,
qui revient sur deux siècles et dont on ne lisait que le premier mot :

```
il-faut copier · si ne-pas · sinon
```

La consigne s'arrête là. Ce qui vient après « sinon » n'est gravé nulle part — c'est la seule
menace du corpus, et elle n'est pas écrite (règle 5 : le jeu n'ajoute rien).

### Une branche qui ne doit pas accélérer

La Modalité ne donne qu'un multiplicateur pour quatre signes, et c'est mesuré, pas oublié.
Cinq variantes d'effets, coûts identiques (`python outils/sim.py`, trois cadences) :

| effets | durée, 27 signes | écart max |
|---|---|---|
| `si` +50 % grammaire · `il-faut` +50 % atelier | 82,5 – 85,6 min | 5,2 |
| `si` +50 % grammaire seul | 82,7 – 85,7 min | 5,2 |
| `si` +30 % grammaire · `il-faut` +50 % atelier | 84,0 – 87,0 min | 5,2 |
| **`il-faut` +50 % atelier seul** | **87,0 – 90,0 min** | **5,2** |
| aucun | 87,2 – 90,1 min | 5,2 |

Deux choses se lisent dans ce tableau. La première : **le bonus d'atelier ne déplace rien**
(87,0 contre 87,2). En fin de partie les occurrences ne sont plus ce qui manque — la
Certitude passe par la Grammaire, qui boit des hypothèses, lesquelles viennent de la Table.
Trois bonus d'atelier existaient déjà (`mille`, `dernière-année`, `scribe`) sans que personne
l'ait remarqué. La seconde : **le bonus de grammaire, lui, rend plus qu'il ne coûte**. Donner
à `si` le troisième ×1,5 de l'instrument exponentiel faisait finir l'acte en 82,5 min au lieu
de 87,0 — quatre signes de plus pour une minute de jeu. C'est la leçon de `REC_R` par l'autre
bout : dans cette économie, seuls les taux mordent, et un taux posé sur l'instrument qui
porte la Certitude se rembourse avant d'être payé.

Retenu : `il-faut` porte l'atelier — la consigne du corpus est « il-faut copier », gravée
vingt-sept fois, et l'atelier est la salle où on la suit — et les trois autres ne paient
qu'en lecture. La zone d'interface de la branche (le panneau de révision, les indices de
confiance, design doc §6) n'existe pas encore : elle s'ouvrira à `peut-être`.

**Mesuré au réglage retenu** : 87,0 à 90,0 min pour les 27 signes (81,6 – 85,0 à 23), écart
max **5,2 min** — inchangé, il est posé à `cinq`, dans le premier quart d'heure —, I6 par
tranches **≤ 27 %** à partir de 10′ (25,8 % avant ce lot), 33 recoupements, la main fournit
22,1 à 23,6 % des occurrences. Le point d'attention est le 27 % de la tranche 20-30′ : il ne
vient pas de la Modalité, qui arrive à la cinquantième minute, mais de `revCount()` — quatre
glyphes d'arbre de plus, c'est un dégagement de tablettes un peu plus lent par signe acquis,
donc un peu moins de gisement, donc un peu moins d'instruments. Chaque lot le poussera. Sous
la barre de 30 % (règle 2), mais le prochain lot devra le regarder.

### `zéro` : ce que le design doc lui prête, et ce qu'il fait

`zéro` est le composé canonique — ⟨ne-pas⟩ posé sur ⟨un⟩, la branche Nombre de l'acte I
rencontrée par la Modalité de l'acte III, exactement ce que la composition existe pour
produire. Le design doc (§7) lui prête « la notation compacte des grands nombres ».
**Il ne l'aura pas** : cette notation est déjà celle de `cent`, que tout le monde achète, et
la déplacer sur un composé facultatif la retirerait à la plupart des joueurs. Son effet est
donc celui du grenier : on le lit, et c'est tout.

Ce qu'on lit suffit. `numLisible()` attend ce signe depuis l'acte I — un nombre nul n'est
lisible que si on l'a —, et onze zéros dorment dans le corpus, dont **neuf sur la tablette
29**, le registre où tout est à zéro (`docs/corpus.md` §5). Elle reste jusque-là un seul
signe répété, l'« heureux accident » qu'il fallait préserver ; elle passe d'un coup en
chiffres, quatre champs, le grain, l'eau, les maisons, le grenier, la semence.

Coût : 120 C, soit deux minutes de progression pour qui le pose (`grenier` en coûte 1,4), et
l'écart max monte alors à 6,2 min — sous les huit minutes d'I4. `sinon`, lui, est un signe
d'**arbre** composable (règle 15) : posé en avance il avance la partie, et saute `il-faut`
dans la chaîne pour une minute de retard. C'est le piège de `scribe`, en beaucoup plus doux,
parce que ses deux parties sont dans sa propre branche : pour composer `sinon` il faut déjà
avoir acheté `si`, donc `ne-pas`.

### Deux outils qui avaient divergé

`outils/sim.py` posait un composé sans vérifier que le joueur en connaissait les deux
parties. Vrai sans conséquence tant que les composés mesurés (`grenier`, `scribe`) se
faisaient de signes de l'acte I ; faux pour `sinon`, qui se compose de deux signes de sa
propre branche. Le simulateur lit désormais `COMP` et `ALIAS` dans `src/signes.js` et en
dérive ses recettes comme le jeu (règle 15) — troisième table lue à la source plutôt que
recopiée, après le corpus et l'ordre de sortie de terre.

`outils/balayage.py` rejetait ses dix-huit combinaisons **depuis le commit `da61b19`**, y
compris le réglage en place, en affichant « 0 sur 18 » sans que rien ne soit cassé : son
garde-fou de durée valait encore (71, 77), la mesure de PT9 à vingt glyphes, quand l'arbre
en comptait vingt-trois. L'écart et le plafond par tranche sont des invariants ; la durée
n'en est pas un, elle suit la taille du lexique. Re-basée à (84, 92) — 14 combinaisons sur
18 passent, dont le réglage retenu.

### Ce que PT10 doit regarder ici

Une question de plus, et elle est de la même famille que ⟨grenier⟩ : **un joueur qui vient
d'acheter ⟨ne-pas⟩ pose-t-il ⟨ne-pas⟩ sur ⟨un⟩ ?** Il a le signe sous les yeux depuis la
première seconde — il est dans la tablette 29 en neuf exemplaires, et dans les compteurs du
jeu à chaque fois qu'une ressource est vide. Le journal d'actions compte les tentatives avec
leur paire et leur minute. Aucun simulateur ne répond à ça.

## La Parole III — le corpus parle de lui-même

11/09/2026. Premier récit de J1 (`docs/backlog-1.0.md`, PAR-1). La branche Parole s'arrêtait
à `copier` ; elle gagne `lire`, `scribe` et `archive`, posés après lui. L'arbre passe de 20 à
**23 signes**. Aucune ligne du corpus ne change : les trois signes y sont depuis la première
seconde — `scribe` signe vingt-sept tablettes, `lire` revient quatre-vingt-douze fois.
`les-lecteurs` reste pour PAR-2.

| glyphe | coût | effet |
|---|---|---|
| `lire` | 300 C | +50 % à la grammaire |
| `scribe` | 600 C | +50 % au copiste et à l'atelier |
| `archive` | 900 C | +50 % à la table de fréquences |

Des multiplicateurs, comme les vingt autres. `lire` en avait besoin d'un pour une raison qui
n'est pas encore dans le jeu : c'est le piège majeur de l'ambiguïté (`docs/corpus.md` §7), et
sa lecture fausse, « compter », devra rendre 25 % de plus. Il faut un effet chiffré à majorer.

### Les coûts ne pèsent presque rien — encore

Balayé aux trois cadences (`python outils/sim.py`, coûts de `lire` / `scribe` / `archive`) :

| coûts | durée, 23 signes | écart max | I6, tranches ≥ 10′ |
|---|---|---|---|
| 150 · 300 · 430 | 74,0 – 77,5 min | 5,2 | ≤ 26 % |
| 200 · 420 · 650 | 77,8 – 81,2 min | 5,2 | ≤ 26 % |
| 250 · 500 · 800 | 79,9 – 83,3 min | 5,2 | ≤ 26 % |
| **300 · 600 · 900** | **81,6 – 85,0 min** | **5,2** | **≤ 26 %** |
| 350 · 700 · 1 100 | 83,8 – 87,1 min | 5,6 | ≤ 26 % |

Au plus bas, les trois signes n'ajoutent que deux minutes : leurs multiplicateurs accélèrent
tout ce qui suit. Retenu **300 · 600 · 900** — neuf minutes de plus pour trois signes à
15 clics/min, `archive` sous les quatre chiffres. Au-delà, chaque palier coûte une minute et
rapproche la Certitude du plafond d'I1 sans rien acheter d'autre.

Mesuré au réglage retenu : **81,6 à 85,0 min**, écart max **5,2 min**, tranches à partir de dix
minutes à 26 / 23 / 22 % au pire, la main à 20–21 % des occurrences, 33 recoupements. `lire`
arrive à 67′, `scribe` à 78′, `archive` à 83′ (15 clics/min). La moyenne tombe à 3,6 min par
signe, sous les 4 à 6 d'I4 — elle y était déjà à vingt signes (3,65).

### Le scribe se compose, et c'est un piège

`scribe` se dessine ⟨dire⟩ sur ⟨graver⟩, `archive` ⟨tablette⟩ sur ⟨graver⟩. La règle 15 les
ouvre donc d'elles-mêmes dans la grille, dès `année` : cinq recettes au lieu de trois. Ce sont
des signes d'arbre — posés en avance, ils avancent la partie, comme `deux` et `siècle`. Et
`scribe` est au bas de chaque tablette : c'est le composé le plus visible du corpus après
`deux`, bien plus que `grenier`.

Le simulateur le fait maintenant épargner pour un composé visé (`compose=` dans `run()`) —
sans quoi il n'a jamais 600 C de côté et « composer tôt » ne mesurait rien. Résultat :

| il vise | durée | écart max |
|---|---|---|
| rien | 81,6 – 85,0 min | 5,2 |
| `scribe` | 88,0 – 91,3 min | **16,6** |
| `scribe` puis `archive` | 98,3 – 101,7 min | **18,8** |

600 C à la 47ᵉ minute, c'est un prix calé pour la 78ᵉ. Le joueur qui épargne pour le poser
reste seize minutes sans rien — le double du plafond d'I4. Et il y a pire que l'attente : tant
qu'il ne peut pas payer, la paire juste coûte ses hypothèses et répond « Rien ne vient »,
exactement comme une fausse (règle 14). **Un joueur qui a vu juste à la 50ᵉ minute a toutes
les raisons de conclure qu'il s'est trompé.** Seule différence : la paire n'entre pas au
carnet, et un joueur attentif peut le remarquer.

Non réglé, et pas au simulateur de trancher : l'acheteur ne sait pas ce que « Rien ne vient »
fait à un joueur. À regarder en PT10 dans le journal d'actions — des tentatives `im+sar` avant
`copier`, et ce qui les suit.

### Une partie finie ne l'est plus

Une sauvegarde `done` à vingt glyphes aurait rouvert sur l'écran de fin, `tick` arrêté, sans
moyen de continuer — le cul-de-sac qui avait déjà coûté un changement de `KEY`. Au chargement,
une partie finie quand l'arbre était plus petit redevient une partie en cours. Chaque lot de
glyphes l'aurait reproduit ; `verifier.py` le vérifie. Les « 20 glyphes » recopiés dans le HTML
se lisent désormais dans `NGL`.

---

## Le fleuve et la cité — deux noms qu'on ne lira pas

11/09/2026. ⟨N1⟩ et ⟨N2⟩ étaient dessinés depuis le premier prototype et employés nulle
part. `docs/corpus.md` §9 laissait deux options — les semer dans les blocs comme en-têtes,
ou les supprimer. **Semés.** Chaque registre s'ouvre désormais sur le nom de ce qu'il tient,
seul sur sa ligne : la cité au-dessus des maisons et de l'archive, le fleuve au-dessus des
champs et de la veille. Le protocole de copie n'en porte pas ; il ne tient le compte de rien.

### « Très fréquentes », promettait la note

Elle se trompait. Un intitulé par bloc donne ⟨N1⟩ **13 fois** et ⟨N2⟩ **16 fois** — rangs 24
et 21 sur 48 formes, quand `tablette` en fait 318. Pour les rendre vraiment fréquents il
aurait fallu un titre courant : repris toutes les cinq lignes de registre, ⟨N2⟩ montait à 75
(rang 12) — mais ⟨N1⟩ restait à 18, parce que ses registres sont courts (quatre champs, trois
veilles). Le titre courant ne rééquilibrait donc que la cité. Retenu : un par bloc. On les
reconnaît d'une tablette à l'autre, ils ne saturent pas le registre.

Ce qui compte plus que leur rang : ⟨N1⟩ est **à l'écran dès la première seconde**, en tête des
champs des tablettes 1 à 4, et il ne se lira jamais. Les quatre tablettes d'ouverture restent
identiques entre elles — le levier de l'acte I tient.

### L'exception au principe des blocs

`docs/corpus.md` §6 interdit qu'un signe n'apparaisse que dans un bloc, « sinon la fréquence
ment ». Les deux noms n'apparaissent **que** là. L'exception est assumée : le principe protège
l'analyse de fréquence d'un signe qu'on va déchiffrer ; un nom propre ne se déchiffre pas, et
sa fréquence ne dit rien d'autre que « il revient ».

### Mesuré

Corpus : 676 → **705 lignes**, 3 809 → **3 838 signes**, 58 % lisibles au MVP (inchangé).
Gisement : 397 → **399** relevés, 13 ouverts au départ (inchangé : 27 jetons font toujours
trois relevés). Simulateur : **71,8 à 76,2 min**, écart max 5,6, contre 71,8 à 76,1 avant ; la
seule tranche d'I6 qui bouge est 30–40′ à 15 clics/min, de 9 à 12 %. PT10 juge toujours le
réglage du 09/09/2026, pas un mélange.

---

## La composition — l'indice était dans le dessin depuis le début

*10/09/2026. Première brique de la seconde moitié de l'acte III, et première tâche prise
dans la feuille de route 1.0 (E1 : COMP-1, COMP-2, COMP-5, plus la moitié réalisable de
COMP-4).*

Une grille assemble deux signes qu'on sait lire. Elle s'ouvre avec `année`, comme la
Grammaire — l'acte III a une seule porte. Elle ne dit jamais quelles paires existent : elle
dessine le signe qu'on propose, et c'est tout. Le reste est dans le corpus, où les dix-sept
composés sont dessinés comme composés depuis la toute première seconde (règle 4). ⟨grenier⟩
y porte ⟨maison⟩ et ⟨grain⟩ dans vingt-quatre lignes, et en PT9 un testeur l'avait concordé
sans pouvoir le lire. L'indice est posé depuis des mois ; il manquait l'endroit où s'en
servir.

### `COMP` ne pouvait pas servir de vérité telle quelle

Le backlog disait « la table `COMP` sert de vérité » (COMP-1). C'était faux, et ça n'a
sauté aux yeux qu'en l'ouvrant : **ses valeurs sont des clés de tracé, pas des glyphes.**
`zéro` s'y écrit `['la','u1']` — `la` est bien l'identifiant de ⟨ne-pas⟩, mais `u1` est le
trait du chiffre un, et le glyphe s'appelle `an`. La branche Nombre entière y paraît sous
ses chiffres, à cause de l'aliasage qui fait que ⟨un⟩ le mot et ⟨1⟩ le chiffre sont le même
trait.

D'où `ALIAS`, qui nomme la correspondance une fois et dans les deux sens — `sv()` la lit par
la gauche pour dessiner, la composition par la droite pour reconnaître — et `RECETTES`, qui
en dérive ce qu'on peut poser. Le filtre est le vrai travail : une recette n'existe que si
sa cible **et** ses deux parties sont au lexique. Sans lui la grille offrait `vingt`, un
signe encore dessinable mais retiré du lexique il y a six jours, et `dernière-année`
composée avec un `finir` qui n'est pas encore un glyphe. Avec lui, il reste exactement trois
recettes ouvertes aujourd'hui — `deux`, `siècle`, `grenier` — et les quatorze autres
apparaîtront d'elles-mêmes à mesure que les actes IV et V entreront au lexique. Rien à tenir
à jour, ce qui est la seule façon de ne pas diverger une troisième fois.

### Ce que coûte une erreur, et pourquoi c'est un taux

L'échec ne coûte que des hypothèses, jamais de Certitude (R3, design doc §7) : la Certitude
mesure ce qu'on a compris, et ça ne se perd pas sur une erreur.

Restait à savoir combien. Le simulateur a répondu, et la réponse a corrigé une intuition :
**le stock ne mesure rien, c'est le débit qui compte.** Il y a de l'ordre de vingt mille
hypothèses en réserve quand la grille s'ouvre, et près de quarante mille à la fin — mais
elles rentrent à six cents par minute nettes, Grammaire déduite. Un coût fixe de quelques
centaines d'hypothèses ne freinerait donc rien du tout : deux cent vingt-cinq paires
ordonnées à balayer, à une demi-minute la tentative, et le joueur qui ne lit pas gagne.

C'est encore la leçon de `REC_R` (PT4, puis le réglage du 09/09) : dans une économie
exponentielle, les coûts de base sont inertes, seuls les taux mordent. La tentative vaut
donc 250 hypothèses et croît de 40 % par paire déjà tentée. Cinq essais coûtent quatre
minutes de production, dix en coûtent vingt-sept, quinze sont hors de portée. Lire revient
structurellement moins cher que chercher — ce qui est le cœur du design (§8) et la seule
réponse honnête au risque R3.

Une paire fausse entre au carnet et ne se repaie plus. On n'empêche pas d'oublier, on
empêche de balayer.

### Le cas qui se serait trahi tout seul

Une paire juste que le joueur n'a pas les moyens de payer perd quand même ses hypothèses, et
n'entre **pas** au carnet. Le premier jet la refusait sans rien prendre — et cette gratuité
était un renseignement : l'absence de perte disait « tu viens de trouver ». Le cas est rare
(soixante certitudes à l'acte III, on les a), mais une mécanique dont le silence parle n'est
pas une mécanique.

### Deux comptes qui n'en faisaient qu'un

`grenier` est le premier signe qu'aucune branche n'offre. Il coûte 60 C, comme `année`, et
n'a **aucun effet mécanique** : on le prend parce qu'on l'a trouvé, pas parce qu'il rapporte.

C'est là qu'était le vrai danger du lot. `S_.gl.length` servait à cinq choses à la fois — la
fin de partie, les tablettes dégagées, l'exposant de la Grammaire, le gain du recoupement et
le compteur du lexique — parce qu'il n'y avait jamais eu qu'une façon d'apprendre un signe.
Un vingt-et-unième glyphe hors arbre terminait donc la partie à dix-neuf, dégageait une
tablette, et offrait 16 % de la première vraie exponentielle du jeu, gratuitement. `nArbre()`
sépare les deux : **ce que l'arbre a rendu n'est pas ce que le joueur sait.** Ce qu'il sait
se mesure ailleurs, dans le corpus, où `mesures()` compte bien le grenier — c'est justement
ce qu'il a gagné.

Mesuré après coup : 71,8 à 76,1 min, écart max 5,6, toutes les tranches d'I6 à partir de dix
minutes sous 26 %. **Chiffre pour chiffre ce qu'affichait le simulateur avant ce lot**, et
c'était le but : PT10 doit encore pouvoir juger le réglage du 09/09/2026, pas un mélange.
Composer coûte au plus 1,4 min de partie, ce qui est le prix des 60 C et de rien d'autre.

### Ce que le simulateur ne peut pas dire

S'il se trouve. Un joueur qui ne sait pas qu'il y a quelque chose à chercher regarde-t-il
assez le dessin des signes pour reconnaître ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩, et lui
vient-il l'idée de les poser l'un sur l'autre ? Aucune simulation ne répond à ça. Le journal
d'actions compte désormais les tentatives, avec leur paire et leur minute ; c'est une
question de PT10, au même titre que la crue qui baisse.

La carte de fin ne compte les compositions que si on en a tenté. Un joueur qui n'a jamais
ouvert la grille ne doit pas apprendre à l'écran de fin qu'il y avait quelque chose à y
trouver.

---

## PT9 — la concordance est allée voir l'eau

Playtest du 08/09/2026, **66 min 49** pour les vingt signes. La question posée était celle de
PT8 : *la crue qui baisse se voit-elle ?*

### Oui — pour ce joueur

Six concordances dans la partie, et les deux qui comptent arrivent au bon moment :

| | achat | concordance | délai |
|---|---|---|---|
| `avant` (la barre se range) | 48:41 | `eau` · 64 attestations | **23 s** |
| `après` (le corpus se range) | 52:54 | `eau` · 64 attestations | **5 s** |

Les quatre autres sont de l'exploration — `grain` (308 attestations), `copier` (44, puis 57
en fin de partie), et le composé `grenier` (23), concordé alors qu'il n'est pas lu. Remarque
du testeur : *« si on choisit de concorder sur eau, le fait qu'il y ait de moins en moins
d'eau devient évident »*. Le bouton est visible, il est allé chercher le bon signe, et la
colonne a dit ce qu'elle devait dire.

Réserve, posée par le testeur lui-même : c'est un joueur qui connaissait la réponse. La
question de PT8 n'est tranchée que pour lui ; elle se repose telle quelle à un joueur qui ne
sait pas ce qu'il cherche.

### I6 = 8,2 %, et toutes les tranches sont sous 30 sauf la première

111 de Certitude recoupée sur 1 347 produites.

| tranche | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 | 50–60 | 60–67 |
|---|---|---|---|---|---|---|---|
| part de la main | **75 %** | 26 % | 21 % | 22 % | 12 % | 1,4 % | 0 % |

Le mur d'ouverture reste : 75 % (83 en PT7, 63 en PT8), neuf de Certitude à la main sur douze
avant la dixième minute. Six hypothèses formulées à la main, les seules de la partie — c'est
le seul usage qui reste au bouton `formuler` : payer les deux premiers recoupements avant
qu'une Table existe.

### L'idle de fin d'acte a disparu — mais c'est le relevé qui l'a rempli

PT8 finissait sur 4 min 51 puis 3 min 52 sans une action dans le corpus. PT9 : **aucun trou
de plus de 2 min 06 après la trentième minute.** Le plus long trou de la partie est
maintenant dans l'acte II — 5 min 34, de 16:28 à 22:02, à acheter des Ateliers et des Tables.

Mais ce n'est pas la concordance qui a occupé l'acte III, c'est le relevé : **219 des 393
relevés de gisement tombent après `année`**, sur quinze tablettes ouvertes dans les
vingt-trois dernières minutes. La concordance est un geste de lecture, pas une boucle — six
usages, dont trois dans les deux minutes qui suivent `avant`. C'est son rôle, et le journal
ne lui en demande pas d'autre.

### La main fournit 36 % des occurrences — le chiffre du thésauriseur

Reconstruction des tarifs figés depuis le TSV : 2,90 millions d'occurrences relevées à la main
sur 7,98 produites, **36,3 %** — deux fois PT7 (17,9 %) et exactement ce que le simulateur
donnait au *thésauriseur* qui garde ses tablettes neuves pour la fin. Ce joueur n'a pas
thésaurisé exprès : à la trentième minute, dix-sept tablettes étaient dégagées et il n'en
avait ouvert que huit. Le tarif des quatorze dernières est le même, **11 996** par relevé —
il ne bouge plus parce que le joueur n'achète plus un producteur passé 42:31 (dernier
Copiste à 33:06) : tout va aux Tables et aux Grammaires. **99,6 % des occurrences relevées à
la main l'ont été après la vingt-cinquième minute.** Une tablette neuve vaut alors une
Grammaire : t23, 28 relevés, 336 000 occurrences, quand la dix-septième Grammaire en coûte
221 000.

Ce n'est pas un défaut d'I6 — ces occurrences traversent les Tables et les Grammaires, et
la Certitude qui en sort n'est pas manuelle. C'est un chiffre à surveiller : R9 voulait que
la tablette tardive vaille plus, et elle vaut maintenant un instrument. Si un second joueur
passe 40 %, c'est `REL_K` qu'il faudra plafonner, pas le geste.

### Le clic vide recule

**36 relevés à vide sur 429** (8 %), contre 129 sur 422 (31 %) en PT7 — première mesure
depuis la marque de la barre (07/09/2026). Ils se concentrent sur quatre tablettes épuisées
en fin de rafale (t15, t23, t26 : 7 à 8 chacune). Le point 3 de la suite descend d'un cran.

### Le recoupement est devenu la soupape des hypothèses — et c'est sans conséquence

Le stock d'hypothèses monte à **27 090** à 45:00, cinq fois les 5 232 de PT7 : entre `année`
(43:12) et la dixième Grammaire (44:15), quarante-sept Tables produisent 73 hyp./s pour
30 Concordances et 10 Grammaires qui en boivent 45. Le joueur vide le stock comme en PT7,
à la main : six recoupements de `en` à 48:00 (−14 000 hypothèses en dix secondes), deux de
`nash` à 53:36 (−10 000), un de `la` à 59:46 (−6 000). Le 49ᵉ recoupement coûte 6 343
hypothèses pour 3 de Certitude quand une Grammaire les rend pour 170 — trente-sept fois
moins bien, et il le fait quand même.

La différence avec PT7 : ça ne pèse rien — 1,4 % de la Certitude de la tranche. La
Grammaire répare le déversoir dès qu'il y en a assez ; les cinq minutes qui suivent `année`
n'en ont pas encore assez. 49 recoupements sur onze signes (`en` 11, `nuit` 8, `shen` 7),
sept des onze ne s'achètent pas, comme en PT6 et PT7.

### Le simulateur surestimait de 20 %, et c'était son acheteur

Deuxième écart franc dans le même sens : 78,6 à 83,5 min annoncées pour 66:49 (PT9) et
63:12 (PT8). Ce n'est pas la main — faire thésauriser le simulateur déplace la durée de
moins de deux minutes. C'est l'**acheteur** : il prenait ce qui passait sous sa main, donc
jamais un Atelier à 1 800 tant qu'un Copiste, une Table ou une Concordance à 900 était
payable. Premier Atelier simulé à la 24ᵉ minute contre la 10ᵉ pour le joueur ; 84 Copistes
en fin de partie contre 50 ; 16 Grammaires contre 22.

**Recalé (08/09/2026)** : l'acheteur compare le rendement par occurrence du Copiste et de
l'Atelier, et **épargne** pour l'Atelier quand il rend plus — sur un socle de 30 Copistes
(`ate_socle` ; le joueur en avait 22 au premier Atelier, 35 à la 14ᵉ minute). Une première
version sans socle bloquait toute la chaîne à 18 occ./s pendant quatre-vingts minutes :
épargner, c'est aussi ne rien acheter d'autre.

| `python outils/sim.py` | 5 clics/min | 15 | 40 |
|---|---|---|---|
| durée, 20 glyphes | 76,6 min | 72,4 min | 71,0 min |
| écart max entre deux signes | 5,7 min | 5,7 min | 5,7 min |
| part manuelle des Occurrences | 24,9 % | 21,6 % | 21,5 % |
| I6, tranche 0–10 | 100 % | 85 % | 81 % |
| I6, tranches suivantes | ≤ 36 % | ≤ 35 % | ≤ 31 % |

L'écart passe de +20 % à **+6 à 15 %**, et les bâtiments de fin (56/56/38/36/18) ressemblent
enfin à ceux d'une partie (50/60/30/30/22). Le thésauriseur coûte maintenant 2,1 minutes
pour 24,2 % des occurrences. Ce qu'il ne reproduit toujours pas : les 36 % de la main — il
ouvre les tablettes à mesure qu'elles sortent, au tarif du moment.

### Ce que le gisement dit

393 sur 397 : seule la tablette 30 reste intacte, et elle ne se dégage qu'au vingtième signe.
Vingt-neuf tablettes relevées, 23 sauts de barre. Rythme d'actions : 10,9 par minute.

---

## La concordance — l'instrument fait enfin ce que son nom annonce

Réponse au défaut central de PT8 : **le rangement chronologique n'a pas suffi.** Il ordonne
les contenants, il ne rassemble pas le signal.

### Le chiffre qui explique l'échec

**Soixante lignes du corpus portent un relevé d'eau, sur six cent soixante-seize.** Entre
deux relevés consécutifs, le corpus rangé intercale de **huit à cinquante-sept lignes** de
registre. Trier les tablettes met les eaux dans le bon ordre ; ça ne les met pas côte à
côte, et une série ne se lit pas à un relevé par écran.

Et le journal d'actions donne mieux qu'une hypothèse : à **44:57**, treize secondes après
avoir acheté `avant`, le joueur est allé sur la **tablette 26** — le relevé d'eau complet,
vingt-deux années dans un seul document, lisible depuis la 38ᵉ minute — et y a fait vingt
relevés sans voir la série. **Le défaut n'était donc pas que la donnée soit illisible :
c'est que la lecture n'était pas assemblée.**

### Ce que fait la Concordance

Une concordance, en philologie, est le relevé de toutes les attestations d'un mot avec leur
contexte. L'instrument porte ce nom depuis l'acte II, on en achète trente-huit dans une
partie, et il ne faisait rien de visible. Il fait maintenant son métier : **choisir un signe
replie le corpus sur ses seules attestations**, dans l'ordre d'affichage courant, chaque
tablette gardant sa première ligne — celle où elle se numérote et se date elle-même.

Rien n'est ajouté, rien n'est commenté (règle 5 tenue : la date affichée est du texte
ancien). Sur `eau`, corpus rangé, la colonne donne :

```
tablette 1 · année 9        eau 14
tablette 2 · année 12       eau 13
tablette 3 · année 19       eau 15
tablette 4 · année 27       eau 12
tablette 7 · année 54       eau 11
…
tablette 25 · année 207     eau 2
tablette 27 · année 211     eau 1
tablette 29 · dernière-année  eau 0
```

**92 lignes au lieu de 676**, et vingt relevés qui descendent de 14 à 0. Le bruit des bonnes
années reste — 15 en 19, 12 en 71, 10 en 112, 6 en 183 : c'est une vraie série, pas une
pente.

Trois décisions dans le détail :

- **Un signe inconnu se concorde aussi bien qu'un signe lu.** C'est même là que l'instrument
  sert le plus : rassembler les contextes d'une forme qu'on ne sait pas encore lire est le
  geste de l'épigraphiste, et le pendant du comptage d'occurrences de la Table de fréquences.
- **Le bouton vit dans l'en-tête du corpus, pas dans « À la main ».** Ce n'est pas le joueur
  qui rassemble les attestations, c'est son instrument — et il n'existe qu'à partir de la
  première Concordance achetée.
- **Le rangement reste la condition.** Sans `avant`/`après`, la concordance de `eau` donne
  la même colonne dans l'ordre de sortie de terre, où elle ne dit rien. L'acte III garde
  donc ses deux temps : dater, ranger — puis rassembler.

### Deux défauts de contenu, trouvés en écrivant la vue

1. **La tablette 26 citait son propre avenir.** `veille(209, EAU)` recevait la série entière
   au lieu de la filtrer à la date de la tablette, comme le font les tablettes 6 et 15 : une
   scribe de l'an 209 y relevait les années 211 et 213, et sa première ligne se datait de
   209 en portant la crue de 213. Sans conséquence tant que personne ne lisait le bloc comme
   une série ; la concordance le met au premier plan, deux lignes au-dessus de « avant ·
   tablette 6 · faux ». Corrigé. Le corpus passe de 678 à **676 lignes**, de 3 825 à
   **3 809 signes**, et le gisement total de 398 à **397**.
2. **`outils/corpus.py` ne pouvait pas écrire sur une console cp1252** — la flèche de
   l'en-tête généré suffisait à le tuer. Le script qui produit `src/corpus.js` dépendait de
   la locale de la machine. `encoding='utf-8'` explicite.

---

## PT8 — le rangement ne suffit pas

Première partie des trois actes, **63 min 12** pour les vingt signes.

### Le simulateur surestime de 20 %

Il annonçait 78,6 à 83,5 minutes. C'est le premier écart franc dans ce sens : jusqu'ici il
sous-estimait (PT5) ou tombait juste (PT6). Écart maximal entre deux déblocages : **5 min
32** — I4 tient. L'acte III seul (de `année` à `dernière-année`) : 24 min 46 pour sept
signes, 3,5 min chacun.

### I6 = 6,0 %, et le simulateur a vu juste

114 de Certitude recoupée sur ~1 902 produites, contre 5 % annoncés. Par tranches de dix
minutes :

| tranche | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 | 50–60 | 60–63 |
|---|---|---|---|---|---|---|---|---|
| part de la main | **63 %** | 0 % | 33 % | 28 % | 2,6 % | 0 % | 1,9 % |

**Le déversoir de fin de PT7 est réparé** — la Grammaire absorbe les hypothèses que les
Concordances laissaient s'entasser, et la part manuelle des cinq dernières minutes passe de
103 % à 1,9 %. Le mur d'ouverture reste, à 63 % (contre 83 % en PT7, mais par différence de
conduite : ce joueur-là n'a recoupé que cinq fois avant la dixième minute).

### L'acte III finit en idle — le risque annoncé s'est réalisé

Les trois derniers signes se paient en attendant. **Entre 49:32 et 54:23, puis entre 54:28
et 58:20, aucune action dans le corpus** — 4 min 51, puis 3 min 52. Le joueur achète des
Grammaires, regarde monter la Certitude, achète un signe, recommence.

C'était la réserve n°2 posée en livrant l'acte III : *« I6 tombe à 5 % ; ce n'est acceptable
que si dater et ranger remplacent le geste de lecture qu'on retire au recoupement. »* Ils ne
l'ont pas remplacé, parce que dater et ranger sont des gestes qu'on fait **une fois**. La
concordance est un geste qu'on refait — et c'est à ce titre autant qu'au titre de la trame
qu'elle entre dans le jeu.

### Ce que le gisement dit

**394 relevés de gisement consommés sur 398** (293 en PT7) : le relevé va maintenant au bout
du corpus. R9 tient, et la main reste un vrai moteur d'occurrences jusqu'à la fin. *(Les
comptes d'actions par genre n'ont pas été extraits cette fois : les chiffres ci-dessus
sortent des lignes d'état et des achats, pas d'un dépouillement complet du TSV.)*

---

## L'acte III — le temps, et le corpus qui se range

Première moitié de l'acte : la branche **Temps** (six glyphes), `mille`, l'instrument
**Grammaire**, et le sommet dramatique — la datation puis le réordonnancement chronologique
des tablettes. Le lexique passe de 13 à **20 signes sur 45**.

### Pourquoi la datation d'abord

Trois raisons, dans cet ordre :

1. **C'est le risque.** Si le rangement chronologique ne fait rien au joueur, le reste de
   l'acte est de la décoration. Les sept playtests ont tous servi à tester la chose risquée
   tôt ; celle-ci ne fait pas exception.
2. **Elle ne coûte aucun texte neuf.** Chaque tablette portait déjà sa date dans sa
   première ligne — « tablette 12 · année 103 » — depuis la première seconde du prototype.
   Le jeu n'ajoute rien : il rend lisible ce qui était là. C'est la règle 5 respectée à la
   lettre, et c'est aussi ce qui rend le moment juste.
3. **La brique existait.** La barre de tablettes a été faite pour ça (07/09/2026).

### Ce que `année` change, et ce qu'elle ne change pas

Une tablette est datée quand le joueur sait lire sa date : le mot **et** chacun des signes
du nombre. Les cinq glyphes de nombre étant acquis à la fin de l'acte II, les vingt-huit
dates tombent d'un coup à l'achat d'`année`. Les deux dernières ne portent aucun nombre —
elles disent « dernière-année », et c'est ce glyphe-là, dernier de la branche, qui les date.
*Après elle, personne n'a plus compté.*

**Dater ne range pas.** `avant` range l'index, `après` range le texte. Deux gestes
d'archiviste, dans cet ordre : on trie ses fiches avant de déplacer les tablettes. Le
premier est bon marché et déjà spectaculaire ; le second est celui qui met deux siècles de
crue en colonne.

### Ce que le rangement démontre

Une fois trié, l'ordre chronologique **est** l'ordre des numéros : 1, 2, 3 … 30. Le corpus
se numérote lui-même dans l'ordre où il a été gravé.

Ce n'est pas un raccourci d'implémentation, c'est le fond du sujet, et il fallait le voir
pour le comprendre : le joueur savait lire les numéros depuis `tablette` (acte II) et n'en
pouvait rien conclure — un numéro peut être un rang d'étagère, un ordre d'inventaire,
n'importe quoi. Ce sont les dates qui prouvent que la numérotation était chronologique,
donc que l'archive était **ordonnée**, donc que quelqu'un l'avait rangée exprès. La
découverte n'est pas « voici l'ordre caché » mais « l'ordre était affiché depuis le début
et je ne pouvais pas le savoir ». C'est exactement la thèse du jeu, et c'est le seul
endroit du prototype où elle se démontre au lieu de s'énoncer.

Le déclin de la crue, lui, n'est commenté nulle part : 14, 13, 15, 12, 13, 11, 12, 10, 9,
10, 8, 7, 8, 6, 5… c'est dans les chiffres, et il faut les avoir mis en ordre pour le voir.
La carte de fin ne pose plus qu'une question, et c'est celle-là.

### La Grammaire, et ce qu'elle répare

Premier instrument dont le rendement dépend de ce que le joueur a **compris** :
`0,0012 × 1,16^lexique` certitude par seconde et par unité — la première vraie exponentielle
du jeu (design doc §5). À 13 signes elle vaut une Concordance ; à 20, quatre.

Elle boit surtout **six fois plus d'hypothèses** qu'une Concordance (3/s contre 0,5), et
c'est le correctif du défaut mesuré en PT7 : la chaîne produisait plus d'hypothèses que les
Concordances n'en consommaient, le stock est monté à 5 232, et le joueur l'a vidé à la main
en douze recoupements. Sans instrument capable d'absorber ce débit, l'action manuelle
redevient la soupape — c'est le mode de défaillance de PT1 et PT2, sous une troisième forme.

Elle reste fermée jusqu'à `année` : **on n'a pas de grammaire avant d'avoir un temps.**

### La nuit

`nuit` débloque la progression hors ligne — 40 % du débit, quatre heures au plus. C'était le
dernier écart assumé du MVP (« pas de progression hors-ligne, conforme : `nuit` est un signe
d'acte III ») ; il est refermé. La nuit est consommée à son crédit, sinon rouvrir deux fois
la même sauvegarde la paierait deux fois. Elle ne passe pas par l'horloge du jeu : le
chronomètre mesure du temps de lecture, pas du temps d'absence.

### Mesures (`python outils/sim.py`)

| | 5 clics/min | 15 | 40 |
|---|---|---|---|
| durée, 20 glyphes | 83,5 min | 79,9 min | 78,6 min |
| écart max entre deux signes | 6,2 min | 6,2 min | 6,2 min |
| part manuelle des Occurrences | 23,5 % | 20,3 % | 20,4 % |
| I6 sur la partie entière | 5 % | 5 % | 5 % |

I4 tient — jamais plus de 8 minutes sans déblocage. L'acte III ajoute une trentaine de
minutes pour sept signes : 4,3 min par signe, dans la fourchette visée.

**Le thésauriseur reste puni** : garder les tablettes neuves pour la fin donne 36 % des
occurrences au lieu de 20, et coûte 2,4 minutes. C'était 42,5 % avant l'acte III.

### I6 tombe à 5 %, et ce n'est pas une bonne nouvelle en soi

Le plafond est un plafond, pas un plancher — mais la Grammaire écrase à ce point la
production de Certitude que le recoupement, seul geste de lecture des actes I et II, ne pèse
plus rien après la cinquantième minute. **C'est acceptable à une condition** : que l'acte III
apporte son propre geste de lecture, et il l'apporte — dater, ranger, relire la série. Si
PT8 montre un acte III qui se joue sans jamais toucher au texte, c'est ce point-là qu'il
faudra reprendre, et non le plafond.

### Ce qui reste de l'acte III

- **`zéro` et la composition** (`ne-pas` + `un`) — la grille de composition n'existe pas
  encore ; `zéro` n'est accessible que par elle et ne peut donc pas être livré avant.
- **L'Élève**, instrument ambivalent : il multiplie tout et se trompe. Il appartient au même
  chantier que les lectures fausses (acte IV) et n'a pas de sens sans elles.
- **Les quatre glyphes de Parole III** (`lire`, `scribe`, `archive`, `les-lecteurs`) et la
  branche **Modalité** — c'est la seconde moitié de l'acte, et c'est du texte à écrire avant
  d'être du code.

---

## PT7 — R9 tranché : la main revient dans le corpus

Playtest du 07/09/2026, 44 min 50. La question posée à PT7 était celle de R9 : le tarif figé
à la première visite donne-t-il envie d'aller ouvrir une tablette neuve en fin de partie ?
Ni le simulateur ni le rejeu de PT6 ne pouvaient le dire.

### Oui, et largement

| | PT6 | PT7 |
|---|---|---|
| relevés | 180 | 422 |
| part des occurrences produites | 0,1 % | **17,9 %** |
| tablettes touchées | 3 | **22** |
| gisement consommé | 54 / 398 | **293 / 398** |
| dernier relevé | 15,5 min | **40,1 min** |

Les tarifs figés, mesurés dans la partie : t1 à **1** occurrence par relevé, t16 (23ᵉ min) à
**128**, t22 à 484, t10 (31ᵉ min) à **777**, t25 à 1 216, t18 (40ᵉ min) à **1 362**.
**95 % des occurrences relevées à la main l'ont été après la vingt-cinquième minute** — la
raison de parcourir le corpus tard existe, et elle se voit sans qu'on l'explique. Le
simulateur annonçait 14 à 19 % ; le joueur réel s'est posé à 17,9 %, alors même que le
simulateur ne pouvait pas modéliser le changement de conduite qu'il mesurait.

### I6 = 31,2 %, et la moyenne ne veut plus rien dire

74 de Certitude recoupée sur 237. Premier dépassement depuis PT4 — mais découpé par
tranches de dix minutes, le nombre global se révèle être une moyenne qui cache deux défauts
opposés :

| tranche | C recoupée | C produite | part |
|---|---|---|---|
| 0–10 min | 10 | ~12 | **83 %** |
| 10–20 | 14 | ~30 | 47 % |
| 20–30 | 14 | ~44 | 32 % |
| 30–40 | 0 | ~68 | **0 %** |
| 40–45 | 36 | ~35 | **103 %** |

1. **Le mur des dix premières minutes**, déjà noté après PT5, maintenant chiffré sur un
   joueur réel : 83 %. Aucune Concordance n'existe encore ; toute la Certitude est à la main.
2. **Un déversoir en fin de partie** : les hypothèses montent à **5 232** à la quarantième
   minute — vingt-neuf Concordances n'en boivent que 14,5 par seconde quand trente-six
   Tables en produisent 28 — et le joueur les convertit à la main en douze recoupements sur
   quatre minutes. **C'est ce seul creux qui fait passer I6 de 29 à 31,2 %.** La Grammaire
   de l'acte III est la réponse.

**Décision : I6 se mesure désormais par tranches de dix minutes**, dans `outils/sim.py`
comme dans le dépouillement. Un invariant qui se pose à 30,0 % en PT6 en cachant un 83 % et
un 103 % n'est pas un instrument, c'est une moyenne. La règle 2 de `CLAUDE.md` est réécrite
en conséquence.

### Un tiers des relevés tombe dans le vide

**129 relevés sur 422 portent sur un gisement épuisé** et ne rendent que le plancher — t7 :
64 relevés pour 27 gisements. La barre éteint bien la cellule d'une tablette épuisée, mais
dans le texte rien ne dit qu'un jeton ne rapporte plus rien. Le rythme d'actions remonte à
10,4 par minute contre 5,7 en PT6, dont un tiers de clics vides. À traiter : c'est un défaut
de retour d'interface, pas d'équilibrage.

### Le recoupement tient toujours le texte

39 recoupements sur 8 signes distincts — `nur` (8), `shen` (6), `la` (6), `tem`, `sar`,
`tab`, `kish` (4 chacun), `zur` (3). **Quatre de ces huit ne s'achètent pas** : le joueur
les a choisis parce qu'ils étaient commodes à retrouver, comme en PT6. Écart médian entre
deux recoupements : 12 secondes.

---

## PT6 — le recoupement tient, le relevé non

Premier playtest des deux actions portées dans le corpus.

### La partie a raccourci

**43 min 49**, la plus courte des six parties menées au bout, et la première dans la fenêtre
visée. C'était la question ouverte : le recoupement passé de « une pression sur un bouton »
à « deux clics et une navigation » allait-il allonger la partie ? Le simulateur, qui ne
modélise aucun coût d'interaction, annonçait 44,4 à 51,3 min. Le joueur réel s'est posé
**sous** la borne basse.

La réponse est donc non, et mieux que non : la partie a gagné sept minutes sur PT5 tout en
passant de 681 à **251 actions manuelles** (5,7 par minute contre 13,5). L'enchaînement y
est pour beaucoup — 21 des 43 intervalles entre deux recoupements tiennent en moins de
30 secondes.

### I6 = 30,0 %

71 de Certitude recoupée sur 237. Exactement au plafond, sans marge. Le simulateur annonçait
29 à 30 % et cette fois il a vu juste — en PT5 il sous-estimait de trois points. Un
instrument qui se trompe dans un sens puis pas dans l'autre n'est pas un instrument de
précision : il donne l'ordre de grandeur, la mesure tranche.

### Le recoupement fonctionne

44 recoupements sur **12 signes distincts**, en chaînes de 1 à 9 (médiane 2) — le joueur
suit bien un signe de tablette en tablette comme le geste l'y invite.

| signe | fois | | signe | fois |
|---|---|---|---|---|
| en | 9 | | nm5 | 3 |
| tab | 8 | | gan, lash, imme, zur | 2 |
| pat | 6 | | shen, nm3 | 1 |
| tem, ur | 4 | | | |

Et le point qui compte : **8 de ces 12 signes ne sont pas dans le lexique des 13 glyphes.**
`en`, `pat`, `nm5`, `lash`, `imme`, `zur`, `shen`, `nm3` ne s'achètent pas, ne rapportent
aucun bonus, n'ouvrent aucun texte. Le joueur les a choisis parce qu'ils étaient commodes à
retrouver. C'est la première fois qu'un journal de playtest montre quelqu'un travaillant sur
**le texte** plutôt que sur la liste de courses.

### Le relevé, lui, est retombé à 0,1 %

| | PT5 (bouton) | PT6 (corpus + gisement) |
|---|---|---|
| relevés | 371 | 180 |
| part des occurrences produites | 0,6 % | **0,1 %** |
| gisement consommé | — | 54 / 398 |
| dernier relevé | 42,9 min *(sur 50,6)* | **15,5 min** *(sur 43,8)* |

Le déplacement dans le corpus a rendu le relevé **moins** utile, pas plus. La cause est le
correctif anti-thésaurisation lui-même : le tarif d'une tablette est figé à son dégagement,
donc les tablettes accessibles tôt — les seules que le joueur relève — valent 1 ou 2
occurrences pour toujours. Les tarifs mesurés dans cette partie : t1, t2, t3, t4 à **1**,
t8 à 2, t16 à 25, t10 à 42. Le gisement cher n'apparaît qu'une fois les Occurrences
devenues sans objet.

Le simulateur annonçait 14 à 19 % parce qu'il modélise un joueur qui vide d'abord la
tablette la mieux payée et épuise 388 gisements sur 398. Le joueur réel en a consommé 54,
là où il se trouvait, au début.

Ce n'est pas un échec du geste — c'est un échec de la prétention. Le relevé dans le corpus
est honnêtement une **mécanique d'ouverture** : il amorce les premiers Copistes, puis on
l'abandonne. Le vouloir « acte de lecture » était l'erreur ; l'acte de lecture, c'est le
recoupement, et lui tient. Reste que la machinerie du gisement — tarifs figés, 398
compteurs, épuisement, extinction dans la barre — est un échafaudage considérable pour
quelque chose qui ne pèse plus rien après la quinzième minute. **Tranché : R9, ci-dessous.**

### R9, 06/09/2026 : le tarif se fige à la première visite

Une tablette n'est plus tarifée quand elle sort de terre, mais **au premier relevé qu'on y
fait**. Arriver sur une tablette restée intacte vaut donc ce que vaut la production du
moment — et cela change tout ce que la règle propose au joueur :

| ouvrir une tablette neuve… | par relevé | une tablette de 14 gisements |
|---|---|---|
| à 0′ (tablettes du départ) | 1 occ. | 14 |
| à 20′ | 543 occ. | 7 602 |
| à 30′ | 1 143 occ. | 15 997 |
| à 40′ | 1 581 occ. | 22 139 |

Dans la partie de PT6, **23 tablettes n'ont jamais été touchées, 322 gisements intacts**.
Aux tarifs de la trentième minute, elles valaient à elles seules 53 % de la production de
la partie. La raison de parcourir le corpus après la quinzième minute existe désormais ;
reste à savoir si elle se voit.

#### Ce que ça règle, et ce que ça ne règle pas

**Rejouer PT6 à comportement identique donne 0,3 % au lieu de 0,1 %.** La règle seule ne
change presque rien : elle ne vaut que si le joueur change de conduite. C'est une borne
basse, pas une prédiction — PT6 n'avait aucune raison d'aller ouvrir une tablette neuve,
puisqu'il n'y avait rien à y gagner.

Le simulateur, dont le flâneur travaille chaque tablette à mesure qu'elle sort, ne bouge
pas non plus : 43,9 à 51,4 min, I6 28,7 à 30,0 %, la main à 13,9–19,2 %. Pour lui,
première visite et dégagement tombent au même instant. Il ne peut donc pas trancher cette
question-là ; c'est PT7 qui le fera.

#### Le thésauriseur, et pourquoi on l'accepte

L'exploit revient : garder les tablettes neuves pour la fin donne **42,5 %** des occurrences
au lieu de 19, et pousse I6 à **32,5 %**, au-dessus du plafond. Mais il se punit tout seul —
faute des occurrences du début, le simulateur lui fait finir la partie **4,7 minutes plus
tard** (48,6 contre 43,9 min). Les Occurrences ne sont pas la condition de victoire ; le
temps mis à déchiffrer treize signes l'est. Optimiser la mauvaise ressource coûte du temps.

On l'accepte donc, en le sachant, avec deux chiffres à surveiller en PT7 : I6, et la part
de la main. `REL_K` reste à 1,2 — on ne rerègle pas une constante en même temps qu'on change
une règle.

#### Le piège qu'elle crée

Relever une seule fois une tablette au début la fige à son tarif de misère, définitivement.
Les treize relevés d'ouverture condamnent ainsi les quatre premières tablettes. C'est
cohérent (on ne tarife qu'une fois) mais ce n'est pas intuitif, et rien ne prévient.

### La marque, 07/09/2026 : ce qui a été lu recule

R9 n'était pas testable en l'état. La seule chose qui distinguait une tablette intacte
d'une tablette travaillée était l'infobulle — il fallait survoler les cellules de la barre
une par une pour découvrir qu'une différence existait. Jouer PT7 comme ça et n'ouvrir
aucune tablette neuve n'aurait rien tranché : on n'aurait pas su si c'est la règle qui ne
tente pas, ou si c'est qu'elle est invisible. Un playtest qui ne peut pas répondre à sa
propre question ne vaut pas la peine d'être joué.

La barre porte donc désormais l'échelle du gisement en entier : **intacte**, la cellule
reste pleine ; **lue**, elle rentre dans le fond ; **épuisée**, elle s'éteint comme avant.

C'est la tablette *lue* qui porte la marque, et non l'intacte, contre l'intuition. Deux
raisons :

- **l'intacte est le cas général** — PT6 n'a touché que 3 tablettes sur 26. Un signe porté
  par presque tout ne signale rien. Ce qui instruit, c'est de voir reculer ce qu'on a lu :
  on comprend que le corpus s'use, donc qu'ailleurs il ne l'est pas.
- **marquer l'intacte l'aurait fait monter**, et en montant elle heurtait le survol, qui
  monte aussi, et l'ocre de `touche` — la tablette où un signe fraîchement acheté apparaît —
  qui prend déjà le cadre et le numéro. Or `touche` s'allume exactement au moment où le
  joueur regarde la barre pour décider où aller : la marque y aurait disparu au pire
  moment. Descendre ne heurte personne.

L'infobulle chiffre ce que la marque ne peut que suggérer, et pour une intacte elle donne
le tarif **du moment** : « intacte : 1 143 occ. par relevé si tu l'ouvres maintenant ».
Ce tarif suit la production et ne peut donc pas être figé dans l'attribut — il s'écrit au
survol. Accessoirement, cela supprime la reconstruction de trente titres par image.

Au passage, un défaut plus ancien : `paintRail` n'était appelée qu'au chargement et à
chaque glyphe acquis, jamais sur un relevé. L'extinction d'une tablette épuisée ne se
voyait donc qu'au glyphe suivant. Les deux axes de la cellule se repeignent maintenant
séparément — la lisibilité à chaque glyphe (elle recompte les 3 809 signes), le gisement à
chaque relevé (deux classes) — parce que les recompter à chaque clic coûterait cent fois
le prix.

**Ce que ça ne fait pas** : la marque dit « ici, c'est lu », pas « là-bas, ça vaut mille
occurrences ». Le chiffre reste dans l'infobulle, donc derrière un survol. Si PT7 montre
que le joueur ne va toujours pas ouvrir de tablette neuve, c'est là qu'il faudra regarder.

### Le blocage volontaire

Partie sacrifiée exprès : cliquer tous les signes et ne formuler que des hypothèses, pour
voir si l'on peut s'enfermer. **On ne peut pas** — le plancher permet de recliquer le même
signe indéfiniment. Le garde-fou tient. Mais il tient lentement : dans cette partie, le
premier Copiste n'est arrivé qu'à **156 minutes** de temps de jeu. Et en partie normale, les
13 relevés du gisement d'ouverture sont épuisés en **2 min 30**.

### Défauts trouvés

1. **Armé sans les ressources, le joueur était enfermé.** Le bouton désactivé ne pouvait
   plus désarmer, et le corpus armé ne relevait plus : seule échap sortait, et rien ne le
   disait. Corrigé — le bouton ne se désactive que pour empêcher d'*armer*, jamais de
   désarmer, et il annonce « pas de quoi recouper ».
2. **Un test de `verifier.py` passait par chance.** Le premier relevé d'état est journalisé
   au démarrage du journal, donc son écart au deuxième valait ce qui restait à courir
   jusqu'au prochain multiple de 30 — entre 0 et 30 s selon la durée du reste de la
   vérification. Horloge fixée, régularité contrôlée à partir du deuxième relevé.

## Le comptage d'occurrences dans le lexique

Fait après PT4. Chaque tête de branche encore à acheter affiche le nombre d'occurrences de
son signe dans le corpus, à côté de son coût. Le joueur compare enfin deux grandeurs au
lieu d'une :

```
NOMBRE     ⋁  544 occ.   11        MATIÈRE   ⇑  315 occ.    3        PAROLE   ⋔  2 occ.   8
```

Conditionné à la **Table de fréquences** — l'instrument fait alors visiblement ce que son
nom annonce, et c'était la seule chose qu'il ne faisait pas.

### Compter les signes, pas les mots

Le piège était là. Les cinq glyphes de la branche Nombre n'apparaissent presque jamais
comme *mots* dans le corpus — mais leur signe est partout **dans les nombres** :

| | comme mot | comme chiffre | total |
|---|---|---|---|
| un | 8 | 1 660 | **1 668** |
| dix | 2 | 1 456 | **1 458** |
| cinq | 0 | 544 | **544** |
| cent | 1 | 184 | **185** |
| grain | 315 | — | 315 |
| dire | 2 | — | 2 |

Un comptage des mots seuls aurait affiché **8, 4, 0, 2, 1** sur les cinq glyphes de nombre
et fait passer la branche la plus rentable du jeu pour la plus pauvre. `freqGlyphe()`
(`src/rendu.js`) additionne donc les deux, et trois contrôles de `outils/verifier.py`
verrouillent les valeurs.

### Le point aveugle de `deux`, et pourquoi il ne se voit pas

`deux` est le seul glyphe dont le comptage mentirait vraiment : il n'ouvre aucun signe de
numération, il ouvre le **principe du redoublement**, qui vaut à lui seul +848 signes
lisibles. Une table de fréquences ne peut pas savoir ça — c'est une limite honnête de
l'instrument, pas un défaut à masquer.

Elle ne se voit pas, parce que le comptage est aussi conditionné à `deux` : sans lui le
nombre affiché serait lui-même illisible. Quand le compteur apparaît, `deux` est déjà
acquis. La contrainte de lisibilité règle le problème d'équilibrage — heureux hasard,
mais à ne pas défaire par mégarde.

### Ce que PT5 devait regarder

Le compteur rend visible ce que le tableau des rendements disait : **`dire` coûte 8 C et
affiche « 2 occ. »**. C'est vrai, et c'est exactement la tension des « trois monnaies » —
Parole ne rapporte pas du texte, elle rapporte des *pouvoirs* (`dire` fait parler le
lexique, `maison` nomme les instruments), mais elle est tarifée et présentée comme si elle
rapportait du texte. Le risque est net : le joueur, muni de l'outil qu'on vient de lui
donner, contourne durablement la branche Parole.

À observer en PT5 : la branche Parole est-elle repoussée plus loin qu'avant ? Si oui, la
réponse n'est pas de retirer le compteur — c'est de faire de Parole une vraie troisième
monnaie, et de cesser de la faire payer au poids du texte.

*Réponse : non, et pour une raison qu'on n'avait pas prévue. Voir PT5 ci-dessous.*

## PT5 — le compteur ne décide rien, et la main non plus

Deux parties : une abandonnée à 10:17, une menée au bout en **50 min 37**, treize glyphes
sur treize. 1 099 entrées au journal.

### I6 : 30,8 %, et une ouverture à 100 %

| | avant PT4 | réglage R6, simulé | PT5, mesuré |
|---|---|---|---|
| durée | 53,3 min | 52,7 min | 50,6 min |
| recoupements | 57 | — | 46 |
| part manuelle de la Certitude | 43,5 % | 27,8 % | **30,8 %** |

Le réglage tient : de 43,5 % à 30,8 %, sans allonger la partie — la durée mesurée tombe
même dans la fenêtre annoncée par le simulateur (50,6 contre 50,6–55,1). Le simulateur
sous-estime la part manuelle de trois points, ce qui est la bonne direction pour un
instrument de contrôle : il joue plus proprement qu'un joueur, donc il flatte. **À traiter
désormais comme un plancher, pas comme une prédiction.**

L'invariant est tenu sur la partie entière et complètement violé sur son ouverture :

> Sur les dix premières minutes, la Certitude produite est de 23 — dont **23 recoupées à la
> main**. La Concordance n'est achetée qu'à 9:46.

Le jeu ouvre sur dix minutes de cliqueur pur, puis bascule. C'est exactement là que la
première partie a été abandonnée : cinq glyphes, 20 % de signes, palier suivant à 11 C
quand un recoupement en rapporte 1. I6 mesuré sur la partie entière ne voit pas ce mur ;
il faudra le mesurer par tranches.

### Le compteur d'occurrences n'a pas servi

Ordre d'achat : `un → grain → deux → maison → dire → cinq → tablette → eau → dix → graver
→ cent → champ → copier`. C'est l'ordre du prix croissant, à une inversion près — et
l'inversion va **contre** le compteur :

| à 27 min | coût | affiché | choix |
|---|---|---|---|
| dix | 18 C | 1 458 occ. | — |
| **eau** | **22 C** | **70 occ.** | **acheté** |
| graver | 27 C | 56 occ. | — |

`dix` était achetable depuis 26:00. Il a attendu une minute de plus pour prendre `eau`,
plus cher et vingt fois plus rare. Et `dire` — 2 occurrences, 8 C, le pire rendement
textuel du jeu — a été acheté à son rang de prix, sans hésitation lisible dans les
horodatages.

La cause est dans le journal : `dire` est acheté à 10:27, et `dire` **affiche l'effet des
glyphes non achetés**. À partir de là, la carte porte trois informations — le signe,
« 70 occ. », et « +30 % à la table de fréquences ». C'est la troisième qu'il a lue.

Ce qui répond à la question laissée ouverte par PT4, mais pas comme on l'attendait :
**le joueur n'achète déjà pas du texte, il achète un bonus.** Décorréler les bonus des mots
ne créerait pas le choix — cela déplacerait l'étiquette que le joueur lit, rien de plus. Un
comptage d'occurrences ne pèse pas contre un pourcentage de production affiché sur la même
carte ; au mieux il départage deux effets équivalents. Si l'on veut que le texte pèse dans
l'achat, il faut qu'il y ait quelque chose à gagner *en texte* — c'est-à-dire des glyphes
sans effet chiffré du tout.

Réserve : un joueur, une partie. À reconfirmer avant d'en tirer une refonte.

### Le relevé manuel est décoratif, et le jeu ne le dit pas

681 actions manuelles en 50 minutes, 13,5 par minute, contre 56 relevés au total en PT4.
Même jeu, deux joueurs, un facteur sept. Le barème est `1 + 3 % du débit brut`, écrit pour
que le relevé « reste utile sans être la colonne vertébrale ». Mesuré sur la partie :

| | occurrences produites | part |
|---|---|---|
| instruments | 672 433 | 99,4 % |
| à la main | 4 323 | **0,6 %** |

3 % du débit *par seconde*, c'est **0,06 seconde de production par clic** : il faudrait
cliquer dix-sept fois par seconde pour égaler les machines. Le commentaire dans
`economie.js` disait le contraire de ce que la formule fait ; il a été corrigé.

Ce n'est pas un défaut d'équilibrage — le relevé ne produit pas de Certitude, I6 n'est pas
menacé. C'est un défaut d'information : le bouton **grossit sa récompense affichée** (26
occurrences à 40 min, contre 1 au départ) exactement pendant qu'elle devient sans effet, et
rien à l'écran ne dit que la main a cessé de compter. Un enfant a passé un tiers de sa
session à cliquer un bouton qui ne faisait rien.

Trois issues étaient ouvertes : afficher la part manuelle du débit à côté du bouton ;
faire plafonner le relevé franchement ; ou accepter le clic comme défouloir. Aucune des
trois n'a été retenue — voir la section suivante, qui déplace le geste au lieu de le
retarifer.

### Ce que le journal montre d'autre

- **La barre de tablettes fait son travail.** 28 navigations, groupées juste après les
  achats de numération : quatre tablettes après `dix`, **dix tablettes en seize secondes
  après `cent`**. Nouvelle lisibilité → il va voir. C'est le seul endroit du journal où
  l'on voit quelqu'un *lire*.
- **Le milieu de partie est vide.** Entre 15 et 30 minutes : les signes passent de 20 % à
  33 %, aucun relevé manuel pendant dix minutes, et l'intervalle entre deux glyphes monte à
  6 min 24. Il attend.
- **Les Hypothèses deviennent une ressource morte.** À 47:30 : O = 62 595, H = 6 982,
  C = 12. Vingt-cinq Concordances ne consomment que 12,5 hyp./s ; tout le reste s'entasse.
  L'explosion des Occurrences est le propos ; celle des Hypothèses est un tuyau bouché.
- **La courbe des lignes est bien back-chargée** : 0 % pendant seize minutes, 4 % à 27 min,
  puis 15 / 19 / 26 % avec `dix`, `cent`, `champ`. Et l'écart final signes/lignes — 57 %
  contre 26 % — reproduit PT4 (58 / 26) à un point près, avec un joueur différent et un
  style de jeu opposé. L'écart est le propos, et il est stable.

### Défaut trouvé, corrigé

La fenêtre de fin couvrait tout l'écran sans pouvoir se fermer : le bouton `copier` du
journal d'actions était inatteignable au moment précis où il faut exporter. La fenêtre se
ferme maintenant (bouton « revenir au corpus », échap, clic sur le fond) et la barre hors
jeu passe au-dessus d'elle. `tick` ne tourne plus une fois `S_.done` : le corpus derrière
reste figé sur la partie terminée et se relit tel quel. Recharger la page ramène la
fenêtre. Six contrôles ajoutés à `outils/verifier.py`.

## Le relevé devient un acte de lecture

**R7, 06/09/2026.** Le bouton « Relever un signe » est supprimé. Le relevé se fait dans le
corpus, sur un signe, et chaque tablette n'offre qu'un **gisement** fini — un dixième de ses
jetons, 398 pour les trente tablettes. Un jeton déjà relevé garde une marque ; une tablette
épuisée s'éteint dans la barre et le dit au journal.

Ce n'est pas un retarifage, c'est un déplacement. Les quatre constats de PT5 n'en faisaient
qu'un — la main ne fait rien (0,6 %), le corpus n'est jamais cliqué (0 sur 414), le texte ne
pèse pas dans l'achat, et il y a dix-sept minutes sans une action. Aucun de ces quatre n'est
un problème d'équilibrage : le joueur n'a simplement **aucune action qui soit de la
lecture**. Le seul moment de PT5 où on le voit lire, ce sont les seize secondes de balayage
après `cent`.

### Trois pièges, tous trouvés au simulateur avant d'écrire une ligne de jeu

| | ce qui arrive | correctif |
|---|---|---|
| Gisement qui coupe vraiment | **L'ouverture se verrouille** : les 4 tablettes du départ n'offrent que 13 relevés quand le premier Copiste en coûte 15. Le simulateur restait bloqué à 600 min, zéro instrument. | épuisé, le gisement rend le plancher (1), jamais zéro — et au départ, débit nul, le plancher et le tarif se valent : l'ouverture est inchangée |
| Tarif indexé sur le débit courant | **Se thésaurise** : ne rien relever pendant quarante minutes puis vider les 369 relevés au débit maximal donne **72 %** des occurrences au lieu de 17 %. La stratégie optimale devient « ne pas lire le corpus ». | le tarif d'une tablette est figé quand elle sort de terre et n'en bouge plus |
| Dégagement dans l'ordre du fichier | `ORDRE` et `CORPUS` divergent dès la cinquième tablette — le simulateur ouvrait les mauvais gisements. | `outils/sim.py` lit `ORDRE`. Deuxième fois que ce simulateur diverge du jeu ; il lit maintenant le corpus à la source. |

### Ce que ça donne

`REL_K = 1.2` : un relevé neuf vaut 1,2 seconde de production, au tarif de sa tablette.

| | avant | après |
|---|---|---|
| durée (cible 45 min) | 47,0–52,5 | **44,4–51,3** |
| I6 | 28,7 % | 29,96 % |
| part de la main dans les occurrences | 0,6 % *(mesuré PT5)* | **13,7–18,6 %** *(simulé)* |

Et une propriété qu'on ne cherchait pas mais qui vaut mieux que le réglage lui-même :
**à 5, 15 ou 40 clics par minute, la part de la main est la même.** C'est le gisement qui
décide de ce que la main rapporte, plus la vitesse du poignet. Le cliqueur frénétique et le
joueur posé convergent — le défaut de PT1 (3 853 relevés) devient structurellement
impossible, sans avoir eu à plafonner quoi que ce soit.

### Réserves, à vérifier en PT6

- **La marge sur I6 est nulle** (29,96 % pour un plafond de 30), et le simulateur
  sous-estime : PT5 a mesuré 30,8 % là où il annonçait 27,8 %. C'est la mesure qui tranchera,
  pas le simulateur.
- **Le trou du thésauriseur est réduit, pas fermé.** Le tarif est figé, mais les tablettes
  tardives sont tarifées plus cher : garder leur gisement pour la fin reste légèrement
  payant. Le modèle du simulateur vide déjà la tablette la mieux payée d'abord — les
  chiffres ci-dessus sont donc le pire cas, pas le cas moyen.
- **Rien ne garantit que le joueur lise pour autant.** Il peut parcourir le corpus en
  cliquant sans regarder. Le journal d'actions le dira : chaque relevé note sa tablette, et
  les relevés d'état portent le gisement consommé (`gis=`).

### Ce qui reste ouvert, et qui est plus gros

Le relevé produit des **Occurrences**, c'est-à-dire la ressource dont PT5 a fini avec
62 595 exemplaires inutilisés. Rendre la main utile dans une ressource déjà sans emploi ne
peut pas suffire à faire du jeu un jeu de déchiffrement.

L'action qui *devrait* être un acte de lecture, c'est le **recoupement** : il s'appelle
« recouper deux passages », il produit la seule ressource rare, il est déjà plafonné à 30 %
par I6 — et c'est un bouton qui n'a aucun rapport avec le texte. Le déplacer dans le corpus
(cliquer deux attestations d'un même signe dans deux tablettes) ne demanderait aucun
rééquilibrage : même coût, même gain, même I6. Seul le geste changerait. Et il rendrait le
comptage d'occurrences enfin opérant, puisque trouver deux attestations est facile pour un
signe fréquent et difficile pour un signe rare.

**R8, 06/09/2026 : fait.** Voir ci-dessous.

## Le recoupement passe dans le corpus

Le bouton n'exécute plus le recoupement : il **arme** le corpus. On choisit alors un passage
dans le texte, et le rapprochement se fait sur une seconde attestation du même signe, dans
une autre tablette.

**Rien n'a été rééquilibré.** Même coût (12 occ. + 3 hyp., ×1,18 par usage), même gain
(min(3, 1 + ⌊lexique/5⌋)), même part dans I6 : le simulateur rend exactement les mêmes
chiffres qu'avant le changement — 44,4 à 51,3 min, I6 29 à 30 %. Seul le geste a bougé.

### Le geste

1. On arme (le bouton, ou échap pour désarmer).
2. On choisit un passage. **Toutes les autres attestations du même signe s'allument dans le
   corpus**, et la barre de tablettes désigne celles où aller les chercher.
3. On clique l'une d'elles : rapprochement fait.
4. **Ce second passage devient le point d'appui du suivant.** On suit alors un signe de
   tablette en tablette, un clic par rapprochement.

La tablette du passage retenu est exclue des attestations allumées. On ne peut donc jamais
rapprocher deux fois le même endroit : la tournée n'est pas suggérée, elle est forcée.

Sans la barre, choisir un passage lançait une chasse au trésor dans trente tablettes dont
une seule tient à l'écran. C'est elle qui rend le geste jouable, et c'est enfin l'usage pour
lequel elle avait été construite : « la relecture devient une tournée guidée ».

### Ce que ça débloque

- **Le comptage d'occurrences devient opérant.** Il ne prédisait rien jusqu'ici (PT5 :
  `eau`, 70 occ., préféré à `dix`, 1 458 occ.). Il prédit maintenant un effort : trouver deux
  attestations d'un signe fréquent est immédiat, d'un signe rare c'est un parcours.
- **La seule ressource rare s'obtient en lisant.** C'était le reproche de fond à PT5 : le
  relevé porté dans le corpus produisait des Occurrences, dont la partie s'est terminée avec
  62 595 inutilisées. Le recoupement produit la Certitude.
- **L'ouverture ne peut pas se bloquer.** Le recoupement fournit 100 % de la Certitude des
  dix premières minutes ; il fallait vérifier qu'il reste toujours possible. Six signes
  (`ur`, `kish`, `gan`, `tab`, `tem`, `nur`) sont présents dans **chacune** des quatre
  tablettes du départ. À trente tablettes, 37 signes sur 46 sont recoupables.

### Ce que le simulateur ne peut pas dire

Le coût du recoupement **en temps de joueur** est passé de zéro — une pression sur un
bouton, répétable en maintenant — à deux clics et une navigation. L'économie est identique ;
le temps réel de la partie, peut-être pas. `outils/sim.py` ne modélise aucun coût
d'interaction et ne verra jamais ce décalage.

C'est la première question de PT6, et le journal d'actions y répondra : chaque recoupement
note le signe rapproché, et l'intervalle entre deux recoupements se lit dans les
horodatages.

### Réserve

Choisir un passage allume toutes les attestations de son signe — c'est un outil de recherche
gratuit dans le corpus. Je le tiens pour une fonctionnalité et non pour une fuite :
l'analyse de fréquences rendue littérale est le sujet du jeu, et la Table de fréquences
garde l'exclusivité du *nombre*, quand cet éclairage ne donne que les *positions*. Mais
c'est gratuit, et à surveiller.

## La numération — deux corrections successives

Défaut signalé après PT3 : acheter `un` convertissait **tous** les nombres des tablettes en chiffres. Pas un bug, une erreur de modèle : je traitais « savoir lire les nombres » comme un interrupteur alors que c'est une compétence qui s'acquiert signe par signe.

**Première correction** : un nombre ne passe en chiffres que si le joueur connaît chacun de ses signes. Insuffisant — avec `un` seul, 2, 3 et 4 se lisaient encore. Or **savoir que ▏ vaut un ne dit rien de ce que vaut ▏▏.**

**Correction finale** : `deux` n'ouvre aucun signe, il ouvre **le principe du redoublement**. Tant qu'on ne l'a pas, on ne lit qu'un nombre où chaque signe apparaît une seule fois. Tableau complet dans `docs/corpus.md` §3.

Vérifié automatiquement par `outils/verifier.py` : rien → aucun · `un` → {1} · `deux` → {1,2,3,4} · `cinq` → {1…9, 50…54} · `dix` → {1…99} · `cent` → {1…999}.

La ligne « 50 à 54 » n'est pas une anomalie : on connaît ⊖ (cinquante) sans connaître ○ (dix). C'est le genre de trou dans le savoir qu'un vrai déchiffrement produit.

---

## La navigation et les infobulles

**Barre de tablettes** — un nouveau signe donne envie de relire les 30 tablettes ; y aller au défilement était long. Une cellule par tablette dégagée, avec son numéro (en signes tant qu'on ne sait pas le lire) et une jauge de lisibilité. Clic pour y aller, `j`/`k` au clavier. **À chaque signe acquis, les tablettes où quelque chose a changé passent en ocre** — la relecture devient une tournée guidée.

C'est la brique qui rendra le réordonnancement chronologique de l'acte III jouable.

**Infobulles** — au survol d'un mot traduit, son signe revient ; sur un composé, les deux parties séparées par un `+`, avec leur sens quand le joueur les connaît. Sur un nombre traduit, la suite de signes.

**Ajout à valider** : au survol d'un signe **inconnu**, l'infobulle donne son nombre d'occurrences dans tout le corpus — mais seulement si le joueur possède une **Table de fréquences**. L'instrument fait alors visiblement ce que son nom annonce, et le joueur reçoit le premier vrai outil d'épigraphiste. Pour retirer : la condition `S_.b.tab > 0` dans `tipHTML()` (`src/rendu.js`).

Pas d'accès clavier aux infobulles : les signes ne sont pas focalisables. À traiter si le jeu vise l'accessibilité.

---

## Le branchement du corpus — une découverte de conception

Première génération du corpus : 1 519 signes, et **82 % déjà lisibles avec 12 signes sur 44**. Les blocs générés n'employaient que `maison`, `grain`, `tablette` et des nombres, tous acquis dès l'acte II : la masse portait zéro vocabulaire tardif.

→ Les blocs sont **salés de modalité, de temps et de personne**, ce qui est aussi plus juste (un vrai registre est plein de conditions), et un bloc `veille()` a été ajouté — le relevé d'eau tenu d'année en année, le document le plus lourd en vocabulaire d'acte III et celui qui porte le déclin.

Résultat : **3 825 signes, 58 % lisibles au MVP.**

### La jauge, et l'invariant I5 retiré

Proposition intermédiaire : faire compter à la jauge les **lignes entièrement lisibles** plutôt que les signes. Mesuré alors : la part de lignes reste entre **0 et 2 %** pendant tout le MVP. Comme jauge de progression, démoralisant.

> **Corrigé après PT4 — ce chiffre n'est plus vrai.** Il datait d'avant la numération
> signe par signe. Mesuré à nouveau, la part de lignes atteint **26 %** en fin de MVP :
> plate de 0 à 2 % pendant les sept premiers signes, elle décolle d'un coup à `dix`
> (2 % → 12 %), qui ouvre les nombres à deux chiffres et donc les lignes de registre
> entières (`maison 12 · grain 300`), puis monte à 26 % à `champ`. La décision d'afficher
> les deux mesures reste bonne ; sa justification était fausse. La forme réelle est
> meilleure que prévu : vingt minutes de plat, puis une récompense franche.

**Décision** : la barre affiche les **signes**, l'en-tête affiche les deux nombres, la carte de fin aussi.

**L'invariant I5 du design doc est faux et a été retiré.** Aucune mesure n'est linéaire : les signes sont front-chargés, les lignes back-chargées. L'écart entre les deux *est* le propos du jeu — on peut lire presque tous les mots et ne comprendre presque rien. L'afficher, ne pas le lisser.

---

## Réglages actuels

| | Valeur |
|---|---|
| Relever | dans le corpus. Jeton neuf : tarif de la tablette, figé à (1 + 1,2 × débit) × mult. **au premier relevé qu'on y fait**. Jeton déjà relevé ou tablette épuisée : le plancher (1 × mult.) |
| Gisement | ⌈jetons/10⌉ par tablette, **399** en tout, dont 13 ouverts au départ |
| Formuler | 3 occ. → 1 hyp. |
| Recouper | dans le corpus : deux attestations d'un même signe, dans deux tablettes différentes. 12 occ. + 3 hyp. → min(3, 1 + ⌊arbre/5⌋) cert., coût **×1,30** par usage (−25 % avec `champ`) *(09/09/2026)* |
| Copiste | **10** occ., ×1,12, +1 occ./s *(09/09/2026)* |
| Table de fréquences | 100 occ., ×1,15, −1 occ./s → +0,6 hyp./s |
| Concordance | 450 occ., ×1,18, −0,5 hyp./s → +0,0039 cert./s |
| Atelier de copie | 1 800 occ., ×1,15, +25 occ./s |
| Grammaire *(acte III)* | 12 000 occ., ×1,20, −3 hyp./s → +0,0012 × 1,16^lexique cert./s. Fermée jusqu'à `année` |
| Hors ligne *(acte III)* | `nuit` : 40 % du débit, 4 h au plus, consommé au crédit |
| Composer *(acte III)* | deux signes acquis, dans l'ordre. Ouvert par `année`. Réussite : le coût normal du glyphe en Certitude. Échec : 250 hyp. ×1,40 par paire déjà tentée, **jamais de Certitude**, et la paire entre au carnet |
| Signes (27) | Nombre 2 · 5 · 11 · 18 · 33 · 110 — Matière 3 · 6 · 14 · 22 · 40 — Parole 8 · 27 · 48 · 300 · 600 · 900 — Temps 60 · 130 · 190 · 260 · 360 · 500 — Modalité **150 · 320 · 550 · 800** = **5 467 C** *(12/09/2026)* |
| Composés secrets (2) | `grenier` 60 C et `zéro` 120 C, hors arbre, sans effet mécanique — on les lit, et c'est tout. Recettes ouvertes aujourd'hui : `deux`, `siècle`, `grenier`, `scribe`, `archive`, **`sinon`**, **`zéro`** |
| Multiplicateurs | `deux` ×1,25 relevé · `grain` ×1,3 copiste · `tablette` ×1,5 relevé · `eau` ×1,3 table · `champ` −25 % recoupement · `graver` ×1,5 concordance · `copier` ×2 sur tout · `lire` ×1,5 grammaire · `scribe` ×1,5 copiste et atelier · `archive` ×1,5 table · `mille` ×1,3 atelier · `siècle` ×1,5 grammaire · `dernière-année` ×1,5 atelier · `il-faut` ×1,5 atelier |
| Datation | une tablette se date quand on sait lire `année` **et** chacun des signes de son nombre. Les deux dernières attendent `dernière-année`. `avant` range la barre, `après` range le corpus |
| Concordance *(effet visible)* | choisir un signe replie le corpus sur ses attestations, chaque tablette gardant sa première ligne. Ouvert dès la première Concordance achetée ; marche aussi sur un signe inconnu |

---

## Écarts assumés par rapport au design doc

1. **Concordance ajoutée comme instrument** — sans elle, toute la Certitude vient du recoupement manuel.
2. **Atelier de copie avancé aux actes I–II** — sa coupe initiale était l'erreur de PT1.
3. **Lexique à 45 signes au lieu de 44** : la branche Nombre gagne `cinq` et `mille`, perd `vingt` (redondant), pour que chaque signe ouvre un rang de numération — ou, pour `deux`, le principe du redoublement.
4. **17 composés au lieu de 9.** En dessinant les signes, presque tout le lexique tardif s'est révélé composable (`nous-fûmes` = nous + finir, `scribe` = dire + graver). La mécanique de composition de l'acte III en devient plus riche — et `zéro`, composé `ne-pas` + `un`, s'affiche dans les compteurs du joueur dès la première seconde, des heures avant qu'il puisse le lire.
5. **Invariant I5 retiré**, invariant I6 ajouté.
6. **La Table de fréquences et la Concordance ont un effet visible** — le comptage d'occurrences pour l'une, le rassemblement des attestations pour l'autre — en plus de leur rôle économique. Un instrument nommé d'après une méthode philologique doit faire cette méthode, sinon le nom ment.
7. **Le chrome de l'interface est en français dès t=0.** L'idéal du doc — un seul mot français à l'écran — rend le prototype injouable sans onboarding. À réexaminer une fois qu'il y en aura un.
8. ~~Pas de progression hors-ligne.~~ **Refermé à l'acte III** : `nuit` la débloque, 40 % du débit, 4 h au plus.
9. **L'acte III est livré par moitiés.** La branche Temps, `mille`, la Grammaire et le
   réordonnancement d'abord ; la composition ensuite *(10/09/2026)*, mais `zéro` n'a pas pu
   la suivre — il se compose avec `ne-pas`, qui appartient à la Modalité. La Parole III est
   arrivée sans son dernier signe *(11/09/2026)* : `lire`, `scribe`, `archive`. La Modalité
   et `zéro` ont suivi *(12/09/2026)*. Restent `les-lecteurs` et l'Élève.
10. **`zéro` ne donne pas la notation compacte des grands nombres**, que le design doc §7 lui
   prête. Elle est déjà celle de `cent`, acquise par tout le monde ; la déplacer sur un
   composé facultatif la retirerait à la plupart des joueurs. Il ne donne que sa lecture —
   les onze zéros du corpus, dont les neuf de la tablette 29.

---

## Décisions

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète du corpus. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.

---

## Suite

1. **PT10, avec un autre joueur.** PT9 a répondu oui à la question de PT8 — la crue qui baisse
   se voit — mais pour un testeur qui savait quoi chercher. La question se repose mot pour
   mot à quelqu'un qui ne le sait pas ; le journal d'actions dira s'il concorde, et sur quoi.
   À surveiller dans le même TSV : la part manuelle des occurrences (36,3 % en PT9 ; au-delà
   de 40 %, plafonner `REL_K`) et le stock d'hypothèses entre `année` et la dixième Grammaire.
   Et deux paires, comptées avec leur minute : ⟨maison⟩+⟨grain⟩, ⟨ne-pas⟩+⟨un⟩. Les deux
   signes sont dans le texte depuis la première seconde ; personne ne dira qu'il y a quelque
   chose à y trouver.
2. **Le mur des dix premières minutes** : 83 % de la Certitude à la main avant la première
   Concordance en PT7, 63 % en PT8, 75 % en PT9 — et c'est là que la partie 1 de PT5 a été
   abandonnée. Le seul défaut d'équilibrage connu qui ne soit pas réglé. Il se traite par
   l'ouverture (un instrument plus tôt, ou un premier signe moins cher), pas par le
   recoupement.
3. **Seconde moitié de l'acte III** — ~~composition~~ *(faite le 10/09/2026)*, ~~`lire`,
   `scribe`, `archive`~~ *(11/09/2026)*, ~~la Modalité et `zéro`~~ *(12/09/2026 : une branche
   tardive mord enfin sur la branche Nombre)*. Reste **`les-lecteurs`**, dernier signe de
   l'acte. L'Élève ensuite, qui n'a pas de sens sans les lectures fausses. Puis les
   **contradictions** (acte IV).
4. **Le clic vide** est descendu à 8 % des relevés (PT9) depuis la marque de la barre ; le
   texte ne dit toujours pas ce que la barre dit. Peut attendre.
5. ~~Trancher le sort de ⟨N1⟩ et ⟨N2⟩ (`docs/corpus.md` §9).~~ *Semés comme intitulés des
   registres le 11/09/2026 — voir « Le fleuve et la cité ».*
6. **La tranche 20-30′ remonte d'un lot à l'autre** : 25,8 % à 23 signes, 27,0 % à 27. Ce
   n'est pas le lot qui la pousse — la Modalité arrive à la cinquantième minute — c'est
   `revCount()` : plus l'arbre est grand, plus lentement les tablettes se dégagent par signe
   acquis, donc moins de gisement au milieu de la partie. Sous 30 % (règle 2), mais à
   regarder au prochain lot, et à traiter dans `revCount()` si ça continue.
