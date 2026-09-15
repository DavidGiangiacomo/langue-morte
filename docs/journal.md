# Journal de bord

Historique des playtests, des défauts trouvés et des décisions prises. À lire avant de modifier l'équilibrage ou la numération : chacune des règles actuelles est là parce qu'une version plus simple a échoué.

---

## Les playtests

| | PT4 | PT5 | PT6 | PT7 | PT8 | PT9 | PT10 | Cible |
|---|---|---|---|---|---|---|---|---|
| Durée | 42 min 12 | 50 min 37 | 43 min 49 | 44 min 50 | **63 min 12** *(20 signes)* | **66 min 49** *(20 signes)* | **96 min 35** *(30 signes)* | 45 min *(13 signes)* |
| Signes relevés à la main | 56 | **371** | 180 | **422** | — | **429** | **164** | — |
| Hypothèses formulées à la main | — | 264 | 27 | 7 | — | 6 | 8 | — |
| Recoupements | **56** | 46 | 44 | 39 | 46 | 49 | **32** | — |
| Part manuelle de la Certitude | 43,5 % *(simulé)* | **30,8 %** | **30,0 %** | **31,2 %** | **6,0 %** | **8,2 %** | **0,7 %** | < 30 % par tranche de 10 min |
| Part manuelle des Occurrences | — | 0,6 % | **0,1 %** | **17,9 %** | — | **36,3 %** | **1,0 %** | — |
| Gisement consommé | — | — | 54 / 398 | 293 / 398 | **394 / 398** | 393 / 397 | **148 / 399** | — |
| Lignes entièrement lues | 26 % | 26 % | 26 % | 26 % | **34 %** | 34 % | **59 %** | — |
| Signes déchiffrés | 58 % | 57 % | 57 % | 57 % | **69 %** | 69 % | **92 %** | — |

PT1 à PT3 sortent du tableau : ils datent d'avant le journal d'actions, et leurs chiffres
vivent dans les sections qui les dépouillent. PT8 est la première partie des trois actes —
sa durée et ses parts ne se comparent pas aux précédentes, qui s'arrêtaient à 13 signes.
PT9 : 429 relevés et 49 recoupements sortent du TSV ; la carte de fin collée au-dessus du
TSV (29 min 27, 271, 69, « corpus lisible 68 % ») était celle de PT2, et n'a pas été retenue.

PT1 à PT4 : l'auteur. **PT5 : un second joueur** (mon fils, 06/09/2026), et le premier
playtest instrumenté par le journal d'actions — d'où le détail de ce qui suit. Tout ce qui
y est chiffré sort du TSV, pas du souvenir. **PT10 : l'auteur de nouveau**, ce qui n'était
pas le plan — ses colonnes valent pour l'économie et pour rien d'autre.

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

## PT10 — la main a disparu du corpus

Playtest du 15/09/2026, le premier sur les trente signes de l'arbre : **96 min 35** au
chrono, 94 min 16 entre le premier et le dernier geste. Trois lectures fausses sur neuf,
contradiction déclenchée, aucune révision.

**Ce n'est pas le playtest qui était prévu.** PT10 devait se jouer avec quelqu'un qui ne sait
pas ce qu'il cherche ; c'est l'auteur qui a joué. Les questions de reconnaissance restent donc
entières et se reposent mot pour mot — ⟨grenier⟩, ⟨nous⟩ dans `les-lecteurs`, ⟨ne-pas⟩ posé
sur ⟨un⟩, la crue qui baisse, et « a-t-on remarqué qu'on choisissait ». Ce que cette partie
mesure, c'est l'économie et l'instrument. Elle y trouve deux défauts que neuf playtests, le
simulateur et tous les balayages avaient manqués.

### La main fournit 1,0 % des occurrences — PT6 est revenu

| | PT6 | PT7 | PT9 | PT10 |
|---|---|---|---|---|
| Part manuelle des Occurrences | **0,1 %** | 17,9 % | **36,3 %** | **1,0 %** |

166 000 occurrences relevées à la main sur **17,0 millions** produites. C'est le défaut que
R9 avait été écrite pour tuer, et qui revient par une porte que personne ne gardait.

Le chiffre est une reconstruction des tarifs figés depuis le TSV — `python outils/depouiller.py`
— contrôlée contre le journal lui-même : sur **71 intervalles que rien ne trouble**, la
production prédite par le modèle colle au ΔO relevé toutes les trente secondes à **0,0 %
d'écart médian**, 0,1 à 0,2 % aux extrêmes. Ce n'est pas une estimation.

La cause n'est pas le tarif, elle est dans la date. **147 des 148 relevés utiles tombent avant
la trente-deuxième minute**, quand le débit est encore petit — et le tarif d'une tablette est
figé à son premier relevé, pour toute la partie (règle 9). Le relevé moyen vaut ici
**1 120 occurrences** ; en PT9, les quatorze dernières tablettes valaient 11 996 par relevé.
Le 148ᵉ relevé de la partie arrive à 86:34, cinquante minutes après le 147ᵉ, et le 149ᵉ
n'existe pas : celui de 94:57 tombe à vide.

Le garde-fou existait pourtant. `outils/balayage.py` trie sur cette part depuis le 14/09/2026,
plancher à 15 %, et le réglage en place donne 22,9 à 23,4 %. Il n'a rien vu, pour une raison
qui vaut bien au-delà de ce chiffre : **il mesure le comportement du simulateur, pas celui du
joueur.** L'acheteur simulé relève tant que c'est rentable, donc tout du long ; ce joueur-ci a
sorti ce qu'il voulait sortir en trente minutes et n'y est jamais revenu. Le plancher tient en
simulation et casse à 1,0 % dans le jeu. Un garde-fou qui ne contraint que la main qui l'a
écrit ne garde rien.

### Cinquante minutes sans un geste dans le corpus

Le plus long trou de la partie sans relevé, recoupement, concordance ni navigation :
**49 min 48, de 36:46 à 86:34** — 53 % d'une partie de 94 minutes.

| | relevés | recoupements | concordances | navigations |
|---|---|---|---|---|
| avant 36:46 | 162 | 28 | 1 | 5 |
| **36:46 → 86:34** | **0** | **0** | **0** | **0** |
| après 86:34 | 2 *(dont 1 à vide)* | 4 *(après la fin)* | 0 | 1 |

Ce n'est pas l'idle de PT8 : il se passe beaucoup de choses à l'écran, vingt-deux signes
s'achètent dans l'intervalle, les compteurs montent de quatre ordres de grandeur. Mais règle 8
dit que les deux actions manuelles se font **dans le corpus**, et que c'est là le point de
bascule entre un incrémental habillé en déchiffrement et un jeu où l'on agit en lisant. Pendant
cinquante minutes, ce jeu-ci est un incrémental habillé.

Six tentatives de composition tombent dans le trou, et ce sont les seules. La grille n'est pas
le corpus : elle assemble deux signes déjà acquis, sans qu'on ait à lire une ligne.

### I6 tombe à 0,7 %, et ce n'est pas une bonne nouvelle

| tranche | 0–10 | 10–20 | 20–30 | 30–40 | 40–50 | 50–60 | 60–70 | 70–80 | 80–90 | 90–96 |
|---|---|---|---|---|---|---|---|---|---|---|
| part de la main | **79 %** | 15 % | 16 % | 9 % | 0 | 0 | 0 | 0 | 0 | 0 |

57 de Certitude recoupée sur environ 7 900 produites. Le mur d'ouverture est à 79 %, dans la
ligne des précédents (83 % en PT7, 63 en PT8, 75 en PT9) et toujours pas réglé. Tout le reste
est très en dessous du plafond — mais **les cinq dernières tranches sont à zéro exact**, et un
invariant qu'on respecte en ne jouant plus n'est pas respecté : il est vide.

**32 recoupements**, contre 49 en PT9. Le réglage du 09/09/2026 — `REC_R` porté à 1,30 —
prévoyait 32 ou 33 : le simulateur tombe juste au recoupement près. Mais la question qu'il
laissait ouverte était « 32 recoupements au lieu de 49 laissent-ils au geste sa place ? », et
la réponse mesurée est non : **les 32 tiennent dans les trente-sept premières minutes**, et
les quatre derniers sont postérieurs à la fin de la partie, sur ⟨N1⟩, un nom propre. Le seuil
d'alarme de PT10 était « sous une vingtaine sur la partie » ; il ne regardait pas au bon
endroit. Ce n'est pas le nombre qui a chuté, c'est sa répartition.

### Le simulateur tombe juste, pour la première fois depuis PT7

91,1 à 94,3 min annoncées toutes lectures justes (MOD-3) ; **94 min 16 jouées**, avec trois
lectures fausses et la contradiction armée sur les treize dernières minutes. PT8 et PT9
l'avaient pris à surestimer de 20 % ; recalé le 08/09/2026, il n'avait plus jamais été
confronté à une partie réelle. C'est fait.

Réserve, et elle est du même ordre que celle de PT9 : ce joueur-là joue comme l'acheteur du
simulateur. Ce que la mesure valide, c'est la cohérence du modèle avec lui-même.

### La contradiction a mordu, et personne n'a révisé

`peut-être` acheté à 83:41. Dette **6** — ⟨grain⟩ 3, ⟨eau⟩ 1, ⟨année⟩ 2 — contre un seuil de
5 : la Certitude est divisée par deux pour les treize dernières minutes. Le journal le confirme
au chiffre, de part et d'autre de l'achat : 155 de Certitude par tranche de trente secondes
avant, 102 après, quand les deux signes d'arbre pris entre-temps en annonçaient 104 une fois
divisés. La sanction a bien mordu.

**Zéro révision.** Le joueur a fini la partie sous sanction sans jamais rouvrir une lecture —
et `faux`, acheté à 90:23, n'y a rien changé : il allume une ligne et une seule (tablette 5,
⟨grain⟩ seul, puisque ⟨maison⟩ est lu juste), et le joueur est allé sur la tablette 14.

Le détail qui valide AMB-1 : **le signe qui fait franchir le seuil est celui qui ne rapporte
rien.** ⟨grain⟩ et ⟨eau⟩ font 4, sous le seuil. C'est ⟨année⟩ — deux points de dette, aucun
multiplicateur, `mfx` ne le touche pas — qui met à 6. Et les trois signes ambigus qui portent
un multiplicateur du côté de la Certitude, ⟨graver⟩ à la concordance, ⟨lire⟩ à la grammaire,
⟨il-faut⟩ à l'atelier, ont tous été lus juste. La prime n'a donc rien payé là où ça comptait,
et la sanction est tombée quand même. C'est exactement le contrat de la prime silencieuse,
vérifié par une partie et non par un balayage.

### `les-lecteurs` s'achète — et avant `sinon`

1 200 C pour trois attestations annoncées, acheté à 95:20, **devant `sinon` qui en coûte 800**
et qui sera le trentième et dernier signe. Le lexique affichait les deux prix et les deux
comptes ; le joueur a pris le plus cher et le plus maigre d'abord. C'est la réponse que PAR-2
attendait, et elle est positive — elle vaut ce que vaut un joueur qui a écrit le signe.

### Six compositions, six paires justes — et l'instrument disait le contraire

Le dépouillement a d'abord conclu à cinq échecs et une réussite. C'était faux, et c'est
l'instrument qui mentait : **les six paires étaient justes.** `tab+sar` (archive) et `im+sar`
(scribe) deux fois chacune, `en+la` (sinon) une fois, toutes refusées faute de Certitude et
non faute d'avoir trouvé — 900 C pour archive quand le joueur en avait 266, puis 592.

| | | |
|---|---|---|
| 51:03 | `tab + sar` | archive, 900 C — 266 en caisse |
| 55:50 | `im + sar` | scribe, 600 C — 220 en caisse |
| 58:09 | `ur + tem` | **acquis** — 60 C |
| 65:24 | `im + sar` | scribe, de nouveau |
| 72:09 | `tab + sar` | archive, de nouveau |
| 80:08 | `en + la` | sinon, 800 C — 465 en caisse |

Le carnet est donc resté **vide toute la partie** : une paire juste qu'on ne peut pas payer n'y
entre pas (règle 14), donc `compCost()` n'a jamais quitté 250 hypothèses et la rampe
anti-balayage ne s'est jamais armée. Les six tentatives ont coûté 1 500 hypothèses en tout,
sur un stock de trente-six mille. Ce n'est pas un défaut — c'est le contrat, « lire coûte moins
cher que chercher », observé pour la première fois chez quelqu'un qui lisait.

Reste que le joueur, lui, n'a aucun moyen de se souvenir d'une recette trouvée et impayable :
le carnet ne garde que les paires fausses. Il a retenté deux fois chacune des deux qu'il avait
trouvées, puis a fini par acheter `scribe`, `archive` et `sinon` à l'arbre, au prix fort.
Question ouverte, pas encore un défaut.

### L'outil qui manquait

PT9 et PT10 ont été dépouillés à la main, et **PT10 l'a été deux fois** : la première lecture
comptait cinq échecs de composition là où le joueur avait trouvé cinq recettes justes sans
avoir de quoi les payer. Le journal ne faisait pas la différence — c'est corrigé — mais rien
n'obligeait non plus à recompter à la main ce qu'un fichier contient déjà.

`outils/depouiller.py` rend désormais tout ce qui est chiffré dans cette section. Il rejoue le
modèle d'économie sur la timeline du journal, ce qui est la seule façon d'obtenir les tarifs
figés du relevé : ils dépendent du débit à l'instant de la première visite de chaque tablette
et ne sont écrits nulle part. Il lit aussi les journaux d'avant le 15/09/2026, où il
reconstitue les issues de composition depuis les recettes et le dit — c'est ce qui aurait
évité l'erreur. Les constantes viennent de `sim.py`, dont les six multiplicateurs sortent de
`run()` pour l'occasion : trois copies du modèle divergeraient au premier réglage, et deux
l'ont déjà fait une fois.

Il finit par se contrôler lui-même, et c'est la section à lire en premier — production prédite
contre production observée, écart médian attendu à zéro. C'est aussi le seul garde-fou contre
une divergence entre `sim.py` et `economie.js`, que rien ne surveillait jusqu'ici.

### Ce que l'instrument ne disait pas

Quatre questions du backlog étaient posées à un journal qui ne pouvait pas y répondre, et rien
ne le signalait — dans un TSV, une mesure absente se lit comme un zéro. `reviser` n'était pas
enveloppée du tout, le degré de doute n'était pas écrit à l'achat malgré ce qu'annonçait
`CLAUDE.md`, une paire juste impayable ne se distinguait pas d'un coup de sonde, et le chrono
gelait au dernier signe — d'où les six dernières actions de cette partie au même instant, et
l'absence de toute ligne de fin pour une partie terminée. Les quatre sont bouchés le même jour,
avec neuf assertions de plus. Le journal date désormais l'arrêt (`finjeu`) et l'ouverture de la
carte (`fin`) séparément, et l'écart entre les deux est la mesure de FIN-1.

### Ce que PT11 doit regarder ici

Tout ce que PT10 devait regarder, puisqu'il ne l'a pas fait — et une question neuve, la plus
grosse : **un joueur revient-il dans le corpus après la quarantième minute ?** Si la réponse
est non chez quelqu'un d'autre aussi, ce n'est plus un accident de joueur, c'est la seconde
moitié du jeu qui n'a rien à faire lire. Les deux leviers connus sont opposés — ralentir encore
le dégagement (`REV_R`) pour que des tablettes neuves restent à sortir tard, ou rendre le
gisement moins épuisable — et aucun des deux ne se règle avant d'avoir la mesure. Ne pas
toucher `REL_K` : le tarif n'est pas en cause, la date l'est.

## `faux` ne donne pas le corrigé — il montre où le texte ne tient pas

15/09/2026, MOD-3. Le premier lot où le jeu dit enfin quelque chose. Trois règles écrites
cette semaine — 17, 18, 19 — tiennent toutes sur « le jeu ne dit jamais que vous vous êtes
trompé ». Il fallait savoir ce que `faux` retourne exactement, et la réponse était dans le
design doc depuis le début, à un endroit où personne n'était allé la chercher.

### La phrase qui a tranché le lot

Le §6 et le §10 disent la même chose : « `faux` affiche **rétroactivement les erreurs déjà
commises** », « le joueur voit rétroactivement tout ce qu'il a mal traduit depuis le début ».
Lu seul, cela veut dire : le corrigé.

Le §11 dit autre chose. La relecture de fin surlignera toutes les erreurs de traduction de la
partie, **« y compris celles jamais détectées »**.

S'il existe des erreurs jamais détectées à la fin de la partie, c'est que `faux` n'a pas donné
le corrigé. Les deux passages ne se contredisent que si l'on suppose que `faux` nomme les
signes. Il ne les nomme pas : **il allume les lignes où la lecture retenue ne se construit
pas.** C'est-à-dire exactement ce que le §8 appelle depuis le premier jour le seul indice
fiable — le texte lui-même. `faux` ne remplace pas la lecture ; il rend visible ce qu'un
lecteur attentif aurait vu tout seul.

Et ce choix-là fait tomber juste, d'un coup, trois décisions prises séparément.

### Ce qui ne s'allume pas

| Lectures fausses | Lignes allumées |
|---|---|
| ⟨grain⟩ seul | tablette 5 — « maison 1 · poussière 20 » |
| ⟨maison⟩ seul | la même ligne, par l'autre bout |
| **les deux** | **aucune** |
| ⟨eau⟩, ⟨année⟩, ⟨lire⟩, ⟨il-faut⟩ | **aucune** |
| ⟨ne-pas⟩ · ⟨avant⟩ · ⟨graver⟩ | tablette 5, 15, 30 |
| **les neuf** | **trois lignes sur cinq** |

- **Les paires réparantes n'allument rien.** « Vingt mesures de poussière à la tombe 1 » se
  tient : la ligne ne s'allume pas. Le §7.3 avait décidé le 14/09 que « le texte ne trahit
  rien » pour ces trois paires — c'est désormais vrai *mécaniquement*, en une ligne de code
  (`sauf` dans `RUPTURES`), et non plus seulement en intention.
- **Les quatre signes sans rupture n'allument rien.** `lire` et `il-faut` sont conçus pour ne
  casser nulle part ; `eau` et `année` n'ont aucune rupture textuelle, et leur seul indice
  reste celui du §7.4, distributionnel, qu'a ouvert MOD-2. Ce sont, très exactement, les
  erreurs « jamais détectées » que promet le §11.
- **Se tromper partout cache deux de ses erreurs.** Neuf lectures fausses n'allument que trois
  lignes : la paire ⟨grain⟩+⟨maison⟩ s'auto-répare, et quatre signes ne cassent nulle part.
  C'est la mesure qui résume le lot, et elle n'était pas cherchée.

### C'est la ligne qui s'allume, jamais le jeton

Marquer le signe fautif le nommerait — l'oracle que tout le reste du jeu refuse. Une ligne
allumée porte quatre ou cinq signes, dont deux ou trois ambigus : elle réduit le champ, elle
ne tranche pas. Le joueur relit, compare, et décide ; le panneau lui dit seulement *combien*
de passages ne se construisent pas, jamais lesquels ni pourquoi.

Un test le verrouille : sur la ligne allumée, zéro jeton marqué et trois signes ambigus
présents.

### Le prix, encore une mesure

Au bout de la Modalité, `faux` tombe **2,1 minutes avant la fin** du prototype, à tous les
prix de 900 à 1 100 — le même plateau que `peut-être` la veille, et pour la même raison : la
queue de partie est un tunnel d'achats forcés. À **700 C**, entre `il-faut` et `sinon`, il en
laisse **six**, de quoi lire les lignes allumées et payer deux ou trois révisions. À ce rang,
les neuf signes ambigus sont tous tranchés avant lui : il ne renseigne aucun choix à venir.

### La tablette 26, sans un mot ajouté

Ses cinq dernières lignes deviennent lisibles à l'achat :

```
avant · tablette 6 · faux
avant · tablette 13 · faux
peut-être eau · faux
⟨je⟩ graver · faux
il-faut faux ne-pas
```

La dernière scribe est revenue sur l'archive pour marquer comme fausses les tablettes qui
espéraient. Elle annule « peut-être eau » — les deux seuls mots d'espoir du corpus, gravés
quatre-vingt-dix-sept ans plus tôt et que le joueur a lus douze minutes avant, à l'achat de
`peut-être`. Le joueur vient de faire exactement le même geste sur son propre corpus. Rien
n'est commenté, et ⟨je⟩ reste illisible jusqu'à l'acte IV.

### Ce que la boucle donne maintenant

`peut-être` classe l'aveuglement, `faux` montre où ça casse, la révision paie, la
contradiction se lève. Les quatre pièces se répondent, et aucune ne dit au joueur qu'il s'est
trompé :

- le **doute** dit ce qu'on n'avait pas regardé — le même chiffre pour les deux lectures ;
- **`faux`** dit quelles lignes ne se construisent pas — sans nommer le signe ;
- la **révision** repeint — sans rendre de verdict ;
- la **contradiction** se lève — sans dire laquelle des révisions l'a levée.

Un signe à fort doute dont aucune ligne ne s'allume est soit juste, soit incassable. Le joueur
ne saura pas lequel avant la relecture de fin, et c'est FIN-3 qui portera l'aveu.

### Mesuré

**91,1–94,3 min** toutes lectures justes pour 30 signes, **85,9–89,1** toutes fausses,
**98,1–101,2** quand la contradiction s'arme, **102,1–105,1** pour la paire réparante — qui
reste le pire cas du jeu. Écart max 5,2 · main 22,2–28,0 % · tranches ≥ 10′ ≤ 26 %. Garde-fou
de durée re-basé à **(83, 96)**. `outils/verifier.py` passe de 239 à **256 assertions**.

---

## La contradiction — le pire cas n'est pas celui qui se trompe le plus

15/09/2026, CONTR-1. La dette courait depuis AMB-3 et personne ne la lisait. Elle a
maintenant son unique lecteur, et la boucle se ferme : voir son doute, payer pour rouvrir,
ou encaisser.

### Deux questions, et le prototype n'avait la réponse ni à l'une ni à l'autre

**Où se déclenche-t-elle ?** Le design doc dit « au franchissement de chaque acte », et §10
place la première à la fin de l'acte III. Or dans le prototype, la fin de l'acte III *est*
le dernier achat de l'arbre : `nArbre() === NGL` clôt la partie à la seconde même, et la
sanction n'aurait pas une seconde pour mordre. La règle 16 avait déjà donné cette leçon sur
`les-lecteurs` ; elle vaut ici telle quelle.

Et la déclencher plus tôt — à `année`, le seul autre franchissement identifiable — l'impose
**trente minutes avant que `peut-être` n'existe**, donc sans explication ni remède. Le joueur
ne lirait pas une sanction : il lirait un bug.

Elle se solde donc à **l'ouverture du doute**, et la règle générale dont le prototype ne voit
que le premier cas s'écrit : *la contradiction s'évalue à chaque franchissement d'acte à
partir de `peut-être`.* Avant lui, le jeu n'admet pas qu'une lecture puisse être fausse ; il
ne peut pas en faire payer le prix. Ce n'est pas un aménagement de prototype, c'est la
condition pour que la sanction soit lisible comme telle.

**Quel passage refuse ?** « Un passage refuse de se résoudre » est la fiction de
l'étranglement, et il fallait en choisir un. Deux impasses d'abord :

- **Le choisir d'après les signes mal lus le désignerait.** C'est l'oracle que les règles 17
  et 18 refusent, et ce serait le plus gros de tous : la ligne pointerait exactement ce qu'il
  faut réviser.
- **Le choisir d'après la densité** donne une ligne de registre générée, identique à quarante
  autres. Les six lignes les plus contestées du corpus sont toutes le même gabarit,
  `maison N · grain 20 · avant · année ne-pas · si lire`.

Le passage est donc **fixe**, et choisi pour ce qu'il dit : **tablette 17, quatrième ligne —
« eau · ne-pas tablette »**, la note de tri qui constate qu'un relevé manque. Le jeu le fait
manquer. Elle sort de terre quinzième, donc elle est sous les yeux du joueur depuis longtemps
quand elle s'éteint ; elle n'est pas une ligne de charge — celles-là sont deux lignes plus
bas, où `devenir-lecture` s'assemble sous les yeux du joueur (acte V) ; et la tablette 21,
l'abécédaire, a été écartée exprès : y attirer l'œil à la 77ᵉ minute, et seulement pour les
joueurs endettés, déséquilibrerait la reconnaissance de l'acte IV pour une partie d'entre eux
seulement.

Reste un risque qu'aucun choix de ligne ne supprime : **le joueur peut croire que le passage
retenu contient ses erreurs.** C'est pourquoi la ligne de journal le dit en toutes lettres —
« Ce n'est pas lui qui est en cause : c'est ce que j'ai lu ailleurs, et je ne sais pas où. »
Le jeu a le droit de parler ici : CONTR-1 demande que l'état soit affiché *sans ambiguïté*.
Il nomme la sanction et sa sortie, jamais un signe.

### Le seuil, et ce qu'il trie

Les poids de dette étant tirés des attestations (AMB-3), le seuil n'est pas un chiffre libre :
il découpe des profils de lecture réels.

| | Dette | Armée ? |
|---|---|---|
| lecture parfaite | 0 | non |
| ne rate que les deux incassables — `lire`, `il-faut` | 3 | non |
| la paire réparante ⟨grain⟩ + ⟨maison⟩ | 6 | **oui** |
| pile ou face sur les neuf, en moyenne | 8 | **oui** |
| toutes fausses | 18 | **oui** |

À **5**, un lecteur qui a fait tout ce que le texte permet passe avec de la marge — les deux
seuls signes conçus pour ne pas casser pèsent 3 à eux deux — et **la paire réparante
déclenche**, ce que le §7.3 exigeait le 14/09 en décidant de la laisser passer. Depuis que
MOD-2 a refermé le §7.4, `eau` et `année` ne sont plus des devinettes : le plancher
incompressible d'un bon lecteur est vraiment de 3, et non de 6.

### Le pire cas n'est pas « tout faux »

Mesuré au simulateur, sur un joueur qui **ne révise jamais** — le pire cas, puisque le
simulateur n'a pas de modèle de lecture :

| | Durée |
|---|---|
| lecture parfaite | 90,5–93,7 min |
| les deux incassables seulement | **89,1–92,4 min** |
| toutes fausses | 96,6–99,5 min |
| **la paire réparante seule** | **100,5–103,4 min** |

Trois choses là-dedans, et deux n'étaient pas prévues.

**La sanction retourne la prime.** Se tromper partout faisait gagner 5,5 minutes (AMB-1) ; il
en coûte désormais 11 de plus, soit 6 de perte nette. L'optimum local du design doc §8 reste
un optimum *local* : il paie pendant soixante-dix minutes et se reprend au franchissement.

**Rater les deux signes incassables paie, et ne coûte rien.** 89,1 min, la partie la plus
rapide du tableau. `lire` et `il-faut` sont conçus pour ne casser nulle part
(`docs/corpus.md` §7.4) ; leur dette de 3 passe sous le seuil. Le joueur qui les rate finit le
jeu plus vite, sans savoir qu'il a lu une autre histoire — et c'est exactement ce que le §7.4
promettait.

**Le pire cas est la paire réparante**, et c'est la mesure que ce lot n'attendait pas : elle
prend la sanction entière avec la prime de deux signes seulement, là où « tout faux » en
encaisse neuf. Le joueur que le texte ne peut pas prévenir est donc celui qui paie le plus
cher. Le §7.3 avait écrit, en décidant de ne rien faire, que « la paire creuse le piège au
lieu de le combler ». Trois minutes de plus que la partie du joueur qui s'est trompé sur tout.

### Ce que la sanction ne prend pas

R2 : on ne perd que du débit. Un test le vérifie en basculant la contradiction sans rien
acheter — `pctTablette`, les deux mesures de `mesures()` et le compteur du lexique sont
identiques armée et levée. Le passage retenu ne compte pas comme illisible : le joueur **sait**
ces mots, et c'est le passage qui refuse de se résoudre, pas sa compréhension qui recule.

Levée, elle ne se réarme pas. Il n'y a plus de franchissement d'acte dans le prototype, et on
ne ballotte pas un joueur entre deux états sur un chiffre qu'il ne voit pas.

### Le bonus rétroactif, enfin payable

Le design doc §8 le promettait à CONTR-2, et le lot A l'avait laissé de côté en écrivant
pourquoi : *un bonus visible est un verdict*. Il se paie ici, et il ne dit toujours rien —
une révision qui fait repasser la dette sous le seuil **lève la contradiction**. Le joueur
voit son débit revenir et un passage se résoudre ; il n'apprend pas lequel de ses signes était
faux, ni même si c'est celui qu'il vient de rouvrir. Une révision qui ne suffit pas ne dit
rien du tout.

### Mesuré

`outils/sim.py` rend un quatrième bloc, le seul endroit du projet où la sanction se lit en
minutes. `outils/balayage.py`, lui, désarme la contradiction : il mesure le **rythme** d'un
réglage, et compter onze minutes de punition ferait rejeter un bon réglage pour une peine
qui n'est pas la sienne et qui a une sortie.

Rythme inchangé — 90,5–93,7 min lectures justes, 85,2–88,1 toutes fausses, écart max 5,2,
tranches ≥ 10′ ≤ 26 %. `outils/verifier.py` passe de 224 à **239 assertions**.

---

## Le doute ne dit pas l'erreur, il dit l'aveuglement

15/09/2026, MOD-2 avec CONTR-2 et CONTR-3. `peut-être` est le pic de malaise du jeu, et il
n'ajoute pas une mécanique : il retire une protection. Depuis la première seconde le lexique
affiche chaque mot comme si le joueur l'avait su ; ce signe-là lui dit que onze de ses
lectures en supportaient une autre, et qu'il a tranché sans jamais en être averti.

### La question du lot : de quoi un degré de doute peut-il être fait ?

Le §7.3 de `docs/corpus.md` demande un doute « calculé par le jeu et non par la lecture ». En
l'écrivant on bute tout de suite sur le mur : **le jeu connaît la vérité, et il n'a pas le
droit de s'en servir.** Un doute calculé sur la justesse serait l'oracle que la prime
silencieuse d'AMB-1 refusait la veille.

Reste ce que le jeu sait d'autre : le corpus, et le travail du joueur. Et le corpus ne
distingue pas deux lectures d'un même signe — il est le même dans les deux cas. Donc, quel
que soit le calcul, **le chiffre est identique pour la lecture juste et pour la fausse**.
C'est la contrainte, et c'est elle qui a donné la réponse : si le doute ne peut pas dire
l'erreur, qu'il dise ce qui la produit — **l'aveuglement au moment de trancher.**

Le degré de doute d'un signe se fait donc de deux moitiés :

- **ce qui était sorti de terre** : la part de ses attestations que le corpus offrait à lire
  quand le joueur a payé. On ne peut pas avoir lu ce qui n'était pas déterré.
- **ce qu'il en a fait** : une concordance sur ce signe vaut plein — c'est l'instrument qui
  rassemble toutes ses attestations d'un coup, et il existe pour ça (règle 11). Un
  recoupement de deux d'entre elles vaut moitié. N'avoir rien fait ne vaut rien, même avec
  les trente tablettes sous les yeux : **avoir pu lire n'est pas avoir lu.**

Trois propriétés en sortent, et ce sont elles qui font tenir le système.

1. **Le chiffre ne ment pas.** Il dit « tu as décidé de ça à l'aveugle », ce qui est vrai,
   et jamais « tu t'es trompé », ce que le jeu n'a pas le droit de dire. Il corrèle quand
   même avec l'erreur — on se trompe davantage sur ce qu'on n'a pas regardé — sans jamais la
   désigner.
2. **Regarder après coup ne le fait pas baisser.** Une concordance faite aujourd'hui n'annule
   pas une décision prise à la douzième minute. Mesuré dans les tests : ⟨grain⟩ concordé
   avant l'achat sort à 20, ⟨maison⟩ acheté au même instant sans rien en faire sort à 72, et
   le concorder ensuite ne bouge pas son chiffre d'un point. Sans cette règle, le doute
   serait une jauge qu'on vide en promenant la souris.
3. **Seule la révision le recalcule**, parce qu'elle seule re-décide. La lecture devient donc
   le chemin vers la révision, pas son substitut.

**Un premier réglage a été jeté.** La forme multiplicative — part sortie de terre × poids du
travail — tassait les neuf signes entre 83 et 99 %. Vrai, inutile : tout était « très
douteux » et la jauge ne classait plus rien. En deux moitiés additives, l'éventail va de 17 à
97 sur la même partie. C'est la deuxième fois de la semaine qu'une formule juste est
inutilisable faute d'échelle.

### La révision ne dit pas si l'on avait raison

CONTR-2 : rouvrir un signe, repayer, choisir à nouveau. La fenêtre est celle de l'achat —
mêmes deux mots, même tirage au sort de l'ordre — et **elle ne rend aucun verdict.** Elle
repeint le corpus, et c'est au joueur de lire ce qui en sort. « Vingt mesures de poussière à
la maison 1 » n'a pas de sens ; c'est la seule chose qui le lui dira.

Le design doc prévoyait un **bonus rétroactif** quand on retombe sur la lecture juste. Il
n'est pas de ce lot, et la raison est la même que pour tout le reste : *un bonus visible est
un verdict*. Payer 240 C et voir une récompense apparaître, c'est apprendre qu'on s'était
trompé — et c'est acheter la réponse au lieu de la lire. Il attend CONTR-1, où la dette
devient lisible et où il pourra être payé en dette effacée, c'est-à-dire sans rien annoncer.

Ce que la révision coûte, en revanche, est bien réel et ne se voit pas non plus : reprendre
la lecture juste **retire les 25 % de prime** que la fausse rendait. Corriger, c'est payer en
Certitude et perdre du débit pour gagner du sens. C'est exactement l'optimum local du design
doc §8, et il tombe là où AMB-1 disait qu'il tomberait.

### CONTR-3, mesuré

Le prix croît par révision faite, jamais par signe — la leçon de `REC_R` et de `COMP_R`, pour
la troisième fois : dans une économie exponentielle un coût de base ne freine rien, seul un
taux mord. À 240 C et ×1,6 :

| Révisions | Coût cumulé | Part de ce qui reste à dépenser |
|---|---|---|
| 1 | 240 C | 5 % |
| 3 | 1 238 C | 27 % |
| 4 | 2 221 C | 49 % |
| 5 | 3 794 C | 83 % |
| 9 | 27 088 C | **595 %** |

Les 4 550 C sont ce que le joueur dépense encore en signes après `peut-être` — mesuré, pas
estimé. Balayer les neuf coûte donc près de six fois son budget entier, tandis que trois
révisions choisies en coûtent un quart. Lire pour choisir lesquelles domine strictement le
tirage au hasard, et c'est tout ce que CONTR-3 demandait.

### Le prix de `peut-être` est une mesure, pas un cran de branche

Placé au bout de la Modalité, à 900 ou 1 100 C, il tombe **2,4 minutes avant la fin du
prototype** : le panneau s'ouvre, et la partie s'arrête. À 450 C, entre `si` et `il-faut`, il
laisse **quatorze minutes** — de quoi faire trois ou quatre révisions et les payer en signes
non achetés.

Un effet de bord qu'on n'avait pas cherché : à cette place, `il-faut` se tranche **après**
l'ouverture du panneau. La dernière décision ambiguë du prototype est donc la seule que le
joueur prenne en sachant ce qu'il risque.

### Le §7.4 est refermé, et sa prémisse était fausse

Le §7.4 proposait une rupture *distributionnelle* pour `eau` et `année`, qui n'ont aucune
rupture textuelle : « ⟨année⟩ porte toujours un nombre et n'est jamais opposé à ⟨nuit⟩ ».
Vérifié contre le corpus : **⟨année⟩ n'est suivi d'un nombre que 67 fois sur 139.** La table
avait tort une fois de plus, et une fois de plus le texte disait mieux.

Les 72 autres, ⟨année⟩ est suivi de ⟨ne-pas⟩ — « année : pas de », l'absence de compte, qui
est un compte, puisque ⟨zéro⟩ **est** ⟨ne-pas⟩⟨un⟩. Mesuré ainsi, en *cadre de nombre* :

| | ⟨année⟩ | ⟨nuit⟩ | ⟨maison⟩ | ⟨grain⟩ | ⟨ne-pas⟩ | ⟨graver⟩ |
|---|---|---|---|---|---|---|
| en cadre de nombre | **100 %** | **0 %** | 100 % | 98 % | 0 % | 2 % |

Le contraste est total, là où la formulation d'origine donnait 48 % contre 0 %. Un soleil
qu'on compte, ou dont on dit qu'il n'y en a pas, n'est pas un soleil.

Le chiffre paraît en infobulle, sur les signes lus comme sur les autres, et seulement après
`peut-être`. Il est identique pour les deux lectures — c'est ce qui l'autorise à être montré.
Et il ne se trouve **qu'en comparant deux signes** : le jeu ne dit nulle part que ⟨année⟩ et
⟨nuit⟩ sont à comparer. Une phrase absurde se trouve en lisant ; une distribution impossible
se trouve en travaillant, et c'est le geste que ce jeu prétend enseigner.

### La dette cesse d'être un solde

Trouvé par un test, et c'est le genre de défaut qui ne se serait jamais vu : tenue en solde,
la dette d'AMB-3 dérivait dès qu'une lecture changeait autrement que par le chemin prévu. Un
compteur faux sur un chiffre que **personne n'affiche** ne se manifeste jamais — jusqu'à
CONTR-1, qui en fera son unique intrant, deux lots plus tard.

Elle se **déduit** désormais des lectures au lieu de s'accumuler. Juste par construction,
elle survit à n'importe quelle sauvegarde, et CONTR-1 n'aura rien à migrer. La règle générale
vaut d'être écrite : *un état dérivable ne se stocke pas, surtout quand rien ne le lit.*

### Mesuré

**90,5–93,7 min** toutes lectures justes, **85,2–88,1** toutes fausses, pour 29 signes. Écart
max 5,2 · main 21,6–25,8 % · tranches ≥ 10′ ≤ 26 %. `peut-être` tombe à 76,7–79,8′.

Garde-fou de durée re-basé à **(82, 96)** — le rituel de tout lot qui ajoute un signe.
`outils/verifier.py` passe de 202 à **224 assertions**.

Une partie d'avant ce lot n'a aucun relevé de décision. Ses signes ambigus comptent alors
pour cent : le jeu ne sait pas ce que le joueur avait sous les yeux, et la seule réponse
honnête à « je n'en ai aucune trace » est le doute entier.

---

## Trancher à l'achat — la prime ne se voit pas, et c'est tout le système

15/09/2026, AMB-1. Avec ce qu'AMB-2 et AMB-3 ne pouvaient pas laisser dehors : le mot faux
partout, et la dette qui court sans être lue. Le texte était écrit depuis la veille
(`docs/corpus.md` §7) ; ce lot est la mécanique, et elle a tenu à une seule décision.

### La décision : la prime de 25 % est silencieuse

Le design doc §8 dit « effet mécanique : nominal / **+25 %** ». Restait à savoir si l'écran de
choix montre ces 25 %.

Il ne les montre pas, et ce n'est pas un scrupule d'ambiance. Deux lignes d'effet
différentes — « +50 % à la grammaire » contre « +62,5 % » — feraient de la prime un
**oracle** : prends toujours le plus gros chiffre et tu sais, pour toujours et sans lire, que
tu viens de choisir la lecture fausse. Onze signes ambigus deviendraient onze péages. La
règle 14 dit que la grille de composition ne renseigne jamais, pas même par son silence ;
l'écran de choix est le même objet, et un « +62,5 % » y serait le renseignement le plus
franc du jeu.

Les deux propositions portent donc le même tracé, le même prix, la même ligne d'effet. La
seule chose qui les distingue est le mot — ce qui est exactement ce qu'il y a à trancher.

**Corollaire, et il déplace le design doc :** la prime ne décide rien à l'achat, puisqu'on ne
la voit pas. Elle mord à la **révision**. Rouvrir un signe pour corriger sa lecture (CONTR-2)
coûtera le prix *et* 25 % du débit qu'il rendait. L'optimum local du §8 n'est pas dans le
choix : il est dans le refus de le défaire. C'est plus juste que ce qu'on croyait coder — un
biais de confirmation qu'on paie pour entretenir.

Deux précisions qui en découlent :

- **La prime porte sur le bonus, pas sur l'instrument.** +30 % devient +37,5 %, pas +62,5 %.
  L'autre lecture ferait de chaque signe mal lu un quart d'instrument gratuit, ce qui à cinq
  signes déplacerait l'économie bien au-delà de ce qu'un piège invisible doit peser.
- **Un signe qui ne multiplie rien ne gagne rien.** Quatre des neuf signes ambigus de l'acte
  III sont dans ce cas — ⟨maison⟩, ⟨année⟩, ⟨avant⟩, ⟨ne-pas⟩. Leur inventer un effet pour
  porter la prime, c'est déplacer une économie réglée sur neuf playtests au profit d'un
  chiffre que personne ne voit. Se tromper sur eux est une perte sèche, et le joueur ne peut
  pas le savoir : le piège en est plus profond, pas moins.

### Ce que la mesure a dit, et que personne n'avait annoncé

Toutes lectures justes : **89,7–92,9 min**, écart max 5,2, main 22,9–23,4 %, tranches ≥ 10′
≤ 26 % — identique au chiffre près à la veille, et c'était le contrat.

Toutes lectures fausses : **84,4–87,5 min**, écart max 4,6, main 23,1–24,8 %, tranches ≥ 10′
≤ 25 %. Se tromper partout fait gagner **cinq minutes et demie**, soit 6 %. C'est le « paie
mieux à court terme » du §8, chiffré pour la première fois, et c'est modeste — ce qu'il faut
pour que la révision coûte sans que la partie d'un lecteur soit punie.

Mais la répartition ne ressemble à rien de ce que le récit annonce. Signe par signe, à trois
cadences :

| Signe mal lu | Ce que ça rend |
|---|---|
| `grain` → poussière | **−2,2 min** |
| `graver` → couper | −1,6 min |
| `lire` → compter | −1,3 min |
| `il-faut` → on peut | −0,1 min |
| `eau` → sang | **0,0 min** |
| `maison` · `année` · `avant` · `ne-pas` | 0,0 min *(aucun multiplicateur)* |

Deux choses là-dedans.

`eau` ne rend **rien**, alors qu'il porte +30 % à la Table de fréquences. En fin de partie les
hypothèses ne sont pas ce qui manque — la même raison qui faisait que le bonus d'atelier
d'`il-faut` ne déplaçait pas la durée de l'acte (MOD-1, 12/09). Deux des cinq signes qui
portent un multiplicateur ne paient donc pas du tout, et c'est mesuré, pas choisi.

Et le signe où la prime paie le plus est **⟨grain⟩ : 3 C, acheté à la troisième minute**,
quatre tablettes sorties de terre, aucun instrument, rien à recouper. C'est-à-dire que le
piège est appâté le plus fort là où le joueur a le moins de quoi trancher. On peut le lire
comme un défaut ; je le lis comme le contraire, parce que la rupture de ⟨grain⟩ est à la
tablette 5, sixième à sortir de terre — la plus précoce du lot. Le pari le plus cher est
aussi celui dont la réponse arrive le plus vite. À vérifier en playtest, pas à régler.

### Le mot faux était la partie facile

`motDe()` remplace tous les accès à `.mot`, le corpus se repeint entièrement à chaque achat,
et AMB-2 est tenu du même coup : **1 726 attestations sur 3 838 — 45 % du corpus** — changent
de mot selon ce qu'on a lu, blocs générés et tablettes déjà lues compris.

Ce qui a demandé le travail, c'est tout ce qui **répète un mot ailleurs que dans le corpus**.
Huit endroits où le jeu se serait contredit tout seul, et une contradiction du jeu avec
lui-même est un renseignement :

- **Les lignes de journal des composés.** `docs/corpus.md` §7.2 donnait les mots faux dérivés
  — ⟨tombe⟩⟨grain⟩ fait « caveau » — mais pas les lignes de journal. Annoncer « le grenier —
  la maison du grain » à un joueur dont le corpus dit « caveau » et « tombe », c'est lui dire
  qu'il s'est trompé. Dix lignes écrites ici, dont trois pour ⟨grenier⟩ seul : poussier,
  caveau, ossuaire.
- **Quatre lignes d'effet présupposaient une lecture.** « chaque tablette porte sa **date** »
  pour ⟨année⟩ était la pire, parce qu'elle s'affiche **avant** le choix : le jeu soufflait la
  réponse au moment précis où il demandait de trancher. Réécrites pour tenir sous les deux
  lectures. Deux autres nommaient carrément le mot — « le grenier se lit », « le zéro se lit ».
- **L'infobulle de la barre de tablettes** répétait « · année 103 ». Elle dit maintenant le
  mot retenu.
- **La citation de la carte de fin** était la ligne de ⟨dernière-année⟩, en dur dans le HTML.

Reste un résidu, écrit ici pour ne pas être découvert par surprise : les lignes d'effet
d'⟨avant⟩ et ⟨après⟩ disent « dans l'ordre du temps ». Sous « dessous », l'ordre est
stratigraphique et le jeu le nomme autrement que le joueur. C'est le seul endroit connu où il
le fait encore, et le corriger demande de réécrire la colonne des effets en pur vocabulaire
de mécanisme — une question pour MOD-2, quand le doute deviendra affichable.

### Le seul hasard du jeu

L'ordre des deux lectures est tiré au sort à chaque ouverture de la fenêtre. La juste toujours
à gauche se retiendrait en une partie, et la seconde n'aurait plus rien à trancher. Ce tirage
ne décide de rien : il empêche seulement une **position** d'être une réponse.

### Ce que le lot ne fait pas

- **La dette court et personne ne la lit.** De 1 à 3 points par lecture fausse, déduits des
  attestations et non choisis — 315 occurrences pèsent plus que quatre. Maximum 18 points pour
  les neuf signes de l'acte III, et une paire réparante en vaut 6 à elle seule, comme le §7.3
  l'exigeait. Aucun compteur, aucune infobulle, aucune ligne à la carte de fin. CONTR-1 sera
  son premier lecteur.
- **AMB-4 est fait pour les cinq ruptures qui existent dans l'arbre d'aujourd'hui** : ⟨grain⟩
  et ⟨maison⟩ tablette 5 (chacune testée en tenant l'autre au juste, §7.3), ⟨ne-pas⟩ sur
  `sinon`, ⟨avant⟩ tablette 15, ⟨graver⟩ tablette 30. Un test vérifie aussi que la **paire
  réparante passe** — « tombe 1 · poussière 20 » se rend sans que rien ne bronche, ce qui est
  la décision du 14/09 et non un défaut.
- **Le §7.4 reste ouvert.** `eau` et `année` n'ont toujours aucune rupture. La sortie proposée
  — admettre une rupture *distributionnelle*, trouvable à la Concordance et à la Table de
  fréquences — n'est pas de ce lot : elle demande une mécanique de détection, pas une table.

### Le garde-fou de durée s'élargit, et c'est le prix

`outils/balayage.py` gagne un axe : chaque combinaison est jouée aux trois cadences **et aux
deux lectures extrêmes**. Deux réglages entre lesquels seule la lecture tranche n'existent
pas — c'est le même réglage, joué par deux joueurs qui n'ont pas lu la même chose.

La fenêtre de durée passe donc de (86, 95) à **(81, 95)** pour couvrir les deux bouts. Elle
trie d'autant moins, et c'est assumé : aucun des trois autres garde-fous n'est touché par la
lecture (pire tranche 26 % juste contre 25 % faux, écart 5,2 contre 4,6, main 22,9 % contre
23,1 %), et ce sont eux qui trient. 38 combinaisons sur 54 passent, le réglage en place
compris. Rappel du 14/09 : cette fenêtre n'est pas un invariant, elle se re-base à chaque lot.

`outils/verifier.py` passe de 177 à **202 assertions**.

---

## Les onze lectures fausses — trois ruptures n'existaient pas

14/09/2026, TXT-1. Le chemin critique du projet : le texte des onze lectures fausses bloque
l'ambiguïté (E3), donc l'Élève (E5), donc `peut-être` et `faux`, donc la relecture de fin. Le
backlog le donnait pour « du travail d'écriture, pas de code ». C'en est — mais la moitié du
travail a été de vérifier, et c'est la vérification qui a tout déplacé.

La table du §7 de `docs/corpus.md` existait depuis le premier jour : onze signes, onze mots faux,
et pour chacun une colonne « où ça casse ». Elle avait été écrite **avant** le corpus. Le corpus a
été écrit ensuite, et personne n'était retourné confronter les deux.

### La méthode : rendre le corpus, puis substituer

Un script hors jeu relit `src/corpus.js`, remonte chaque identifiant à son mot français et sort les
705 lignes des trente tablettes en clair. On y cherche alors, non pas le signe, mais **tous ses
contextes distincts** : `grep`, normalisation des nombres, `sort | uniq -c`. Trois cent quinze
attestations de `grain` se réduisent à seize contextes ; deux cent quatre-vingt-dix de `ne-pas`, à
vingt-deux. À cette taille-là, on peut lire chaque contexte avec le mot faux à la place du juste et
juger s'il tient.

C'est exactement le geste que le jeu demande au joueur, et c'est exactement ce que fait la
Concordance. Ça vaut d'être noté : l'outil qui manquait à l'auteur pour écrire cet acte est celui
qu'il avait déjà donné au joueur en PT9.

> *Corrigé le 15/09/2026.* Cette entrée écrivait « 735 lignes », repris ensuite dans le backlog et
> dans le `CLAUDE.md`. Le compte est **705** — `src/corpus.js`, trente tablettes. Le chiffre n'avait
> jamais été compté, seulement recopié, ce qui est exactement le défaut que cette section-ci
> reproche à la table du §7. Rien de ce qu'il servait à dire ne change : la séquence
> ⟨ne-pas⟩⟨ne-pas⟩ n'existe toujours nulle part.  *(Tous les autres chiffres de l'entrée ont été
> recomptés à cette occasion et sont justes : 315, 290, 131, 41, 24, 1 533.)*

### Ce que la confrontation a cassé

Trois des onze ruptures annoncées n'existent pas dans le texte.

| Annoncé | Ce que dit le corpus |
|---|---|
| `eau` casse tablette 25 : « champ 3 · sang 21 » | La ligne est `champ 3 · grain 21`. Les champs se mesurent en grain — **aucune** ligne du corpus ne met un nombre d'eau à côté d'un champ. |
| `ne-pas` casse sur « ne-pas ne-pas » (tablette 26) | La séquence n'existe **nulle part** dans les 705 lignes. |
| `avant` casse « au réordonnancement chronologique » | Le rangement marche aussi bien avec « dessous » : l'ordre stratigraphique est un ordre. La rupture annoncée était mécanique, or AMB-4 demande une rupture **textuelle**. |

Deux des trois se remplacent, et par mieux :

- **`ne-pas` → « fin » casse sur `sinon`.** `sinon` est ⟨si⟩⟨ne-pas⟩ ; il se tient sur la même ligne
  que ⟨ne-pas⟩ **131 fois**, dès la tablette 5, sixième à sortir de terre. « si fin · à la fin » :
  deux signes différents, presque le même mot, cent trente et une fois. Et ⟨ne-pas⟩⟨un⟩ — le zéro —
  devient homographe de ⟨finir⟩⟨un⟩, qui est `le-dernier`. La rupture annoncée était la plus tardive
  et la plus rare ; la vraie est la plus précoce et la plus fréquente du lot.
- **`avant` → « dessous » casse tablette 15, lignes 3 et 4**, qui se suivent : `siècle 1 · après`
  puis `avant · siècle 1 · eau 14`. Un siècle n'a pas de dessous, et les deux lignes mettent la
  paire avant/après sur le même objet à un interligne d'écart.

La troisième ne se remplace pas : **`eau` → « sang » ne casse nulle part.** Un relevé annuel de sang
qui descend de 14 à 1 sur deux siècles pendant que les maisons passent de 31 à 2 se tient ; « il
faut lire le sang » se tient ; le seul endroit où un nombre trancherait — un champ mesuré en eau —
n'existe pas. En cherchant, `année` → « soleil » s'est révélé avoir le même défaut : `siècle` devient
« cent-soleils » et reste juste, la tablette 15 étant datée 139.

Deux signes conçus pour casser ne cassent pas. Ils rejoignent `lire` et `il-faut`, qui sont conçus
pour ça — soit quatre sur onze, alors que le design en prévoyait deux.

### Le vrai défaut : les paires qui se réparent

Le plus sérieux n'était annoncé nulle part. **Trois paires de lectures fausses s'annulent
mutuellement.**

`grain` → poussière est absurde à la tablette 5 : on ne distribue pas vingt mesures de poussière à
chaque maison. `maison` → tombe est absurde à la même ligne, par l'autre bout : on ne distribue pas
de grain aux tombes. Le joueur qui se trompe **sur les deux** lit « vingt mesures de poussière à la
tombe 1 » — un culte funéraire, cohérent d'un bout à l'autre des trente tablettes. Les deux erreurs
les plus lourdes du corpus (315 et 266 attestations, plus d'un signe sur sept à elles deux) se couvrent
l'une l'autre.

Même chose pour `semence`/`devenir` — ⟨semence⟩⟨devenir⟩ se lit alors « porter-enfant » et « si
l'enfant ne porte pas » se tient — et pour `lire`/`devenir`, qui est la pire : ⟨lire⟩⟨devenir⟩ est
`devenir-lecture`, **le dernier signe du jeu**, et deux erreurs le font lire « porter-compte ». La
tablette 27, sommet de l'acte V, devient une note d'archive, et rien ne casse.

### Tranché le même jour : on ne fait rien

Les trois réponses possibles étaient : ne rien faire, interdire la seconde lecture fausse d'une
paire, ou écrire la ligne de corpus qui manque. **C'est la première qui est retenue.**

Les deux autres coûtaient plus qu'elles ne rendaient. Interdire, c'est renseigner : refuser une
lecture, c'est dire au joueur qu'elle est fausse, et rien dans ce jeu n'a ce droit (R3, règle 14).
Écrire la ligne, c'est déplacer des fréquences — donc l'équilibrage, donc un balayage — pour couvrir
trois cas sur les cinquante-cinq paires que onze signes permettent de former.

Reste l'argument de fond, et c'est lui qui emporte : un joueur qui se trompe deux fois de la bonne
façon **finit sur un autre livre**, et c'est le propos du jeu. C'est la même décision que le retrait
de l'invariant I5 — on peut lire presque tous les mots et ne comprendre presque rien, et l'écart
entre les deux est ce qu'il y a à montrer, pas à lisser.

Ce que la décision déplace, en revanche, n'est pas rien, et c'est écrit au §7.3 de `docs/corpus.md` :

- La **dette court quand même** (+2 à +6 points pour une paire), donc la contradiction se déclenche
  au franchissement d'acte comme pour tout le monde. Le joueur est privé de l'indice, pas de la
  sanction. La paire creuse le piège, elle ne le comble pas.
- Le design doc §8 promettait que « le seul indice fiable pour trouver le signe fautif est le texte
  lui-même ». Pour ces trois paires, c'est faux. L'exception est inscrite au design doc plutôt que
  laissée à la mémoire de celui qui codera AMB-4.
- **MOD-2 change de statut.** `peut-être` n'était que le pic de malaise du jeu ; il devient la
  soupape de cette décision, parce que le degré de doute par signe est calculé par le jeu et non
  lu dans le texte. Sans lui, une paire réparante enferme le joueur dans le brute-force que CONTR-3
  rend cher — exactement le joueur que le design voulait punir, et pour une fois sans qu'il l'ait
  mérité.
- **FIN-3 devient porteuse.** La relecture de fin est désormais le seul endroit où le jeu admet
  jamais qu'on a lu autre chose. « Ne pas la sacrifier au planning » cesse d'être une préférence
  d'auteur.

Et une note pour les tests : une rupture de paire réparante ne se vérifie qu'en tenant l'autre signe
à sa lecture juste. Sinon l'assertion échoue alors que le jeu fait exactement ce qui a été décidé.

### Le mot, pas le concept

Un détail décide de tout, et il mérite d'être écrit avant qu'on l'oublie.

`devenir` → faux dit **porter**. Sa rupture est tablette 17 : « il faut la tablette · porter lire »
ne se construit pas en français. Si le mot faux avait été *tenir* — même concept, même plausibilité,
même effet sur le reste du corpus — la ligne aurait donné « il faut la tablette · tenir compte » dès
lors que `lire` est lu « compter ». Idiomatique, banal, invisible. **Le choix du mot français, et
lui seul, sépare une rupture d'un corpus cohérent.**

C'est l'argument qui justifie que TXT-1 soit de l'écriture et pas une table de correspondances, et
c'est aussi pourquoi les onze lignes de journal des lectures fausses sont écrites en entier au §7.5
plutôt que laissées à l'implémentation.

### Une sortie possible pour `eau` et `année`

Ce qui trahit « soleil », ce n'est pas une phrase : c'est une **distribution**. ⟨année⟩ porte
toujours un nombre et n'est jamais opposé à ⟨nuit⟩, qui n'en porte jamais. Un soleil qu'on compte et
qu'on n'oppose pas à la nuit est une année.

AMB-4 demande aujourd'hui une absurdité repérable. Admettre en plus une **rupture
distributionnelle** donnerait à `eau` et `année` leur indice sans écrire une ligne de corpus — et le
donnerait à la Table de fréquences et à la Concordance, c'est-à-dire aux deux instruments que le jeu
a construits pour ça et qui n'ont encore rien à trouver que le joueur ne puisse voir à l'œil. Une
phrase absurde se trouve en lisant ; une distribution impossible se trouve en travaillant. Le second
geste est celui que ce jeu prétend enseigner.

Non tranché : c'est une décision d'AMB-1/AMB-4, elle change ce que la mécanique doit détecter, et
elle n'a pas à être prise dans le même lot que le texte.

### Ce qui est fait, ce qui ne l'est pas

Écrit : les onze mots faux, les onze lignes de journal, les onze composés dérivés (⟨dire⟩⟨couper⟩
donne « le juge », ⟨tombe⟩⟨grain⟩ donne « caveau », ⟨si⟩⟨fin⟩ donne « à la fin »), et le point de
rupture de chacun vérifié ligne à ligne. `semence` et `devenir` n'ayant pas encore d'entrée juste —
leur branche est l'acte V — leurs lectures fausses sont écrites d'avance et attendent leur signe.

Pas écrit, et pas de ce lot : l'effet chiffré de chaque lecture fausse. La règle est « +25 %
d'effet mécanique » ; le chiffre par signe se pose au simulateur, pas à la plume (règle 7).

Une trouvaille sans rapport, laissée là pour la branche Personne : **`moi-absent` (⟨je⟩⟨ne-pas⟩) n'a
aucune attestation dans le corpus.** C'est le seul signe non numéral des 45 dans ce cas — `cinq` et
`mille` sont absents eux aussi comme signes, mais ils paraissent dans les nombres, ce qui est leur
façon d'être attestés. VOIX-1 devra soit donner une ligne à `moi-absent`, soit expliquer ce qu'on
achète en l'achetant.

---

## Le dégagement ne dérive pas, il oscille

14/09/2026, dans la foulée de PAR-2. `revCount()` était signalé depuis trois lots comme le
prochain chantier d'équilibrage : la tranche 20-30′ d'I6 montait à chaque fois — 25,8 % à
23 signes, 27,0 % à 27, 27,8 % à 28 — et le journal en concluait une dérive qui finirait par
crever le plafond de 30 % (règle 2). Traité. Le mécanisme était le bon ; la conclusion, non.

### D'abord vérifier que c'est bien le dénominateur

`revCount()` vaut `4 + 26 × nArbre / NGL`. Les lots changent deux choses à la fois : ils
ajoutent des signes, et ils augmentent `NGL`. On les sépare — même arbre, dénominateur forcé ;
même dénominateur, arbre changé :

| | tranche 20-30′ | durée max | gisement |
|---|---|---|---|
| 23 signes, dénominateur 23 *(mesure du journal : 25,8)* | **25,8 %** | 85,0 | 99,0 % |
| 27 signes, dénominateur 27 *(mesure : 27,0)* | **26,9 %** | 90,0 | 96,4 % |
| 28 signes, dénominateur 28 *(mesure : 27,8)* | **27,8 %** | 92,7 | 97,9 % |
| 23 signes, **dénominateur forcé à 28** | 27,8 % | 85,4 | 84,7 % |
| 28 signes, **dénominateur forcé à 23** | 25,8 % | 92,3 | 100 % |

Le simulateur reproduit les trois mesures d'archive au dixième, et les deux dernières lignes
tranchent : **le chiffre suit le dénominateur, et lui seul.** Les signes ajoutés n'y sont pour
rien. Jusque-là, le journal avait raison.

### Puis vérifier que ça monte

Ça ne monte pas. En balayant le dénominateur de 28 à 45 — l'arbre grandit sous les mêmes
28 signes atteignables, ce qui est exactement ce que fait chaque lot — la pire tranche donne :

```
28    29    30    31    32    33    34    35    36 …  45
27,8  27,7  26,2  26,2  23,9  23,9  26,4  26,3  26,3  25,3
```

Une **dent de scie de quatre points**, sans tendance, dont 28 se trouve être le sommet. Trois
points de cette dent, lus dans l'ordre, font une pente convaincante. Ce n'en est pas une : à
45 signes, toutes choses égales par ailleurs, ce chiffre vaut 25,3 % — mieux qu'aujourd'hui.

D'où vient la dent ? De `round()`, et de tout ce qui est discret en dessous : le nombre de
tablettes ouvertes à un instant donné saute d'une unité, le gisement avec, et l'achat d'une
Concordance tombe d'un côté ou de l'autre de la tranche. Ce n'est pas du bruit de simulation
— le simulateur est déterministe et reproduit l'historique au dixième — c'est la granularité
réelle d'un jeu qui a trente tablettes et pas trois mille.

### Ce qui se passe vraiment dans la tranche

Dénominateur 23 contre 28, à cadence moyenne, par tranche de dix minutes :

| | tablettes ouvertes | gisement relevé | Concordances | I6 |
|---|---|---|---|---|
| 10-20′, dénom. 23 | 11 | **32** | 2 | 15 % |
| 10-20′, dénom. 28 | 10 | **10** | 2 | 8 % |
| 20-30′, dénom. 23 | 14 | **77** | 11 | 23 % |
| 20-30′, dénom. 28 | 12 | **45** | 10 | 28 % |

Deux tablettes de moins sous la main entre la dixième et la trentième minute, c'est trente
relevés de gisement en moins, une Concordance en moins, et la part manuelle qui remonte
d'autant. Le mécanisme est propre et il est petit.

### Le premier candidat était le bon, et il était mauvais

Puisque la tranche veut des tablettes plus tôt, on les donne plus tôt : tout dégager quand
80 % de l'arbre est acquis, au lieu du dernier signe. La tranche tombe à 25,8 %, le gisement
est consommé à 100 %, la durée ne bouge pas. Et **la part manuelle des occurrences tombe de
22,9 % à 12,4 %.**

C'est PT6 en miniature, et c'est la règle 9 qui l'explique : le tarif d'une tablette se fige
**au premier relevé qu'on y fait**. Une tablette sortie tôt est relevée tôt, donc tarifée au
débit du début, donc bon marché pour le reste de la partie. Dégager vite, c'est solder le
corpus. PT6 avait mesuré le fond de ce trou : la main à **0,1 %** des occurrences.

Aucun garde-fou ne voyait ça. Le balayage triait sur la durée, l'écart et I6 — trois mesures
qu'un dégagement précoce améliore toutes les trois.

### L'autre sens, que rien n'annonçait

Si accélérer coûte la main, ralentir devrait coûter I6. Mesuré, c'est faux : ralentir
améliore **les deux**.

| exposant sur la courbe | pire tranche ≥ 10′ | part manuelle | durée | tablettes au 1er signe |
|---|---|---|---|---|
| 0,8 *(plus vite)* | 25,8 % | 19,2 % | 88,7 – 92,8 | 6 |
| 1,0 *(en place)* | **27,8 %** | 22,1 % | 89,6 – 92,7 | 5 |
| **1,1** | **26,1 %** | **22,9 %** | 89,7 – 92,9 | 5 |
| 1,25 | 25,2 % | 24,0 % | 90,1 – 93,9 | **4** |

Le réglage en place est un **maximum local** : on descend des deux côtés. Et du côté lent, la
main monte au lieu de tomber — une tablette sortie tard est une tablette chère.

### Ce qui a été retenu, et pourquoi pas mieux

`REV_R = 1,1` : `4 + 26 × (nArbre / NGL)^1,1`. Le dégagement suit le déchiffrement, un peu en
retard.

Ce qu'on achète n'est pas le point et demi sur la tranche — c'est la **fin de la dent de
scie**. Sur les mêmes dénominateurs 28 → 44 :

| courbe | pire tranche par dénominateur | pire | main |
|---|---|---|---|
| linéaire | 27,8 · 26,2 · 23,9 · 26,4 · 26,3 · 25,3 · 25,3 · 25,4 · 25,4 | **27,8 %** | 16,3 % |
| **1,1** | 26,1 · 26,3 · 25,2 · 25,2 · 25,4 · 25,3 · 25,4 · 25,4 · 25,8 | **26,3 %** | 18,3 % |
| 1,25 | 25,2 · 25,3 · 25,3 · 25,4 · 25,8 · 25,8 · 25,9 · 25,9 · 25,9 | 25,9 % | 18,9 % |
| tout à 85 % | 25,8 · 26,9 · 26,9 · 27,7 · 26,2 · 23,9 · 26,4 · 26,3 · 25,2 | 27,7 % | 13,9 % |

L'amplitude passe de 3,9 points à 1,1. **Ce chiffre cesse de dépendre de la taille du
lexique**, et c'est la seule chose qui empêche de rouvrir ce dossier à chaque lot — ce qu'on
vient de faire trois fois.

1,25 mesure un peu mieux sur les deux colonnes. Écarté quand même : à 1,25, le premier signe
acheté ne dégage **aucune** tablette (4 → 4, contre 4 → 5 aujourd'hui). L'ouverture est la
zone qu'aucune mesure ne couvre — c'est là que la partie 1 de PT5 a été abandonnée, c'est
ECO-1, et le seul chiffre qu'on en ait est la date de la première Concordance, inchangée dans
les deux cas. On ne touche pas à l'ouverture pour un demi-point sur une tranche.

À 1,1, mesuré aux trois cadences : **89,7 – 92,9 min**, écart max 5,2, tranches ≥ 10′ ≤ 26 %,
33 recoupements, la main fournit 22,9 à 23,4 % des occurrences, gisement consommé 96,8 à
99 %. Tout est à l'identique ou meilleur.

### Le garde-fou qui manquait

`outils/balayage.py` balaie désormais `rev_r` comme il balaie les prix, et trie sur une mesure
de plus : **la part manuelle des occurrences, plancher à 15 %**. Aucune combinaison de la
grille actuelle ne s'en approche — elles sont toutes entre 22 et 24 %. Il n'est pas là pour
elles : il est là pour la famille de courbes qui a failli passer, celle qui gagnait deux
points d'I6 en vidant la main, et que trois garde-fous sur trois trouvaient excellente.

C'est la même leçon que la fenêtre de durée restée à (71, 77) pendant trois lots : **un
garde-fou qui ne mesure pas la chose qu'on est en train de casser dit oui avec assurance.**

### Ce que PT10 doit regarder ici

Le nombre de recoupements (33 simulés) et la part manuelle des occurrences, comme prévu — mais
avec une raison de plus : ce réglage-ci les déplace tous les deux, et aucun playtest n'est
derrière lui. Si la main descend au lieu de monter, c'est `REV_R` qu'il faut défaire en
premier, avant les prix.

## Les lecteurs — le nom, et le mot qui manque dedans

14/09/2026. Troisième récit de J1 (`docs/backlog-1.0.md`, PAR-2), et le dernier : l'acte III
se termine. `les-lecteurs` entre dans la branche Parole après `archive`. L'arbre passe de 27
à **28 signes**, le lexique du joueur à 30 avec les deux composés secrets.

| glyphe | coût | effet |
|---|---|---|
| `les-lecteurs` | 1 200 C | **aucun** — trois attestations, une seule tablette |

C'est le plus mauvais achat du jeu à toute mesure d'épigraphiste : 1 200 C pour trois
occurrences, quand `ne-pas` en rendait 290 pour 150. Et le jeu le dit — la Table de
fréquences affiche « 3 occ. » à côté du prix, depuis PT4. Ce qu'on paie ici n'est pas de la
lisibilité, c'est une phrase :

```
tablette 18 · année 164
grain 352 · eau 6 · maison 17
⟨nous⟩ · les-lecteurs
avant · ⟨nous⟩ · les-lecteurs
après · ⟨nous⟩ · les-lecteurs
si ne-pas lire · ⟨nous⟩ ne-pas
scribe ⟨N4⟩
```

### Le dernier signe de l'arbre ne peut pas porter de taux

Aucun effet chiffré, et ce n'est pas un oubli : c'est une mesure. Cinq variantes —
concordance, table, grammaire, atelier, aucune — aux trois cadences, quatre prix chacune :
**la même durée à la décimale près**, vingt fois de suite. La raison est structurelle et vaut
au-delà de ce signe : `les-lecteurs` est le dernier achat de l'arbre, donc `nArbre() === NGL`
clôt la partie à la seconde même où le multiplicateur commencerait à rendre. Un effet posé
là ne serait pas un réglage, ce serait une décoration.

Et c'était déjà vrai avant ce lot, sans que personne l'ait vu : le ×1,5 à la table
d'`archive` ne déplace rien non plus — 86,99–89,98 min avec ou sans, à 27 signes, où il était
le dernier achat ; 89,64–92,66 avec ou sans, à 28, où il a pourtant 2,8 minutes pour agir.
La queue de l'arbre est l'endroit où un multiplicateur cesse d'être un argument, et ce n'est
pas une raison de retirer celui d'`archive` — il est dans la fiction, et l'acte IV lui rendra
du temps. C'est une raison de ne pas en poser un de plus par habitude.

Le jour où l'acte IV mettra `les-lecteurs` au milieu de l'arbre, la question de son effet se
mesurera pour la première fois. Aujourd'hui, elle ne se mesure pas.

### Ce que l'achat ne donne pas

⟨nous⟩. Le nom se dessine ⟨lire⟩ sur ⟨nous⟩ (table `COMP`, règle 4), et ⟨nous⟩ se tient seul
juste devant lui, sur la même ligne — **41 fois dans le corpus**, jamais au lexique avant la
branche Personne. La tablette 18 passe de **68 % à 80 %** de lisibilité et s'arrête là : ils
se nomment, et le mot qui dit « nous » reste à déchiffrer. Ce qui subsiste, exactement :
quatre ⟨nous⟩ et un nom propre.

C'est la porte de l'acte IV, et elle est dans le texte — pas dans une annonce, pas dans la
carte de fin, pas dans l'infobulle. Un joueur qui regarde le signe qu'il vient d'acheter voit
qu'il en contient un autre, et que cet autre est posé juste devant, tout seul. Personne ne le
lui dira. C'est la même mécanique que ⟨grenier⟩ et que le zéro, une troisième fois, et cette
fois-ci elle ne mène pas à un composé à poser mais à un acte à jouer.

Aucune recette ne s'ouvre pour autant (règle 15) : `RECETTES` filtre sur les deux parties, et
`nash` n'est pas au lexique. `les-lecteurs` ne se composera que le jour où `nous` y entrera —
et ce jour-là, la grille l'offrira d'elle-même, sans qu'on ait une liste à tenir.

### La carte de fin attend qu'on ait lu

Le dernier achat de l'arbre est aussi celui qui rend lisible ce que l'acte avait à dire. Or
`showEnd()` était appelée dans la foulée d'`acheterGl()` : la carte « Fin du prototype », un
écran de statistiques à 93 % d'opacité, tombait sur la tablette 18 avant qu'on l'ait
regardée — et la question de playtest qu'elle porte s'y serait répondue toute seule. Tant que
le dernier signe était `archive` ou `dernière-année`, ça ne coûtait rien. Ici, ça couvrait le
sommet de l'acte.

Elle attend donc d'être allé voir. Rien de neuf pour ça : `touchees` sait déjà quelles
tablettes le dernier signe a changées, `tabletteVisible()` sait laquelle on a sous les yeux,
et la carte vient quand les deux se rencontrent. Deux bornes l'encadrent, et ce sont des
garde-fous, pas des réglages : jamais avant six secondes — sinon elle tomberait sur le joueur
déjà posé sur la bonne tablette, à l'instant où les mots changent sous ses yeux — et jamais
au-delà de quatre-vingt-dix, sinon celui qui ne va pas voir n'aurait pas de fin du tout.

`S_.done` est posé tout de suite, lui : **la production s'arrête net pendant qu'on lit la
dernière tablette.** Compteurs figés, chronomètre arrêté, le texte seul. Ce n'est pas un
défaut d'ordre, c'est FIN-1 en avance (design doc §11) — et c'est la seule chose de ce lot
qui touche à autre chose qu'un glyphe. Cinq tests la couvrent, et elle se retire en un
commit si elle déplaît.

### Mesuré

`python outils/sim.py`, trois cadences, `les-lecteurs` à 1 200 C :

| | 28 signes | 27 signes *(lot précédent)* |
|---|---|---|
| durée | **89,6 – 92,7 min** | 87,0 – 90,0 min |
| écart max | **5,2 min** *(posé à `cinq`, 16ᵉ minute)* | 5,2 min |
| dernier écart | 2,8 min | — |
| I6, tranches ≥ 10′ | **≤ 28 %** | ≤ 27 % |
| recoupements | 33 | 33 |
| part manuelle des occurrences | 22,1 – 22,9 % | 22,1 – 23,6 % |

*(Chiffres mesurés à courbe de dégagement linéaire, celle de ce lot-là. `REV_R` l'a changée
le jour même : le réglage livré mesure 89,7–92,9 min et des tranches ≤ 26 % — voir « Le
dégagement ne dérive pas, il oscille ».)*

1 200 C suit l'arithmétique de la branche — 300, 600, 900, 1 200 — et non le drame. Un prix
plus haut était tentant : à 1 800 C le dernier écart monte à 4,2 min, en plein dans la cible
de I4 (4 à 6 min). Écarté, et pour une raison mesurée ailleurs : PT8 a fini l'acte sur
**4 min 51 sans une seule action dans le corpus**, et c'est le défaut que la Concordance a
été écrite pour réparer. Quatre minutes d'attente avant la dernière révélation, quand il n'y
a plus rien à acheter, c'est ce trou-là qu'on rouvrirait.

`outils/balayage.py` : garde-fou de durée re-basé de (84, 92) à **(86, 95)** — mêmes marges
qu'au lot précédent, trois minutes sous le plancher mesuré, deux au-dessus du plafond.
13 combinaisons sur 18 passent, dont le réglage en place. Troisième lot de suite où cette
fenêtre doit bouger : elle suit la taille du lexique, elle n'est pas un invariant.

### La tranche 20-30′, troisième lot de suite

25,8 % à 23 signes · 27,0 % à 27 · **28 % à 28**. Le journal du lot précédent annonçait la
dérive et son mécanisme ; ce lot le confirme par l'autre bout. Elle ne vient pas des signes
ajoutés — `les-lecteurs` s'achète à la quatre-vingt-dixième minute — mais de `revCount()`,
qui vaut `4 + nArbre × 26 / NGL` : **c'est le dénominateur qui bouge**. Un signe de plus dans
l'arbre, et chaque signe acquis dégage un peu moins de tablettes, donc moins de gisement au
milieu de la partie, donc moins d'instruments, donc une part manuelle qui remonte. D'où un
lot d'un seul signe qui la pousse de 0,8 point quand un lot de quatre l'avait poussée de 1,2.

Il reste deux points de marge sous la barre des 30 % (règle 2), et dix-sept signes à ajouter.
**Le prochain lot n'a plus le choix : c'est `revCount()` qu'il faut traiter, pas les prix.**
Le balayage le montre déjà — une des dix-huit combinaisons est rejetée sur cette seule
tranche, à 31 %.

> *Repris le jour même, et à moitié faux.* Le mécanisme est le bon — c'est bien le
> dénominateur, et la décomposition le prouve au dixième près. Mais **ce n'est pas une
> dérive** : balayé de 28 à 45, ce chiffre oscille entre 23,9 % et 27,8 % sans tendance, et
> 28 en est le sommet. Trois mesures lues comme une pente étaient trois points d'une dent de
> scie. Voir la section suivante, « Le dégagement ne dérive pas, il oscille ».

### Ce que PT10 doit regarder ici

Deux questions, et aucun simulateur ne répond ni à l'une ni à l'autre.

**Est-ce qu'on achète un signe à 1 200 C qui annonce trois occurrences ?** C'est l'arbitrage
de l'épigraphiste posé à nu : le lexique affiche le prix, le compte d'attestations et l'effet
(« le nom qu'ils se donnaient se lit »), et c'est tout. Un joueur qui optimise passe son
chemin — et s'arrête là, sans fin, sans tablette 18. Le journal d'actions dira combien de
temps le signe est resté payable avant d'être acheté.

**Est-ce qu'on voit ⟨nous⟩ dans le nom ?** Même famille que ⟨grenier⟩ et que ⟨ne-pas⟩ posé
sur ⟨un⟩, mais sans grille pour la recueillir : il n'y a rien à poser, rien à cliquer, aucune
trace dans le TSV. Ça ne se saura qu'en demandant, après la partie, ce que le joueur a compris
de la dernière tablette. Question à poser à voix haute, pas à instrumenter.

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
   et `zéro` ont suivi *(12/09/2026)*, `les-lecteurs` a fermé l'acte *(14/09/2026)*. Reste
   l'Élève, qui n'a rien à fausser tant que les lectures fausses ne sont pas écrites.
10. **`zéro` ne donne pas la notation compacte des grands nombres**, que le design doc §7 lui
   prête. Elle est déjà celle de `cent`, acquise par tout le monde ; la déplacer sur un
   composé facultatif la retirerait à la plupart des joueurs. Il ne donne que sa lecture —
   les onze zéros du corpus, dont les neuf de la tablette 29.
11. **La carte de fin ne s'ouvre plus au dernier clic** : elle attend qu'on ait eu sous les
   yeux la tablette que le dernier signe vient d'ouvrir — six secondes au plus tôt,
   quatre-vingt-dix au plus tard. Le prototype se fermait sinon sur la tablette 18 sans
   qu'on l'ait lue. `S_.done` est posé à l'achat : la production s'arrête pendant cette
   lecture, et c'est FIN-1 en avance plutôt qu'un défaut d'ordre.
12. **Le dernier signe de l'arbre ne porte aucun effet chiffré**, et ce n'est pas propre à
   `les-lecteurs` : il est payé à la seconde où la partie se termine. Mesuré — cinq effets
   possibles, quatre prix, trois cadences, la même durée à la décimale près. Le ×1,5 à la
   table d'`archive`, qui occupait cette place au lot précédent, ne déplaçait rien non plus.

---

## Décisions

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète du corpus. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.

---

## Suite

1. **PT11, avec un autre joueur.** PT10 a bien eu lieu (15/09/2026) mais l'auteur l'a joué :
   il a répondu sur l'économie et sur l'instrument, pas une seule fois sur la lecture. Toutes
   les questions de reconnaissance repassent donc telles quelles — la crue qui baisse,
   ⟨maison⟩+⟨grain⟩, ⟨ne-pas⟩+⟨un⟩, ⟨nous⟩ dans `les-lecteurs`, et « a-t-on remarqué qu'on
   choisissait », à poser de vive voix et à la fin. Deux réponses sont acquises et ne valent
   que pour un joueur : **`les-lecteurs` s'achète**, à 95:20 et devant `sinon` qui coûte 400 de
   moins ; et **trois lectures fausses sur neuf**, ce qui reste compatible avec le hasard.
   Voir « PT10 — la main a disparu du corpus ».
2. **Le mur des dix premières minutes** : 83 % de la Certitude à la main avant la première
   Concordance en PT7, 63 % en PT8, 75 % en PT9 — et c'est là que la partie 1 de PT5 a été
   abandonnée. Le seul défaut d'équilibrage connu qui ne soit pas réglé. Il se traite par
   l'ouverture (un instrument plus tôt, ou un premier signe moins cher), pas par le
   recoupement.
3. ~~**Seconde moitié de l'acte III**~~ — ~~composition~~ *(10/09/2026)*, ~~`lire`,
   `scribe`, `archive`~~ *(11/09/2026)*, ~~la Modalité et `zéro`~~ *(12/09/2026 : une branche
   tardive mord enfin sur la branche Nombre)*, ~~`les-lecteurs`~~ *(14/09/2026)*. **L'acte III
   est fini.** Le chemin critique est maintenant **TXT-1**, les onze lectures fausses : c'est
   de l'écriture, et elle bloque l'ambiguïté, donc l'Élève, donc `peut-être` et `faux`, donc
   la relecture de fin.
4. **Le clic vide** : 8 % des relevés en PT9, 10 % en PT10 (16 sur 164) depuis la marque de
   la barre ; le texte ne dit toujours pas ce que la barre dit. Peut attendre.
5. ~~Trancher le sort de ⟨N1⟩ et ⟨N2⟩ (`docs/corpus.md` §9).~~ *Semés comme intitulés des
   registres le 11/09/2026 — voir « Le fleuve et la cité ».*
6. ~~**`revCount()`, maintenant.**~~ *Fait le 14/09/2026, et la prémisse était fausse : ce
   chiffre n'est pas en pente, il oscille — 28 en était le sommet.* `REV_R = 1,1` ramène
   l'amplitude de la dent de scie de 3,9 points à 1,1 et rend la mesure indépendante de la
   taille du lexique. Ce qui reste ouvert, c'est la question que ce travail a soulevée :
   **le dégagement fixe le prix de la main** (règle 9), et aucun playtest n'est derrière ce
   réglage-là. Voir « Le dégagement ne dérive pas, il oscille ».

7. **La main a disparu du corpus** *(PT10, 15/09/2026)* — 1,0 % des occurrences contre 36,3 %
   en PT9, et **cinquante minutes d'affilée sans un geste dans le texte**, de 36:46 à 86:34.
   Les deux ont la même cause : le gisement est sorti en trente minutes, donc tarifé au débit
   du début, donc bon marché pour toujours, et il ne reste plus rien à y faire ensuite. C'est
   le défaut de PT6 revenu par la porte que R9 ne garde pas — R9 fige le tarif à la première
   visite, elle ne dit rien de qui ne revient jamais. **Le défaut d'équilibrage le plus grave
   depuis PT6**, et il attend la mesure de PT11 avant tout réglage : ne pas toucher `REL_K`,
   c'est la date des relevés qui est en cause, pas leur prix.

8. **Un garde-fou qui ne contraint que le simulateur ne garde rien.** Le plancher de 15 % sur
   la part manuelle des occurrences, entré dans `outils/balayage.py` le 14/09/2026, donne 22,9
   à 23,4 % sur le réglage en place et n'a pas vu venir le 1,0 % de PT10 — parce qu'il mesure
   l'acheteur simulé, qui relève tant que c'est rentable, et pas un joueur qui s'arrête. Vrai
   de ce plancher-là ; à vérifier sur les trois autres. C'est la limite de méthode que huit
   balayages n'avaient pas rencontrée, et elle ne se corrige pas en déplaçant un seuil.
