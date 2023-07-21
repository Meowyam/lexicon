import spacy
import csv
import re
import itertools
import functools

x = input()
file = x + ".md"

with open(file) as f:
    t = f.read()
    print(t)

txt = " ".join(filter(None, t.replace("//", "").replace("/n", "").split(",")))

print(txt)

nlp = spacy.load("en_core_web_sm")
doc = nlp(txt)

words = []

lexicalCats = "N V A N2 N3 V2 A2 VA V2V VV V3 VS V2A V2S V2Q Adv AdV AdA AdN ACard CAdv Conj Interj PN Prep Pron Quant Det Card Text Predet Subj"

posDict = {
    "NOUN": "N",
    "VERB": "V",
    "AUX": "AUX",
    "ADJ": "A",
    "ADV": "Adv",
    "DET": "Det",
    "PRON": "Pron",
    "CCONJ": "Conj",
    "SCONJ": "Conj",
    "PART": "PART",
    "PUNCT": "PUNCT",
    "ADP": "Prep",
    "PROPN": "PN",
    "SPACE": "",
    "NUM": "Num",
}


def getBasic(t):
    lem = t.lemma_
    pos = posDict[t.pos_]
    word = lem + "_" + pos + " = " + "mk" + pos + ' "' + lem + '"'
    return word


def getCmpnd(t1, t2):
    lem = t1.lemma_ + "_" + t2.lemma_
    pos = posDict[t2.pos_]
    word = lem + "_" + pos + " = " + "mk" + pos + ' "' + lem + '"'
    return word


tok = enumerate(doc)

for i, t in tok:
    print(t, " :", t.lemma_, t.pos_, t.morph, t.dep_)
    if t.dep_ == "compound":
        words.append(getCmpnd(doc[i], doc[i + 1]))
        next(tok)
    elif t.pos_ == "PART":
        if t.dep_ == "neg" or t.dep_ == "pos":
            pass
        elif t.dep_ == "aux":
            words.append(getBasic(doc[i + 1]))
            next(tok)
        else:
            print(t.lemma_, t.pos_, t.tag_, t.morph, t.dep_)
    elif (
        t.pos_ == "AUX"
        or t.pos_ == "PUNCT"
        or t.pos_ == "DET"
        or posDict[t.pos_] == "Conj"
        or t.pos_ == "ADP"
        or t.pos_ == "SPACE"
    ):
        pass
    else:
        print("word :", getBasic(doc[i]))
        words.append(getBasic(doc[i]))

lex = open(x, "w")
lex.write("lin")
lex.write("\n")
for w in words:
    lex.write("  ")
    lex.write(w)
    lex.write("\n")
