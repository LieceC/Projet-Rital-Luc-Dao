# -*- coding: utf-8 -*-

import utils.scoring as sc
from wordcloud import STOPWORDS 
import sklearn.naive_bayes as nb
from sklearn import svm
from sklearn import linear_model as lin
from utils.utils import Loader
import numpy as np

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

params = {
    "lowercase":[False,True],
    "punct":[False,"separe","fuse"],
    "marker":[False,True],
    "number":[False,True],
    "stemming":[False,True],
     # "ligne": [None,-2,0],
    "strip_accents":[False,True],
    "stopwords": [None,set(STOPWORDS)]
}

# SVM => Penser à utiliser des SVM linéaire !!!!
clf = svm.LinearSVC()
# Naive Bayes
# clf = nb.MultinomialNB() # frequentiels
# regression logistique
# clf = lin.LogisticRegression()

train,test = sc.gridSearch(alltxts,alllabs,clf,params)

print("Meilleurs résultats en test")
print(params.keys())
maxi = np.argmax(list(test.values()))
print(list(test.keys())[maxi])