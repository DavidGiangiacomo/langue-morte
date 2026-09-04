# -*- coding: utf-8 -*-
"""Génère src/corpus.js à partir des 30 tablettes.\n\nLe contenu éditorial de référence est dans docs/corpus.md : ce fichier en est la\ntranscription exécutable. Toute modification du texte se fait ICI, puis on relance\n`python outils/corpus.py`, puis `python build.py`.\n"""
import json, re

MOT = {
 'un':'an','deux':'anna','dix':'sela','vingt':'selanna','cent':'meku','zéro':'lan',
 'grain':'tem','eau':'kish','champ':'gan','maison':'ur','grenier':'urtem','tablette':'tab',
 'dire':'im','dis':'im','graver':'sar','grave':'sar','gravait':'sar','copier':'kal','copie':'kal',
 'lire':'shen','lis':'shen','lisait':'shen','scribe':'imme','archive':'tabsar','les-lecteurs':'shenu',
 'année':'nur','avant':'pat','après':'zur','siècle':'nurnur','nuit':'esh','dernière-année':'nurhal',
 'ne-pas':'la','si':'en','il-faut':'dun','peut-être':'mik','faux':'lash','sinon':'enla',
 'je':'mu','toi':'ta','nous':'nash','toi-qui':'taru','moi-absent':'mula','nous-fûmes':'nashal',
 'finit':'hal','finir':'hal','semence':'mesh','devenir':'ke','deviens':'ke','devient':'ke',
 'le-dernier':'halan','germer':'meshke','notre-fin':'halnash','devenir-lecture':'shenke',
 'N1':'nm1','N2':'nm2','N3':'nm3','N4':'nm4','N5':'nm5','N6':'nm6',
}

def L(s):
    out=[]
    for tk in s.split():
        if tk=='·': out.append('·')
        elif re.fullmatch(r'\d+', tk): out.append('%'+tk)
        elif tk==':': out.append('·')
        else:
            if tk not in MOT: raise KeyError(tk)
            out.append(MOT[tk])
    return ' '.join(out)

def maisons(n, q, vides=0):
    """Registre de distribution. Salé de mots de modalité, de temps et de personne :
    un vrai registre est plein de « si », « ne-pas », « il-faut ». C'est ce qui empêche
    la masse répétitive d'être intégralement déchiffrable dès l'acte II."""
    out=[]
    for i in range(1, n+1):
        if i > n-vides:      out.append(L(f'maison {i} · ne-pas · grenier ne-pas · avant · année ne-pas'))
        elif i % 7 == 0:     out.append(L(f'maison {i} · grain {q} · si semence · il-faut ne-pas · après'))
        elif i % 5 == 0:     out.append(L(f'maison {i} · grain {q} · scribe · nuit · il-faut graver'))
        elif i % 3 == 0:     out.append(L(f'maison {i} · grain {q} · avant · année ne-pas · si lire'))
        elif i % 4 == 1:     out.append(L(f'maison {i} · grain {q} · après · nous · il-faut'))
        else:                out.append(L(f'maison {i} · grain {q} · si ne-pas · sinon'))
    return out

def veille(annee, serie):
    """Le relevé d'eau tenu d'année en année — le document le plus lourd en vocabulaire
    d'acte III (avant, après, année, ne-pas, peut-être). C'est lui qui porte le déclin."""
    out=[L(f'année {annee} · eau {serie[-1][1]}')]
    for an, e in reversed(serie[:-1]):
        out.append(L(f'avant · année {an} · eau {e} · si ne-pas · sinon'))
    out += [L('il-faut lire · eau'), L('peut-être eau · peut-être ne-pas'), L('après · il-faut lire')]
    return out

def archive(a, b, step=1):
    out=[]
    for k in range(a, b+1, 4*step):
        grp=[str(i) for i in range(k, min(k+4, b+1))]
        out.append(L('tablette '+' · tablette '.join(grp)))
        if (k//(4*step)) % 3 == 0:  out.append(L('il-faut copier · si ne-pas · sinon'))
        if (k//(4*step)) % 4 == 2:  out.append(L('nuit · copier · après'))
    return out

def champs(vals):  return [L(f'champ {i+1} · grain {v}') for i,v in enumerate(vals)]

def consignes(k):
    """Le protocole de copie, répété tel quel de tablette en tablette."""
    base=[L('il-faut copier tablette'), L(f'copier {k}'), L('si copier · ne-pas faux'),
          L('si faux · il-faut ne-pas'), L('nuit · il-faut graver'), L('après · il-faut lire')]
    return base

EAU=[(9, 14), (12, 13), (19, 15), (27, 12), (40, 13), (54, 11), (71, 12), (88, 10), (103, 9), (112, 10), (126, 8), (139, 7), (150, 8), (164, 6), (177, 5), (183, 6), (195, 4), (201, 3), (207, 2), (209, 2), (211, 1), (213, 1)]

T=[]
def tab(n, lines): T.append({'t':n,'l':lines})

# ---------------- ACTE I ----------------
tab(1,[L('tablette 1 · année 9')]+champs([212,198,140,206])+[L('grain 756'),L('eau 14'),L('maison 31')])
tab(2,[L('tablette 2 · année 12')]+champs([205,191,138,208])+[L('grain 742'),L('eau 13'),L('maison 31')])
tab(3,[L('tablette 3 · année 19')]+champs([224,210,152,215])+[L('grain 801'),L('eau 15'),L('maison 33')])
tab(4,[L('tablette 4 · année 27')]+champs([190,176,130,194])+[L('grain 690'),L('eau 12'),L('maison 30'),
      L('grenier 1 · grain 690'),L('scribe N3')])
# ---------------- ACTE II ----------------
tab(5,[L('tablette 5 · année 40'),L('grenier 1 · grain 705')]+maisons(31,20)+
      [L('grain 620'),L('grenier 1 · grain 85'),L('semence 60'),L('grain 25'),L('scribe N3')])
tab(6,[L('tablette 6 · année 40')]+veille(40,[e for e in EAU if e[0]<=40])+[L('scribe N3')])
tab(7,[L('tablette 7 · année 54')]+champs([180,168,124,176])+[L('grain 648'),L('eau 11'),L('maison 29')]+
      maisons(29,20)+[L('grain 580'),L('grenier 1 · grain 62')])
tab(8,[L('tablette 8 · année 54'),L('archive 1')]+archive(1,24)+consignes(2)+[L('scribe N3')])
tab(9,[L('tablette 9 · année 71')]+champs([184,171,126,180])+[L('grain 661'),L('eau 12'),L('maison 30')]+
      maisons(30,20)+[L('grain 600'),L('grenier 1 · grain 1')])
tab(10,[L('tablette 10 · année 88')]+champs([165,153,112,160])+[L('grain 590'),L('eau 10'),L('maison 27'),
       L('semence 60')]+maisons(27,20)+[L('grenier 1 · grain 0')])
tab(11,[L('tablette 11 · année 88'),L('scribe N3 finit'),L('archive 1 · tablette 11'),
       ]+consignes(2)+[L('scribe N4')])
# ---------------- ACTE III ----------------
tab(12,[L('tablette 12 · année 103')]+champs([146,135,99,142])+[L('grain 522'),L('eau 9'),L('maison 24'),
       L('semence 80')]+maisons(24,20,1)+[L('grenier 1 · grain 12')])
tab(13,[L('tablette 13 · année 112')]+champs([153,142,104,149])+[L('grain 548'),L('eau 10'),L('maison 25'),
       L('après · année 103 · grain 522'),L('après · année 112 · grain 548'),L('peut-être eau')]+
       maisons(25,20,1)+[L('scribe N4')])
tab(14,[L('tablette 14 · année 126'),L('grain 470'),L('eau 8'),L('maison 22'),L('semence 100'),
        L('grenier 1 · grain 0')]+maisons(22,20,2)+
       [L('grain 440'),L('grain 30')]+consignes(10))
tab(15,[L('tablette 15 · année 139'),L('grain 401'),L('maison 19'),L('siècle 1 · après'),
        L('avant · siècle 1 · eau 14')]+veille(139,[e for e in EAU if e[0]<=139])+
       [L('il-faut lire · grain'),L('scribe N4')])
tab(16,[L('tablette 16 · année 150'),L('archive 1 · tablette 300')]+archive(1,96)+consignes(10)+
       [L('maison 17 · scribe 6'),L('grain 418'),L('eau 8')])
tab(17,[L('tablette 17 · année 150'),L('tablette · si copier · il-faut'),L('tablette · si ne-pas copier · sinon'),
        L('grain · ne-pas tablette'),L('eau · ne-pas tablette'),L('il-faut tablette · lire'),
        L('il-faut tablette · devenir lire'),L('scribe N4')])
tab(18,[L('tablette 18 · année 164'),L('grain 352'),L('eau 6'),L('maison 17'),L('nous · les-lecteurs'),
        L('avant · nous · les-lecteurs'),L('après · nous · les-lecteurs'),L('si ne-pas lire · nous ne-pas'),
        L('scribe N4')])
tab(19,[L('tablette 19 · année 177')]+champs([80,74,54,79])+[L('grain 287'),L('eau 5'),L('maison 14'),
       ]+maisons(14,20,2)+[L('scribe N4 finit'),L('scribe N5')])
# ---------------- ACTE IV ----------------
tab(20,[L('tablette 20 · année 183'),L('grain 301'),L('eau 6'),L('maison 15')]+maisons(15,20,2)+
       [L('toi · lis'),L('toi-qui lis · toi'),L('je grave · toi lis'),L('peut-être toi'),L('scribe N5')])
tab(21,[L('tablette 21 · année 183'),L('il-faut graver · un'),L('il-faut graver · un · deux · un'),
        L('il-faut graver · dix'),L('tablette 1 · tablette 1 · tablette 1'),L('si lire un · après lire deux'),
        L('il-faut · faux ne-pas'),L('scribe N5')])
tab(22,[L('tablette 22 · année 195'),L('grain 224'),L('eau 4'),L('maison 11'),L('semence 100'),
        L('grain ne-pas')]+maisons(11,15,3)+
       [L('si semence · ne-pas germer'),L('si tablette · germer'),L('scribe N5')])
tab(23,[L('tablette 23 · année 201'),L('grain 166'),L('eau 3'),L('maison 9 · scribe 5'),
        L('archive 1 · tablette 900')]+archive(1,120,2)+maisons(9,15)+consignes(100)+
       [L('si copier 100 · un devenir'),L('scribe N5')])
tab(24,[L('tablette 24 · année 201'),L('toi-qui lis · toi ne-pas nous'),L('toi-qui lis · toi après'),
        L('si toi lis · nous ne-pas finir'),L('si toi ne-pas lis · nous finir'),L('il-faut toi'),L('scribe N5')])
tab(25,[L('tablette 25 · année 207'),L('grain 110'),L('eau 2'),L('maison 6')]+maisons(6,10,3)+
       [L('champ 1 · ne-pas'),L('champ 2 · ne-pas'),L('champ 3 · grain 21'),L('champ 4 · ne-pas'),
        L('grenier 1 · ne-pas'),L('scribe N5')])
tab(26,[L('tablette 26 · année 209'),L('grain 98'),L('maison 5')]+veille(209,EAU)+
       [L('avant · tablette 6 · faux'),
        L('avant · tablette 13 · faux'),L('peut-être eau · faux'),L('je grave : faux'),
        L('il-faut faux ne-pas'),L('scribe N5')])
# ---------------- ACTE V ----------------
tab(27,[L('tablette 27 · année 211'),L('grain 54'),L('eau 1'),L('maison 3'),L('semence · ne-pas grain'),
        L('semence · tablette'),L('tablette · devenir-lecture'),L('si tablette lire · tablette germer'),
        L('nous · semence'),L('scribe N5')])
tab(28,[L('tablette 28 · année 213'),L('grain 29'),L('eau 1'),L('maison 2'),L('nous graver · tablette'),
        L('nous graver · tablette · si lire · devenir'),L('un · deux · dix · cent · zéro'),
        L('grain · eau · champ · maison'),L('lire · graver · copier'),L('si toi lis un · toi lis grain'),
        L('si toi lis grain · toi lis nous'),L('il-faut tablette · si un · après deux'),
        L('peut-être toi · après siècle'),L('scribe N5')])
tab(29,[L('tablette 29 · dernière-année'),L('champ 1 · 0'),L('champ 2 · 0'),L('champ 3 · 0'),L('champ 4 · 0'),
        L('grain 0'),L('eau 0'),L('maison 0'),L('grenier 0'),L('semence 0')]+archive(1,160,2)+
       [L('archive 1 · tablette 1200'),L('scribe 1')])
tab(30,[L('tablette 30 · dernière-année'),L('je grave · le-dernier'),L('scribe N5'),L('N6 lisait'),
        L('N6 lisait · nuit'),L('je ne-pas dire N6 · dire finit'),
        L('je grave N6 · graver ne-pas finit'),L('notre-fin · ne-pas'),L('toi-qui lis · toi devenir'),
        L('nous-fûmes')])

# ---- statistiques ----
MVP = {'an','anna','sela','meku','tem','ur','tab','kish','gan','im','sar','kal'}
tot=lis=0; lines=0
for t in T:
    for ln in t['l']:
        lines+=1
        for tk in ln.split():
            if tk=='·': continue
            tot+=1
            if tk.startswith('%') or tk in MVP: lis+=1
print(f"{len(T)} tablettes · {lines} lignes · {tot} signes · lisibles au MVP : {lis} ({100*lis/tot:.0f} %)")

EN_TETE = ('/* GÉNÉRÉ — ne pas éditer à la main.\n'
           '   Source : docs/corpus.md → outils/corpus.py → ce fichier.\n'
           '   Régénérer avec : python outils/corpus.py */\n\n"use strict";\n\n')
ORDRE = ("\n/* Ordre de sortie de terre — pas l'ordre chronologique. La tablette 21 (l'abécédaire)\n"
         "   arrive 7e et ne sera comprise qu'à l'acte IV ; la 29 (le registre de zéros) arrive\n"
         "   avant la 28 qui l'explique. Voir docs/corpus.md §8. */\n"
         "const ORDRE = [1,2,3,4,8,5,21,7,6,11,9,16,10,12,17,13,15,22,14,18,19,25,20,23,26,24,27,29,28,30];\n"
         "const TB = ORDRE.map(n => CORPUS.find(t => t.t === n));\n")
js = EN_TETE + 'const CORPUS=' + json.dumps(T, ensure_ascii=False, separators=(',',':')) + ';\n' + ORDRE
open(str(__import__('pathlib').Path(__file__).parent.parent/'src'/'corpus.js'),'w').write(js)
print('src/corpus.js :', len(js)//1024, 'Ko')
