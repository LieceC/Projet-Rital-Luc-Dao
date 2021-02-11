#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 15:10:57 2021

@author: dao
"""

import collection as c
import utils.TextRepresenter as tr
import weighters as w
import modeles as m

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

col1 = c.Parser.parse("data/cacm/cacm.qry")
index = c.IndexerSimple(col1)
q = "Algorithm Comparison" # j'ai aussi test avec des mots qui n'apparaissent pas
q = pretraitement_requete(q)

weighter = w.Weighter1(index)

model = m.Vectoriel(index,weighter,True)
# print(model.getScores(q))
print(model.getRanking(q))

model = m.ModeleLangue(index)
# print(model.getScores(q))
print(model.getRanking(q))

model = m.Okapi(index)
# print(model.getScores(q))
print(model.getRanking(q))
