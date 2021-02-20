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
import utils.modeles as m
from utils.collection import IndexerSimple
from utils.metrique import Précision_moyenne, EvalIRModel
import numpy as np
import matplotlib.pyplot as plt


col0 = c.Parser.parse("../data/cisi/cisi.txt")
col1 = c.QueryParser.parse("../data/cisi/cisi.qry","../data/cisi/cisi.rel")
index_txt = IndexerSimple(col0)

def gridsearch(coltext,index_txt,colquery,model,
               nb_parameters = 1, range_1 = np.arange(0, 1.1, 0.1), range_2 = np.arange(0, 1.1, 0.1)
               ,plot = False):

    train, test = ms.train_test_split(list(colquery.keys()) ,test_size = 0.2)
    train = {x:colquery[x] for x in train}
    test = {x:colquery[x] for x in test}
    
    ret = np.zeros(len(range_1)) if nb_parameters == 1 else np.zeros((len(range_1),len(range_2)))
    for idd,i in enumerate(range_1):
        if nb_parameters == 1:
            model_L = model(index_txt, i)
            ret[idd] = EvalIRModel.eval(Précision_moyenne,model_L,train)[0]
        else:
            for idd2,j in enumerate(range_2):
                 print(idd,idd2,i,j)
                 model_L = model(index_txt, i, j)
                 ret[idd][idd2] = EvalIRModel.eval(Précision_moyenne,model_L,train)[0]
    if plot and nb_parameters==1:
        plt.plot(range_1,ret)
        plt.show()
    res = np.unravel_index(ret.argmax(), ret.shape)
    if nb_parameters == 1:
        model_L = model(index_txt, res[0])
        return EvalIRModel.eval(Précision_moyenne,model_L,test)[0],ret[res[0]],range_1[res[0]]
    model_L = model(index_txt, res[0],res[1])
    return EvalIRModel.eval(Précision_moyenne,model_L,test)[0],ret[res[0]][res[1]],(range_1[res[0]],range_2[res[1]])
'''
def validationcroisee(coltext,index_txt,colquery,model_L,n_splits=5):
    kf = ms.KFold(n_splits=n_splits,shuffle=True)
    res = 0
    for train, test in kf.split(list(colquery.keys())):
        print(train,test)
        liste = list(colquery.keys())
        train = {liste[x]:colquery[liste[x]] for x in train}
        test = {liste[x]:colquery[liste[x]] for x in test}
        res += EvalIRModel.eval(Précision_moyenne,model_L,train)[0]
    return res/n_splits
'''

range_ =  np.arange(0, 1.1, 0.1)
range_2 =  np.arange(0.2, 1.3, 0.1)

'''
score_test, score_train, best = gridsearch(col0,index_txt,col1,m.ModeleLangue)
print("meilleur parametre pour ModeleLangue",best) # 0.9
print("score en test :", score_test)
print("score en train :", score_train)
'''

score_test, score_train, best = gridsearch(col0,index_txt,col1,m.Okapi,nb_parameters = 2,range_1 = range_2,range_2 = range_2)
print("meilleur parametre pour Okapi",best)
print("score en test :", score_test)
print("score en train :", score_train) 
'''
model_L = m.ModeleLangue
print("resultat moyen ",validationcroisee(col0,index_txt,col1,model_L,n_splits=5))
'''
'''
model_L = m.Okapi(0.9)
print("resultat moyen ",validationcroisee(col0,index_txt,col1,model_L,n_splits=5))
'''