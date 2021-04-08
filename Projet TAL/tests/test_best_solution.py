# -*- coding: utf-8 -*-

from utils.utils import Loader
from sklearn.model_selection import train_test_split
from utils.preprocessing import Preprocessing
from sklearn.feature_extraction.text import CountVectorizer
import sklearn.naive_bayes as nb
from sklearn import svm
from sklearn import linear_model as lin
import numpy as np
from utils.equilibrage import Equilibrage

fname = "Data/AFDpresidentutf8/corpus.tache1.learn.utf8"
alltxts,alllabs = Loader.load_pres(fname)

# parametres de la meilleur solution
params = {
    "lowercase":False,
    "punct":"separe",
    "marker":False,
    "number":True,
    "stemming":False,
    "strip_accents":False,
    "stopwords": None
}

clf = svm.LinearSVC()

f = lambda x: Preprocessing.preprocessing(x,params)
vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern)
X = vectorizer.fit_transform(alltxts)


# train test split sans équilibrage
X_train, X_test, y_train, y_test = train_test_split( X, alllabs, test_size=0.4, random_state=0) 
clf.fit(X_train, y_train)
res = clf.predict(X_test)
print(clf.score(X_test,y_test))
print(np.unique(res,return_counts=True))


# train test split avec équilibrage
to_keep = Equilibrage.remove_prioritaire_2(y_test)
res = clf.predict(X_test[to_keep])

y_test = np.array(y_test)
print(clf.score(X_test[to_keep],y_test[to_keep]))
print(np.unique(res,return_counts=True))

# cross validation sans équilibrage
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_validate

scoring = {'accuracy' : make_scorer(accuracy_score), 
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score), 
           'f1_score' : make_scorer(f1_score)}

res_cross = cross_validate( clf, X, alllabs, cv=5,scoring=scoring)
for score,scores in res_cross.items():
    print(score,":",scores.mean())
    
datax, datay = Equilibrage.remove_prioritaire(alltxts,alllabs)


f = lambda x: Preprocessing.preprocessing(x,params)
vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern)
X = vectorizer.fit_transform(datax)

# cross validation avec équilibrage
from sklearn.metrics import make_scorer, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_validate

scoring = {'accuracy' : make_scorer(accuracy_score), 
           'precision' : make_scorer(precision_score),
           'recall' : make_scorer(recall_score), 
           'f1_score' : make_scorer(f1_score)}

res_cross = cross_validate( clf, X, datay, cv=5,scoring=scoring)
for score,scores in res_cross.items():
    print(score,":",scores.mean())
    
# train_test_split avec equilibrage
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split( X, datay, test_size=0.4, random_state=0) 
clf.fit(X_train_2, y_train_2)
res = clf.predict(X_test_2)
print(np.unique(res,return_counts=True))
print(clf.score(X_test_2,y_test_2))