# PT11 — protocole

*Établi le 17/09/2026, après LIV-2. Premier playtest joué à distance, et le premier depuis
PT5 (06/09/2026, treize signes) par quelqu'un d'autre que l'auteur.*

> **La règle qui commande tout ce fichier** : le message ne doit rien apprendre. Neuf des
> questions de PT11 portent sur ce qu'un joueur trouve **sans savoir qu'il y a quelque chose
> à trouver** — la composition, les deux lectures, ⟨nous⟩ dans le nom. Une phrase de trop
> dans le courrier d'accompagnement les annule toutes, et aucune ne se repose ensuite : on ne
> désapprend pas à un joueur qu'il choisissait.

---

## 1. Le message à envoyer

*À copier tel quel. Rien à y ajouter — en particulier rien sur ce qu'est le jeu.*

---

Salut,

J'ai un prototype à faire tester, et j'ai besoin de quelqu'un qui ne sait rien de ce que j'ai
construit. C'est exactement pour ça que je ne te dis rien de plus.

**Le lien :** https://davidgiangiacomo.github.io/langue-morte/

**Ce qu'il faut savoir avant de cliquer, et c'est tout :**

- Compte **une heure et demie**, d'une traite. C'est long, et c'est fait pour être long —
  mais choisis un moment où tu ne seras pas coupé, ça vaut mieux pour ce que je mesure.
- Ça se joue à la souris et au clavier, dans le navigateur, sur un ordinateur. Pas sur
  téléphone.
- **Tu ne peux rien casser, et tu ne peux pas mal jouer.** Il n'y a pas de score, pas de
  bonne méthode, et personne ne regarde par-dessus ton épaule.
- Reste sur le même navigateur : la partie se sauvegarde toute seule, mais dans celui-là
  seulement.
- **Ne va pas voir le dépôt GitHub.** Il contient toutes les réponses, littéralement.

**La seule chose que je te demande vraiment :**

En haut à droite il y a un bouton **`copier`**, sous l'étiquette « journal de partie — à
renvoyer ». Quand tu t'arrêtes, clique dessus et colle-moi ce que ça donne — par mail, par
message, comme tu veux. Ça fait un gros pavé de texte, c'est normal.

**Et surtout : fais-le même si tu arrêtes en cours de route.** Une partie abandonnée au bout
de dix minutes m'apprend plus qu'une partie finie. C'est sincèrement le cas, ce n'est pas une
formule pour que tu ailles au bout — si tu t'ennuies, si tu ne comprends pas, si tu as autre
chose à faire : arrête, clique `copier`, envoie. C'est un résultat, pas un échec.

Dernière chose, facultative : si à un moment tu es bloqué ou agacé, note le chiffre du
chronomètre en haut à droite et deux mots. Pas plus — ne prends pas de notes en jouant.

On se rappelle après, j'aurai quelques questions. Merci —

David

---

## 2. Avant l'entretien : dépouiller d'abord

```bash
python outils/depouiller.py traces-AAAAMMJJ-HHMM.tsv
```

**Dans cet ordre, et pas l'inverse.** Cinq des questions ci-dessous ne se posent que si la
chose a eu lieu — la contradiction s'est-elle déclenchée, `faux` a-t-il été acheté, y a-t-il
eu une révision, la grille a-t-elle servi. Les poser à vide apprend au joueur qu'il a raté
quelque chose, ce qui est un renseignement et fausse tout ce qui suit.

Trois contrôles à lire en premier :

1. **L'avertissement d'en-tête.** Le build de playtest n'a pas de sélecteur de vitesse, donc
   il ne devrait pas y avoir de ligne `vitesse` — s'il y en a une, le joueur n'a pas joué la
   page déployée.
2. **L'écart médian ΔO prédit / observé**, attendu à 0,0 %. S'il ne l'est pas, ne rien croire
   de la section « la main ».
3. **Les coupures.** La production hors ligne de `nuit` est créditée *sans avancer le chrono
   de jeu* (`economie.js:629`) : si le joueur a fermé l'onglet en cours de partie après avoir
   acheté `nuit`, l'intervalle qui enjambe la coupure porte une production que le modèle ne
   peut pas prédire. Le contrôle 2 la montrera comme une anomalie locale — c'est une coupure,
   pas une divergence entre `sim.py` et `economie.js`.

---

## 3. Les questions, dans l'ordre

**L'ordre est la moitié du travail.** Chaque question enseigne quelque chose au joueur ; une
fois enseignée, elle contamine toutes les suivantes. On va donc de l'ouvert au précis, et les
trois dernières — celles qui révèlent — se posent à la fin, dans cet ordre-là.

Les questions 1 à 8 peuvent se poser par écrit. **Les questions 9 à 11 se posent de vive
voix**, et la 11 une seule fois.

### Premier tour — ouvert, ne rien nommer

1. **Raconte-moi la partie.**
   → *Laisser parler, ne pas relancer sur un mot précis. Ce qu'il nomme spontanément, et
   l'ordre dans lequel il le nomme, est la donnée.*
2. **Qu'est-ce que tu faisais, en fait ?** À quel moment tu l'as compris ?
3. **Y a-t-il eu un moment où tu as failli arrêter ?** Lequel, et qu'est-ce qui t'a fait
   continuer ?
   → *La dixième minute. C'est là que la partie 1 de PT5 s'est arrêtée, et c'est le seul
   défaut d'équilibrage connu qui ne soit pas réglé. Croiser avec l'heure du premier achat de
   Concordance dans le TSV — 6,8′ au réglage actuel.*
4. **Est-ce que le texte raconte quelque chose ?** Quoi ?
   → *R4, et la remarque de PT3 : « la qualité de ce qui se découvre sera déterminante ».
   Question ouverte — ne surtout pas suggérer qu'il y a une histoire.*
5. **Y a-t-il eu un moment où tu as compris quelque chose que le jeu ne t'avait pas dit ?**
   → *La plus large du lot, et la seule qui puisse faire remonter la crue, les composés ou les
   deux lectures sans qu'on les nomme. Si quelque chose remonte ici, c'est la meilleure
   réponse de tout le playtest.*

### Deuxième tour — les mécaniques, sans dire ce qu'elles cachent

6. **Après la quarantième minute, tu faisais quoi ?**
   → *LA question neuve de PT11. PT10 : cinquante minutes d'affilée sans un geste dans le
   texte, de 36:46 à 86:34. Le TSV répond aussi, mais on veut savoir s'il l'a senti comme un
   vide ou pas du tout. Ne pas demander « tu t'es ennuyé ? », qui souffle la réponse.*
7. **Le panneau où on assemble deux signes — tu t'en es servi ?** Qu'est-ce que tu attendais
   qu'il se passe ?
   → *Le seul retour qualitatif de PT10 portait là-dessus, et COMP-6 (17/09) y a répondu par
   un intitulé, « CE QUE JE SAIS LIRE ». On vérifie que la perplexité ne revient pas. Ne pas
   demander « as-tu trouvé des signes » : ça dirait qu'il y en a.*
8. *(si le TSV dit que la contradiction s'est déclenchée)* **Le bandeau qui est apparu, tu
   l'as compris comment ?** Qu'est-ce que tu as fait ?
   → *Le point : sanction, ou panne ? S'il l'a lu comme un bug, c'est le texte du bandeau
   qu'on reprend, jamais le seuil.*

   *(si `faux` a été acheté)* **Les lignes qui se sont allumées, tu en as fait quoi ?**
   → *Si elles n'ont servi à choisir aucune révision, la marque ne suffit pas — mais la
   réponse ne sera jamais de nommer le signe.*

### Troisième tour — les trois qui révèlent

*À partir d'ici chaque question apprend quelque chose de définitif. Ne pas remonter au tour
précédent après les avoir posées.*

9. **Montrer ⟨grenier⟩, puis le zéro. « Qu'est-ce que tu vois là-dedans ? »**
   → *Reconnaît-il ⟨maison⟩ et ⟨grain⟩ dans l'un, ⟨ne-pas⟩ et ⟨un⟩ dans l'autre ? Le zéro est
   sous ses yeux depuis la première seconde. Règle 4 : le corpus dessine les composés comme
   composés, et c'est le seul indice du jeu. Montrer le tracé, ne pas le nommer.*
10. **Montrer `les-lecteurs`. « Et là ? »**
    → *Le nom se dessine ⟨lire⟩ sur ⟨nous⟩, et ⟨nous⟩ se tient seul juste devant lui, sur la
    même ligne — 41 fois dans le corpus, jamais au lexique. C'est la porte de l'acte IV, et
    elle n'est nulle part ailleurs que dans le texte. La ligne de journal de l'achat le dit
    déjà (« la moitié du nom est un signe que je ne sais pas lire ») : la question est donc
    s'il l'a lue, et s'il est allé voir.*
11. **« Tu as remarqué que tu choisissais ? »**
    → **Une seule fois, en dernier, et jamais avant.** Neuf signes proposent deux lectures au
    moment de payer, à prix, tracé et ligne d'effet identiques ; le jeu ne l'admet pas avant
    `peut-être`. Cette question révèle la colonne vertébrale des actes III à V — une fois
    posée, ce joueur ne peut plus jamais servir à la mesurer.
    → *Croiser avec le TSV : combien de lectures fausses sur neuf ? Pile ou face donnerait
    4,5. Nettement moins = quelque chose souffle la réponse. Nettement plus = le corpus induit
    en erreur. PT10 : trois sur neuf, compatible avec le hasard, mais c'est l'auteur qui
    jouait.*

---

## 4. Ce qu'on ne dit à aucun moment

- Qu'il s'agit de déchiffrer. Le jeu le montre ou ne le montre pas ; c'est la mesure.
- Qu'on peut assembler des signes, et qu'il en existe hors de l'arbre.
- Qu'un signe puisse avoir deux lectures, ou qu'on ait pu se tromper.
- Qu'il existe un relevé, un recoupement, une concordance — les trois gestes du corpus se
  trouvent ou ne se trouvent pas.
- Qu'il y a une fin, et à quelle minute elle tombe.
- Combien de joueurs sont passés avant, et ce qu'ils ont fait.

---

## 5. Pendant PT11 : rien ne va sur `develop`

Le workflow Pages déploie **à chaque poussée sur `develop`**. Une partie en cours change donc
de jeu au rechargement suivant, et LIV-3 n'est pas traité — la sauvegarde ne porte pas de
version et ne se migre pas.

La parade est un usage, et un usage n'est gardé par rien : travailler sur branche, ne pas
merger avant le retour du TSV. C'est aussi pourquoi **E5 (l'Élève) n'est pas le prochain
lot** — il ajoute un instrument, donc la règle 2 impose de reprendre les tranches d'I6, donc
il déplace l'économie que PT11 doit mesurer.
