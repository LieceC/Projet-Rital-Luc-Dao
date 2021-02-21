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
import utils.modeles as mod
import utils.metrique as metr
from utils.metrique import EvalIRModel

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

col0 = c.Parser.parse("./data/cisi/cisi.txt")
col1 = c.QueryParser.parse("./data/cisi/cisi.qry", "./data/cisi/cisi.rel")

index = c.IndexerSimple(col0)
#index = IndexerSimple(col0)
weighter = w.Weighter1(index)

model_V = mod.Vectoriel(index,weighter,True)

model_L = mod.ModeleLangue(index)




fs = [ [ metr.Précision,[5]], 
       # [metr.NDCG,None],\
       # [metr.Précision_moyenne,None],
       # [metr.Rappel,[5]],
       # [metr.reciprocal_rank,None],
       # [metr.F_mesure,[5, 0.5]]
       ]

    
"""
for mesure,args in fs:
    print(mesure.__name__)
    print(EvalIRModel.eval(mesure,model_V,col1,args))
"""
# me.EvalIRModel.precision_interpolée_graph(model_V,col1)
print(EvalIRModel.significativité(95,metr.Précision,model_V,model_V,col1,[5]))