#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:48:36 2021

@author: dao
"""
import sys
sys.path.insert(1,"..")
import sklearn.model_selection as ms
import utils.collection as c
import utils.TextRepresenter as tr
import utils.weighters as w
import utils.modeles as m
import numpy as np
import utils.metrique as me

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

col0 = c.Parser.parse("../data/cisi/cisi.txt")
col1 = c.QueryParser.parse("../data/cisi/cisi.qry", "../data/cisi/cisi.rel")

index = c.IndexerSimple(col0)

#index = IndexerSimple(col0)
weighter = w.Weighter1(index)

model_V = m.Vectoriel(index,weighter,True)
fs = [ #[ me.Précision,[5]], 
       # [me.NDCG,None],\
       # [me.Précision_moyenne,None],
       # [me.Rappel,[5]],
       # [me.reciprocal_rank,None],
       # [me.F_mesure,[5, 0.5]]
       ]
for mesure,args in fs:
    print(mesure.__name__)
    print(me.EvalIRModel.eval(mesure,model_V,col1,args))

# me.EvalIRModel.precision_interpolée_graph(model_V,col1)

"""

import re
file = "data/cisi/cisi.txt"
dico = dict()
text = open(file, "r").read()

I = r"\.I (.*)\n"
T = r"(\.T\s*(([^.].*\n+)*))?"
B = r"(\.B\s*(([^.].*\n+)*))?"
A = r"((\.A\s*(([^.].*\n+)*))*)"
K = r"(\.K\s*(([^.].*\n+)*))?"
W = r"(\.W\s*(([^.].*\n+)*))?"
X = r"(\.X\s*(([^.].*\n+)*))?"

res = re.findall(I+T+A+B+K+W+X,text,re.MULTILINE)


model_O = m.Okapi(index, k1 = 1.2, b = 0.75)


for id_doc in index.getIds():
    if index.getDocSize(id_doc) == 0:
        print(id_doc)

# indices du  train et du test
base = list(col1.items())
train, test = ms.train_test_split(base ,test_size = 0.2)

ret = []
X = np.arange(0, 1, 0.1)
for i in X:
    model_L = m.ModeleLangue(index, _lambda = i)
    sc = 0
    for _, q in train:
        q = pretraitement_requete(q.text)
        print(q)
        tmp = model_L.getScores(q)
        print(tmp)
        sc += tmp
            
    
    ret += sc
"""