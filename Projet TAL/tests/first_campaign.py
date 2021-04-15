# -*- coding: utf-8 -*-

import utils.scoring as sc
import sklearn.naive_bayes as nb
from sklearn import svm
from utils.utils import Loader
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy as np
from nltk.corpus import stopwords
from utils.preprocessing import Preprocessing
from sklearn.linear_model import LogisticRegression
stop = list(stopwords.words('french'))

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)
params = {
    "lowercase":[False,True],
    "punct":[False,True],
    "marker":[False,True],
    "number":[False,True],
    "stemming":[False,Preprocessing.stem],
    "ligne": [None,-2,0],
    "strip_accents":[False,True],
    "stopwords": [None,stop], # set(STOPWORDS)],
    "Vectorizer": [CountVectorizer,TfidfVectorizer],
    "binary": [True,False],
    "class_weight": ["balanced",None],
    "max_features": [None, 16000, 10000, 7000],
    "ngram_range" : [(1,1),(1,2)],
    "max_df" : [1.,0.08,0.02,0.005],
    "min_df" : [1,2,5,10],
    "clf" : [nb.MultinomialNB,svm.LinearSVC,LogisticRegression]
}

# SVM => Penser à utiliser des SVM linéaire !!!!
clf = svm.LinearSVC
# Naive Bayes
# clf = nb.MultinomialNB() # frequentiels
# regression logistique
# clf = lin.LogisticRegression()

train,test = sc.gridSearch(alltxts,alllabs,params,stock = True)

print("Meilleurs résultats en test")
print(params.keys())
maxi = np.argmax(list(test.values()))
print(list(test.keys())[maxi])