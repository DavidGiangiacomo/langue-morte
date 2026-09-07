# Le corpus

*30 tablettes. Contenu intégral et règles de génération.*
*R5 tranché le 04/09/2026 : **français seul**. Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable.*

> **Transcription exécutable : `outils/corpus.py`.** Ce document est la référence éditoriale ; le script en est la mise en œuvre. Modifier le texte se fait dans le script, puis `python outils/corpus.py`, puis `python build.py`. Garder les deux d'accord.

---

## 1. Principe

Le corpus n'est pas un texte long : c'est un **corpus administratif**, massivement répétitif, avec très peu de matière non répétitive dispersée dedans. C'est ce qui le rend déchiffrable — l'analyse de fréquence n'existe que s'il y a du volume — et c'est ce qui rend bouleversantes les rares lignes qui sortent du registre.

Trois conséquences de production :

- **La masse répétitive n'est pas du remplissage, elle est le substrat du déchiffrement.** Elle se génère à partir de règles (§6), elle ne s'écrit pas à la main.
- **Tout le corpus tient dans 45 mots** plus les nombres et six noms propres jamais déchiffrés. Cette contrainte n'est pas une limite subie : c'est elle qui produit le style. Un peuple qui n'a que « ne-pas » pour dire l'absence écrit « eau ne-pas », et c'est plus dur que n'importe quelle phrase qu'on pourrait écrire à sa place.
- **Le français lu est télégraphique.** Pas d'articles, pas de prépositions, pas d'accord. La couche d'affichage n'ajoute rien. « champ 3 · grain 140 » est le texte, pas un résumé du texte.

**Réalisé** : 678 lignes, **3 825 signes**, dont 58 % lisibles avec les 13 signes du MVP.

---

## 2. Le lexique — 45 mots

| Branche | Mots |
|---|---|
| **Nombre** | un · deux · cinq · dix · cent · mille · zéro |
| **Matière** | grain · eau · champ · maison · grenier · tablette |
| **Parole** | dire · graver · copier · lire · scribe · archive · les-lecteurs |
| **Temps** | année · avant · après · siècle · nuit · dernière-année |
| **Modalité** | ne-pas · si · il-faut · peut-être · faux · sinon |
| **Personne** | je · toi · nous · toi-qui · moi-absent · nous-fûmes |
| **Fin** | finir · semence · devenir · le-dernier · germer · notre-fin · devenir-lecture |

La branche Nombre a été portée de 6 à 7 signes après le playtest 3 : chaque signe doit ouvrir un rang de numération (§3), et `vingt` — redondant — a été retiré au profit de `cinq` et `mille`.

**17 composés** se dessinent comme composés (table `COMP` dans `src/signes.js`) : `deux` = un + un, `grenier` = maison + grain, `scribe` = dire + graver, `nous-fûmes` = nous + finir, `zéro` = ne-pas + un, `devenir-lecture` = lire + devenir. Le joueur reconnaît les parties avant de savoir lire le tout.

### Les noms propres — jamais déchiffrés

Six signes qui ne se résolvent à aucun acte. Le joueur apprend à reconnaître leur forme sans jamais en connaître le son. C'est ce que fait un épigraphiste devant un anthroponyme, et c'est un des rares endroits où le jeu est honnête sans effort.

| Signe | Ce que c'est *(note de conception, jamais dite au joueur)* |
|---|---|
| ⟨N1⟩ | le fleuve |
| ⟨N2⟩ | la cité |
| ⟨N3⟩ | le premier scribe — tablettes 4 à 11 |
| ⟨N4⟩ | le deuxième scribe — tablettes 11 à 19 |
| ⟨N5⟩ | la dernière scribe — tablettes 19 à 30 |
| ⟨N6⟩ | quelqu'un qu'elle a aimé — tablette 30 seulement |

⟨N6⟩ apparaît quatre fois, dans les six dernières lignes du corpus, et nulle part ailleurs.

---

## 3. La numération

Additive : 1 · 5 · 10 · 50 · 100 · 500 · 1000.

**Elle s'acquiert signe par signe.** Un nombre du corpus ne passe en chiffres que si le joueur connaît *chacun* de ses signes :

| Signe acquis | Ce qu'il ouvre | Nombres lisibles |
|---|---|---|
| `un` | ▏ | **1** seulement |
| `deux` | le principe du redoublement — aucun signe | 1 à 4 |
| `cinq` | ⋀ ⊖ ◈ — un signe vaut cinq du rang d'en dessous, à tous les rangs | 1 à 9 **et 50 à 54** |
| `dix` | ○ | 1 à 99 |
| `cent` | ◇ | 1 à 999 |
| `mille` | ✳ | tout |

`deux` n'ouvre aucun signe : savoir que ▏ vaut un ne dit rien de ce que vaut ▏▏. Tant qu'on ne l'a pas, on ne lit qu'un nombre où chaque signe apparaît une seule fois. La ligne « 50 à 54 » n'est pas une anomalie : on connaît ⊖ sans connaître ○, et c'est le genre de trou dans le savoir qu'un vrai déchiffrement produit.

Conséquence : une ligne se lit **en partie**. « champ 1 · grain ⟨◇◇○▏▏⟩ ». Le joueur voit l'étendue exacte de ce qu'il sait.

Les tablettes 1 à 4 sont **structurellement identiques** : même gabarit, mêmes positions, seuls les nombres changent. C'est le levier de déchiffrement de l'acte I — et c'est aussi, on ne l'apprend qu'à la tablette 21, un abécédaire volontaire.

---

## 4. Ce que disent les chiffres

Le vrai récit n'est dans aucune phrase. Il est dans trois séries, que personne ne commente jamais.

| Année | Eau | Grain | Maisons | Semence | Copies exigées |
|---|---|---|---|---|---|
| 9 | 14 | 756 | 31 | 60 | — |
| 12 | 13 | 742 | 31 | 60 | — |
| 19 | 15 | 801 | 33 | 60 | — |
| 27 | 12 | 690 | 30 | 60 | — |
| 40 | 13 | 705 | 31 | 60 | — |
| 54 | 11 | 648 | 29 | 60 | 2 |
| 71 | 12 | 661 | 30 | 60 | 2 |
| 88 | 10 | 590 | 27 | 60 | 2 |
| 103 | 9 | 522 | 24 | 80 | 2 |
| 112 | 10 | 548 | 25 | 80 | 2 |
| 126 | 8 | 470 | 22 | 100 | 10 |
| 139 | 7 | 401 | 19 | 100 | 10 |
| 150 | 8 | 418 | 17 | 100 | 10 |
| 164 | 6 | 352 | 17 | 100 | 10 |
| 177 | 5 | 287 | 14 | 100 | 10 |
| 183 | 6 | 301 | 15 | 100 | 100 |
| 195 | 4 | 224 | 11 | 100 | 100 |
| 201 | 3 | 166 | 9 | 100 | 100 |
| 207 | 2 | 110 | 6 | 100 | 100 |
| 209 | 2 | 98 | 5 | 100 | 100 |
| 211 | 1 | 54 | 3 | 100 | 100 |
| 213 | 1 | 29 | 2 | 100 | 100 |
| 214 | 0 | 0 | 0 | 0 | — |

*(Cette table est la source de vérité. Elle vit aussi dans `outils/corpus.py`, constante `EAU` et arguments de `champs()`.)*

Trois lectures s'emboîtent, et elles n'arrivent pas au même moment :

1. **L'eau baisse.** Bruitée — 15 en année 19, 10 en année 112 — donc invisible tant que les tablettes ne sont pas datées et triées. C'est le déblocage de l'acte III.
2. **La semence monte pendant que le grain descend.** Ils sèment de plus en plus pour récolter de moins en moins. Personne ne l'écrit.
3. **Les copies exigées explosent : 2 → 10 → 100.** À l'année 201, cinq scribes sur neuf foyers. La moitié d'un peuple qui meurt de faim recopie des tablettes. Aberrant jusqu'à l'acte V, où ça devient la seule chose sensée qu'ils aient faite.

Les quatre champs, quand ils sont détaillés, somment toujours au total de l'année. Vérifier cette somme est une méthode de déchiffrement à part entière — un joueur qui la trouve gagne un tour d'avance sur les signes de nombres.

---

## 5. Les 30 tablettes

*`·` sépare les segments d'une même ligne. `[bloc]` renvoie au §6. Chaque tablette est classée par l'acte où elle devient substantiellement lisible — mais toutes sont présentes dès le début, en signes.*

### ACTE I — les nombres

Quatre tablettes de même gabarit. Aucun mot n'y est déchiffrable au départ ; seule la position des nombres l'est.

**Tablette 1 — année 9**
```
tablette 1 · année 9
champ 1 · grain 212
champ 2 · grain 198
champ 3 · grain 140
champ 4 · grain 206
grain 756
eau 14
maison 31
```

**Tablette 2 — année 12** — même gabarit : 205 · 191 · 138 · 208 · total 742 · eau 13 · maison 31
**Tablette 3 — année 19** — 224 · 210 · 152 · 215 · total 801 · eau 15 · maison 33

**Tablette 4 — année 27**
```
tablette 4 · année 27
champ 1 · grain 190      champ 3 · grain 130
champ 2 · grain 176      champ 4 · grain 194
grain 690 · eau 12 · maison 30
grenier 1 · grain 690
scribe ⟨N3⟩
```

### ACTE II — les choses

Le registre s'élargit : distribution, réserve, archive. Ton volontairement plat. On installe un quotidien pour que sa disparition compte.

**Tablette 5 — année 40 — registre de distribution**
```
tablette 5 · année 40
grenier 1 · grain 705
[bloc-maisons 31 · 20]
grain 620
grenier 1 · grain 85
semence 60
grain 25
scribe ⟨N3⟩
```
*705 sortis, 620 distribués, 85 gardés, 60 semés, 25 restants. L'arithmétique est juste et vérifiable : c'est un outil de déchiffrement offert au joueur attentif.*

**Tablette 6 — année 40 — relevé d'eau**
```
tablette 6 · année 40
[bloc-veille jusqu'à l'année 40]
scribe ⟨N3⟩
```
*Première tablette qui contient sa propre histoire. Illisible à l'acte II, elle devient à l'acte III la première série temporelle du corpus — et la preuve qu'ils surveillaient l'eau exprès.*

**Tablette 7 — année 54** — champs 180 · 168 · 124 · 176, total 648, eau 11, maison 29, `[bloc-maisons 29 · 20]`, grenier 62
**Tablette 8 — année 54 — l'archive** — `archive 1`, `[bloc-archive 1→24]`, `[consignes 2]`, `scribe ⟨N3⟩`
**Tablette 9 — année 71** — champs 184 · 171 · 126 · 180, total 661, eau 12, `[bloc-maisons 30 · 20]`, *grenier 1* — une bonne année qui ne remplit plus le grenier
**Tablette 10 — année 88** — champs 165 · 153 · 112 · 160, total 590, eau 10, semence 60, `[bloc-maisons 27 · 20]`, **grenier 0**

**Tablette 11 — année 88**
```
tablette 11 · année 88
scribe ⟨N3⟩ finit
archive 1 · tablette 11
[consignes 2]
scribe ⟨N4⟩
```
*Le premier scribe meurt en une ligne, dans un registre, entre deux consignes de copie. C'est le ton du corpus entier.*

### ACTE III — le temps

**Tablette 12 — année 103** — total 522, eau 9, **semence 80**, grenier 12
*La semence passe de 60 à 80. Personne ne le commente. Première fois qu'ils sèment plus pour récolter moins.*

**Tablette 13 — année 112**
```
tablette 13 · année 112
[bloc-champs 153 · 142 · 104 · 149]  grain 548 · eau 10 · maison 25
après · année 103 · grain 522
après · année 112 · grain 548
peut-être eau
[bloc-maisons 25 · 20]
scribe ⟨N4⟩
```
*Une bonne année. Deux mots d'espoir : « peut-être eau ». La seule fois du corpus où quelqu'un espère. La tablette 26 les annulera, quatre-vingt-dix-sept ans plus tard.*

**Tablette 14 — année 126** — total 470, eau 8, semence 100, grenier 0, `[bloc-maisons 22 · 20]`, `[consignes 10]`
*Les copies exigées passent de 2 à 10, la même année où le grenier reste vide.*

**Tablette 15 — année 139 — le siècle**
```
tablette 15 · année 139
grain 401 · maison 19
siècle 1 · après
avant · siècle 1 · eau 14
[bloc-veille jusqu'à l'année 139]
il-faut lire · grain
scribe ⟨N4⟩
```
*Le déclin est posé pour la première fois : deux nombres côte à côte, à cent trente ans d'écart, et pas un mot dessus.*

**Tablette 16 — année 150 — le protocole**
```
tablette 16 · année 150
archive 1 · tablette 300
[bloc-archive 1→96]
[consignes 10]
maison 17 · scribe 6
grain 418 · eau 8
```
*Six scribes pour dix-sept foyers. Un tiers de ce qui reste du peuple grave des tablettes la nuit. Aberrant — jusqu'à l'acte V.*

**Tablette 17 — année 150 — le tri**
```
tablette 17 · année 150
tablette · si copier · il-faut
tablette · si ne-pas copier · sinon
grain · ne-pas tablette
eau · ne-pas tablette
il-faut tablette · lire
il-faut tablette · devenir lire
scribe ⟨N4⟩
```
*Première tablette qui parle de la langue et non de la récolte. « il-faut tablette · devenir lire » : le composé `devenir-lecture` n'est pas encore employé, il est assemblé sous les yeux du joueur. Celui qui a composé le signe en avance reçoit cette ligne en pleine figure.*

**Tablette 18 — année 164 — le nom**
```
tablette 18 · année 164
grain 352 · eau 6 · maison 17
nous · les-lecteurs
avant · nous · les-lecteurs
après · nous · les-lecteurs
si ne-pas lire · nous ne-pas
scribe ⟨N4⟩
```
*Ils s'appellent « les lecteurs ». Et : si on ne lit pas, nous ne sommes pas. La thèse du jeu, posée à plat, cinquante ans avant la fin.*

**Tablette 19 — année 177** — champs 80 · 74 · 54 · 79, total 287, eau 5, `[bloc-maisons 14 · 20, 2 vides]`, `scribe ⟨N4⟩ finit`, `scribe ⟨N5⟩`

### ACTE IV — toi

**Tablette 20 — année 183**
```
tablette 20 · année 183
grain 301 · eau 6 · maison 15
[bloc-maisons 15 · 20, 2 vides]
toi · lis
toi-qui lis · toi
je grave · toi lis
peut-être toi
scribe ⟨N5⟩
```

**Tablette 21 — année 183 — l'abécédaire**
```
tablette 21 · année 183
il-faut graver · un
il-faut graver · un · deux · un
il-faut graver · dix
tablette 1 · tablette 1 · tablette 1
si lire un · après lire deux
il-faut · faux ne-pas
scribe ⟨N5⟩
```
*La tablette qui enseigne les nombres — délibérément. Le joueur comprend ici que les quatre tablettes sur lesquelles il a appris à compter, à l'acte I, avaient été écrites pour lui apprendre à compter. La révélation de l'acte V, en avance, pour qui lit vraiment.*

**Tablette 22 — année 195**
```
tablette 22 · année 195
grain 224 · eau 4 · maison 11 · semence 100
grain ne-pas
[bloc-maisons 11 · 15, 3 vides]
si semence · ne-pas germer
si tablette · germer
scribe ⟨N5⟩
```

**Tablette 23 — année 201**
```
tablette 23 · année 201
grain 166 · eau 3 · maison 9 · scribe 5
archive 1 · tablette 900
[bloc-archive 1→120]
[bloc-maisons 9 · 15]
[consignes 100]
si copier 100 · un devenir
scribe ⟨N5⟩
```
*« si copier cent · un devenir » — copié cent fois, un exemplaire survit. Ce n'est pas de la piété : c'est du calcul de redondance. Ils savaient exactement ce qu'ils faisaient.*

**Tablette 24 — année 201**
```
tablette 24 · année 201
toi-qui lis · toi ne-pas nous
toi-qui lis · toi après
si toi lis · nous ne-pas finir
si toi ne-pas lis · nous finir
il-faut toi
scribe ⟨N5⟩
```

**Tablette 25 — année 207**
```
tablette 25 · année 207
grain 110 · eau 2 · maison 6
[bloc-maisons 6 · 10, 3 vides]
champ 1 · ne-pas
champ 2 · ne-pas
champ 3 · grain 21
champ 4 · ne-pas
grenier 1 · ne-pas
scribe ⟨N5⟩
```
*Les champs s'éteignent un par un, en colonne, sans commentaire. Le seul effet de style du corpus est le blanc.*

**Tablette 26 — année 209 — l'erreur**
```
tablette 26 · année 209
grain 98 · maison 5
[bloc-veille complet]
avant · tablette 6 · faux
avant · tablette 13 · faux
peut-être eau · faux
je grave : faux
il-faut faux ne-pas
scribe ⟨N5⟩
```
*La dernière scribe reprend l'archive et marque comme fausses les tablettes qui espéraient. Elle annule « peut-être eau » quatre-vingt-dix-sept ans après. C'est ici que le signe `faux` arrive dans le jeu — et il empoisonne rétroactivement ce que le joueur a déjà lu.*

### ACTE V — la graine

**Tablette 27 — année 211**
```
tablette 27 · année 211
grain 54 · eau 1 · maison 3
semence · ne-pas grain
semence · tablette
tablette · devenir-lecture
si tablette lire · tablette germer
nous · semence
scribe ⟨N5⟩
```

**Tablette 28 — année 213 — la fabrique**
```
tablette 28 · année 213
grain 29 · eau 1 · maison 2
nous graver · tablette
nous graver · tablette · si lire · devenir
un · deux · dix · cent · zéro
grain · eau · champ · maison
lire · graver · copier
si toi lis un · toi lis grain
si toi lis grain · toi lis nous
il-faut tablette · si un · après deux
peut-être toi · après siècle
scribe ⟨N5⟩
```
*Le programme, en clair : d'abord les nombres, puis les choses, puis les verbes. C'est exactement l'ordre des branches de l'arbre du jeu. Le joueur découvre le plan de cours qu'il suit depuis trois heures. « il-faut tablette · si un · après deux » est le principe d'ingénierie de toute la langue : chaque déchiffrement doit en produire un autre.*

**Tablette 29 — année 214 — le compte**
```
tablette 29 · dernière-année
champ 1 · 0    champ 3 · 0
champ 2 · 0    champ 4 · 0
grain 0 · eau 0 · maison 0 · grenier 0 · semence 0
[bloc-archive 1→160]
archive 1 · tablette 1200
scribe 1
```
*Un registre de zéros, et deux nombres qui n'en sont pas : mille deux cents tablettes, un scribe. Aucun commentaire, presque aucun mot. C'est la tablette la plus forte du corpus.*
*Note : `zéro` étant un composé d'acte III, cette tablette reste un seul signe répété pendant presque toute la partie. Heureux accident, à préserver.*

**Tablette 30 — année 214 — la dernière**
```
tablette 30 · dernière-année
je grave · le-dernier
scribe ⟨N5⟩
⟨N6⟩ lisait
⟨N6⟩ lisait · nuit
je ne-pas dire ⟨N6⟩ · dire finit
je grave ⟨N6⟩ · graver ne-pas finit
notre-fin · ne-pas
toi-qui lis · toi devenir
nous-fûmes
```

*Elle ne prononce pas le nom — la parole finit. Elle le grave — la gravure ne finit pas. Et la seule chose qu'elle consigne de quelqu'un qu'elle a aimé, c'est qu'il lisait. Toute la civilisation tient dans ce geste privé.*

*« notre-fin · ne-pas » ne se tranche pas : « notre fin : non » ou « pas notre fin ». Le jeu ne dira jamais laquelle. C'est là que vit l'ambiguïté héritage/parasite du design doc §2.*

*Dernier mot du corpus : `nous-fûmes` — le passé que le joueur a débloqué à l'acte IV, employé une seule fois, ici.*

---

## 6. Blocs générés

Quatre règles produisent la masse répétitive. Implémentation dans `outils/corpus.py`.

**`maisons(n, q, vides)`** — registre de distribution, n lignes. **Salées de modalité, de temps et de personne** (`si`, `ne-pas`, `il-faut`, `avant`, `après`, `nuit`, `nous`) selon l'indice de la maison. Ce salage n'est pas décoratif : sans lui le bloc n'emploie que le vocabulaire des actes I–II et 82 % du corpus devient lisible dès l'acte II (constat du playtest 3). C'est aussi plus juste — un vrai registre est plein de conditions. Les `vides` derniers foyers sont notés absents.

**`archive(a, b)`** — listes de tablettes groupées par quatre, entrecoupées de consignes.

**`champs(vals)`** — les 4 lignes de l'année. Les valeurs viennent du §4 et somment toujours juste.

**`veille(année, série)`** — le relevé d'eau tenu d'année en année. **Le document le plus lourd en vocabulaire d'acte III**, et celui qui porte le déclin.

**`consignes(k)`** — le protocole de copie, répété tel quel de tablette en tablette, avec k copies exigées.

Trois principes non négociables :

1. Les blocs emploient **exactement le même vocabulaire** que les lignes écrites à la main. Aucun signe ne doit apparaître uniquement dans un bloc — sinon la fréquence ment.
2. Ils sont **longs**. Un joueur doit pouvoir scruter cinquante lignes `maison i · grain 20` et en déduire que le deuxième signe varie et pas le quatrième. C'est le cœur de la méthode.
3. Ils ne contiennent **jamais** de contenu narratif. Tout ce qui a du sens est écrit à la main, au §5.

---

## 7. Les 11 signes ambigus

*(Mécanique de l'acte IV, pas encore implémentée.)*

Chacun a une lecture juste et une lecture fausse. La fausse marche longtemps, paie 25 % de plus (design doc §8), et finit par produire une absurdité **repérable dans le texte**. C'est le seul indice, et c'est ce qui fait que le jeu récompense la lecture.

| Signe | Juste | Faux | Où ça casse |
|---|---|---|---|
| `lire` | lire | compter | **Le piège majeur.** « compter » marche dans tout le corpus administratif, deux actes durant. Ne casse qu'à la tablette 18 : « nous · les-compteurs », puis à la 30 : « ⟨N6⟩ comptait ». Le joueur croit avoir affaire à une civilisation de comptables jusqu'à ce que l'acte V devienne incompréhensible. |
| `eau` | eau | sang | Tient jusqu'à la tablette 6 (un relevé annuel de sang), casse à la 25 : « champ 3 · sang 21 ». |
| `grain` | grain | poussière | Plausible dans un grenier, absurde tablette 5 quand on en distribue vingt à chaque maison. |
| `maison` | maison | tombe | Sinistre et cohérent au début — casse au même endroit : on ne distribue pas de grain aux tombes. |
| `semence` | semence | enfant | Bouleversant et faux. Tient jusqu'à la tablette 27 : « enfant · tablette ». |
| `année` | année | soleil | Tient comme datation, casse sur `siècle` (tablette 15) qui devient « cent-soleils ». |
| `graver` | graver | couper | Casse tablette 30 : « je coupe ⟨N6⟩ ». |
| `il-faut` | il faut | on peut | Transforme les ordres en permissions. Ne produit aucune absurdité — seulement un corpus qui perd son urgence. Le plus difficile à repérer, et celui qui abîme le plus la fin. |
| `avant` | avant | dessous | Piège d'archéologue : parfaitement plausible pour des tablettes empilées. Casse au réordonnancement chronologique de l'acte III, qui devient incohérent. |
| `devenir` | devenir | porter | « toi tu portes » au lieu de « toi tu deviens ». Casse tout l'acte V d'un coup. |
| `ne-pas` | ne pas | fin | « eau fin » passe. « ne-pas ne-pas » (tablette 26) ne passe pas. |

Deux d'entre eux — `lire` et `il-faut` — sont conçus pour **ne pas** casser mécaniquement. Ils ne produisent qu'un corpus légèrement faux, cohérent, et plus plat. Le joueur qui les rate finit le jeu sans savoir qu'il a lu une autre histoire. C'est voulu, et c'est ce que la relecture de fin (design doc §11) lui montrera.

---

## 8. Ordre de découverte

Les tablettes ne sont **pas** révélées dans l'ordre chronologique. Elles arrivent dans l'ordre où on les a sorties de terre ; c'est l'acte III (`avant` / `après`) qui permettra de les trier — moment où l'écran se réorganise et où les séries du §4 deviennent lisibles d'un coup.

```
1 · 2 · 3 · 4 · 8 · 5 · 21 · 7 · 6 · 11 · 9 · 16 · 10 · 12 · 17 · 13 · 15
· 22 · 14 · 18 · 19 · 25 · 20 · 23 · 26 · 24 · 27 · 29 · 28 · 30
```
*(constante `ORDRE` dans `src/corpus.js`, produite par `outils/corpus.py`)*

> **Implémenté à l'acte III** (07/09/2026). `année` date les tablettes — la date est déjà
> dans leur première ligne, il suffit de savoir la lire — puis `avant` range la barre et
> `après` range le corpus. Ce que le rangement démontre n'était pas prévu ici et mérite
> d'être noté : **l'ordre chronologique est l'ordre des numéros.** Le joueur sait lire les
> numéros depuis l'acte II et ne peut rien en conclure ; ce sont les dates qui prouvent que
> la numérotation était chronologique, donc que l'archive avait été rangée exprès. La
> découverte n'est pas « voici l'ordre caché », c'est « l'ordre était affiché depuis le
> début et je ne pouvais pas le savoir ».

Deux choix dans cet ordre :

- **La tablette 21 arrive 7ᵉ.** C'est l'abécédaire ; le joueur le lit comme du charabia numérique et ne comprendra qu'à l'acte IV qu'il tenait le mode d'emploi depuis le début.
- **La tablette 29 arrive avant la 28.** Le registre de zéros est lu avant l'explication. On voit la fin avant d'en connaître la raison — c'est l'ordre qui rend l'acte V supportable.

Le dégagement est progressif : 4 tablettes au départ, les 30 au dernier signe du MVP (`revCount()` dans `src/rendu.js`).

---

## 9. Ce qui reste à faire sur le texte

1. **Vérifier la densité de l'acte II.** C'est le passage le plus plat par conception (« on installe le quotidien pour que sa disparition compte ») et donc le seul endroit où le joueur peut décrocher. Si un playtest montre un décrochage, la réponse n'est pas d'ajouter du drame : c'est d'avancer la tablette 6 dans l'ordre de révélation.
2. **Décider du sort de ⟨N1⟩ et ⟨N2⟩** (le fleuve, la cité). Ils ne sont employés dans aucune tablette. Soit on les sème dans les blocs générés comme en-têtes — ce qui donne deux formes très fréquentes et jamais résolues, très frustrant et très juste — soit on les supprime. Je penche pour les semer.
3. **Écrire les lectures fausses des 11 signes ambigus** (§7) : chacune doit produire une phrase absurde repérable. C'est du travail d'écriture, pas de code.
