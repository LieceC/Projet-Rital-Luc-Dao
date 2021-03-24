#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 18:48:36 2021

@author: dao
"""
import sys
sys.path.insert(1,"..")
import utils.collection as c
import utils.TextRepresenter as tr
import utils.weighters as w
import utils.modeles as mod
import utils.metrique as metr
from utils.metrique import EvalIRModel

def pretraitement_requete(q):
    ps = tr.PorterStemmer()
    return ps.getTextRepresentation(q)

base = "cisi" # cacm
col0 = c.Parser.parse("./data/"+base+"/"+base+".txt")
col1 = c.QueryParser.parse("./data/"+base+"/"+base+".qry", 
                           "./data/"+base+"/"+base+".rel")

index = c.IndexerSimple(col0)

'''
Modeles
'''

weighter = w.Weighter1(index)
# weighter = w.Weighter2(index)
# weighter = w.Weighter3(index)
# weighter = w.Weighter4(index)
# weighter = w.Weighter5(index)
model_V = mod.Vectoriel(index,weighter,True)
model_O = mod.Okapi(index)
model_L = mod.ModeleLangue(index)

modele_test = model_V
'''
Metriques à tester
'''
# on peut aussi tester par rapport au nombre de pertinents avec 0
rank_test = 5

fs = [ # [ metr.Précision,[rank_test]], 
       # [metr.NDCG,None],
       # [metr.Précision_moyenne,None],
       # [metr.Rappel,[rank_test]],
       # [metr.reciprocal_rank,None],
       # [metr.F_mesure,[rank_test, 0.5]] 
       ]

for mesure,args in fs:
    print(mesure.__name__)
    print(EvalIRModel.eval(mesure,modele_test,col1,args))

'''
Graphe interpolée
# metr.EvalIRModel.precision_interpolée_graph(model_V,col1,5)
'''

first_model = model_V
second_model = model_L 
param = [5]

# print(EvalIRModel.significativité(95,metr.Précision_moyenne,first_model,second_model,col1,param))