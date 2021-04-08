#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:10:57 2021

@author: dao
"""
import sys
sys.path.insert(1,"..")
import utils.collection as c
import utils.TextRepresenter as tr
import utils.weighters as w
import utils.modeles as m

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

base = "cisi" # cacm
col0 = c.Parser.parse("./data/"+base+"/"+base+".txt")
col1 = c.QueryParser.parse("./data/"+base+"/"+base+".qry", None)


index = c.IndexerSimple(col0)

test_query = '1'

print("query : ", col1[test_query].text)
q = pretraitement_requete(col1[test_query].text)

print("-------------------------")
print("modele Vectoriel, Weighter1 : ")
weighter = w.Weighter1(index)
model_V = m.Vectoriel(index,weighter,False)
ranking = model_V.getRanking(q)
print("meilleurs score :", ranking[0][1])
print("contenu de l'article:")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Vectoriel, Weighter2 : ")
weighter = w.Weighter2(index)
model_V = m.Vectoriel(index,weighter,False)
ranking = model_V.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Vectoriel, Weighter3 : ")
weighter = w.Weighter3(index)
model_V = m.Vectoriel(index,weighter,False)
ranking = model_V.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Vectoriel, Weighter4 : ")
weighter = w.Weighter4(index)
model_V = m.Vectoriel(index,weighter,False)
ranking = model_V.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Vectoriel, Weighter5 : ")
weighter = w.Weighter5(index)
model_V = m.Vectoriel(index,weighter,False)
ranking = model_V.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Langue : ")
model_L = m.ModeleLangue(index)
ranking = model_L.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)

print("-------------------------")
print("modele Okapi : ")
model_O = m.Okapi(index)
ranking = model_O.getRanking(q)
print("meilleurs score", ranking[0][1])
print("contenu : ")
print(col0[ranking[0][0]].text)
