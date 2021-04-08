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

base = "cisi" # cisi
col0 = c.Parser.parse("../data/"+base+"/"+base+".txt")
col1 = c.QueryParser.parse("../data/"+base+"/"+base+".qry", "../data/"+base+"/"+base+".rel")
index_txt = IndexerSimple(col0)

def gridsearch(coltext,index_txt,colquery,model,
               test, # indice des querys de test
               train, # indice des querys de train
               nb_parameters = 1, # nombre de parametres à tester (1 ou 2)
               range_1 = np.arange(0, 1.1, 0.1), # les valeurs à tester pour le parametre 1
               range_2 = np.arange(0, 1.1, 0.1), # les valeurs à tester pour le parametre 2
               plot = False # affichage du score en fonction des valeurs des parametres (si un parametre) 
               ):
    """
        Renvoie dans l'ordre :
            score de test du meilleurs parametre
            score de train du meilleurs parametre
            le meilleurs parametre (avec le meilleurs score de train)
    """
    train = {x:colquery[x] for x in train}
    test = {x:colquery[x] for x in test}
    
    # valeurs de tests
    tab_train_score = np.zeros(len(range_1)) if nb_parameters == 1 else np.zeros((len(range_1),len(range_2)))
    
    # on test les valeurs
    for idd,i in enumerate(range_1):
        if nb_parameters == 1:
            model_L = model(index_txt, i)
            tab_train_score[idd] = EvalIRModel.eval(Précision_moyenne,model_L,train)[0]
        else:
            for idd2,j in enumerate(range_2):
                 # print(idd,idd2,i,j)
                 model_L = model(index_txt, i, j)
                 tab_train_score[idd][idd2] = EvalIRModel.eval(Précision_moyenne,model_L,train)[0]
                 
    if plot and nb_parameters==1:
        plt.plot(range_1,tab_train_score)
        plt.show()
    
    # on récupère les indices du meilleurs parametre
    i_best_train_score = np.unravel_index(tab_train_score.argmax(), tab_train_score.shape)
    
    # on fait le score en test
    if nb_parameters == 1: 
        model_L = model(index_txt, i_best_train_score[0]) 
        score_test = EvalIRModel.eval(Précision_moyenne,model_L,test)[0]
        score_train = tab_train_score[i_best_train_score[0]]
        best_parameter = range_1[i_best_train_score[0]]
        return score_test,score_train,best_parameter
    model_L = model(index_txt, i_best_train_score[0],i_best_train_score[1])
    score_test = EvalIRModel.eval(Précision_moyenne,model_L,test)[0]
    score_train = tab_train_score[i_best_train_score[0]][i_best_train_score[1]]
    best_parameter = (range_1[i_best_train_score[0]],range_2[i_best_train_score[1]])
    return score_test,score_train,best_parameter


def validationcroisee(coltext,index_txt,colquery,model_L,
                      n_splits=5, # nombre de plits
                      nb_parameters = 1, # nombre de parametres à tester (1 ou 2)
               range_1 = np.arange(0, 1.1, 0.1), # les valeurs à tester pour le parametre 1
               range_2 = np.arange(0, 1.1, 0.1), # les valeurs à tester pour le parametre 2
               ):
    kf = ms.KFold(n_splits=n_splits,shuffle=True)
    res_test = 0
    res_train = 0
    res_best = []
    for train, test in kf.split(list(colquery.keys())):
        print("->")
        liste = list(colquery.keys())
        train = {liste[x]:colquery[liste[x]] for x in train}
        test = {liste[x]:colquery[liste[x]] for x in test}
        score_test, score_train, best = gridsearch(coltext,index_txt,colquery,model_L,test, train,
                   nb_parameters = nb_parameters,range_1 = range_1, range_2 = range_2
               )

        res_test += score_test
        res_train += score_train
        res_best += [res_best]
    return res_test/n_splits,res_train/n_splits, res_best


range_ =  np.arange(0, 1.1, 0.1)
range_k =  np.arange(1.2, 2.2, 0.1)
range_b = np.arange(1.2, 1.7, 0.05)

train, test = ms.train_test_split(list(col1.keys()) ,test_size = 0.8)

'''
score_test, score_train, best = gridsearch(col0,index_txt,col1,m.ModeleLangue,test,train)
print("meilleur parametre pour ModeleLangue",best) # 0.9
print("score en test :", score_test) # 0.3163861722672842
print("score en train :", score_train) # 0.28227663490812865
'''

'''
score_test, score_train, best = gridsearch(col0,index_txt,col1,m.Okapi,test,train,nb_parameters = 2,range_1 = range_k,range_2 = range_b)
print("meilleur parametre pour Okapi",best) # 1.9 1.5 (pour range de 0.3 à 1.2)
print("score en test :", score_test) # 0.1364908066074799
print("score en train :", score_train)# 0.299986391077477
'''

'''
model_L = m.ModeleLangue
print("resultat moyen ",validationcroisee(col0,index_txt,col1,model_L,n_splits=5)) # 0.3164479744415069, 0.2736021751729737
'''


model_L = m.Okapi
print("resultat moyen ",validationcroisee(col0,index_txt,col1,model_L,n_splits=5,nb_parameters = 2,range_1 = range_k,range_2 = range_b))
# 0.1 0.3