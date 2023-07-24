import spacy
import csv
import re
import itertools
import functools
import sys
# no xcomp in spacy, so it's easier doing it like this
import spacy_udpipe

spacy_udpipe.download("en")

x = sys.argv[1]
file = x + ".md"

with open(file) as f:
    t = f.read()
    # print(t)

txt = " ".join(filter(None, t.replace("//", "").replace("/n", "").split(",")))

# print(txt)

nlp = spacy_udpipe.load("en")
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
    "X": "X",
    "INTJ": "Interj",
    "SYM": "PUNCT",
}


def getBasic(t):
    lem = t.lemma_
    pos = posDict[t.pos_]
    word = lem + "_" + pos + " = " + "mk" + pos + ' "' + lem + '"'
    return word

def getVerb(t, v):
    word = t.lemma_ + "_" + v + " = " + "mk" + v + ' (mkV "' + t.lemma_ + '")'
    return word

def getCmpnd(t1, t2):
    lem = t1.lemma_ + "_" + t2.lemma_
    pos = posDict[t2.pos_]
    word = lem + "_" + pos + " = " + "mk" + pos + ' "' + lem + '"'
    return word

def getHyph(t0, t1, t2):
    lem = t0.lemma_ + t1.lemma_ + t2.lemma_
    pos = posDict[t2.pos_]
    word = lem + "_" + pos + " = " + "mk" + pos + ' "' + lem + '"'
    return word

tok = enumerate(doc)

def checkSubChild(dep, ls):
    return any(child[2] == dep for child in ls)

def checkWhichVerb(t):
    childList = [[child.lemma_, child.pos_, child.dep_] for child in t.children]
    print(t.lemma_, childList)
    # dobj is obj in the spacy-udpipe
    if checkSubChild("obj", childList):
        if checkSubChild("iobj", childList):
            words.append(getVerb(t, "V3"))
        else:
            words.append(getVerb(t, "V2"))
    # also for adjectival complement
    # https://universaldependencies.org/fi/dep/xcomp.html
    elif checkSubChild("xcomp", childList):
        for child in childList:
            if child[1] == "ADJ":
                word = child[0] + "_VA = " + "mkVA" + ' (mkV "' + child[0] + '")'
                words.append(word)
            elif child[1] == "VERB":
                word = child[0] + "_VV = " + "mkVV" + ' (mkV "' + child[0] + '")'
                words.append(word)
    elif checkSubChild("ccomp", childList):
        words.append(getVerb(t, "VS"))
    else:
        getBasic(t)

def hasChild(t):
    return any(True for _ in t.children)


for i, t in tok:
    print(t, " :", t.lemma_, t.pos_, t.morph, t.dep_, t.head, hasChild(t))
    if t.dep_ == "compound":
        if doc[i + 1].lemma_ == " ":
            words.append(getBasic(doc[i]))
        elif doc[i+1].lemma_ == "-":
            words.append(getHyph(doc[i], doc[i+1], doc[i+2]))
        else:
            words.append(getCmpnd(doc[i], doc[i + 1]))
        next(tok)
    elif t.lemma_ == "-" and t.pos_ == "ADJ":
        words.append(getHyph(doc[i - 1], doc[i], doc[i + 1]))
        next(tok)
    elif t.pos_ == "VERB" and hasChild(t):
        checkWhichVerb(t)
    elif t.pos_ == "PART":
        if t.dep_ == "neg" or t.dep_ == "pos":
            pass
        elif t.dep_ == "aux":
            words.append(getBasic(doc[i + 1]))
            next(tok)
        else:
            pass
            # print(t.lemma_, t.pos_, t.tag_, t.morph, t.dep_)
    elif (
        t.pos_ == "AUX"
        or t.pos_ == "PUNCT"
        or t.pos_ == "DET"
        or posDict[t.pos_] == "Conj"
        or t.pos_ == "ADP"
        or t.pos_ == "SPACE"
        or t.pos_ == "NUM"
        or t.pos_ == "X"
    ):
        pass

    else:
        # print("word :", getBasic(doc[i]))
        words.append(getBasic(doc[i]))

lex = open(x, "w")
lex.write("lin")
lex.write("\n")
for w in words:
    lex.write("  ")
    lex.write(w)
    lex.write("\n")
