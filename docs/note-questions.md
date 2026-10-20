# Les Questions — note de conception (VOIX-3)

*19/10/2026. Trois options mesurées et une recommandation. Issue
[#36](https://github.com/DavidGiangiacomo/langue-morte/issues/36).*

> **Tranché le même jour par l'auteur : l'option 3, avec le gel** — la recommandation du §6.
> Elle est codée depuis : règle 24 de `CLAUDE.md`, et `docs/journal.md`, « Les Questions ». Les
> points du §7 ont été réglés à l'écriture : les nombres ne font pas partie de la condition,
> la nuit ne remplit aucune question, la réponse s'écrit à l'infinitif et ses lignes
> s'allument dans le corpus, sans question en main rien ne se pose. Restent ⟨nous-fûmes⟩,
> ⟨devenir-lecture⟩ et les deux instruments à venir, qui sont de GRAINE-1 et de VOIX-4.
> La suite de ce document est la note telle qu'elle a été soumise.

---

## 1. Ce qui est fixé avant de commencer

- **Design doc §4** : une quatrième ressource, Q, « acte IV+, interroger le texte », **0 à 12 sur
  toute la partie**.
- **Design doc §6 et §10** : ⟨toi⟩ débloque les Questions, la branche Personne rend lisible « le
  panneau de questions ». « On peut interroger le texte, il répond, **dans les limites de ce qui a
  été gravé il y a quatre mille ans**. »
- **Backlog, R8** : chaque réponse est une ligne du corpus, jamais un texte écrit pour l'occasion.
  C'est le seul système où le jeu pourrait se mettre à *parler* au lieu de laisser lire.
- **Les règles qui bornent tout le reste** : §4 du design doc (un signe ne s'achète qu'en
  Certitude) ; 14 (la grille ne renseigne jamais) ; 17, 18 et 20 (le jeu connaît la vérité et
  n'a pas le droit de s'en servir) ; I1 (la Certitude ne dépasse jamais quatre chiffres).
- **ECO-3** : depuis la Personne, il ne reste plus un cran de prix sous le plafond d'I1 pour
  régler le rythme de l'acte V. Les Questions sont citées comme candidat. Cette note le mesure.

---

## 2. La forme : une question est une condition

La langue n'a pas d'interrogatif, et ⟨si⟩ est ce qui s'en approche le plus. Le corpus pose
**seize conditions**, dont quatorze ont au moins une ligne écrite à la main ; chacune est suivie
de ce qui en découle. Relevé sur le corpus rendu :

| Condition | Ce qui est gravé après | Tablette | Mot de la Fin dans la réponse |
|---|---|---|---|
| si ne-pas | sinon | registres, ×130 | — |
| si lire | *rien* | registres, ×58 | — |
| si lire | devenir | 28 | **devenir** |
| si semence | il-faut ne-pas · après | registres, ×27 | — |
| si semence | ne-pas germer | 22 | **germer** |
| si copier | ne-pas faux | consignes, ×5 | — |
| si copier | il-faut | 17 | — |
| si faux | il-faut ne-pas | consignes, ×5 | — |
| si ne-pas copier | sinon | 17 | — |
| si ne-pas lire | nous ne-pas | 18 | — |
| si lire un | après lire deux | 21 | — |
| si tablette | germer | 22 | **germer** |
| si copier 100 | un devenir | 23 | **devenir** |
| si toi lire | nous ne-pas finir | 24 | **finir** |
| si toi ne-pas lire | nous finir | 24 | **finir** |
| si tablette lire | tablette germer | 27 | **germer** |
| si toi lire un | toi lire grain | 28 | — |
| si toi lire grain | toi lire nous | 28 | — |
| si un | après deux | 28 | — |

Trois choses en sortent, et aucune n'a été écrite pour ce lot :

- **Le corpus répond à des questions que personne n'a posées.** C'est l'acte V en avance : un
  texte conçu pour un lecteur à venir a déjà écrit les réponses. Le joueur qui demande « si toi
  lire » reçoit « nous ne-pas finir » : la thèse du jeu, rendue à une question qu'il pose sur
  lui-même.
- **Cinquante-huit lignes de registre finissent sur « si lire », et rien après.** Demander « si
  lire » rend une seule réponse gravée, « devenir », et cinquante-huit silences.
- **Trois mots de la Fin se trouvent dans ce qui suit un « si »** : ⟨finir⟩ (tablette 24),
  ⟨devenir⟩ (23 et 28) et ⟨germer⟩ (22 et 27), ce dernier nulle part ailleurs. ⟨semence⟩ n'est
  jamais que dans une condition. Les autres sont des composés que la grille ouvre d'elle-même dès
  qu'on a leurs parties (règle 15) : ⟨le-dernier⟩ = finir + un, ⟨notre-fin⟩ = finir + nous,
  ⟨devenir-lecture⟩ = lire + devenir. ⟨germer⟩ aussi est un composé, semence + devenir : la
  question qui le donne peut être contournée par la grille, comme `scribe` l'est à l'acte III.

**Les règles de la forme**, communes aux trois options :

1. Le joueur pose ⟨si⟩ suivi d'un à trois signes. La palette ne montre que les signes acquis, pour
   la même raison que la grille de composition (règle 14).
2. La réponse est ce qui est gravé après cette condition exacte, dans toutes les tablettes, chaque
   suite distincte une seule fois. Les lignes s'allument dans le corpus.
3. La réponse s'écrit avec les lectures du joueur (`motDe()`), et un mot inconnu reste en signes.
   Une lecture fausse peut donc rendre la réponse absurde : c'est le texte qui parle, comme pour
   les ruptures (règles 17 et 20). La réponse ne dépend jamais de la justesse des lectures.
4. Une condition qui n'est gravée nulle part : « Le texte ne dit rien. », et rien n'est dépensé.
   Ce n'est pas un renseignement : une Concordance sur ⟨si⟩ montre les mêmes lignes.
5. Poser une question ne compte pas dans le degré de doute : c'est le texte qui montre, pas le
   joueur qui rassemble (règle 18, même décision que le repli de VOIX-2).

**Écarté : montrer un signe et demander ce qu'il veut dire.** Ça doublonne la Concordance, et
il faudrait choisir *la* ligne qui répond. Pour un signe ambigu, la ligne la plus parlante est sa
rupture : la question deviendrait l'oracle que les règles 17 à 20 refusent.

---

## 3. Trois options

Elles ont toutes la forme ci-dessus. Elles diffèrent sur deux points : ce que fait la réponse, et
d'où vient la question.

### Option 1 — La réponse se lit, et c'est tout

Les questions sont données à l'achat des signes, par exemple trois par signe de la Personne à
partir de ⟨toi⟩, soit douze. La réponse met en scène des lignes du corpus et ne change rien
d'autre.

- **Pour** : la plus simple, et l'économie n'est pas touchée.
- **Contre** : c'est à peu près ce que fait déjà une Concordance sur ⟨si⟩. Un panneau qui
  s'appelle « questions » sans changer ce qu'on peut faire, c'est le nom qui ment (règle 11).
  ECO-3 reste entier.

### Option 2 — La réponse ouvre les mots de la fin, et les questions sont données

L'arbre n'offre plus ⟨finir⟩, ⟨devenir⟩ ni ⟨germer⟩. **Une réponse qui contient un signe que
l'arbre n'offrait pas encore l'ouvre**, et il se paie en Certitude comme les autres : la question
donne l'accès, pas la compréhension, et le §4 tient. ⟨semence⟩ reste dans l'arbre, les composés
passent par la grille. Les questions sont données, comme dans l'option 1.

- **Pour** : les Questions ont un vrai rôle. L'acte V sort du texte par les questions du joueur,
  et R8 tient par construction.
- **Contre** : une question ne coûte pas de temps. Le rythme de l'acte V reste donc celui des prix,
  et les prix sont au plafond. Mesuré, avec les sept signes de la Fin à 9 999 : **16,7 min**
  d'acte V avec Élèves, **23,7** sans, et des écarts qui retombent à 1,4 et 2,0 min. I4 cède dès
  le troisième signe.
- **Le seul autre levier mesuré** : arrêter la croissance de la Grammaire à 36 signes. L'acte V
  passe à **24,3 min** avec Élèves, avec des écarts de 3,3 à 3,7 min, sous la moyenne de 4 que
  demande I4. Sans Élève, il fait **34,7 min**, écarts de 4,7 à 5,2. Mais alors tous les prix sont
  au plafond et le gel est déjà dépensé : il ne restera rien à régler quand le Corpus jumeau et le
  Lecteur viendront accélérer l'acte V.

### Option 3 — Ce qui déborde devient question

La Certitude s'arrête à **9 999**. I1 cesse d'être une contrainte sur les prix et devient une
règle du jeu. À partir de ⟨toi⟩, **le surplus remplit la question suivante**, et chaque question
qui obtient une réponse en consomme une. Les réponses ouvrent les mots de la fin, comme dans
l'option 2.

C'est le seul levier mesuré qui n'ait pas de plafond : le prix d'une question n'est jamais détenu
d'un coup, il peut donc croître. Le surplus remplit la question, puis le signe se paie sur les
9 999 : une marche coûte q + p, et l'écran n'affiche jamais plus de quatre chiffres.

- **Si chaque signe de la Fin attend une question**, à 10 000 × 1,15ⁿ : l'acte V fait
  **32,7 min** avec Élèves, avec des écarts de 4,4 à 4,9 min, et **46,8 min** sans, écarts de 6,4
  à 6,8. Les écarts sont plats parce que 1,15 compense le 1,16 de la Grammaire : c'est encore la
  leçon de `REC_R`, seul un taux mord.
- **Mais le texte n'en donne que trois.** Avec trois questions seulement (Fin en rampe), le rythme
  fait des dents de scie : une longue attente avant chaque mot ouvert, puis une rafale. Pour garder
  l'écart max sous 8 min, la moyenne ne dépasse pas 2,8 min avec Élèves et 4,0 sans. Les questions
  seules ne tiennent pas l'acte.
- **Trois questions à 4 000, plus la Grammaire gelée à 36** (Fin au plafond) : l'acte V fait
  **28,2 min** avec Élèves, avec des écarts de 3,2 à 5,2 et une moyenne de 4,0. Sans Élève :
  **40,3 min**, écarts de 4,7 à 7,2, moyenne 5,8. **I4 tient dans les deux cas**, et c'est la seule
  combinaison mesurée qui le fasse.
- **Deux questions seulement**, quand ⟨germer⟩ passe par la grille : à 4 000, la moyenne tombe à
  3,8 min avec Élèves, juste sous I4 ; à 6 000, elle remonte à 4,0, mais l'écart max sans Élève
  passe à 8,3. La fenêtre est étroite. La troisième question compte.
- **La curiosité a un prix.** Chaque question au-delà des trois coûte 1,3 min d'acte V avec
  Élèves et 1,9 sans (mesuré avec deux, puis quatre questions de plus). Seize conditions pour
  douze questions au plus : on ne peut pas tout demander.
- **Variante écartée : payer la question en Certitude, sous le plafond.** Même à 10 000 la
  question et sept questions sur le chemin, l'acte V ne dépasse pas 25,8 min avec Élèves, et ses
  écarts retombent à 2,7 min. On retrouve le plafond.

### Le tableau

Les durées d'acte V sont à 15 clics par minute. L'acte V ne dépend pas de la cadence : à 5 et à
40 clics, les chiffres sont identiques au dixième près.

| | Partie entière | Acte V | Écarts de l'acte V | I4 |
|---|---|---|---|---|
| Aujourd'hui, actes I–IV, 36 signes | 104,7–108,6 · *118,6–122,2* | — | — | tient |
| Options 1 et 2, Fin au plafond | 122,0–125,4 · *142,9–146,0* | 16,7 · *23,7* | 1,4–3,7 · *2,0–5,2* | **cède** |
| Option 2 + Grammaire gelée à 36 | 129,6–133,0 · *153,8–157,0* | 24,3 · *34,7* | 3,3–3,7 · *4,7–5,2* | cède avec Élèves |
| Option 3, sept questions, 10 000 × 1,15ⁿ | 138,0–141,4 · *166,0–169,1* | 32,7 · *46,8* | 4,4–4,9 · *6,4–6,8* | tient |
| Option 3, trois questions à 4 000 + gel à 36 | 133,5–136,9 · *159,5–162,6* | 28,2 · *40,3* | 3,2–5,2 · *4,7–7,2* | tient |

*En romain l'acheteur qui prend des Élèves (8 ou 9), en italique le joueur qui n'en prend aucun.
La pire tranche d'I6 hors ouverture reste à 25 %, à 20–30′, dans toutes les lignes : une question
n'est pas une action manuelle.*

---

## 4. Ce que la contradiction coûte dans un acte V

Mesuré chez le joueur sans Élève qui ne révise jamais, comme `sim.py` le fait :

| | Lecture parfaite | Paire réparante | Toutes fausses |
|---|---|---|---|
| Options 1 et 2, Fin au plafond | 142,9–146,0 | 194,0–197,0 | 183,2–186,2 |
| Option 2 + gel à 36 | 153,8–157,0 | 213,6–216,6 | 201,3–204,3 |
| Option 3, trois questions + gel | 159,5–162,6 | 223,6–226,6 | 210,5–213,6 |

La Personne avait déjà montré que la sanction grandit avec la longueur de l'acte : +32 min pour
la paire réparante au lieu de +11. Avec un acte V, elle passe à **+51 à +64 min**, quelle que soit
l'option. Ça ne se règle pas ici : c'est la question que la Personne posait déjà au playtest (un
joueur sous contradiction révise-t-il, ou encaisse-t-il ?), devenue plus pressante.

---

## 5. Trouvé en chemin : une nuit dépasse déjà le plafond

`nuit` rend 40 % du débit pendant quatre heures au plus, soit 96 minutes de production pleine.
Débits mesurés au simulateur :

- à l'achat de ⟨nuit⟩ : 2,5 à 3,0 cert./s, donc une nuit de quatre heures rapporte **14 500 à
  17 400 C** ;
- à l'achat de ⟨nous⟩ : **66 000 à 89 000 C**, plus de deux fois le prix de toute la branche
  Personne (30 900 C), à dépenser au retour.

L'écran le cache, puisque la notation de ⟨cent⟩ affiche « 17,4 k ». Mais la lecture d'I1 qui a
fixé les prix de la Personne (aucun prix au-delà de 9 999, parce que la Certitude n'en détient
jamais plus) est déjà fausse hors ligne. **L'option 3 referme ce trou au passage** : la Certitude
plafonne, et le surplus ne fait au plus que douze questions. Avec les options 1 et 2, il reste
ouvert, et il faudra le régler à part.

---

## 6. Recommandation

1. **La forme, sans hésiter** : une question est une condition, la réponse est ce qui est gravé
   après (§2).
2. **La réponse ouvre les mots de la fin** (options 2 et 3). Sans ça, le panneau ne fait rien
   qu'une Concordance ne fasse déjà.
3. **Les questions naissent de ce qui déborde** (option 3), **avec trois questions et la Grammaire
   gelée à 36 signes**. C'est la seule combinaison mesurée qui tienne I4 avec et sans Élèves.
   Elle referme le trou de la nuit et laisse un levier sans plafond, le prix des questions, pour
   le Corpus jumeau et le Lecteur, qui accéléreront l'acte V.

Ce que ça coûte :

- **Deux règles neuves au lieu d'une** : le plafond et le gel.
- **⟨germer⟩ se compose** : qui le pose à la grille fait l'économie d'une question, et la moyenne
  avec Élèves passe juste sous I4 (§3). À surveiller au playtest plutôt qu'à interdire :
  retirer une recette, c'est recopier `COMP` à la main (règle 15).
- **Le gel contredit la lettre du design doc §5**, selon laquelle la Grammaire « croît avec la
  taille du lexique ». L'argument pour : une fois les mots de la Personne connus, la grammaire est
  complète, et les mots de la fin n'en sont pas. C'est d'ailleurs l'ordre que la tablette 28 donne
  au programme : les nombres, les choses, les verbes.
- **Si le gel est refusé**, l'option 3 ne tient qu'avec plus de trois signes ouverts par une
  réponse. Il faudrait alors élargir la forme : demander le **début d'une ligne**, dont « si » ne
  serait que le cas canonique. « je graver · » rend ⟨le-dernier⟩, « nous · » rend ⟨semence⟩.
  ⟨notre-fin⟩ resterait hors d'atteinte : il ouvre sa ligne. Cette variante n'est pas mesurée.

---

## 7. Ce que la note ne tranche pas

- **Les nombres dans une condition.** « si copier 100 » : faut-il demander le nombre, ou laisser
  « si copier » rendre ses trois suites, dont « un devenir » ?
- **La nuit remplit-elle les questions ?** Le corpus « se lit la nuit » ; mais une question
  demande quelqu'un pour la poser.
- **À l'écran** : une Certitude figée à 9 999, une jauge de question qui se remplit, et ce qu'en
  dit la ligne d'effet de ⟨toi⟩. Le jeu n'explique rien, il doit seulement le rendre visible
  (même famille que la règle 14 : il ne se tait jamais sur lui-même).
- **La révision sous le plafond** : la neuvième coûte 10 308 C et deviendrait impossible.
  Aujourd'hui, elle demande déjà de détenir cinq chiffres.
- **⟨nous-fûmes⟩** est ⟨nous⟩ + ⟨finir⟩, et ⟨finir⟩ devient un mot de l'acte V : la fin de l'arbre
  et la règle 16 sont à revoir avec GRAINE-1, de même que la place exacte de ⟨devenir-lecture⟩
  (COMP-4).
- **Le Corpus jumeau (VOIX-4) et le Lecteur (GRAINE-2)** accéléreront l'acte V. Le prix des
  questions est le levier à re-régler à ce moment-là.

---

## 8. Comment c'est mesuré

Une copie de `outils/sim.py` (état de ce commit), modifiée hors du dépôt. Les chiffres valent
pour ce modèle et pour aucun autre. **ECO-2 doit le porter dans `sim.py` avant tout réglage**
(règle 7).

- **Un acte V provisoire** : les sept signes de la Fin, derrière la Personne et en file, dans
  l'ordre finir · semence · devenir · le-dernier · germer · notre-fin · devenir-lecture. Ils sont
  sans effet chiffré, au plafond (9 999) ou en rampe de 3 000 à 9 999. L'option 3 à sept
  questions, la variante en Certitude et le cas à trois questions seules sont mesurés en rampe ;
  toutes les autres lignes au plafond. Le modèle n'a ni Lecteur ni Corpus jumeau, et la
  composition n'y est pas distinguée de l'achat.
- **Une question sur le chemin** est un pseudo-signe hors de l'arbre, payé en Certitude juste
  avant le signe qu'elle ouvre. C'est exact en temps pour le débordement : le surplus remplit la
  question, puis le signe se paie sur les 9 999, soit q + p par marche. Les questions de
  l'option 3 « trois questions » précèdent ⟨finir⟩, ⟨devenir⟩ et ⟨germer⟩.
- **Grammaire gelée** : `gramMul` vaut 1,16^min(arbre, 36), donc rien ne change avant l'acte V.
- **Les conditions de mesure** sont celles de `sim.py` : cadences 5, 15 et 40, l'acheteur avec
  Élèves (il en prend 8 ou 9) et sans, lecture parfaite sauf mention. Les lignes de contradiction
  sont jouées sans Élève et sans révision.
- **Le relevé des conditions** (§2) est fait sur `src/corpus.js`, segment par segment, entre deux
  « · ».
