# La langue morte

Un jeu incrémental où l'interface est illisible au départ. Chaque signe déchiffré rend une zone d'écran lisible et débloque des mécaniques qu'on ne soupçonnait pas. Le corpus — trente tablettes d'un peuple disparu — se traduit sous les yeux du joueur, et finit par expliquer pourquoi ce peuple a disparu.

Prototype jouable des **cinq actes** : les 43 signes de l'arbre et deux composés qu'aucune branche n'offre, le corpus complet — 30 tablettes, 705 lignes, 3 838 signes —, deux fins et une relecture. Une partie dure de deux heures à deux heures quarante au simulateur.

## Jouer

Ouvrir `dist/langue-morte.html` dans un navigateur. Un seul fichier, aucune dépendance.

Pour développer, `src/index.html` se joue directement sans rien construire.

Au clavier : `j` / `k` passent d'une tablette à l'autre, `c` ouvre et ferme la concordance, `échap` annule le geste en cours. Le survol d'un mot traduit redonne son signe ; celui d'un signe inconnu donne son nombre d'occurrences, une fois la Table de fréquences posée.

Les deux actions manuelles du jeu — relever un signe, recouper deux attestations d'un même signe dans deux tablettes différentes — se choisissent **dans le texte** : aucun bouton ne produit d'occurrences ni de Certitude par lui-même.

En haut à droite, la barre marquée « hors jeu » (chronomètre, ×1/×3/×10, `traces`, `copier`, `réinitialiser`) est de l'instrumentation de playtest. Elle ne fait pas partie du jeu, et le build la réduit ou la retire selon la page produite — voir *Construire*.

## Construire

```bash
python build.py
```

Assemble `src/` en quatre pages autonomes, en un seul passage :

| | contient | pour |
|---|---|---|
| `dist/langue-morte.html` | tout | jouer et développer |
| `dist/artefact.html` | tout, sans `<!doctype>/<html>/<head>/<body>` | l'outil Artifact de Claude |
| `dist/playtest.html` | le journal d'actions, sans le sélecteur de vitesse ni « réinitialiser » | un playtest à distance |
| `dist/public.html` | ni barre hors jeu, ni journal d'actions | la version publique |

Le sélecteur de vitesse sort du build de playtest parce qu'il multiplie les secondes de **jeu** — celles que le journal d'actions horodate : une partie accélérée par mégarde rendrait des minutes qui n'ont jamais été vécues, et rien, après coup, ne permettrait de s'en apercevoir.

## Modifier le texte

Le contenu éditorial de référence est `docs/corpus.md`. Sa transcription exécutable est `outils/corpus.py`. Après toute modification :

```bash
python outils/corpus.py   # regénère src/corpus.js
python build.py
```

Ne jamais éditer `src/corpus.js` à la main.

## Vérifier

```bash
pip install playwright && playwright install chromium
python build.py && python outils/verifier.py
```

444 assertions bout en bout, en trente-cinq sections : absence d'erreur JS, rendu complet du corpus, échelle de la numération signe par signe, infobulles, gisement et tarif du relevé, recoupement, datation et rangement chronologique, concordance, composition, ambiguïté, doute, révision, contradiction et passages rompus, l'Élève qui tranche à la place du joueur, la branche Personne et le franchissement d'acte, les Questions, le Corpus jumeau, la branche Fin et son dernier signe, le Lecteur, les deux fins et la relecture, les nombres du joueur au million, la sanction aux actes IV et V, progression hors ligne, reprise d'une sauvegarde commencée avant une mécanique neuve, sa migration d'une version à l'autre, ce que le panneau de composition dit de lui-même, et ce que chacun des builds n'a pas. Chaque mécanique ajoutée doit y ajouter les siennes.

```bash
python build.py && python outils/repetition.py
```

La répétition générale du dépouillement : une partie entière jouée au build de playtest par l'acheteur de `sim.py`, dans l'interface, sur une horloge simulée — deux séances, les deux fins, la relecture —, puis son journal d'actions confronté ligne à ligne à ce que `outils/depouiller.py` en lit. Environ cinq minutes. À relancer avant chaque playtest : un journal de joueur ne se refait pas.

## Équilibrer

```bash
python outils/sim.py        # une partie simulée, à trois cadences de clic
python outils/balayage.py   # une grille de constantes, filtrée sur les garde-fous
```

`sim.py` rejoue l'économie avec un acheteur heuristique et rend la durée, l'écart maximal entre deux déblocages, la part manuelle des occurrences, et **la part de la Certitude venue d'actions manuelles, par tranches de dix minutes** — la métrique à surveiller (règle 2 du `CLAUDE.md`).

`balayage.py` rejoue `sim.run` sur une grille de valeurs et ne garde que les combinaisons qui passent les garde-fous. Il joue chaque combinaison aux trois cadences **et aux deux lectures extrêmes** : depuis l'acte III, la durée d'une partie dépend aussi de ce que le joueur a compris.

**Aucun chiffre de rythme ne s'annonce sans avoir été simulé ou mesuré** : les neuf playtests ont tous invalidé une intuition d'équilibrage, et le simulateur lui-même deux fois.

## Documentation

> Ces documents racontent le jeu en entier, ses pièges compris. À lire après y avoir joué, ou en sachant ce qu'on y perd.

| | |
|---|---|
| `docs/design-doc.md` | la vision complète : boucle, courbes, arbre, arc narratif sur cinq actes |
| `docs/corpus.md` | les 30 tablettes, le lexique de 45 signes, les règles de génération, les signes ambigus |
| `docs/journal.md` | les neuf playtests, les défauts trouvés, les décisions prises et pourquoi |
| `docs/backlog-1.0.md` | ce qui reste jusqu'à la 1.0 : onze épics, leurs dépendances, leur ordre |
| `docs/pt11-protocole.md` | le prochain playtest : le message au joueur, le dépouillement, l'entretien |
| `CLAUDE.md` | contexte et règles pour travailler sur le projet |
