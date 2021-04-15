# -*- coding: utf-8 -*-

from sklearn.model_selection import KFold
import itertools
import collections
from sklearn.metrics import f1_score
from sklearn import svm
from sklearn.model_selection import train_test_split
from utils.preprocessing import Preprocessing
from sklearn.feature_extraction.text import CountVectorizer
import pickle
import numpy as np
import sklearn.naive_bayes as nb

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

def gridSearch(datax,datay,params,stock = False):
    '''
    Parameters
    ----------
    datax
        Liste des données.
    datay 
        Liste des labels des données.
    clf_class
        Classifieur à utiliser.
    params
        Dictionnaire des parametres.

    Returns
    -------
    res_train 
        Dictionnaire des F1-score en train en fonction des différents parametres.
    res_test : TYPE
        Dictionnaire des F1-score en train en fonction des différents parametres..

    '''
    el = params.keys()
 
    res_test = dict()
    res_train = dict()
    size = len(list(itertools.product(*params.values())))
    for i,v in enumerate(list(itertools.product(*params.values()))):
        print(i+1,"on",size)
        tag = tuple(x if isinstance(x, collections.Hashable) else "YES" for x in v)
        print(tag)
        current_params = dict(zip(el,v))
        
        # choix du classifieur
        clf_class = current_params.get("clf",svm.LinearSVC)
        if clf_class == nb.MultinomialNB:
            class_prior = current_params.get("class_weight",None)
            if class_prior == "balanced":   
                class_prior = len(datax) / (2 * np.bincount(np.where(np.array(datay) == 1,1,0)))
                print(class_prior)
            clf = clf_class(class_prior = class_prior)
        else:
            clf = clf_class(class_weight = current_params.get("class_weight",None))
        # choix du vectorizer
        Vectorizer = current_params.get("Vectorizer",CountVectorizer)
        # application des parametres au preprocessing
        f = lambda x: Preprocessing.preprocessing(x,current_params)
        
        # Vectorization
        print( current_params.get("max_df",1),current_params.get("min_df",1))
        vectorizer = Vectorizer(preprocessor = f,lowercase=False,
                                token_pattern = Preprocessing.token_pattern, 
                                binary = current_params.get("binary",False), 
                                max_df = current_params.get("max_df",1),
                                min_df = current_params.get("min_df",1),
                                ngram_range = current_params.get("ngram_range",(1,1)),
                                max_features = current_params.get("max_features",None))
        X = vectorizer.fit_transform(datax)
        X_train, X_test, y_train, y_test = train_test_split( X, datay, test_size=0.4, random_state=0) 
        clf.fit(X_train, y_train)
        # Application 
        yhat_test = clf.predict(X_test)
        yhat_train = clf.predict(X_train)
        
        res_test[tag] = f1_score(y_test,yhat_test)
        res_train[tag] = f1_score(y_train,yhat_train)
        print(res_test[tag])
    if stock:
        pickle.dump(res_train,open("train","wb"))
        pickle.dump(res_test,open("test","wb"))
    return res_train,res_test