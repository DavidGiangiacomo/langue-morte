# Journal de bord

Historique des playtests, des défauts trouvés et des décisions prises. À lire avant de modifier l'équilibrage ou la numération : chacune des règles actuelles est là parce qu'une version plus simple a échoué.

---

## Les playtests

| | PT4 | PT5 | PT6 | PT7 | PT8 | Cible |
|---|---|---|---|---|---|---|
| Durée | 42 min 12 | 50 min 37 | 43 min 49 | 44 min 50 | **63 min 12** *(20 signes)* | 45 min *(13 signes)* |
| Signes relevés à la main | 56 | **371** | 180 | **422** | — | — |
| Hypothèses formulées à la main | — | 264 | 27 | 7 | — | — |
| Recoupements | **56** | 46 | 44 | 39 | 46 | — |
| Part manuelle de la Certitude | 43,5 % *(simulé)* | **30,8 %** | **30,0 %** | **31,2 %** | **6,0 %** | < 30 % par tranche de 10 min |
| Part manuelle des Occurrences | — | 0,6 % | **0,1 %** | **17,9 %** | — | — |
| Gisement consommé | — | — | 54 / 398 | 293 / 398 | **394 / 398** | — |
| Lignes entièrement lues | 26 % | 26 % | 26 % | 26 % | **34 %** | — |
| Signes déchiffrés | 58 % | 57 % | 57 % | 57 % | **69 %** | — |

PT1 à PT3 sortent du tableau : ils datent d'avant le journal d'actions, et leurs chiffres
vivent dans les sections qui les dépouillent. PT8 est la première partie des trois actes —
sa durée et ses parts ne se comparent pas aux précédentes, qui s'arrêtaient à 13 signes.

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
|---|---|---|---|---|---|---|---|
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
| Gisement | ⌈jetons/10⌉ par tablette, **397** en tout, dont 13 ouverts au départ |
| Formuler | 3 occ. → 1 hyp. |
| Recouper | dans le corpus : deux attestations d'un même signe, dans deux tablettes différentes. 12 occ. + 3 hyp. → min(3, 1 + ⌊lexique/5⌋) cert., coût ×1,18 par usage (−25 % avec `champ`) |
| Copiste | 15 occ., ×1,12, +1 occ./s |
| Table de fréquences | 100 occ., ×1,15, −1 occ./s → +0,6 hyp./s |
| Concordance | 450 occ., ×1,18, −0,5 hyp./s → +0,0039 cert./s |
| Atelier de copie | 1 800 occ., ×1,15, +25 occ./s |
| Grammaire *(acte III)* | 12 000 occ., ×1,20, −3 hyp./s → +0,0012 × 1,16^lexique cert./s. Fermée jusqu'à `année` |
| Hors ligne *(acte III)* | `nuit` : 40 % du débit, 4 h au plus, consommé au crédit |
| Signes (20) | Nombre 2 · 5 · 11 · 18 · 33 · 110 — Matière 3 · 6 · 14 · 22 · 40 — Parole 8 · 27 · 48 — Temps 60 · 130 · 190 · 260 · 360 · 500 = **1 847 C** |
| Multiplicateurs | `deux` ×1,25 relevé · `grain` ×1,3 copiste · `tablette` ×1,5 relevé · `eau` ×1,3 table · `champ` −25 % recoupement · `graver` ×1,5 concordance · `copier` ×2 sur tout · `mille` ×1,3 atelier · `siècle` ×1,5 grammaire · `dernière-année` ×1,5 atelier |
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
   réordonnancement d'abord ; la composition (donc `zéro`), l'Élève, la Parole III et la
   Modalité ensuite. Le doc décrit l'acte entier, le code en tient la première moitié.

---

## Décisions

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète du corpus. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.

---

## Suite

1. **PT9**, la première partie avec la concordance. Une seule question, et elle est la même
   que celle de PT8 : **la crue qui baisse se voit-elle ?** La colonne existe maintenant,
   elle tient en quatre-vingt-douze lignes, elle descend de 14 à 0 — reste à savoir si le
   joueur y va, et ce qu'il concorde. Le journal d'actions note désormais chaque
   concordance et son signe : si le TSV n'en contient aucune, l'instrument est invisible et
   c'est le bouton qu'il faut reprendre, pas la vue.
   Deux questions secondaires : les quatre minutes d'idle de la fin d'acte reculent-elles ?
   et le simulateur, qui a surestimé PT8 de 20 %, doit-il être recalé ?
2. **Le mur des dix premières minutes** : 83 % de la Certitude à la main avant la première
   Concordance en PT7, 63 % en PT8 — et c'est là que la partie 1 de PT5 a été abandonnée.
   Le seul défaut d'équilibrage connu qui ne soit pas réglé. Il se traite par l'ouverture (un
   instrument plus tôt, ou un premier signe moins cher), pas par le recoupement.
3. **Le clic vide** : un tiers des relevés de PT7 tombent sur un gisement épuisé. Le texte
   doit dire ce que la barre dit déjà.
4. **Seconde moitié de l'acte III** — composition (donc `zéro`), Élève, Parole III,
   Modalité. Puis les **contradictions** (acte IV).
5. Trancher le sort de ⟨N1⟩ et ⟨N2⟩ (`docs/corpus.md` §9).
