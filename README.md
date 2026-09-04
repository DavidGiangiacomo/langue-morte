# La langue morte

Un jeu incrémental où l'interface est illisible au départ. Chaque signe déchiffré rend une zone d'écran lisible et débloque des mécaniques qu'on ne soupçonnait pas. Le corpus — trente tablettes d'un peuple disparu — se traduit sous les yeux du joueur, et finit par expliquer pourquoi ce peuple a disparu.

Prototype jouable des **actes I et II** : 13 signes sur 45, le corpus complet.

## Jouer

Ouvrir `dist/langue-morte.html` dans un navigateur. Un seul fichier, aucune dépendance.

Pour développer, `src/index.html` se joue directement sans rien construire.

Au clavier : `j` / `k` passent d'une tablette à l'autre. Le survol d'un mot traduit redonne son signe.

## Construire

```bash
python build.py
```

Assemble `src/` en `dist/langue-morte.html` (page autonome) et `dist/artefact.html` (variante pour l'outil Artifact de Claude).

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

Contrôle l'absence d'erreurs JS, le rendu complet du corpus, l'échelle de la numération signe par signe, et les infobulles.

## Équilibrer

```bash
python outils/sim.py
```

Simule une partie complète avec un acheteur heuristique et une cadence de clic paramétrable. Donne la durée, l'écart maximal entre deux déblocages, et **la part de la Certitude venue d'actions manuelles** — la métrique à surveiller (voir `CLAUDE.md`).

## Documentation

| | |
|---|---|
| `docs/design-doc.md` | la vision complète : boucle, courbes, arbre, arc narratif sur cinq actes |
| `docs/corpus.md` | les 30 tablettes, le lexique de 45 signes, les règles de génération, les signes ambigus |
| `docs/journal.md` | les trois playtests, les défauts trouvés, les décisions prises |
| `CLAUDE.md` | contexte et règles pour travailler sur le projet |
