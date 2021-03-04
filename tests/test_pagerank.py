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
import utils.pagerank as pr
import numpy as np

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

base = "cisi" # cacm
col0 = c.Parser.parse("../data/"+base+"/"+base+".txt")
col1 = c.QueryParser.parse("../data/"+base+"/"+base+".qry", None)


index = c.IndexerSimple(col0)

q = pretraitement_requete(col1['16'].text)

weighter = w.Weighter1(index)

model_V = m.Vectoriel(index,weighter,False)


V, S = pr.sous_graph(model_V, q, 10, 5)

"""
cpt = np.zeros(len(list(V)))
for j in range(len(list(V))):
    In = model_V.index.getHyperlinksTo(list(V)[j])
    if len(In) != 0:
        In = np.array(list(In.items()))
        In = In[np.isin(In[:,0], list(V))]c
        cpt[j] = len(In)
        
        
"""
rank = pr.page_ranking(model_V, V, 0.85, 100, epsilon = 1e-3)