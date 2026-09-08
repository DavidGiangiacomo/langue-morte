# La langue morte — design doc

*Format visé : partie unique, 3 h à 3 h 30, pas de prestige. Cadrage : Universal Paperclips (durée, arc, brutalité de la fin), Cifi (texture textuelle).*

> **Ce document décrit la cible, pas l'état du code.** Les écarts assumés entre la vision et l'implémentation sont listés dans `docs/journal.md` — le lire avant de « corriger » le code pour le faire coïncider avec ce doc. Trois points de ce document sont explicitement **caducs** : l'invariant I5 (§9), le compte de 44 signes (§6, désormais 45), et la formulation d'I6 (§9), qui se mesure depuis PT7 par tranches de dix minutes et non sur la partie entière.

---

## 1. Thèse

Un incrémental classique demande : *combien peux-tu produire ?*
Celui-ci demande : *combien peux-tu comprendre ?* — et il sépare violemment les deux.

Deux courbes coexistent et divergent :

- **Les Occurrences** (la donnée brute) suivent une exponentielle de genre : de 1 à ~10¹⁰.
- **La Certitude** (la compréhension) reste à échelle humaine : elle ne dépasse jamais quatre chiffres de toute la partie.

Le joueur passe trois heures à voir sa masse de données exploser pendant que son savoir progresse par petits paliers durement gagnés. C'est le propos du jeu, et c'est une contrainte d'équilibrage, pas une métaphore décorative.

**Le vrai upgrade, c'est la compréhension du joueur, pas celle du personnage.** L'écran est illisible au départ ; chaque signe déchiffré rend littéralement une zone d'interface lisible et opérable. L'arbre d'améliorations *est* le lexique.

---

## 2. Fiction

Un corpus unique : une trentaine de tablettes d'un peuple disparu, sans bilingue, sans descendant, sans contexte. Le joueur n'a ni nom ni avatar — il est simplement celui qui lit.

Ce que le corpus finit par dire : ce peuple ne s'est pas éteint par accident. Il a vu venir sa fin sur deux ou trois générations et il a fait un choix — cesser de tenter de survivre, et consacrer ce qui restait de ressources à concevoir une langue faite pour être déchiffrée. Pas une langue à conserver : une langue à *attraper*. Ils s'appelaient eux-mêmes « les lecteurs ».

La question laissée ouverte à la fin, et jamais tranchée : ce que le joueur emporte est-il un héritage ou un parasite ?

**Ton** : pas de mystère brumeux, pas d'horreur cosmique. Le registre est administratif et tendre — des inventaires de grain, des relevés de crue, et au milieu quelqu'un qui note que la personne qu'il aimait savait lire. La fin est bouleversante parce qu'elle est petite.

---

## 3. Boucle de jeu

**Boucle courte (5–30 s)**

```
Relever (clic/auto) → Occurrences
      ↓ conversion
   Hypothèses
      ↓ recoupement (consomme des Occurrences)
   Certitude
      ↓ dépense
   Signe déchiffré
      ↓
Une zone d'UI devient lisible → nouvel outil → meilleur taux de relevé
```

**Boucle moyenne (5–15 min)** — Rééquilibrer la chaîne. Les convertisseurs *consomment* leur intrant : trop de Tables de fréquences avec trop peu de Copistes et la chaîne s'assèche. Le joueur n'empile pas des générateurs parallèles, il règle des ratios.

**Boucle longue (30–60 min)** — Un acte. Chaque acte débloque une branche du lexique, donc un pan d'interface entier, donc une mécanique dont le joueur ignorait l'existence.

---

## 4. Ressources

| Ressource | Rôle | Ordre de grandeur en fin de partie |
|---|---|---|
| **Occurrences** (O) | matière brute, relevés | ~10¹⁰ |
| **Hypothèses** (H) | candidats de sens | ~10⁷ |
| **Certitude** (C) | seule monnaie des signes | jamais plus de 4 chiffres affichés |
| **Questions** (Q) | acte IV+, interroger le texte | 0 à 12 sur toute la partie |

Règle structurante : **on n'achète jamais un instrument avec de la Certitude, et on n'achète jamais un signe avec autre chose.** Les deux économies ne se touchent que par le taux de conversion. C'est ce qui empêche d'acheter de la compréhension avec du volume.

---

## 5. Instruments

Les générateurs ne sont pas des bâtiments : ce sont des **méthodes philologiques**. L'échelle va de l'œil nu à la machine.

| # | Instrument | Effet | Acte |
|---|---|---|---|
| 1 | **Œil** | le clic | I |
| 2 | **Copiste** | produit des occurrences | I |
| 3 | **Table de fréquences** | occurrences → hypothèses ; donne aussi le comptage d'occurrences au survol d'un signe inconnu | I |
| 4 | **Concordance** | hypothèses → certitude ; rassemble aussi les attestations d'un signe en une colonne — c'est elle qui rend la série de la crue lisible à l'acte III | II |
| 5 | **Atelier de copie** | gros producteur d'occurrences | II |
| 6 | **Grammaire** | hypothèses → certitude, **croît avec la taille du lexique** — la première vraie exponentielle | III |
| 7 | **Élève** | multiplie tout, **et introduit un taux d'erreur** | III |
| 8 | **Corpus jumeau** | une deuxième inscription est trouvée | IV |
| 9 | **Le Lecteur** | acheté avant qu'on sache ce que c'est. On découvre à l'acte V que ce n'est pas un instrument : c'est le corpus qui a commencé à lire. | V |

*(Valeurs numériques : voir `docs/journal.md` § Réglages actuels pour les 1 à 6, qui sont implémentés et équilibrés sur sept playtests. La Grammaire est arrivée avec l'acte III ; l'Élève attend les lectures fausses de l'acte IV, sans lesquelles son taux d'erreur n'a rien à fausser.)*

**L'Élève** est le premier générateur *ambivalent*. Il multiplie tout, mais il déchiffre aussi tout seul, et il se trompe. Le joueur qui empile les Élèves déchiffre vite et faux. C'est l'arbitrage central de la seconde moitié du jeu.

---

## 6. L'arbre des signes

45 signes, 7 branches. **Chaque branche déverrouille une zone d'écran précise** — la carte du lexique et la carte de l'interface sont la même carte.

| Branche | Zone d'UI rendue lisible | Acte |
|---|---|---|
| **Nombre** | les compteurs eux-mêmes | I |
| **Matière** | le panneau des instruments | II |
| **Parole** | les infobulles, les coûts, les taux | II–III |
| **Temps** | la barre de progression, l'horloge, le hors-ligne | III |
| **Modalité** | le panneau de révision, les indices de confiance | III–IV |
| **Personne** | le journal, le panneau de questions | IV |
| **Fin** | l'écran de fin | V |

Le détail des 45 signes est dans `docs/corpus.md` §2. Effets notables :

- **Nombre** — chaque signe ouvre un rang de numération ; `deux` ouvre le principe du redoublement. Voir `docs/corpus.md` §3.
- **Matière** — nomme les instruments et les rend opérables.
- **Parole** — `dire` fait annoncer au lexique ce qu'il fait (avant, on achète à l'aveugle) ; `les-lecteurs` déclenche le premier basculement narratif.
- **Temps** — `nuit` débloque la progression hors-ligne (le corpus « se lit la nuit ») ; `avant`/`après` permettent de dater les tablettes, donc de les **ordonner** — le corpus se réorganise chronologiquement à l'écran et des passages jusque-là absurdes prennent sens.
- **Modalité** — ouvre le système de confiance. Avant `peut-être`, le jeu ne dit jamais qu'une lecture est incertaine : le joueur croit tout ce qu'il achète. `faux` affiche rétroactivement les erreurs déjà commises. Le pic de malaise du jeu.
- **Personne** — `toi` révèle que tout le corpus est à la deuxième personne. Débloque les **Questions**. `nous-fûmes` verrouille le récit au passé, y compris les passages déjà lus.
- **Fin** — `devenir-lecture` est le dernier signe et la clé de tout. Un joueur qui a `lire` et `devenir` peut le **composer lui-même** avant que le récit ne l'y amène, et griller la révélation de vitesse. C'est voulu.

---

## 7. Composition

À partir de l'acte III, une grille permet de poser un signe sur un autre pour tenter un composé.

- Tentative valide → le composé est acquis (coût normal en C), souvent en avance sur le récit.
- Tentative invalide → on perd les H engagés, **jamais de C**, et la paire est notée dans un carnet pour ne pas la retenter.
- **17 des 45 signes sont des composés** (table `COMP` dans `src/signes.js`), et ils sont dessinés comme composés dès le premier écran : le joueur voit ⟨maison⟩ et ⟨grain⟩ dans ⟨grenier⟩ bien avant de pouvoir composer quoi que ce soit.
- **3 ne sont accessibles que par composition** et ne sont jamais offerts par la progression : `zéro` (= `ne-pas` + `un`), `grenier`, `devenir-lecture`.

`zéro` est l'exemple canonique : un signe de la branche Nombre qui se compose avec un signe de la branche Modalité, deux actes plus tard. Il donne rétroactivement la notation compacte des grands nombres. Le joueur qui le trouve seul comprend, à ce moment précis, que ce peuple a *inventé* le zéro — et qu'il regardait ce signe dans ses propres compteurs depuis la première seconde de jeu sans le savoir.

C'est le système qui fait la différence entre ce jeu et un Cookie Clicker rethématisé : il y a un espace de découverte que le jeu ne guide pas.

---

## 8. Confiance, ambiguïté, contradiction

Onze signes sur 45 sont **ambigus** : deux lectures possibles, le joueur tranche à l'achat. La liste et leurs lectures fausses sont dans `docs/corpus.md` §7.

| | Lecture juste | Lecture fausse |
|---|---|---|
| Effet mécanique | nominal | **+25 %** |
| Texte narratif | cohérent | un mot faux, partout où le signe apparaît |
| Dette | 0 | +1 à +3 points, invisible avant `peut-être` |

Le piège est délibéré : se tromper *paie mieux à court terme*. C'est du biais de confirmation transformé en optimum local.

**Contradiction** — au franchissement de chaque acte, si dette > seuil, un passage refuse de se résoudre : la production de C est divisée par deux jusqu'à révision. On ne perd jamais de progression, seulement du débit.

**Révision** — rouvrir un signe, payer un coût en C, choisir à nouveau. Juste → dette effacée + bonus rétroactif. Faux → on repaie.

**Ce qui rend le système honnête** : le seul indice fiable pour trouver le signe fautif est le texte lui-même. Un joueur qui lit voit que « le grenier pleure trois fois par nuit » n'a pas de sens et sait quoi réviser. Un joueur qui optimise sans lire doit brute-forcer, ce qui coûte cher.

**Le jeu récompense la lecture, mécaniquement.** C'est le cœur du design.

---

## 9. Courbes, invariants, rythme

### Rythme cible

| Acte | Temps cumulé | Signes |
|---|---|---|
| I — Signes | 0–15 min | 0 → 6 |
| II — Noms | 15–45 min | 6 → 14 |
| III — Grammaire | 45–100 min | 14 → 26 |
| IV — La voix | 100–165 min | 26 → 36 |
| V — La graine | 165–210 min | 36 → 45 |

### Invariants

- **I1** — La Certitude ne dépasse jamais 4 chiffres à l'écran.
- **I2** — Pas de notation scientifique avant l'acte IV. Quand elle apparaît, elle apparaît **d'abord en signes non déchiffrés** : le joueur perd la lisibilité de ses propres nombres au moment où ils deviennent énormes.
- **I3** — Chaque nouveau palier d'instrument devient abordable ~90 s après le premier achat du palier précédent.
- **I4** — Un signe toutes les 4 à 6 min en moyenne ; **jamais plus de 8 min sans déblocage**.
- ~~**I5** — Le pourcentage de corpus lisible progresse quasi linéairement.~~ **RETIRÉ.** Mesuré faux : les signes se déchiffrent front-chargé (la masse administrative tombe tôt), les lignes entières back-chargé (le sens ne se complète qu'à la fin). L'écart entre les deux *est* le propos du jeu. Le jeu affiche les deux mesures et n'en lisse aucune.

**Invariant ajouté après les playtests 1 et 2 :**

- **I6** — Aucune action manuelle répétée ne doit fournir plus de **30 %** de la Certitude produite, **sur aucune tranche de dix minutes**. Mesuré par `outils/sim.py`. Deux playtests de suite, c'est ce qui a cassé le jeu ; et le ratio sur la partie entière, mesuré à 30,0 % en PT6, cachait un 83 % au premier quart d'heure et un 103 % aux cinq dernières minutes (PT7). Une moyenne n'est pas un invariant.

### Hors-ligne

40 % du taux, plafonné à 4 h. Débloqué par `nuit` (acte III). Avant ça, le jeu ne progresse pas hors-ligne — et c'est diégétique : il n'y a personne pour lire.

---

## 10. Arc narratif — 5 actes

**Acte I — Signes.** Écran opaque. Un seul mot français à l'écran, en bas : *commence*. Le joueur clique sur des signes, un compteur bouge dans une numération inconnue. La première découverte est celle du système de numération : le signe de « deux » est celui de « un » redoublé. *Un joueur attentif peut décoder les chiffres tout seul en observant son compteur monter, avant d'acheter le signe.* C'est le premier plaisir du jeu et il faut le protéger absolument.

**Acte II — Noms.** Le corpus livre des inventaires : grain, eau, champs, maisons. Rien de dramatique — de la comptabilité agricole. Ton sec, administratif, presque décevant. C'est voulu : on installe le quotidien pour que sa disparition compte.

**Acte III — Grammaire.** L'exponentielle démarre : les signes connus aident à en déchiffrer d'autres. Les tablettes se datent et **se réordonnent** — et l'ordre chronologique révèle que les relevés de crue diminuent, année après année, sur trois générations. Personne ne le commente. C'est dans les chiffres. Fin d'acte : ce peuple s'appelait « les lecteurs ». Première contradiction majeure ici.

**Acte IV — La voix.** Le corpus n'est pas un registre : il est écrit à la deuxième personne, et il l'a toujours été — le jeu réaffiche les passages déjà lus, désormais adressés au joueur. Déblocage des Questions : on peut interroger le texte, il répond, dans les limites de ce qui a été gravé il y a quatre mille ans. Puis `faux` : le joueur voit rétroactivement tout ce qu'il a mal traduit depuis le début.

**Acte V — La graine.** La révélation : ce n'est pas un message conservé, c'est un message *conçu*. Structure, redondance, ambiguïtés placées, récompenses de déchiffrement — la langue est un objet d'ingénierie, optimisé pour qu'un inconnu la casse et, ce faisant, l'installe. Ils avaient environ deux siècles. Ils ont arrêté d'essayer de survivre et ont tout mis là-dedans.

**Dernière tablette.** Courte, pas grandiose, signée. Une note de la dernière personne à avoir gravé. Elle parle du grain, de la crue, et de quelqu'un qu'elle a aimé. Elle ne demande rien. *(Texte exact : `docs/corpus.md`, tablette 30.)*

---

## 11. Fins et relecture

Un dernier signe reste à l'écran. Deux boutons :

- **Achever** — lire le dernier signe. Le corpus est à 100 %. L'écran se vide progressivement de son interface : plus de compteurs, plus d'instruments, juste le texte, entièrement en français. Puis le texte s'efface aussi.
- **Interrompre** — laisser un signe non lu. Le jeu se ferme sur le corpus figé, et ne propose pas de reprendre.

Aucune n'est présentée comme la bonne. Le jeu n'attribue pas de score.

**Relecture (NG+)** — après *Achever*, une option « relire » : le corpus est intégralement lisible dès le départ, et le jeu **surligne toutes les erreurs de traduction de la première partie**, y compris celles jamais détectées. Vingt minutes, sans mécanique. Ce n'est pas un prestige, c'est un épilogue. Coût de production quasi nul, valeur émotionnelle importante.

---

## 12. Interface

**Écran unique**, trois colonnes :

- **Gauche** — le corpus. Un mur de texte défilant, en signes, précédé d'une barre de tablettes pour y naviguer. Les mots déchiffrés sont remplacés *sur place*, avec une transition, à l'instant de l'achat. C'est le spectacle central du jeu. Le survol d'un mot traduit redonne son signe.
- **Centre** — relevés, actions manuelles, instruments.
- **Droite** — le lexique, en branches.
- **Trois états par élément d'UI** : *opaque* (signes, inerte) → *reconnu* (on sait que c'est un compteur, pas ce qu'il compte) → *lisible* (label + infobulle + opérable).

**Coût de production réel** : le budget du jeu est le texte, pas le code.

---

## 13. Risques

| | Risque | Réponse |
|---|---|---|
| R1 | Les trois premières minutes d'illisibilité font fuir | Premier signe accessible en < 60 s ; un mot français en clair dès t=0 ; le compteur bouge visiblement à chaque clic |
| R2 | Le système de contradiction paraît punitif | On ne perd jamais de progression, seulement du débit ; la révision est toujours disponible ; l'indice est dans le texte |
| R3 | La composition devient un jeu de devinettes | Échec = coût en H seulement, jamais en C ; carnet des tentatives ; 3 composés secrets seulement |
| R4 | Le texte doit tenir trois heures | **Confirmé par le playtest 3** : le testeur a explicitement dit que la qualité de ce qui se découvre serait déterminante. Écrire avant de coder. |
| R5 | Localisation | **Tranché : français seul.** Le jeu *est* un acte de traduction vers le français. Pas de localisation sans réécriture complète du corpus. |
| R6 | *(nouveau)* Une action manuelle répétée devient la source principale de la Certitude | Invariant I6, mesuré par `outils/sim.py` à chaque ajout d'instrument |
