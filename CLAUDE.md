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
python build.py && python outils/verifier.py    # tests
```

`dist/artefact.html` est la variante sans `<!doctype>/<html>/<head>/<body>`, format attendu par l'outil Artifact de Claude.

---

## Règles à ne pas casser

1. **`src/corpus.js` est généré.** Toute modification du texte se fait dans `outils/corpus.py` (transcription exécutable de `docs/corpus.md`), puis `python outils/corpus.py`, puis `python build.py`. Éditer `corpus.js` à la main, c'est perdre le travail au prochain build.

2. **Aucune action manuelle ne doit dépasser 30 % de la Certitude produite, sur aucune tranche de dix minutes.** C'est le mode de défaillance par défaut du jeu : la Certitude est rare, le joueur cherche le chemin le plus court, et deux playtests de suite une action répétée (le clic, puis le recoupement) est devenue la source principale de la ressource centrale. **Mesuré par tranches depuis PT7** : le ratio sur la partie entière s'était posé à 30,0 % en PT6 en cachant un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes — une moyenne, pas un instrument. `outils/sim.py` affiche les tranches ; les vérifier à chaque ajout d'instrument. La tranche 0–10 min est le seul dépassement connu et non réglé (voir `docs/journal.md`, « le mur des dix premières minutes »).

3. **La numération s'acquiert signe par signe, jamais d'un bloc.** Un nombre du corpus ne passe en chiffres que si le joueur connaît *chacun* de ses signes — et `deux` n'ouvre aucun signe, il ouvre le principe du redoublement (sans lui, on ne lit qu'un nombre où chaque signe apparaît une seule fois). Voir `numLisible()` dans `signes.js` et le tableau dans `docs/journal.md`.

4. **Les composés se dessinent comme composés.** `sv()` rend un signe composé à partir de ses deux parties (table `COMP` dans `signes.js`). Le joueur doit pouvoir reconnaître ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ avant de savoir le lire.

5. **Le corpus n'a aucun en-tête ajouté par le jeu.** Chaque tablette se numérote elle-même dans sa première ligne. Rien dans cette colonne qui ne soit du texte ancien.

6. **Pas de dépendance externe, pas de framework.** Un seul fichier doit rester distribuable.

7. **Ne jamais annoncer un chiffre de rythme sans l'avoir simulé ou mesuré.** Les sept playtests ont tous invalidé une intuition d'équilibrage.

8. **Les deux actions manuelles se font dans le corpus.** Le relevé, sur un signe ; le recoupement, sur deux attestations d'un même signe dans deux tablettes différentes. Aucun bouton ne produit plus rien directement — c'est le point de bascule entre « un incrémental habillé en déchiffrement » et un jeu où l'on agit en lisant. Ne pas remettre de raccourci qui contourne le texte.

9. **Le relevé : le tarif d'une tablette est figé au premier relevé qu'on y fait**, jamais à son dégagement — le figer au dégagement laisse à 1 occurrence, pour toute la partie, les seules tablettes qu'on atteint tôt (PT6 : la main retombée à 0,1 % des occurrences). Deux versions plus simples ont échoué au simulateur avant d'atteindre le jeu : un gisement qui coupe vraiment verrouille l'ouverture (13 relevés disponibles pour un premier Copiste à 15), et un tarif indexé sur le débit courant se thésaurise (72 % des occurrences au lieu de 17 %). Le gisement, et non la cadence de clic, décide de ce que la main rapporte — c'est ce qui rend impossible le retour du défaut de PT1.

10. **La date d'une tablette n'est jamais ajoutée par le jeu.** Chaque tablette porte la sienne dans sa première ligne depuis la première seconde ; `année` ne fait que la rendre lisible, et il faut encore savoir lire le nombre, signe par signe. Corollaire : le rangement chronologique ne réordonne que ce que le joueur sait dater — le reste garde l'ordre de sortie de terre. Ne jamais dater depuis une table externe : la vérité est dans `tb.l[0]`.

11. **Un instrument nommé d'après une méthode philologique doit faire cette méthode.** La Table de fréquences compte les occurrences au survol ; la Concordance rassemble les attestations d'un signe. Sans ça le nom ment, et le jeu redevient un incrémental habillé. Corollaire trouvé en PT8 : **ranger n'est pas rassembler** — l'ordre chronologique ne sert à rien tant que 8 à 57 lignes de registre séparent deux relevés de la même série.

12. **Le dégagement suit la sortie de terre, l'affichage suit le temps.** `IDX` (rang dans `ORDRE`) décide de ce qui est visible, l'ordre du DOM décide de ce qu'on lit. Les confondre ferait dégager des tablettes en rangeant. `ranger()` déplace les nœuds existants au lieu de les reconstruire — les jetons relevés et les caches de peinture y survivent.

---

## Ce qui a été tranché

- **R5, 04/09/2026 : français seul.** Le corpus est écrit pour être déchiffré vers le français ; la langue cible n'est pas une variable. Pas de localisation sans réécriture complète. Décision prise en connaissance de cause : elle libère les composés, les ambiguïtés et la morphologie.
- **L'invariant I5 du design doc (« progression quasi linéaire ») est retiré.** Aucune mesure de progression n'est linéaire : les signes sont front-chargés, les lignes back-chargées. L'écart entre les deux *est* le propos — on peut lire presque tous les mots et ne comprendre presque rien. L'afficher, ne pas le lisser.
- Lexique porté à **45 signes** (la branche Nombre gagne `cinq` et `mille`, perd `vingt`).
- **17 composés** au lieu des 9 prévus.

---

## État actuel et suite

**Fait** : actes I à III (première moitié), **20 signes sur 45**, corpus complet des 30 tablettes (676 lignes, 3 809 signes), économie réglée sur sept playtests, numération signe par signe jusqu'à `mille`, barre de navigation entre tablettes, infobulles, comptage d'occurrences dans le lexique, journal d'actions horodaté, relevé et recoupement dans le corpus avec gisement par tablette, **datation et réordonnancement chronologique**, instrument **Grammaire**, progression **hors ligne**.

**PT7 fait** (07/09/2026) : 44 min 50. R9 est tranché — le tarif figé à la première visite ramène la main de 0,1 % à **17,9 % des occurrences**, sur 22 tablettes au lieu de 3, jusqu'à la quarantième minute au lieu de la quinzième. I6 global à 31,2 %, mais découpé par tranches il montre deux défauts opposés : 83 % au premier quart d'heure (le mur d'ouverture, connu, non réglé) et 103 % aux cinq dernières minutes (5 232 hypothèses que les Concordances ne buvaient pas). D'où la mesure d'I6 par tranches, et la Grammaire.

**L'acte III, première moitié** (07/09/2026) :

- branche **Temps** — `année`, `avant`, `après`, `siècle`, `nuit`, `dernière-année` — et `mille`
- **datation** : chaque tablette porte sa date depuis la première seconde ; `année` la rend lisible, à condition de savoir lire le nombre. Les deux dernières attendent `dernière-année`.
- **réordonnancement** : `avant` range la barre, `après` range le corpus. Une fois trié, l'ordre chronologique *est* l'ordre des numéros — ce que le joueur ne pouvait pas savoir, et ce que le rangement démontre. La série de la crue devient lisible ; personne ne la commente.
- instrument **Grammaire** : `0,0012 × 1,16^lexique` cert./s, −3 hyp./s, fermé jusqu'à `année`. Première vraie exponentielle, et la seule chose capable d'absorber les hypothèses que PT7 laissait s'entasser.
- **hors ligne** par `nuit` : 40 % du débit, 4 h au plus.

Mesuré : **78,6 à 83,5 min** pour les 20 signes, écart max 6,2 min entre deux déblocages, I6 global 5 %.

**PT8 fait** (07/09/2026) : 63 min 12 pour les 20 signes — le simulateur surestimait de 20 %. I6 tombe à 6,0 % et le déversoir de fin de PT7 est réparé. Mais **le rangement chronologique n'a pas suffi** : 60 lignes du corpus portent un relevé d'eau sur 676, et de 8 à 57 lignes de registre séparent deux relevés consécutifs. Trier ordonne les contenants, ça ne rassemble pas le signal — le joueur est allé sur la tablette 26 (le relevé d'eau complet) treize secondes après avoir acheté `avant`, y a fait vingt relevés, et n'a pas vu la série.

**La Concordance fait enfin son métier** (07/09/2026) : choisir un signe replie le corpus sur ses seules attestations, chaque tablette gardant sa première ligne — celle où elle se date elle-même. Sur `eau`, corpus rangé : 92 lignes au lieu de 676, et vingt relevés qui descendent de 14 à 0. Rien d'ajouté, rien de commenté. C'est aussi le geste répétable qui manquait à l'acte III, dont la fin se jouait en attendant (4 min 51 sans une action dans le corpus en PT8).

**Prochaine étape — PT9, puis la seconde moitié de l'acte III.** PT9 repose la question de PT8 : **la crue qui baisse se voit-elle ?** La colonne existe, reste à savoir si le joueur y va. Le journal d'actions note chaque concordance et son signe — si le TSV n'en contient aucune, c'est le bouton qu'il faut reprendre, pas la vue.

Restent ensuite : la mécanique de **composition** (et donc `zéro` = `ne-pas` + `un`), l'instrument **Élève**, la branche **Modalité**, les glyphes de **Parole III** (`lire`, `scribe`, `archive`, `les-lecteurs`), puis les **contradictions** de l'acte IV — voir `docs/design-doc.md` §7 et §8.

---

## Conventions

- Commentaires en français, au-dessus de ce qui est non évident. Expliquer **pourquoi**, pas quoi.
- Les noms de fonctions et variables suivent la fiction quand c'est naturel : `veille()`, `consignes()`, `recouper()`, `tablette`.
- Le sélecteur de vitesse ×1/×3/×10, le chronomètre et les boutons `traces`/`copier` en haut à droite sont des **outils de test**, marqués « hors jeu ». À retirer de toute version publique.
- `src/traces.js` n'édite aucune règle : il **enveloppe** les actions déjà déclarées. Le retirer = supprimer le fichier, sa ligne dans `index.html` et dans `build.py`, et les deux boutons. Ne jamais y mettre de logique de jeu.
- Écrire les nombres à la française dans l'interface (espace fine insécable, virgule décimale) — `nf` et `f()` s'en chargent.
