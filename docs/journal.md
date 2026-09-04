# Journal de bord

Historique des playtests, des défauts trouvés et des décisions prises. À lire avant de modifier l'équilibrage ou la numération : chacune des règles actuelles est là parce qu'une version plus simple a échoué.

---

## Les trois playtests

| | PT1 | PT2 | PT3 | Cible |
|---|---|---|---|---|
| Durée | 145 min | 29 min 27 | 41 min 54 *(dont ~10 min de pause)* | 45 min |
| Signes relevés à la main | 3 853 | 271 | **45** | — |
| Recoupements | 67 | 69 | 51 | — |

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

Proposition intermédiaire : faire compter à la jauge les **lignes entièrement lisibles** plutôt que les signes. Mesuré sur une partie complète, la part de lignes reste entre **0 et 2 %** pendant tout le MVP et ne décollerait qu'aux actes IV–V. Comme jauge de progression, démoralisant.

**Décision** : la barre affiche les **signes**, l'en-tête affiche les deux nombres, la carte de fin aussi.

**L'invariant I5 du design doc est faux et a été retiré.** Aucune mesure n'est linéaire : les signes sont front-chargés, les lignes back-chargées. L'écart entre les deux *est* le propos du jeu — on peut lire presque tous les mots et ne comprendre presque rien. L'afficher, ne pas le lisser.

---

## Réglages actuels

| | Valeur |
|---|---|
| Relever | (1 + 3 % du débit brut) × mult. |
| Formuler | 3 occ. → 1 hyp. |
| Recouper | 12 occ. + 3 hyp. → min(3, 1 + ⌊lexique/5⌋) cert., coût ×1,12 par usage (−25 % avec `champ`) |
| Copiste | 15 occ., ×1,12, +1 occ./s |
| Table de fréquences | 100 occ., ×1,15, −1 occ./s → +0,6 hyp./s |
| Concordance | 450 occ., ×1,18, −0,5 hyp./s → +0,003 cert./s |
| Atelier de copie | 1 800 occ., ×1,15, +25 occ./s |
| Signes (13) | Nombre 2 · 5 · 11 · 18 · 33 — Matière 3 · 6 · 14 · 22 · 40 — Parole 8 · 27 · 48 = **237 C** |
| Multiplicateurs | `deux` ×1,25 relevé · `grain` ×1,3 copiste · `tablette` ×1,5 relevé · `eau` ×1,3 table · `champ` −25 % recoupement · `graver` ×1,5 concordance · `copier` ×2 sur tout |

---

## Écarts assumés par rapport au design doc

1. **Concordance ajoutée comme instrument** — sans elle, toute la Certitude vient du recoupement manuel.
2. **Atelier de copie avancé aux actes I–II** — sa coupe initiale était l'erreur de PT1.
3. **Lexique à 45 signes au lieu de 44** : la branche Nombre gagne `cinq` et `mille`, perd `vingt` (redondant), pour que chaque signe ouvre un rang de numération — ou, pour `deux`, le principe du redoublement.
4. **17 composés au lieu de 9.** En dessinant les signes, presque tout le lexique tardif s'est révélé composable (`nous-fûmes` = nous + finir, `scribe` = dire + graver). La mécanique de composition de l'acte III en devient plus riche — et `zéro`, composé `ne-pas` + `un`, s'affiche dans les compteurs du joueur dès la première seconde, des heures avant qu'il puisse le lire.
5. **Invariant I5 retiré**, invariant I6 ajouté.
6. **La Table de fréquences a un effet visible** (comptage d'occurrences au survol), en plus de son rôle économique.
7. **Le chrome de l'interface est en français dès t=0.** L'idéal du doc — un seul mot français à l'écran — rend le prototype injouable sans onboarding. À réexaminer une fois qu'il y en aura un.
8. **Pas de progression hors-ligne** (conforme : `nuit` est un signe d'acte III).

---

## Décisions

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète du corpus. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.

---

## Suite

1. **PT4** — partie complète avec la numération signe par signe, la barre et les infobulles. À observer : la lisibilité partielle des nombres donne-t-elle envie de finir la branche Nombre avant les autres ? Le marquage ocre des tablettes touchées est-il suivi ? Le comptage d'occurrences sert-il à quelque chose, ou n'est-il qu'un ornement ?
2. **Acte III** — branche Temps, `mille`, `zéro` par composition, instruments Grammaire et Élève, et surtout la **datation puis le réordonnancement chronologique** des tablettes. C'est le sommet dramatique : une fois triées, la série de l'eau devient lisible et le déclin apparaît.
3. Puis la mécanique de **composition**, puis les **contradictions** (acte IV).
4. Trancher le sort de ⟨N1⟩ et ⟨N2⟩ (`docs/corpus.md` §9).
