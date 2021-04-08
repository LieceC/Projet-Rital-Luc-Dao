# -*- coding: utf-8 -*-

from sklearn.model_selection import KFold
import itertools
import collections
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.model_selection import train_test_split
from utils.preprocessing import Preprocessing
from sklearn.feature_extraction.text import CountVectorizer

def kFold_scores(X,alllabs,clf,nb_splits = 2):
    scores = []
    kf = KFold(n_splits=nb_splits,shuffle=True)
    for train, test in kf.split(X):
        # print("%s %s" % (train, test))
        X_train = X[train]
        y_train = alllabs[train]
        X_test  = X[test]
        y_test  = alllabs[test]
    
        clf.fit(X_train, y_train)
        # evaluation
        scores += [clf.score(X_test,y_test)]
    return scores

def gridSearch(datax,datay,clf,params):
    el = params.keys()
    res_test = dict()
    res_train = dict()
    size = len(list(itertools.product(*params.values())))
    for i,v in enumerate(list(itertools.product(*params.values()))):
        print(i+1,"on",size)
        tag = tuple(x if isinstance(x, collections.Hashable) else "YES" for x in v)
        print(tag)
        current_params = dict(zip(el,v))
        f = lambda x: Preprocessing.preprocessing(x,current_params)
        vectorizer = CountVectorizer(preprocessor = f,lowercase=False,token_pattern = Preprocessing.token_pattern)
        
        X = vectorizer.fit_transform(datax)
        X_train, X_test, y_train, y_test = train_test_split( X, datay, test_size=0.4, random_state=0) 
        clf.fit(X_train, y_train)
        # Application 
        yhat_test = clf.predict(X_test)
        yhat_train = clf.predict(X_train)
        
        res_test[tag] = f1_score(y_test,yhat_test)
        res_train[tag] = f1_score(y_train,yhat_train)
        print(res_test[tag])
    
    return res_train,res_test