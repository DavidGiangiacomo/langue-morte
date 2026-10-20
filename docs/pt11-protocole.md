# PT11 — protocole

*Réécrit le 20/10/2026 pour les cinq actes. La version du 17/09/2026 couvrait les actes I à
III ; elle n'a jamais servi, faute de joueur, et elle reste dans l'historique (`319f671`).
L'auteur a tranché le jour même : **le prochain joueur joue la branche entière** — l'Élève,
les actes IV et V, les deux fins, la relecture — et non plus `develop` tel qu'il était. C'est
toujours le premier playtest joué à distance, et le premier depuis PT5 (06/09/2026, treize
signes) par quelqu'un d'autre que l'auteur.*

> **La règle qui commande tout ce fichier** : le message ne doit rien apprendre. Plus de la
> moitié des questions de PT11 portent sur ce qu'un joueur trouve **sans savoir qu'il y a
> quelque chose à trouver** — la composition, les deux lectures, ⟨nous⟩ dans le nom, ce que
> fait l'instrument sans nom, le zéro qui rend les nombres. Une phrase de trop dans le
> courrier d'accompagnement les annule toutes, et aucune ne se repose ensuite : on ne
> désapprend pas à un joueur qu'il choisissait.

**Ce que ce playtest ne mesurera pas, et c'est un choix** : l'économie sans Élève. La branche
le met à la portée du joueur dès la 48ᵉ minute ; on saura combien il en prend, pas ce qu'aurait
été sa partie sans lui. Le simulateur, lui, le sait (règle 31) ; le joueur dira le reste.

---

## 1. Le message à envoyer

**Avant de l'envoyer** : `python build.py && python outils/repetition.py` doit finir sur
« répétition tenue ». La répétition fait jouer une partie entière à la page que Pages
déploie et dépouille son journal ; un défaut de `traces.js` qu'elle trouverait ne se corrige
plus une fois le message parti (§5), et le journal du joueur, lui, ne se refait pas.

*À copier tel quel. Rien à y ajouter — en particulier rien sur ce qu'est le jeu, ni sur ce qui
se passe à la fin.*

---

Salut,

J'ai un prototype à faire tester, et j'ai besoin de quelqu'un qui ne sait rien de ce que j'ai
construit. C'est exactement pour ça que je ne te dis rien de plus.

**Le lien :** https://davidgiangiacomo.github.io/langue-morte/

**Ce qu'il faut savoir avant de cliquer, et c'est tout :**

- Compte **trois heures**, en une fois ou en deux — pas plus de deux. C'est long, et c'est
  fait pour être long. Si tu coupes, coupe une seule fois, et choisis des moments où tu ne
  seras pas dérangé : ça vaut mieux pour ce que je mesure.
- Pour faire une pause, ferme simplement l'onglet. Pour reprendre, rouvre le même lien
  **dans le même navigateur** : la partie se sauvegarde toute seule, mais dans celui-là
  seulement.
- Ça se joue à la souris et au clavier, dans le navigateur, sur un ordinateur. Pas sur
  téléphone.
- **Tu ne peux rien casser, et tu ne peux pas mal jouer.** Il n'y a pas de score, pas de
  bonne méthode, et personne ne regarde par-dessus ton épaule.
- **Ne va pas voir le dépôt GitHub.** Il contient toutes les réponses, littéralement.

**La seule chose que je te demande vraiment :**

En haut à droite il y a un bouton **`copier`**, sous l'étiquette « journal de partie — à
renvoyer ». Quand tu t'arrêtes pour de bon, clique dessus et colle-moi ce que ça donne — par
mail, par message, comme tu veux. Ça fait un gros pavé de texte, c'est normal. Pas besoin de
le faire à la pause : le journal attend la suite avec la partie.

**Et surtout : fais-le même si tu arrêtes en cours de route.** Une partie abandonnée au bout
de dix minutes m'apprend plus qu'une partie finie. C'est sincèrement le cas, ce n'est pas une
formule pour que tu ailles au bout — si tu t'ennuies, si tu ne comprends pas, si tu as autre
chose à faire : arrête, clique `copier`, envoie. C'est un résultat, pas un échec.

Dernière chose, facultative : si à un moment tu es bloqué ou agacé, note le chiffre du
chronomètre en haut à droite et deux mots. Pas plus — ne prends pas de notes en jouant.

On se rappelle après, j'aurai quelques questions. Merci —

David

---

*Ce que le message ne dit pas, exprès* : qu'il y a une fin, et ce qu'on y trouve. Le joueur
qui achève verra « relire » et cliquera sans doute avant l'entretien. C'est tranché : **on le
laisse faire**, et l'entretien s'adapte (§3, questions 19 et 20). Prévenir aurait protégé
l'ordre des questions au prix d'un renseignement — qu'il y a quelque chose après la fin.

---

## 2. Avant l'entretien : dépouiller d'abord

```bash
python outils/depouiller.py traces-AAAAMMJJ-HHMM.tsv
```

**Dans cet ordre, et pas l'inverse.** Plus de la moitié des questions ci-dessous ne se posent
que si la chose a eu lieu — un Élève acheté, la contradiction déclenchée, ⟨toi⟩ atteint, une
question posée, le Lecteur acheté, la notation des grands nombres apparue, une fin choisie, la
relecture ouverte. Les poser à vide apprend au joueur qu'il a raté quelque chose, ce qui est un
renseignement et fausse tout ce qui suit.

### Trois contrôles à lire en premier

1. **L'avertissement d'en-tête.** Le build de playtest n'a pas de sélecteur de vitesse : s'il y
   a une ligne `vitesse`, le joueur n'a pas joué la page déployée. Et l'en-tête dit de quel
   build sort le journal — il doit dire `playtest` et `43 glyphes d'arbre`.
2. **L'écart médian ΔO prédit / observé**, attendu à 0,0 %. S'il ne l'est pas, ne rien croire
   de la section « la main ». Il porte sur chaque intervalle de trente secondes, relevés,
   achats et recoupements compris : il contrôle donc aussi le tarif de chaque tablette, c'est-à-
   dire la part de la main elle-même. Jusqu'à la répétition générale du 20/10/2026, il ne
   lisait que les intervalles sans un relevé, et un joueur qui relève régulièrement — ce que
   le Corpus jumeau demande — aurait rendu un journal sans contrôle.
3. **La coupure.** On en attend une, entre les deux séances, et le journal la date. Avant
   ⟨nuit⟩ (vers la 73ᵉ minute au simulateur), rien ne se passe pendant qu'elle dure : la
   partie attend. Après, la production hors ligne est créditée au retour *sans avancer le
   chrono de jeu* — 40 % du débit, quatre heures au plus, et jamais une question (règle 24) —,
   et la ligne `veillee` porte le total au retour, pas le gain. Le contrôle 2 écarte
   l'intervalle qui l'enjambe et le dit (« 1 écarté par la coupure »). **Le chrono du journal
   est du temps de jeu** : la durée de la partie se lit dessus, coupure exclue — et jusqu'à
   l'arrêt de la partie seulement, que le rapport donne en tête ; après, le journal court à
   l'horloge (la dernière tablette, l'effacement, la relecture).

### Ce que le journal répond seul — à lire, jamais à demander

- **La main** : la part manuelle des occurrences (au-delà de 40 %, plafonner `REL_K`), le
  nombre de recoupements (sous une vingtaine, le réglage du 09/09 a vidé un geste), et
  **après ⟨nous⟩, revient-on relever** — sur la copie du Corpus jumeau, et sur quelles
  tablettes (« · copie » dans le journal). C'est la question que PT10 a ouverte : cinquante
  minutes sans un geste dans le texte, de 36:46 à 86:34.
- **La composition** : chaque tentative, sa paire, sa minute et son issue (carnet, impayable,
  acquis). ⟨grenier⟩ et le zéro ont-ils été posés, et quand ; ⟨germer⟩ ou ⟨devenir-lecture⟩
  l'ont-ils été avant que le lexique les offre ?
- **Les lectures** : combien de fausses, et lesquelles — **en séparant celles du joueur de
  celles des Élèves** (le dépouillement les distingue). Pile ou face donnerait la moitié.
  Le degré de doute à chaque achat, et si le joueur a concordé un signe *avant* de le trancher.
- **Les Élèves** : combien, à quelle minute le premier, et avant ou après ⟨avant⟩ et ⟨ne-pas⟩.
- **Le doute et la contradiction** : le nombre de révisions et leurs signes (zéro voudrait dire
  que le panneau ne pointe rien, plus de cinq que le prix ne mord pas) ; la contradiction
  s'est-elle déclenchée, et **a-t-elle été levée par une révision** — en PT10, elle s'est
  déclenchée et le joueur n'a rien révisé.
- **L'acte IV** : la durée du repli de ⟨toi⟩ (relit-on, ou referme-t-on tout de suite ?) ; les
  conditions posées au panneau des questions, dans l'ordre et à leur minute ; la minute de la
  ligne `zeros` (premier nombre écrit avec leurs zéros) et celle de ⟨zéro⟩, s'il vient.
- **L'acte V** : à quelle minute le Lecteur est acheté, et combien de tablettes il a lues ; si
  le joueur est allé voir une tablette qu'il venait de marquer.
- **La fin** : combien de fois la fenêtre des deux fins s'est ouverte avant le choix, et
  combien de temps entre la première et le choix ; **achevée ou interrompue** ; le temps entre
  l'arrêt et l'effacement (règle 16) ; la relecture ouverte ou non, quand, et ce qu'elle a
  avoué.
- **Le rythme** : la durée, et chaque attente de plus de huit minutes sans déblocage (I4) —
  avec sa minute, pour la croiser avec la question 3.

---

## 3. Les questions, dans l'ordre

**L'ordre est la moitié du travail.** Chaque question enseigne quelque chose au joueur ; une
fois enseignée, elle contamine toutes les suivantes. On va donc de l'ouvert au précis, et les
dernières — celles qui révèlent — se posent à la fin, dans cet ordre-là.

Les questions 1 à 14 peuvent se poser par écrit. **Les questions 15 à 21 se posent de vive
voix**, et la 20 une seule fois.

### Premier tour — ouvert, ne rien nommer

1. **Raconte-moi la partie.**
   → *Laisser parler, ne pas relancer sur un mot précis. Ce qu'il nomme spontanément, et
   l'ordre dans lequel il le nomme, est la donnée.*
2. **Qu'est-ce que tu faisais, en fait ?** À quel moment tu l'as compris ?
3. **Y a-t-il eu un moment où tu as failli arrêter ?** Lequel, et qu'est-ce qui t'a fait
   continuer ?
   → *La dixième minute d'abord : c'est là que la partie 1 de PT5 s'est arrêtée (ECO-1), et
   c'est le seul défaut d'équilibrage connu qui ne soit pas réglé. Croiser avec le premier
   achat de Concordance dans le journal — 6,8′ au réglage actuel. Puis toute attente de plus
   de huit minutes que le journal date.*
   → *Et la coupure : **pourquoi là ?** Une pause prise juste après une révélation n'est pas
   celle prise dans un creux.*
4. **Est-ce que le texte raconte quelque chose ?** Quoi ?
   → *R4, et la remarque de PT3 : « la qualité de ce qui se découvre sera déterminante ».
   Question ouverte — ne surtout pas suggérer qu'il y a une histoire. Avec les cinq actes, elle
   porte aussi la révélation de l'acte V : la langue conçue pour qu'un inconnu la casse. Si
   elle remonte ici, c'est GRAINE-3 réussi sans qu'on ait rien demandé.*
5. **Y a-t-il eu un moment où tu as compris quelque chose que le jeu ne t'avait pas dit ?**
   → *La plus large du lot, et la seule qui puisse faire remonter la crue, les composés, les
   deux lectures, le texte adressé à ⟨toi⟩ ou les nombres du compteur sans qu'on les nomme. Si
   quelque chose remonte ici, c'est la meilleure réponse de tout le playtest.*
6. **Comment ça s'est terminé, pour toi ?**
   → *Ouverte, et seulement si le journal montre une fin. Laisser dire « j'ai arrêté » ou
   « ça s'est arrêté » : la différence est la donnée.*

### Deuxième tour — les mécaniques, sans dire ce qu'elles cachent

*Chacune ne se pose que si le journal dit que la chose a eu lieu.*

7. **Après la quarantième minute, tu faisais quoi ?**
   → *LA question ouverte par PT10. Le journal répond sur les gestes ; on veut savoir s'il a
   senti un vide, ou pas du tout. Ne pas demander « tu t'es ennuyé ? », qui souffle la
   réponse. Croiser avec les relevés sur la copie après ⟨nous⟩.*
8. **Le panneau où on assemble deux signes — tu t'en es servi ?** Qu'est-ce que tu attendais
   qu'il se passe ?
   → *Le seul retour qualitatif de PT10 portait là-dessus ; COMP-6 y a répondu par un intitulé.
   Ne pas demander « as-tu trouvé des signes » : ça dirait qu'il y en a.*
9. *(si un Élève a été acheté)* **L'Élève — qu'est-ce qu'il faisait, d'après toi ?**
   → *Ne rien dire de ce qu'il lit, ni qu'il peut se tromper (règle 21). Croiser avec le nombre
   d'Élèves et la minute du premier.*
10. *(si la contradiction s'est déclenchée)* **Le bandeau qui est apparu, tu l'as compris
    comment ?** Qu'est-ce que tu as fait ?
    → *Le point : sanction, ou panne ? S'il l'a lu comme un bug, c'est le texte du bandeau
    qu'on reprend, jamais le seuil. Et le journal dit s'il a révisé — ECO-3 a rendu la sanction
    supportable à qui ne révise pas, il ne lui a pas appris à réviser.*

    *(si `faux` a été acheté)* **Les lignes qui se sont allumées, tu en as fait quoi ?**
    → *Si elles n'ont servi à choisir aucune révision, la marque ne suffit pas — mais la
    réponse ne sera jamais de nommer le signe.*
11. *(si ⟨toi⟩ a été acheté)* **Quand le texte s'est replié, à cet achat-là — qu'est-ce que tu
    as fait ?**
    → *Relit-on, ou referme-t-on ? Le journal donne la durée ; on veut savoir s'il a lu
    « toi », et ce qu'il en a pensé.*
12. *(si le panneau des questions s'est ouvert)* **Qu'est-ce que tu y as demandé, et pourquoi
    ça ?**
    → *Après avoir lu les « si » du corpus, ou au hasard ? Le journal a les conditions et leur
    minute. Ne pas dire d'où viennent les réponses.*
13. *(si le Lecteur a été acheté)* **L'instrument qui n'avait pas de nom — qu'est-ce qu'il
    faisait ?**
    → *Ne pas le nommer, ne pas dire qu'il lit. A-t-il vu les tablettes se marquer, à quelle
    minute, et a-t-il lu son nom à la fin ? (Règle 28 : « on le voit lire ».)*
14. *(si la fenêtre des deux fins s'est ouverte)* **À la fin, qu'est-ce que tu as choisi, et
    pourquoi ?**
    → *Le journal dit lequel, et combien de fois la fenêtre s'est ouverte avant. S'il a
    achevé : **« le texte qui est resté seul à l'écran, tu en as fait quoi ? »** — les quarante
    secondes de `FIN_EFF` sont un choix de mise en scène, et c'est ici qu'elles se mesurent.*

### Troisième tour — celles qui révèlent

*De vive voix. À partir d'ici chaque question apprend quelque chose de définitif. Ne pas
remonter au tour précédent après les avoir posées.*

15. **Montrer ⟨grenier⟩, puis le zéro. « Qu'est-ce que tu vois là-dedans ? »**
    → *Reconnaît-il ⟨maison⟩ et ⟨grain⟩ dans l'un, ⟨ne-pas⟩ et ⟨un⟩ dans l'autre ? Le zéro est
    sous ses yeux depuis la première seconde. Règle 4 : le corpus dessine les composés comme
    composés, et c'est le seul indice du jeu. Montrer le tracé, ne pas le nommer.*
    → *S'il les a posés à la grille, la question devient « comment tu les as trouvés ? ».*
16. *(si la ligne `zeros` est au journal)* **« Vers la fin, tes nombres en haut ont changé
    d'écriture. Tu en as fait quoi ? »** Puis, seulement s'il les a relus : « comment ? »
    → **Après la 15, jamais avant** : elle désigne le tracé du zéro dans les compteurs, ce qui
    est exactement ce que la 15 mesure. Posée avant, elle lui donne sa réponse.
    → *Règle 30. Les a-t-il relus en les regardant monter, comme le compteur de l'acte I, ou
    les a-t-il ignorés ? Et s'il a composé ⟨zéro⟩ ensuite, était-ce pour ça ? Croiser avec la
    minute de `zeros` et celle de ⟨zéro⟩.*
17. **Montrer `les-lecteurs`. « Et là ? »**
    → *Le nom se dessine ⟨lire⟩ sur ⟨nous⟩, et ⟨nous⟩ se tient seul juste devant lui, sur la
    même ligne — 41 fois dans le corpus. Dans cette branche, ⟨nous⟩ s'achète ensuite : la
    question est s'il l'avait vu dans le nom **avant** que l'acte IV le lui donne. La ligne de
    journal de l'achat le dit déjà (« la moitié du nom est un signe que je ne sais pas lire ») :
    l'a-t-il lue, et est-il allé voir ?*
18. **« Au tout début, avant ton premier achat, les compteurs en haut montaient en signes.
    Tu en as fait quoi ? »**
    → *Ne pas demander « tu les as lus ? », qui souffle qu'il y avait quelque chose à lire.
    Laisser venir, puis, seulement s'il a lu : « jusqu'où ? »*
    → **Après la 15, jamais avant**, pour la même raison que la 16 : elle apprend à regarder
    les signes de nombre comme des composés.
    → *Le point : ⟨un⟩ coûte 2 C et fait passer les trois compteurs en chiffres arabes d'un
    bloc. Le design doc §10 appelle le décodage du compteur « le premier plaisir du jeu ». La
    conversion est-elle reçue comme une récompense, ou comme une énigme qu'on vient de perdre ?
    Croiser avec la minute du premier achat, et si c'est ⟨un⟩. Rien n'est à régler avant cette
    réponse : issue [#57](https://github.com/DavidGiangiacomo/langue-morte/issues/57).*
    → *Elle se double maintenant de la 16 : le jeu rend le même plaisir à l'acte IV, à
    l'envers. Les deux réponses se lisent ensemble.*
19. *(si l'acte V a été atteint)* **Montrer la tablette 28, puis la 21. « Celles-là, qu'est-ce
    qu'elles disent ? »** Puis : **« Et l'ordre, dans la 28 — ça te rappelle quelque chose ? »**
    → *GRAINE-3, la révélation : la tablette 28 donne au programme l'ordre des branches de
    l'arbre qu'il suit depuis trois heures, la 21 est l'abécédaire. Ne pas dire « l'arbre », ne
    pas dire « le lexique ». S'il le voit seul, la révélation tient sans rien de plus ; sinon,
    c'est elle qu'il faut reprendre, et c'est le seul récit de l'acte V qui reste à écrire.*
    → *S'il a ouvert la relecture, elle lui a montré ces tablettes en entier : demander s'il
    l'avait vu **avant**.*
20. **« Tu as remarqué que tu choisissais ? »**
    → **Une seule fois, et jamais avant.** Onze signes proposent deux lectures au moment de
    payer, à prix, tracé et ligne d'effet identiques. Une fois posée, ce joueur ne peut plus
    jamais servir à le mesurer.
    → **Si le journal montre la relecture avant l'entretien**, elle a déjà répondu : la
    question devient **« pendant la partie, avant la fin, tu l'avais remarqué ? »**, et la
    réponse vaut moins — c'est le prix, accepté, de ne rien dire de la fin.
    → *Croiser avec le nombre de lectures fausses du joueur seul (les Élèves à part). PT10 :
    trois sur neuf, compatible avec le hasard, mais c'est l'auteur qui jouait.*
21. *(si un Élève a tranché au moins un signe)* **« Et un mot faux, d'après toi, qui l'avait
    lu ? »**
    → *À lui, ou à l'Élève ? La ligne « Un élève l'avait déjà recopié au propre » dit qui a lu,
    jamais quoi (règle 21). Après la 20 seulement : elle présuppose qu'il y a eu des mots faux.*
    → *Si la relecture a eu lieu, son survol le lui a dit (« un élève avait lu … ») : demander
    plutôt si ça l'a surpris.*

---

## 4. Ce qu'on ne dit à aucun moment

- Qu'il s'agit de déchiffrer. Le jeu le montre ou ne le montre pas ; c'est la mesure.
- Qu'on peut assembler des signes, et qu'il en existe hors de l'arbre.
- Qu'un signe puisse avoir deux lectures, ou qu'on ait pu se tromper — et que l'Élève, lui,
  se trompe.
- Qu'il existe un relevé, un recoupement, une concordance — les trois gestes du corpus se
  trouvent ou ne se trouvent pas.
- Que les nombres du compteur se lisaient avant ⟨un⟩, et qu'on pouvait les décoder seul ; que
  ⟨zéro⟩ rend les grands nombres.
- D'où viennent les réponses aux questions, et ce qu'elles ouvrent.
- Que l'instrument sans nom lit, et ce que son nom veut dire.
- Qu'il y a une fin, qu'il y en a deux, et à quelle minute elle tombe ; qu'il y a quelque
  chose après.
- Combien de joueurs sont passés avant, et ce qu'ils ont fait.

---

## 5. Pendant PT11 : rien ne va sur `develop`

Le workflow Pages déploie **à chaque poussée sur `develop`**. Une partie en cours change donc
de jeu au rechargement suivant — et celle-ci se joue en deux séances, donc **au moins un
rechargement est prévu**. LIV-3 n'y change rien : la sauvegarde porte sa version et se migre,
mais une version protège le format d'une partie, pas son économie.

La branche a été fusionnée sur `develop` le 20/10/2026 **pour être déployée**, et pour rien
d'autre. À partir de l'envoi du message, la parade est un usage, et un usage n'est gardé par
rien : travailler sur branche, ne pas fusionner avant le retour du journal et l'entretien.
